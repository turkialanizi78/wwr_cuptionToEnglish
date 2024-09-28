import os
import subprocess
import wave
import json
import datetime
import logging
from flask import Flask, request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
from vosk import Model, KaldiRecognizer
import concurrent.futures
import threading
import time
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['VOSK_MODEL_PATH'] = 'vosk-model-arabic'

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

# Simple in-memory task storage
tasks = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_model():
    model_path = app.config['VOSK_MODEL_PATH']
    if not os.path.exists(model_path):
        raise ValueError(f"Vosk model not found. Please download the Arabic model and place it in '{model_path}'")
    return Model(model_path)

def get_video_resolution(video_path):
    command = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', 
               '-count_packets', '-show_entries', 'stream=width,height', 
               '-of', 'csv=p=0', video_path]
    output = subprocess.check_output(command).decode('utf-8').strip().split(',')
    return int(output[0]), int(output[1])

def process_video(task_id, video_path):
    try:
        tasks[task_id]['status'] = 'Processing'
        
        # Extract audio
        audio_path = extract_audio(video_path)
        tasks[task_id]['status'] = 'Audio extracted'

        # Transcribe audio
        transcription = transcribe_audio_vosk(audio_path, task_id)
        tasks[task_id]['status'] = 'Transcription complete'

        # Create subtitle file
        subtitle_path = video_path.rsplit('.', 1)[0] + '.ass'
        create_ass_subtitle(transcription, subtitle_path, video_path)
        tasks[task_id]['status'] = 'Subtitle created'

        # Cleanup
        os.remove(audio_path)

        tasks[task_id]['status'] = 'Completed'
        tasks[task_id]['result'] = subtitle_path
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        tasks[task_id]['status'] = f'Error: {str(e)}'

def extract_audio(video_path):
    start_time = time.time()
    audio_path = video_path.rsplit('.', 1)[0] + '.wav'
    command = ['ffmpeg', '-i', video_path, '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', audio_path]
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    logger.info(f"Audio extraction completed in {time.time() - start_time:.2f} seconds")
    return audio_path

def transcribe_audio_chunk(chunk, model):
    rec = KaldiRecognizer(model, 16000)
    rec.AcceptWaveform(chunk)
    result = json.loads(rec.FinalResult())
    return result

def transcribe_audio_vosk(audio_path, task_id):
    start_time = time.time()
    chunk_size = 4000 * 10
    results = []
    model = get_model()

    with wave.open(audio_path, 'rb') as wf:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            total_chunks = wf.getnframes() // chunk_size
            for i in range(total_chunks):
                chunk = wf.readframes(chunk_size)
                if len(chunk) == 0:
                    break
                futures.append(executor.submit(transcribe_audio_chunk, chunk, model))
                if i % 10 == 0:
                    tasks[task_id]['status'] = f'Transcribing: {i/total_chunks:.2f}'

            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result.get('text'):
                    results.append(result)

    logger.info(f"Transcription completed in {time.time() - start_time:.2f} seconds")
    return results

def create_ass_subtitle(transcription, output_path, video_path):
    width, height = get_video_resolution(video_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("[Script Info]\n")
        f.write("ScriptType: v4.00+\n")
        f.write(f"PlayResX: {width}\n")
        f.write(f"PlayResY: {height}\n")
        f.write("ScaledBorderAndShadow: yes\n\n")
        f.write("[V4+ Styles]\n")
        f.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
        f.write(f"Style: Default,Arial,{height//20},&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1\n\n")
        f.write("[Events]\n")
        f.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")

        start_time = 0.0
        for result in transcription:
            if 'text' in result:
                end_time = start_time + 2.0  # Adjust this value to change subtitle duration
                start = str(datetime.timedelta(seconds=start_time)).split('.')[0]
                end = str(datetime.timedelta(seconds=end_time)).split('.')[0]
                text = result['text']
                f.write(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n")
                start_time = end_time

@app.route('/')
def index():
    model_path = app.config['VOSK_MODEL_PATH']
    model_exists = os.path.exists(model_path)
    return render_template('upload.html', model_exists=model_exists, model_path=model_path)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        task_id = str(uuid.uuid4())
        tasks[task_id] = {'status': 'Queued'}
        
        thread = threading.Thread(target=process_video, args=(task_id, file_path))
        thread.start()

        return jsonify({'task_id': task_id}), 202

    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/status/<task_id>')
def task_status(task_id):
    task = tasks.get(task_id, {})
    return jsonify({
        'status': task.get('status', 'Not found'),
        'result': task.get('result')
    })

@app.route('/download/<task_id>')
def download_file(task_id):
    task = tasks.get(task_id, {})
    if task.get('status') == 'Completed' and 'result' in task:
        return send_file(task['result'], as_attachment=True)
    else:
        return jsonify({'error': 'File not ready'}), 404

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)