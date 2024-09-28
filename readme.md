# Video to Subtitle Application Documentation
# توثيق تطبيق تحويل الفيديو إلى ترجمات

## Table of Contents / جدول المحتويات
1. [Overview / نظرة عامة](#overview--نظرة-عامة)
2. [Requirements / المتطلبات](#requirements--المتطلبات)
3. [Setup / الإعداد](#setup--الإعداد)
4. [Usage / الاستخدام](#usage--الاستخدام)
5. [Application Structure / هيكل التطبيق](#application-structure--هيكل-التطبيق)
6. [Key Components / المكونات الرئيسية](#key-components--المكونات-الرئيسية)
7. [Troubleshooting / استكشاف الأخطاء وإصلاحها](#troubleshooting--استكشاف-الأخطاء-وإصلاحها)

## Overview / نظرة عامة

**English:**  
This application is a Flask-based web service that converts video files to subtitle files (.ass format) using speech recognition. It utilizes the Vosk speech recognition library to transcribe audio from videos into text, which is then formatted into subtitles.

**العربية:**  
هذا التطبيق هو خدمة ويب مبنية على Flask تقوم بتحويل ملفات الفيديو إلى ملفات ترجمة (بتنسيق .ass) باستخدام التعرف على الكلام. يستخدم التطبيق مكتبة Vosk للتعرف على الكلام لتحويل الصوت من مقاطع الفيديو إلى نص، ثم يتم تنسيقه إلى ترجمات.

## Requirements / المتطلبات

**English:**  
- Python 3.7+
- Flask
- Vosk
- FFmpeg and FFprobe
- Arabic Vosk model

**العربية:**  
- بايثون 3.7+
- Flask
- Vosk
- FFmpeg و FFprobe
- نموذج Vosk العربي

## Setup / الإعداد

**English:**  
1. Install the required Python libraries:
   ```
   pip install flask vosk
   ```
2. Install FFmpeg and FFprobe on your system and ensure they're accessible from the command line.
3. Download the Arabic Vosk model and place it in a directory named `vosk-model-arabic` in the same folder as the script.
4. Create two directories in the same folder as the script:
   - `uploads`: for storing uploaded video files
   - `templates`: for storing the HTML template
5. Place the `upload.html` file in the `templates` directory.

**العربية:**  
1. قم بتثبيت مكتبات بايثون المطلوبة:
   ```
   pip install flask vosk
   ```
2. قم بتثبيت FFmpeg و FFprobe على نظامك وتأكد من إمكانية الوصول إليهما من سطر الأوامر.
3. قم بتنزيل نموذج Vosk العربي وضعه في مجلد باسم `vosk-model-arabic` في نفس المجلد الذي يوجد فيه النص البرمجي.
4. قم بإنشاء مجلدين في نفس المجلد الذي يوجد فيه النص البرمجي:
   - `uploads`: لتخزين ملفات الفيديو المرفوعة
   - `templates`: لتخزين قالب HTML
5. ضع ملف `upload.html` في مجلد `templates`.

## Usage / الاستخدام

**English:**  
1. Run the application:
   ```
   python app.py
   ```
2. Open a web browser and navigate to `http://localhost:5000`.
3. Upload a video file through the web interface.
4. The application will process the video and provide a download link for the generated subtitle file.

**العربية:**  
1. قم بتشغيل التطبيق:
   ```
   python app.py
   ```
2. افتح متصفح ويب وانتقل إلى `http://localhost:5000`.
3. قم برفع ملف فيديو من خلال واجهة الويب.
4. سيقوم التطبيق بمعالجة الفيديو وتوفير رابط تنزيل لملف الترجمة الذي تم إنشاؤه.

## Application Structure / هيكل التطبيق

**English:**  
The application consists of a single Python script (`app.py`) and an HTML template (`upload.html`). The script handles all the backend processing, while the template provides the user interface.

**العربية:**  
يتكون التطبيق من نص برمجي بايثون واحد (`app.py`) وقالب HTML (`upload.html`). يتعامل النص البرمجي مع جميع عمليات المعالجة الخلفية، بينما يوفر القالب واجهة المستخدم.

## Key Components / المكونات الرئيسية

**English:**  
1. Flask Application Setup
2. Video Processing
3. Audio Extraction
4. Speech Recognition
5. Subtitle Creation
6. Web Routes
7. Utility Functions

**العربية:**  
1. إعداد تطبيق Flask
2. معالجة الفيديو
3. استخراج الصوت
4. التعرف على الكلام
5. إنشاء الترجمات
6. مسارات الويب
7. الوظائف المساعدة

## Troubleshooting / استكشاف الأخطاء وإصلاحها

**English:**  
1. **No transcription results:**
   - Verify that the Vosk model is correctly installed
   - Check the console output for error messages
   - Ensure the video contains audible Arabic speech
2. **FFmpeg errors:**
   - Confirm that FFmpeg and FFprobe are correctly installed
   - Check the console output for FFmpeg-related error messages
3. **File upload issues:**
   - Ensure the `uploads` directory exists and has write permissions
   - Verify that the uploaded file is in a supported format
4. **Subtitle file is empty:**
   - Check the console output for warnings about empty transcription data
   - Verify that the audio extraction process completed successfully

**العربية:**  
1. **عدم وجود نتائج نسخ:**
   - تحقق من تثبيت نموذج Vosk بشكل صحيح
   - تحقق من مخرجات وحدة التحكم للبحث عن رسائل الخطأ
   - تأكد من أن الفيديو يحتوي على كلام عربي مسموع
2. **أخطاء FFmpeg:**
   - تأكد من تثبيت FFmpeg و FFprobe بشكل صحيح
   - تحقق من مخرجات وحدة التحكم للبحث عن رسائل خطأ متعلقة بـ FFmpeg
3. **مشاكل رفع الملفات:**
   - تأكد من وجود مجلد `uploads` وأنه يمتلك أذونات الكتابة
   - تحقق من أن الملف المرفوع بتنسيق مدعوم
4. **ملف الترجمة فارغ:**
   - تحقق من مخرجات وحدة التحكم للبحث عن تحذيرات حول بيانات نسخ فارغة
   - تأكد من اكتمال عملية استخراج الصوت بنجاح

For persistent issues, review the detailed logging output in the console.

للمشاكل المستمرة، راجع مخرجات التسجيل المفصلة في وحدة التحكم.