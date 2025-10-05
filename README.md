# training-search[search-training.html](https://github.com/user-attachments/files/22708744/search-training.html)
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
// 🔗 رابط Google Sheets المنشور بصيغة CSV
const SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS87lvYltE1YCV9guU9zbmhcMJar37Uw0WRib-IkLGyPfC00mpIz2eoA_McZBEn2Q/pub?gid=1388607762&single=true&output=csv";
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
      const decoder = new TextDecoder('utf-16le');
      text = decoder.decode(await blob.arrayBuffer());
    }
    allRows = parseCSV(text);
    status.textContent = "تم تحميل " + (allRows.length - 1) + " سجلاً.";
  } catch (err) {
    status.textContent = "حدث خطأ أثناء تحميل البيانات: " + err.message;
  }
}

function search() {
  const query = document.getElementById('searchBox').value.trim();
  const resultsDiv = document.getElementById('results');
  resultsDiv.innerHTML = '';

  if (!query) return;

  const headers = allRows[0];
  const rows = allRows.slice(1);
  let results = [];

  if (/^\d+$/.test(query)) {
    // رقم الموظف
    const idx = headers.findIndex(h => h.includes('رقم'));
    results = rows.filter(r => r[idx] && r[idx].includes(query));
  } else {
    // اسم البرنامج
    const idx = headers.findIndex(h => h.includes('برنامج'));
    results = rows.filter(r => r[idx] && r[idx].includes(query));
  }

  if (results.length === 0) {
    resultsDiv.innerHTML = "<p>❌ لا توجد نتائج.</p>";
    return;
  }

  for (let r of results) {
    const obj = {};
    headers.forEach((h,i)=> obj[h] = r[i]);
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
      <strong>الموظف:</strong> ${obj['اسم الموظف'] || obj['الاسم'] || '-'}<br>
      <strong>رقم الموظف:</strong> ${obj['رقم الموظف'] || '-'}<br>
      <strong>البرنامج:</strong> ${obj['اسم البرنامج'] || '-'}<br>
      <strong>التاريخ:</strong> ${obj['تاريخ البرنامج'] || '-'}
    `;
    resultsDiv.appendChild(card);
  }
}

document.getElementById('searchBox').addEventListener('input', search);
loadData();
</script>
</body>
</html>
