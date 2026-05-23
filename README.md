# AI Gemini App - تطبيق ذكاء اصطناعي محلي

تطبيق دردشة ذكي يعمل محلياً على جهازك، شبيه بـ Gemini من Google.

## 🚀 الميزات

- 💬 دردشة ذكية مع نموذج AI محلي
- 🔒 خصوصية كاملة - كل البيانات تعمل على جهازك
- ⚡ سريع وخفيف الوزن
- 🎨 واجهة مستخدم حديثة
- 📱 يعمل على أي جهاز

## 🛠️ التقنيات المستخدمة

### Backend
- **Python 3.9+**
- **Flask** - إطار العمل للخادم
- **Ollama** - لتشغيل نماذج AI محلياً
- **LLaMA/Mistral** - نموذج اللغة

### Frontend
- **React.js** - واجهة المستخدم
- **Tailwind CSS** - تصميم عصري
- **Axios** - للتواصل مع الخادم

## 📋 المتطلبات

- Python 3.9+
- Node.js 16+
- Ollama (تحميل من https://ollama.ai)
- RAM: 8GB على الأقل (16GB أفضل)

## 🔧 التثبيت السريع

### 1. استنساخ المشروع
```bash
git clone https://github.com/dhmdbeyhi096-commits/blank-app.git
cd blank-app
```

### 2. تثبيت Ollama
```bash
# على Linux/macOS
curl -fsSL https://ollama.com/install.sh | sh

# أو تحميل من https://ollama.ai
```

### 3. تحميل النموذج
```bash
ollama pull mistral
```

### 4. إعداد Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. إعداد Frontend
```bash
cd ../frontend
npm install
```

## ▶️ التشغيل

**نافذة 1:**
```bash
ollama serve
```

**نافذة 2:**
```bash
cd backend
python app.py
```

**نافذة 3:**
```bash
cd frontend
npm start
```

الآن افتح: **http://localhost:3000** 🎉
