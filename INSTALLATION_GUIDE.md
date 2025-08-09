# دليل التثبيت المفصل - OCR Enhancer

## مقدمة

هذا الدليل يوضح خطوات تثبيت وإعداد تطبيق OCR Enhancer بالتفصيل على أنظمة التشغيل المختلفة. يرجى اتباع الخطوات بعناية لضمان التثبيت الناجح.

## متطلبات النظام

### الحد الأدنى للمتطلبات
- **المعالج**: Intel Core i3 أو AMD Ryzen 3 أو ما يعادلهما
- **الذاكرة**: 4 جيجابايت RAM
- **مساحة التخزين**: 2 جيجابايت مساحة فارغة
- **اتصال الإنترنت**: مطلوب للتحميل والذكاء الاصطناعي

### المتطلبات الموصى بها
- **المعالج**: Intel Core i5 أو AMD Ryzen 5 أو أحدث
- **الذاكرة**: 8 جيجابايت RAM أو أكثر
- **مساحة التخزين**: 5 جيجابايت مساحة فارغة
- **كرت الرسوميات**: مدعوم للمعالجة المتسارعة (اختياري)

## التثبيت على Ubuntu/Debian

### الخطوة 1: تحديث النظام

```bash
sudo apt update && sudo apt upgrade -y
```

### الخطوة 2: تثبيت Python والأدوات الأساسية

```bash
# تثبيت Python 3.8+ وأدوات التطوير
sudo apt install python3 python3-pip python3-venv python3-dev -y

# تثبيت أدوات البناء الضرورية
sudo apt install build-essential libssl-dev libffi-dev -y

# تحقق من إصدار Python
python3 --version
```

### الخطوة 3: تثبيت Node.js و npm

```bash
# تثبيت Node.js من المستودع الرسمي
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# تحقق من التثبيت
node --version
npm --version

# تثبيت pnpm (اختياري ولكن موصى به)
npm install -g pnpm
```

### الخطوة 4: تثبيت Tesseract OCR

```bash
# تثبيت Tesseract وحزم اللغات
sudo apt install tesseract-ocr -y
sudo apt install tesseract-ocr-ara tesseract-ocr-eng -y

# تثبيت حزم لغات إضافية (اختياري)
sudo apt install tesseract-ocr-fra tesseract-ocr-deu tesseract-ocr-spa -y

# تحقق من التثبيت
tesseract --version
tesseract --list-langs
```

### الخطوة 5: تثبيت أدوات معالجة الصور

```bash
# تثبيت مكتبات معالجة الصور
sudo apt install libimage-exiftool-perl -y
sudo apt install poppler-utils -y  # لمعالجة PDF
sudo apt install imagemagick -y    # لمعالجة الصور
```

### الخطوة 6: تحميل وإعداد المشروع

```bash
# إنشاء مجلد للمشروع
mkdir ~/ocr_enhancer
cd ~/ocr_enhancer

# نسخ ملفات المشروع (استبدل بالمسار الصحيح)
# git clone <repository-url> .
# أو نسخ الملفات يدوياً

# إنشاء بيئة Python افتراضية
python3 -m venv backend/venv

# تفعيل البيئة الافتراضية
source backend/venv/bin/activate

# تثبيت تبعيات Python
cd backend
pip install --upgrade pip
pip install flask flask-cors pillow pytesseract openai python-dotenv requests
```

### الخطوة 7: إعداد الواجهة الأمامية

```bash
# الانتقال إلى مجلد الواجهة الأمامية
cd ../frontend

# تثبيت التبعيات
pnpm install
# أو
npm install
```

### الخطوة 8: إعداد متغيرات البيئة

```bash
# إنشاء ملف البيئة
cd ../backend
cp .env.example .env

# تحرير ملف البيئة
nano .env
```

أضف المحتوى التالي:
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1
FLASK_ENV=development
FLASK_DEBUG=True
MAX_CONTENT_LENGTH=52428800
UPLOAD_FOLDER=uploads
OUTPUT_FOLDER=outputs
```

## التثبيت على macOS

### الخطوة 1: تثبيت Homebrew

```bash
# تثبيت Homebrew إذا لم يكن مثبتاً
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### الخطوة 2: تثبيت Python

```bash
# تثبيت Python 3.9+
brew install python@3.9

# إنشاء رابط رمزي
brew link python@3.9

# تحقق من التثبيت
python3 --version
pip3 --version
```

### الخطوة 3: تثبيت Node.js

```bash
# تثبيت Node.js
brew install node

# تحقق من التثبيت
node --version
npm --version

# تثبيت pnpm
npm install -g pnpm
```

### الخطوة 4: تثبيت Tesseract OCR

```bash
# تثبيت Tesseract مع حزم اللغات
brew install tesseract tesseract-lang

# تحقق من التثبيت
tesseract --version
tesseract --list-langs
```

### الخطوة 5: تثبيت أدوات إضافية

```bash
# تثبيت أدوات معالجة الصور
brew install imagemagick poppler
```

### الخطوة 6: إعداد المشروع

```bash
# إنشاء مجلد المشروع
mkdir ~/ocr_enhancer
cd ~/ocr_enhancer

# إنشاء بيئة Python افتراضية
python3 -m venv backend/venv

# تفعيل البيئة
source backend/venv/bin/activate

# تثبيت التبعيات
cd backend
pip install --upgrade pip
pip install flask flask-cors pillow pytesseract openai python-dotenv requests

# إعداد الواجهة الأمامية
cd ../frontend
pnpm install
```

## التثبيت على Windows

### الخطوة 1: تثبيت Python

1. قم بتحميل Python 3.9+ من [python.org](https://www.python.org/downloads/)
2. تأكد من تحديد "Add Python to PATH" أثناء التثبيت
3. افتح Command Prompt وتحقق من التثبيت:
```cmd
python --version
pip --version
```

### الخطوة 2: تثبيت Node.js

1. قم بتحميل Node.js من [nodejs.org](https://nodejs.org/)
2. اتبع معالج التثبيت
3. تحقق من التثبيت:
```cmd
node --version
npm --version
```

### الخطوة 3: تثبيت Tesseract OCR

1. قم بتحميل Tesseract من [GitHub Releases](https://github.com/UB-Mannheim/tesseract/wiki)
2. ثبت البرنامج في `C:\Program Files\Tesseract-OCR`
3. أضف المسار إلى متغير PATH:
   - افتح "System Properties" → "Environment Variables"
   - أضف `C:\Program Files\Tesseract-OCR` إلى PATH
4. تحقق من التثبيت:
```cmd
tesseract --version
```

### الخطوة 4: إعداد المشروع

```cmd
# إنشاء مجلد المشروع
mkdir C:\ocr_enhancer
cd C:\ocr_enhancer

# إنشاء بيئة Python افتراضية
python -m venv backend\venv

# تفعيل البيئة
backend\venv\Scripts\activate

# تثبيت التبعيات
cd backend
pip install --upgrade pip
pip install flask flask-cors pillow pytesseract openai python-dotenv requests

# إعداد الواجهة الأمامية
cd ..\frontend
npm install
```

## إعداد قاعدة البيانات

### إنشاء قاعدة البيانات

```bash
# تفعيل البيئة الافتراضية
source backend/venv/bin/activate  # Linux/macOS
# أو
backend\venv\Scripts\activate     # Windows

# إنشاء قاعدة البيانات
cd backend
python -c "
from src.models.user import db
from src.main import app
with app.app_context():
    db.create_all()
    print('Database created successfully')
"
```

## اختبار التثبيت

### اختبار الواجهة الخلفية

```bash
# تشغيل الخادم
cd backend
source venv/bin/activate
python src/main.py
```

يجب أن ترى رسالة مشابهة لـ:
```
INFO:src.ocr_engines:Tesseract OCR is available
INFO:src.ai_corrector:OpenAI client initialized successfully
* Running on http://0.0.0.0:5000
```

### اختبار الواجهة الأمامية

في نافذة طرفية جديدة:
```bash
cd frontend
pnpm run dev
```

يجب أن ترى:
```
Local:   http://localhost:5173/
Network: http://192.168.x.x:5173/
```

### اختبار التكامل

1. افتح المتصفح وانتقل إلى `http://localhost:5173`
2. يجب أن ترى واجهة OCR Enhancer
3. جرب رفع صورة تحتوي على نص
4. تحقق من عمل OCR والتصحيح الذكي

## حل المشاكل الشائعة

### مشكلة: "tesseract: command not found"

**الحل على Linux:**
```bash
sudo apt install tesseract-ocr
export PATH=$PATH:/usr/bin/tesseract
```

**الحل على macOS:**
```bash
brew install tesseract
```

**الحل على Windows:**
- تأكد من إضافة مسار Tesseract إلى PATH
- أعد تشغيل Command Prompt

### مشكلة: "No module named 'PIL'"

```bash
pip install Pillow
```

### مشكلة: "OpenAI API key not found"

1. احصل على مفتاح API من [OpenAI](https://platform.openai.com/api-keys)
2. أضفه إلى ملف `.env`:
```env
OPENAI_API_KEY=sk-your-actual-key-here
```

### مشكلة: "Port 5000 already in use"

```bash
# إيقاف العملية المستخدمة للمنفذ
sudo lsof -ti:5000 | xargs kill -9

# أو تغيير المنفذ في main.py
app.run(host='0.0.0.0', port=5001, debug=True)
```

### مشكلة: بطء في معالجة PDF

1. تأكد من تثبيت poppler-utils:
```bash
sudo apt install poppler-utils  # Linux
brew install poppler            # macOS
```

2. قم بتحسين إعدادات PDF في الكود

### مشكلة: خطأ في تثبيت التبعيات

```bash
# تحديث pip
pip install --upgrade pip

# تثبيت wheel
pip install wheel

# إعادة تثبيت التبعيات
pip install -r requirements.txt --force-reinstall
```

## التحقق من التثبيت الناجح

### قائمة التحقق النهائية

- [ ] Python 3.8+ مثبت ويعمل
- [ ] Node.js 16+ مثبت ويعمل
- [ ] Tesseract OCR مثبت ويتعرف على اللغات
- [ ] تبعيات Python مثبتة في البيئة الافتراضية
- [ ] تبعيات Node.js مثبتة
- [ ] ملف .env معرّف بشكل صحيح
- [ ] قاعدة البيانات منشأة
- [ ] الواجهة الخلفية تعمل على المنفذ 5000
- [ ] الواجهة الأمامية تعمل على المنفذ 5173
- [ ] التطبيق يستجيب في المتصفح
- [ ] رفع الملفات يعمل
- [ ] OCR يستخرج النص بنجاح
- [ ] التصحيح الذكي يعمل (إذا كان مفتاح OpenAI متوفراً)

### اختبار شامل

```bash
# اختبار Tesseract
echo "Hello World" | tesseract stdin stdout

# اختبار Python modules
python -c "import pytesseract, PIL, flask, openai; print('All modules imported successfully')"

# اختبار API
curl http://localhost:5000/api/ocr/health
```

## الخطوات التالية

بعد التثبيت الناجح:

1. **اقرأ دليل المستخدم** في `README.md`
2. **جرب الميزات المختلفة** مع ملفات تجريبية
3. **اضبط الإعدادات** حسب احتياجاتك
4. **راقب الأداء** وحسّن الإعدادات إذا لزم الأمر
5. **انشئ نسخة احتياطية** من إعداداتك

## الدعم

إذا واجهت مشاكل في التثبيت:

1. راجع قسم "حل المشاكل" أعلاه
2. تحقق من سجلات الأخطاء
3. ابحث في الوثائق الرسمية للأدوات المستخدمة
4. أنشئ issue في GitHub مع تفاصيل المشكلة

---

**تم إعداد هذا الدليل بواسطة Manus AI**

*آخر تحديث: يناير 2024*

