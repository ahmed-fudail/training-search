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
    padding: 12px 15px;
    margin-bottom: 10px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }
  .card strong { color: #0077aa; }
  .status { text-align: center; font-size: 13px; color: #777; margin-bottom: 10px; }
</style>
</head>
<body>
<h2>🔍 بحث البرامج التدريبية للموظفين</h2>
<input type="text" id="searchBox" placeholder="اكتب رقم الموظف أو اسم البرنامج..." />
<div class="status" id="status">جارٍ تحميل البيانات...</div>
<div id="results"></div>

<script>
// تم التعديل: أصبح الرابط يشير إلى ملف 'data.csv' داخل مستودع GitHub
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
        row.push(cur);
        cur = '';
      } else cur += ch;
    }
    row.push(cur);
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
      const decoder = new TextDecoder('utf-8');
      text = decoder.decode(await blob.arrayBuffer());
    } catch(e) {
      // محاولة فك الترميز بترميز مختلف في حالة فشل UTF-8
      const decoder = new TextDecoder('windows-1256'); 
      text = decoder.decode(await blob.arrayBuffer());
    }
    allRows = parseCSV(text);
    // تم التعديل: لا تقم بالعرض إذا كان هناك صف واحد فقط (العناوين)
    if (allRows.length <= 1) {
        status.textContent = "⚠️ فشل تحميل البيانات أو الملف فارغ.";
        return;
    }
    status.textContent = "✅ تم تحميل " + (allRows.length - 1) + " سجلاً.";
  } catch (err) {
    status.textContent = "❌ حدث خطأ أثناء تحميل البيانات: " + err.message;
  }
}

function search() {
  const query = document.getElementById('searchBox').value.trim();
  const resultsDiv = document.getElementById('results');
  resultsDiv.innerHTML = '';

  if (!query) return;

  // تأكد من وجود بيانات قبل البحث
  if (allRows.length <= 1) {
        resultsDiv.innerHTML = "<p>البيانات غير متوفرة للبحث.</p>";
        return;
    }
    
  const headers = allRows[0];
  const rows = allRows.slice(1);
  let results = [];

  // البحث عن مؤشرات أسماء الأعمدة (قد تختلف بناءً على ملفك)
  const indexMap = {
    'رقم_الموظف': headers.findIndex(h => h && h.trim().includes('رقم')),
    'اسم_البرنامج': headers.findIndex(h => h && h.trim().includes('برنامج'))
  };

  // فحص إذا كان الإدخال رقماً
  if (/^\d+$/.test(query) && indexMap['رقم_الموظف'] !== -1) {
    // البحث برقم الموظف
    const idx = indexMap['رقم_الموظف'];
    results = rows.filter(r => r[idx] && r[idx].toString().includes(query));
  } else if (indexMap['اسم_البرنامج'] !== -1) {
    // البحث باسم البرنامج
    const idx = indexMap['اسم_البرنامج'];
    results = rows.filter(r => r[idx] && r[idx].toString().includes(query));
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
    card.innerHTML = `
      <strong>الموظف:</strong> ${obj['اسم الموظف'] || obj['الاسم'] || '-'}<br>
      <strong>رقم الموظف:</strong> ${obj['رقم الموظف'] || obj['رقم'] || '-'}<br>
      <strong>البرنامج:</strong> ${obj['اسم البرنامج'] || obj['البرنامج'] || '-'}<br>
      <strong>التاريخ:</strong> ${obj['تاريخ البرنامج'] || obj['التاريخ'] || '-'}
    `;
    resultsDiv.appendChild(card);
  }
}

document.getElementById('searchBox').addEventListener('input', search);
loadData();
</script>
</body>
</html>
