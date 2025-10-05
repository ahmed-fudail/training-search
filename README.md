<!doctype html>
<html lang="ar">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>بحث البرامج التدريبية للموظفين</title>

<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">

<style>
    /* ------------------ تعريفات الألوان والتدرجات ------------------ */
    :root {
      --primary-color: #667eea;
      --secondary-color: #764ba2;
      --primary-gradient: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
      --glass-bg: rgba(255, 255, 255, 0.2);
      --glass-border: rgba(255, 255, 255, 0.3);
      --card-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    }
    
    /* ------------------ نمط الجسم العام والخلفية ------------------ */
    body {
        font-family: 'Cairo', "Noto Naskh Arabic", Arial, sans-serif;
        direction: rtl;
        padding: 20px;
        min-height: 100vh;
        color: #333;
        /* خلفية متدرجة متحركة */
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ------------------ العناوين وحالة التحميل ------------------ */
    h2 { 
        text-align: center; 
        color: #fff; /* لون أبيض للخلفية الداكنة */
        margin-bottom: 25px; 
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .status { 
        text-align: center; 
        font-size: 14px; 
        color: #fff; 
        margin-bottom: 20px;
        font-weight: 600;
        padding: 10px;
        background: rgba(0,0,0,0.2);
        border-radius: 8px;
    }
    .status.success {
        background: rgba(4, 182, 4, 0.7); /* لون أخضر للنجاح */
    }
    .status.error {
        background: rgba(255, 0, 0, 0.7); /* لون أحمر للخطأ */
    }

    /* ------------------ حقل البحث ------------------ */
    #searchBox {
        width: 100%;
        max-width: 500px; /* لتقييد حجم صندوق البحث */
        margin: 0 auto 25px auto;
        display: block;
        padding: 14px 20px;
        font-size: 16px;
        border-radius: 30px; /* شكل دائري أكثر */
        border: none;
        background: rgba(255, 255, 255, 0.95); /* خلفية بيضاء شفافة قليلاً */
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    #searchBox:focus {
        outline: none;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
        transform: translateY(-2px);
    }
    
    /* ------------------ بطاقات النتائج (Glass Card) ------------------ */
    .card {
        background: var(--glass-bg);
        backdrop-filter: blur(10px); /* تأثير الزجاج */
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: var(--card-shadow);
        border: 1px solid var(--glass-border);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(31, 38, 135, 0.45);
    }

    /* شريط التمييز الجانبي */
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 10px;
        height: 100%;
        background: var(--primary-gradient); /* شريط ملون بتدرج */
    }

    /* تنسيق المحتوى داخل البطاقة */
    .card-content div {
        display: flex;
        align-items: center;
        margin-bottom: 8px;
        padding-right: 15px; /* مسافة للعلامات */
    }
    .card-content strong { 
        color: var(--secondary-color); /* لون بنفسجي لعناوين البيانات */
        font-weight: 700;
        min-width: 110px; /* عرض ثابت لترتيب البيانات */
        display: inline-block;
    }
    .card-content span {
        font-weight: 600;
        color: #333;
    }
    .card-content i {
        color: var(--primary-color); /* لون أزرق للأيقونات */
        margin-left: 10px;
        font-style: normal; /* لإزالة الميلان الافتراضي للأيقونات */
    }

    /* حالة لا توجد نتائج */
    #results p {
        text-align: center;
        padding: 20px;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        font-weight: 600;
        color: #e73c7e;
    }
</style>
</head>
<body>

<div class="max-w-3xl mx-auto">
    <h2>🔍 بحث البرامج التدريبية للموظفين</h2>
    <input type="text" id="searchBox" placeholder="اكتب رقم التوظيف أو اسم البرنامج..." />
    <div class="status" id="status">جارٍ تحميل البيانات...</div>
    <div id="results"></div>
</div>

<script>
// الرابط يشير إلى ملف 'data.csv' في نفس المستودع
const SHEET_CSV_URL = "data.csv"; 

let allRows = [];

function parseCSV(text) {
  const rows = [];
  const lines = text.split(/\r?\n/).filter(l => l.trim() !== '');
  for (let line of lines) {
    const row = [];
    let cur = '', inQuotes = false;
    for (let i = 0; i < line.length; i++) {
      const ch = line[i];
      if (ch === '"') {
        if (inQuotes && line[i + 1] === '"') { cur += '"'; i++; }
        else inQuotes = !inQuotes;
      } else if (ch === ',' && !inQuotes) {
        row.push(cur.trim()); // إضافة trim لتنظيف الفراغات
        cur = '';
      } else cur += ch;
    }
    row.push(cur.trim());
    rows.push(row);
  }
  return rows;
}

async function loadData() {
  const status = document.getElementById('status');
  try {
    const resp = await fetch(SHEET_CSV_URL, { cache: "no-store" });
    if (!resp.ok) throw new Error("HTTP " + resp.status);
    const blob = await resp.blob();
    let text;
    try {
      // المحاولة الأولى: UTF-8 (الأكثر شيوعاً)
      const decoder = new TextDecoder('utf-8');
      text = decoder.decode(await blob.arrayBuffer());
    } catch(e) {
      // المحاولة الثانية: windows-1256 (ترميز عربي شائع)
      const decoder = new TextDecoder('windows-1256'); 
      text = decoder.decode(await blob.arrayBuffer());
    }
    
    allRows = parseCSV(text);

    if (allRows.length <= 1) {
        status.textContent = "⚠️ فشل تحميل البيانات: الملف فارغ أو به مشكلة في التنسيق.";
        status.classList.add('error');
        return;
    }
    
    status.textContent = "✅ تم تحميل " + (allRows.length - 1) + " سجلاً. ابدأ البحث.";
    status.classList.add('success');
  } catch (err) {
    status.textContent = "❌ حدث خطأ أثناء تحميل البيانات: " + err.message;
    status.classList.add('error');
  }
}

function search() {
  const query = document.getElementById('searchBox').value.trim();
  const resultsDiv = document.getElementById('results');
  resultsDiv.innerHTML = '';

  if (!query || allRows.length <= 1) return;

  const headers = allRows[0].map(h => h.trim()); // تنظيف رؤوس الأعمدة
  const rows = allRows.slice(1);
  let results = [];

  // تحديد مؤشرات الأعمدة بناءً على الكلمات المفتاحية في رؤوس الأعمدة
  // هذا يضمن المرونة في حالة اختلاف اسم العمود قليلاً عن المتوقع
  const indexMap = {
    'رقم_التوظيف': headers.findIndex(h => h.includes('رقم التوظيف') || h.includes('رقم الموظف') || h.includes('رقم')),
    'اسم_المستخدم': headers.findIndex(h => h.includes('اسم المستخدم') || h.includes('اسم الموظف') || h.includes('الاسم')),
    'اسم_البرنامج': headers.findIndex(h => h.includes('اسم البرنامج') || h.includes('البرنامج')),
    'التاريخ': headers.findIndex(h => h.includes('السنة') || h.includes('التاريخ') || h.includes('عام') || h.includes('تاريخ'))
  };
  
  // تنفيذ البحث
  let searchIndex = -1;
  
  // البحث برقم التوظيف إذا كان الإدخال رقماً
  if (/^\d+$/.test(query) && indexMap['رقم_التوظيف'] !== -1) {
    searchIndex = indexMap['رقم_التوظيف'];
  } 
  // البحث باسم البرنامج كخيار افتراضي أو إذا لم يكن رقماً
  else if (indexMap['اسم_البرنامج'] !== -1) {
    searchIndex = indexMap['اسم_البرنامج'];
  } else if (indexMap['اسم_المستخدم'] !== -1) {
        // إذا لم يعثر على عمود البرنامج، يبحث في اسم المستخدم
    searchIndex = indexMap['اسم_المستخدم'];
    }


  if (searchIndex !== -1) {
    const lowerQuery = query.toLowerCase();
    results = rows.filter(r => r[searchIndex] && r[searchIndex].toString().toLowerCase().includes(lowerQuery));
  }
  

  if (results.length === 0) {
    resultsDiv.innerHTML = "<p>❌ لا توجد نتائج مطابقة لـ: <strong>" + query + "</strong></p>";
    return;
  }

  for (let r of results) {
    const obj = {};
    headers.forEach((h,i)=> obj[h] = r[i]);
    const card = document.createElement('div');
    card.className = 'card';
    
    // استخراج أسماء الأعمدة الفعلية من الخريطة
    const nameCol = headers[indexMap['اسم_المستخدم']];
    const idCol = headers[indexMap['رقم_التوظيف']];
    const programCol = headers[indexMap['اسم_البرنامج']];
    const dateCol = headers[indexMap['التاريخ']];

    // العرض بتنسيق احترافي
    card.innerHTML = `
        <div class="card-content">
            <div><i>🧑‍💻</i><strong>الموظف:</strong> <span>${obj[nameCol] || '-'}</span></div>
            <div><i>🆔</i><strong>رقم التوظيف:</strong> <span>${obj[idCol] || '-'}</span></div>
            <div><i>📚</i><strong>البرنامج:</strong> <span>${obj[programCol] || '-'}</span></div>
            <div><i>📅</i><strong>التاريخ/السنة:</strong> <span>${obj[dateCol] || '-'}</span></div>
        </div>
    `;
    
    resultsDiv.appendChild(card);
  }
}

document.getElementById('searchBox').addEventListener('input', search);
loadData();
</script>
</body>
</html>
