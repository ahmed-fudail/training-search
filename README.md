<!doctype html>
<html lang="ar">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>بحث البرامج التدريبية للموظفين</title>
<style>
  body {
    font-family: "Noto Naskh Arabic", Arial, sans-serif;
    background: #f6f7fb;
    direction: rtl;
    padding: 20px;
  }
  h2 { text-align: center; color: #333; margin-bottom: 15px; }
  #searchBox {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    border-radius: 8px;
    border: 1px solid #ccc;
    margin-bottom: 15px;
  }
  .card {
    background: #fff;
    border-radius: 10px;
    padding: 15px; /* زيادة التباعد لتحسين العرض */
    margin-bottom: 10px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    border-right: 4px solid #0077aa; /* إضافة خط جانبي للتمييز */
  }
  .card strong { color: #0077aa; display: inline-block; width: 100px; } /* لترتيب العناوين */
  .status { text-align: center; font-size: 13px; color: #777; margin-bottom: 10px; }
</style>
</head>
<body>
<h2>🔍 بحث البرامج التدريبية للموظفين</h2>
<input type="text" id="searchBox" placeholder="اكتب رقم التوظيف أو اسم البرنامج..." />
<div class="status" id="status">جارٍ تحميل البيانات...</div>
<div id="results"></div>

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
        return;
    }
    
    status.textContent = "✅ تم تحميل " + (allRows.length - 1) + " سجلاً. ابدأ البحث.";
  } catch (err) {
    status.textContent = "❌ حدث خطأ أثناء تحميل البيانات: " + err.message;
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
  const indexMap = {
    'رقم_التوظيف': headers.findIndex(h => h.includes('رقم التوظيف') || h.includes('رقم التامين') || h.includes('رقم')),
    'اسم_المستخدم': headers.findIndex(h => h.includes('اسم المستخدم') || h.includes('اسم الموظف') || h.includes('الاسم')),
    'اسم_البرنامج': headers.findIndex(h => h.includes('اسم البرنامج') || h.includes('البرنامج')),
    'التاريخ': headers.findIndex(h => h.includes('السنة') || h.includes('التاريخ') || h.includes('عام'))
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
    
    // العرض: تم التعديل ليتطابق مع أسماء أعمدتك
    card.innerHTML = `
      <strong>الموظف:</strong> ${obj[headers[indexMap['اسم_المستخدم']]] || '-'}<br>
      <strong>رقم الموظف:</strong> ${obj[headers[indexMap['رقم_التوظيف']]] || '-'}<br>
      <strong>البرنامج:</strong> ${obj[headers[indexMap['اسم_البرنامج']]] || '-'}<br>
      <strong>التاريخ:</strong> ${obj[headers[indexMap['التاريخ']]] || '-'}
    `;
    
    resultsDiv.appendChild(card);
  }
}

document.getElementById('searchBox').addEventListener('input', search);
loadData();
</script>
</body>
</html>
