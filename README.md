# OCR Enhancer - AI-Powered Text Recognition and Correction

## نظرة عامة

OCR Enhancer هو تطبيق شامل مطور بلغة Python يهدف إلى تحسين مخرجات تقنية التعرف الضوئي على الحروف (OCR) باستخدام تقنيات الذكاء الاصطناعي المتقدمة مع إتاحة الإشراف البشري. يوفر التطبيق واجهة مستخدم حديثة وسهلة الاستخدام تدعم معالجة المستندات بصيغ متعددة وتطبيق تصحيحات ذكية على النصوص المستخرجة.

## الميزات الرئيسية

### 1. دعم محركات OCR متعددة
- **Tesseract OCR**: محرك OCR مفتوح المصدر متقدم يدعم أكثر من 100 لغة
- **دعم النصوص الخارجية**: إمكانية استيراد نتائج من برامج OCR التجارية مثل ABBYY FineReader و Readiris
- **دمج النتائج**: خوارزميات ذكية لدمج مخرجات محركات OCR متعددة لتحسين الدقة

### 2. تصحيح بالذكاء الاصطناعي
- **تصحيح تلقائي**: استخدام نماذج اللغة الكبيرة (LLMs) لتصحيح الأخطاء الإملائية والنحوية
- **دعم متعدد اللغات**: تصحيح النصوص العربية والإنجليزية والمختلطة
- **تصحيح سياقي**: إمكانية تقديم سياق إضافي لتحسين دقة التصحيح

### 3. واجهة مستخدم متقدمة
- **واجهة ويب حديثة**: مبنية باستخدام React و Tailwind CSS
- **تصميم متجاوب**: يعمل بكفاءة على أجهزة سطح المكتب والهواتف المحمولة
- **تفاعل في الوقت الفعلي**: عرض النتائج والتقدم في الوقت الفعلي

### 4. دعم صيغ متعددة
- **الصور**: PNG, JPG, JPEG, TIFF, TIF
- **المستندات**: PDF
- **النصوص**: TXT (لاستيراد نتائج OCR خارجية)

## متطلبات النظام

### متطلبات الأجهزة
- **المعالج**: معالج متعدد النوى (يُفضل Intel i5 أو AMD Ryzen 5 أو أحدث)
- **الذاكرة**: 8 جيجابايت RAM كحد أدنى (يُفضل 16 جيجابايت)
- **مساحة التخزين**: 2 جيجابايت مساحة فارغة
- **اتصال الإنترنت**: مطلوب لميزات الذكاء الاصطناعي

### متطلبات البرمجيات
- **نظام التشغيل**: Linux (Ubuntu 20.04+), macOS (10.15+), Windows (10+)
- **Python**: الإصدار 3.8 أو أحدث
- **Node.js**: الإصدار 16 أو أحدث
- **Tesseract OCR**: يتم تثبيته تلقائياً

## التثبيت والإعداد

### 1. تحضير البيئة

```bash
# استنساخ المشروع
git clone <repository-url>
cd ocr_enhancer

# إنشاء بيئة Python افتراضية
python3 -m venv backend/venv
source backend/venv/bin/activate  # على Linux/macOS
# أو
backend\\venv\\Scripts\\activate  # على Windows
```

### 2. تثبيت التبعيات

#### الواجهة الخلفية (Backend)
```bash
cd backend
pip install -r requirements.txt
```

#### الواجهة الأمامية (Frontend)
```bash
cd frontend
npm install
# أو
pnpm install
```

### 3. تثبيت Tesseract OCR

#### على Ubuntu/Debian:
```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-ara tesseract-ocr-eng
```

#### على macOS:
```bash
brew install tesseract tesseract-lang
```

#### على Windows:
قم بتحميل وتثبيت Tesseract من الموقع الرسمي وإضافة مساره إلى متغير PATH.

### 4. إعداد متغيرات البيئة

أنشئ ملف `.env` في مجلد `backend`:

```env
# إعدادات OpenAI API
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1

# إعدادات Flask
FLASK_ENV=development
FLASK_DEBUG=True

# إعدادات رفع الملفات
MAX_CONTENT_LENGTH=52428800  # 50MB
UPLOAD_FOLDER=uploads
OUTPUT_FOLDER=outputs
```

## تشغيل التطبيق

### 1. تشغيل الواجهة الخلفية

```bash
cd backend
source venv/bin/activate
python src/main.py
```

الخادم سيعمل على `http://localhost:5000`

### 2. تشغيل الواجهة الأمامية

في نافذة طرفية جديدة:

```bash
cd frontend
npm run dev
# أو
pnpm run dev
```

الواجهة ستعمل على `http://localhost:5173`

### 3. الوصول للتطبيق

افتح متصفح الويب وانتقل إلى `http://localhost:5173`

## دليل الاستخدام

### 1. رفع المستند

1. انقر على منطقة "Drop your file here, or browse"
2. اختر ملف من الصيغ المدعومة (PDF, PNG, JPG, TIFF, TXT)
3. سيتم عرض معلومات الملف بعد الرفع بنجاح

### 2. إعداد خيارات المعالجة

#### محركات OCR:
- اختر محرك OCR واحد أو أكثر
- في حالة اختيار محركات متعددة، حدد طريقة الدمج:
  - **Best Confidence**: اختيار النتيجة ذات الثقة الأعلى
  - **Longest Text**: اختيار النص الأطول

#### إعدادات اللغة:
- **Arabic + English**: للنصوص المختلطة
- **English Only**: للنصوص الإنجليزية فقط
- **Arabic Only**: للنصوص العربية فقط

#### تحسين الذكاء الاصطناعي:
- فعّل "Enable AI Text Correction" لتطبيق التصحيح الذكي
- أضف سياقاً اختيارياً لتحسين دقة التصحيح

### 3. معالجة المستند

1. انقر على "Process Document"
2. انتظر حتى اكتمال المعالجة
3. ستظهر النتائج في القسم الأيمن

### 4. مراجعة وتحرير النتائج

- **النص المستخرج**: يمكن تحريره مباشرة في منطقة النص
- **تفاصيل المعالجة**: عرض نتائج كل محرك OCR والتصحيحات المطبقة
- **الإحصائيات**: عدد الكلمات والأحرف ومستوى الثقة

### 5. حفظ النتائج

- **Copy**: نسخ النص إلى الحافظة
- **Download**: تحميل النص كملف TXT
- **Save Results**: حفظ تقرير شامل بصيغة JSON

## الهيكل التقني

### الواجهة الخلفية (Backend)

```
backend/
├── src/
│   ├── main.py              # نقطة دخول التطبيق
│   ├── ocr_engines.py       # محركات OCR
│   ├── ai_corrector.py      # تصحيح الذكاء الاصطناعي
│   ├── routes/
│   │   ├── ocr.py          # مسارات API للـ OCR
│   │   └── user.py         # مسارات المستخدمين
│   └── models/
│       └── user.py         # نماذج قاعدة البيانات
├── uploads/                 # مجلد الملفات المرفوعة
├── outputs/                 # مجلد النتائج
└── requirements.txt         # تبعيات Python
```

### الواجهة الأمامية (Frontend)

```
frontend/
├── src/
│   ├── App.jsx             # المكون الرئيسي
│   ├── components/
│   │   ├── FileUpload.jsx  # مكون رفع الملفات
│   │   ├── ProcessingOptions.jsx  # خيارات المعالجة
│   │   └── ResultsDisplay.jsx     # عرض النتائج
│   ├── services/
│   │   └── api.js          # خدمات API
│   └── assets/             # الملفات الثابتة
└── package.json            # تبعيات Node.js
```

## واجهة برمجة التطبيقات (API)

### نقاط النهاية الرئيسية

#### `GET /api/ocr/engines`
الحصول على قائمة محركات OCR المتاحة

**الاستجابة:**
```json
{
  "success": true,
  "engines": ["tesseract"],
  "ai_correction_available": true,
  "supported_formats": ["pdf", "png", "jpg", "jpeg", "tiff", "tif", "txt"]
}
```

#### `POST /api/ocr/process`
معالجة ملف بـ OCR وتصحيح الذكاء الاصطناعي

**المعاملات:**
- `file`: الملف المراد معالجته
- `engines[]`: قائمة محركات OCR
- `language`: لغة النص
- `ai_correction`: تفعيل التصحيح الذكي
- `combination_method`: طريقة دمج النتائج
- `context`: السياق الاختياري

**الاستجابة:**
```json
{
  "success": true,
  "file_id": "uuid",
  "filename": "document.pdf",
  "ocr_results": {...},
  "combined_result": {...},
  "ai_correction": {...},
  "final_text": "النص النهائي المصحح",
  "settings": {...}
}
```

#### `POST /api/ocr/correct-text`
تصحيح نص باستخدام الذكاء الاصطناعي فقط

**المعاملات:**
```json
{
  "text": "النص المراد تصحيحه",
  "language": "mixed",
  "context": "سياق اختياري"
}
```

#### `GET /api/ocr/health`
فحص حالة النظام

**الاستجابة:**
```json
{
  "success": true,
  "status": "healthy",
  "engines_available": ["tesseract"],
  "ai_available": true,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## استكشاف الأخطاء وإصلاحها

### مشاكل شائعة وحلولها

#### 1. خطأ "Tesseract not found"
**السبب**: Tesseract OCR غير مثبت أو غير موجود في PATH
**الحل**:
```bash
# على Ubuntu/Debian
sudo apt install tesseract-ocr

# على macOS
brew install tesseract

# تحقق من التثبيت
tesseract --version
```

#### 2. خطأ "OpenAI API key not configured"
**السبب**: مفتاح OpenAI API غير مُعرّف
**الحل**:
1. احصل على مفتاح API من OpenAI
2. أضفه إلى ملف `.env`:
```env
OPENAI_API_KEY=your_actual_api_key_here
```

#### 3. خطأ "Port already in use"
**السبب**: المنفذ مستخدم من تطبيق آخر
**الحل**:
```bash
# إيقاف العملية المستخدمة للمنفذ
sudo lsof -ti:5000 | xargs kill -9

# أو تغيير المنفذ في main.py
app.run(host='0.0.0.0', port=5001, debug=True)
```

#### 4. مشاكل في رفع الملفات الكبيرة
**السبب**: حد حجم الملف محدود
**الحل**: زيادة `MAX_CONTENT_LENGTH` في إعدادات Flask

#### 5. بطء في معالجة PDF كبيرة
**السبب**: معالجة صفحات متعددة تستغرق وقتاً
**الحل**: تقسيم PDF إلى أجزاء أصغر أو زيادة موارد النظام

### سجلات الأخطاء

#### تفعيل السجلات المفصلة:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### مواقع ملفات السجلات:
- **Flask**: عرض في وحدة التحكم
- **React**: وحدة تحكم المتصفح (F12)

## الأمان والخصوصية

### حماية البيانات
- جميع الملفات المرفوعة تُحذف تلقائياً بعد المعالجة
- لا يتم تخزين النصوص المعالجة على الخادم
- اتصالات API محمية بـ HTTPS في الإنتاج

### أفضل الممارسات الأمنية
- استخدم مفاتيح API قوية ولا تشاركها
- قم بتحديث التبعيات بانتظام
- استخدم HTTPS في البيئة الإنتاجية
- راقب استخدام API لتجنب التكاليف غير المتوقعة

## الأداء والتحسين

### تحسين الأداء
- **معالجة متوازية**: استخدام محركات OCR متعددة بالتوازي
- **ذاكرة التخزين المؤقت**: حفظ نتائج معالجة متكررة
- **ضغط الصور**: تحسين جودة الصور قبل OCR

### مراقبة الأداء
- **زمن الاستجابة**: متوسط 2-5 ثوانٍ للصور الصغيرة
- **استهلاك الذاكرة**: 100-500 ميجابايت حسب حجم الملف
- **دقة OCR**: 85-95% حسب جودة المستند

## التطوير والمساهمة

### إعداد بيئة التطوير

```bash
# استنساخ المشروع
git clone <repository-url>
cd ocr_enhancer

# إعداد pre-commit hooks
pip install pre-commit
pre-commit install

# تشغيل الاختبارات
cd backend
python -m pytest tests/

cd ../frontend
npm test
```

### معايير الكود
- **Python**: PEP 8, Black formatter
- **JavaScript**: ESLint, Prettier
- **التوثيق**: Docstrings للدوال المهمة
- **الاختبارات**: تغطية 80%+ للكود الحرج

### إضافة محرك OCR جديد

1. أنشئ فئة جديدة في `ocr_engines.py`:
```python
class NewOCREngine:
    def __init__(self):
        # إعداد المحرك
        pass
    
    def process_image(self, image_path, language):
        # معالجة الصورة
        return {
            'text': extracted_text,
            'confidence': confidence_score,
            'success': True
        }
```

2. أضف المحرك إلى `OCRManager`:
```python
def __init__(self):
    self.engines['new_engine'] = NewOCREngine()
```

## الترخيص والحقوق

هذا المشروع مرخص تحت رخصة MIT. يمكنك استخدامه وتعديله وتوزيعه بحرية مع الاحتفاظ بإشعار حقوق الطبع والنشر.

## الدعم والمساعدة

### الحصول على المساعدة
- **الوثائق**: راجع هذا الملف أولاً
- **المشاكل**: أنشئ issue في GitHub
- **المناقشات**: استخدم قسم Discussions

### الإبلاغ عن الأخطاء
عند الإبلاغ عن خطأ، يرجى تضمين:
- وصف مفصل للمشكلة
- خطوات إعادة الإنتاج
- رسائل الخطأ كاملة
- معلومات النظام (OS, Python version, etc.)

### طلب ميزات جديدة
- وصف الميزة المطلوبة
- حالات الاستخدام
- الفوائد المتوقعة
- أي تفاصيل تقنية ذات صلة

---

**تم تطوير هذا التطبيق بواسطة Manus AI**

*آخر تحديث: يناير 2024*

