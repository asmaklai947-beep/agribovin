<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<meta name="theme-color" content="#2e7d32">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<title>AgriBovin IA</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
  *{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
  body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f5f7f5;color:#1a1a1a;min-height:100vh}

  /* ── TOPBAR ── */
  .topbar{background:#ffffff;border-bottom:1px solid #e0ede0;padding:12px 16px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100}
  .topbar-left{display:flex;align-items:center;gap:10px}
  .logo{width:36px;height:36px;background:#e8f5e9;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px}
  .app-name{font-size:16px;font-weight:700;color:#1b5e20}
  .app-sub{font-size:11px;color:#81c784}
  .topbar-right{display:flex;align-items:center;gap:8px}

  /* ── LANG SWITCHER ── */
  .lang-switcher{display:flex;background:#f1f8e9;border-radius:20px;padding:3px;gap:2px}
  .lang-btn{border:none;background:transparent;padding:4px 10px;border-radius:16px;font-size:12px;font-weight:600;color:#388e3c;cursor:pointer;transition:all .15s}
  .lang-btn.active{background:#2e7d32;color:#ffffff}

  /* ── REFRESH BTN ── */
  .refresh-btn{width:34px;height:34px;border-radius:50%;background:#f1f8e9;border:1px solid #c8e6c9;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:16px;transition:transform .3s}
  .refresh-btn.spinning{animation:spin .6s linear infinite}
  @keyframes spin{to{transform:rotate(360deg)}}

  /* ── STATUS BAR ── */
  .status-bar{background:#e8f5e9;padding:6px 16px;display:flex;align-items:center;justify-content:space-between;font-size:11px;color:#2e7d32}
  .status-dot{width:7px;height:7px;border-radius:50%;background:#4caf50;display:inline-block;margin-right:5px;animation:pulse 2s infinite}
  @keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}

  /* ── MAIN ── */
  .main{padding:14px 14px 80px}

  /* ── ERROR ── */
  .error-card{background:#ffebee;border:1px solid #ffcdd2;border-radius:12px;padding:16px;margin-bottom:14px;color:#b71c1c;font-size:14px}

  /* ── METRICS GRID ── */
  .metrics{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px}
  .metric{background:#ffffff;border-radius:12px;padding:14px;border:1px solid #e8f0e8}
  .metric-label{font-size:11px;color:#78909c;margin-bottom:4px;font-weight:500}
  .metric-value{font-size:26px;font-weight:800;line-height:1}
  .metric-value.green{color:#2e7d32}
  .metric-value.orange{color:#e65100}
  .metric-value.red{color:#c62828}
  .metric-value.blue{color:#1565c0}
  .metric-badge{display:inline-block;margin-top:5px;font-size:10px;font-weight:600;padding:2px 8px;border-radius:10px}
  .badge-ok{background:#e8f5e9;color:#2e7d32}
  .badge-warn{background:#fff3e0;color:#e65100}
  .badge-crit{background:#ffebee;color:#c62828}

  /* ── SECTION TITLE ── */
  .section-title{font-size:13px;font-weight:700;color:#37474f;margin:16px 0 10px;text-transform:uppercase;letter-spacing:.06em}

  /* ── CARD ── */
  .card{background:#ffffff;border-radius:14px;border:1px solid #e8f0e8;padding:14px;margin-bottom:12px}
  .card-title{font-size:13px;font-weight:600;color:#546e7a;margin-bottom:12px}

  /* ── DONUT LEGEND ── */
  .legend{display:flex;gap:12px;flex-wrap:wrap;margin-top:10px}
  .legend-item{display:flex;align-items:center;gap:5px;font-size:12px;color:#546e7a}
  .legend-dot{width:10px;height:10px;border-radius:2px;flex-shrink:0}

  /* ── ALERTS ── */
  .alert-item{padding:10px 12px;border-radius:10px;margin-bottom:8px;font-size:13px}
  .alert-item:last-child{margin-bottom:0}
  .alert-crit{background:#ffebee;border-left:3px solid #e53935;color:#b71c1c}
  .alert-warn{background:#fff8e1;border-left:3px solid #fb8c00;color:#e65100}
  .alert-ok{background:#e8f5e9;border-left:3px solid #43a047;color:#1b5e20;padding:10px 12px;border-radius:10px;font-size:13px}
  .alert-name{font-weight:700;margin-bottom:2px}

  /* ── TABLE ── */
  .table-scroll{overflow-x:auto;border-radius:10px}
  table{width:100%;border-collapse:collapse;font-size:13px;min-width:320px}
  th{font-size:11px;font-weight:600;color:#78909c;padding:8px 10px;border-bottom:1px solid #e8f0e8;text-align:left;white-space:nowrap}
  td{padding:10px 10px;border-bottom:1px solid #f5f7f5;color:#263238;vertical-align:middle}
  tr:last-child td{border-bottom:none}
  .pill{font-size:11px;padding:3px 8px;border-radius:10px;font-weight:600;white-space:nowrap}
  .pill-normal{background:#e8f5e9;color:#1b5e20}
  .pill-alerte{background:#fff3e0;color:#e65100}
  .pill-critique{background:#ffebee;color:#c62828}

  /* ── FILTER PILLS ── */
  .filters{display:flex;gap:7px;margin-bottom:12px;flex-wrap:wrap}
  .filter-pill{border:1px solid #c8e6c9;border-radius:20px;padding:5px 13px;font-size:12px;font-weight:600;cursor:pointer;background:transparent;color:#546e7a;transition:all .15s}
  .filter-pill.active{background:#2e7d32;border-color:#2e7d32;color:#ffffff}

  /* ── FOOTER ── */
  .footer{text-align:center;font-size:11px;color:#aaa;padding:12px 0 4px;border-top:1px solid #e8f0e8;margin-top:8px}

  /* ── RTL support ── */
  body.rtl{direction:rtl}
  body.rtl .alert-crit,body.rtl .alert-warn{border-left:none;border-right:3px solid}
  body.rtl .alert-crit{border-right-color:#e53935}
  body.rtl .alert-warn{border-right-color:#fb8c00}
</style>
</head>
<body>

<!-- TOPBAR -->
<div class="topbar">
  <div class="topbar-left">
    <div class="logo">🐄</div>
    <div>
      <div class="app-name">AgriBovin IA</div>
      <div class="app-sub" id="sub-tagline">Santé animale intelligente</div>
    </div>
  </div>
  <div class="topbar-right">
    <div class="lang-switcher">
      <button class="lang-btn active" onclick="setLang('fr')">FR</button>
      <button class="lang-btn" onclick="setLang('ar')">AR</button>
      <button class="lang-btn" onclick="setLang('en')">EN</button>
    </div>
    <div class="refresh-btn" id="refreshBtn" onclick="refreshData()">&#x21bb;</div>
  </div>
</div>

<!-- STATUS BAR -->
<div class="status-bar">
  <span><span class="status-dot"></span><span id="status-txt">En ligne · Dernière maj :</span> <span id="last-update">—</span></span>
  <span id="source-txt">Source: PHP</span>
</div>

<!-- MAIN -->
<div class="main">
  <div id="error-zone"></div>

  <!-- METRICS -->
  <div id="section-overview" class="section-title">Vue d'ensemble</div>
  <div class="metrics">
    <div class="metric">
      <div class="metric-label" id="lbl-total">Total animaux</div>
      <div class="metric-value blue" id="m-total">—</div>
      <span class="metric-badge badge-ok" id="b-total">têtes</span>
    </div>
    <div class="metric">
      <div class="metric-label" id="lbl-sains">En bonne santé</div>
      <div class="metric-value green" id="m-sains">—</div>
      <span class="metric-badge badge-ok" id="b-sain">normal</span>
    </div>
    <div class="metric">
      <div class="metric-label" id="lbl-alertes">En alerte</div>
      <div class="metric-value orange" id="m-alertes">—</div>
      <span class="metric-badge badge-warn" id="b-alert">alerte</span>
    </div>
    <div class="metric">
      <div class="metric-label" id="lbl-critiques">Critiques</div>
      <div class="metric-value red" id="m-critiques">—</div>
      <span class="metric-badge badge-crit" id="b-crit">critique</span>
    </div>
  </div>

  <!-- DONUT -->
  <div id="section-charts" class="section-title">Graphiques</div>
  <div class="card">
    <div class="card-title" id="lbl-repartition">Répartition santé</div>
    <div style="position:relative;width:100%;height:200px">
      <canvas id="donutChart" role="img" aria-label="Répartition des statuts de santé"></canvas>
    </div>
    <div class="legend" id="donut-legend"></div>
  </div>

  <!-- BAR CHART -->
  <div class="card">
    <div class="card-title" id="lbl-confiance">Confiance IA par animal</div>
    <div id="bar-wrap" style="position:relative;width:100%;height:240px">
      <canvas id="barChart" role="img" aria-label="Score de confiance IA par animal"></canvas>
    </div>
  </div>

  <!-- ALERTS -->
  <div id="section-alerts" class="section-title">Alertes récentes</div>
  <div class="card" id="alerts-card">
    <div id="alert-list"><div style="color:#aaa;font-size:13px">Chargement...</div></div>
  </div>

  <!-- TABLE -->
  <div id="section-diag" class="section-title">Diagnostic détaillé</div>
  <div class="card">
    <div class="filters" id="filter-row">
      <button class="filter-pill active" onclick="filterTable('all',this)" id="f-all">Tous</button>
      <button class="filter-pill" onclick="filterTable('normal',this)" id="f-normal">Normal</button>
      <button class="filter-pill" onclick="filterTable('alerte',this)" id="f-alerte">Alerte</button>
      <button class="filter-pill" onclick="filterTable('critique',this)" id="f-critique">Critique</button>
    </div>
    <div class="table-scroll">
      <table>
        <thead>
          <tr>
            <th id="th-animal">Animal</th>
            <th id="th-statut">Statut</th>
            <th id="th-diag">Diagnostic</th>
            <th id="th-conf">Confiance</th>
          </tr>
        </thead>
        <tbody id="diag-tbody"></tbody>
      </table>
    </div>
  </div>

  <div class="footer" id="footer-txt">AgriBovin IA v3.0 · Auto-refresh 30s</div>
</div>

<script>
const API_URL = "https://bovin.atwebpages.com/api/ia_data.php";
let allResults = [];
let donutInst = null, barInst = null;
let currentLang = 'fr';

const T = {
  fr: {
    tagline:"Santé animale intelligente", online:"En ligne · Dernière maj :", source:"Source",
    overview:"Vue d'ensemble", total:"Total animaux", sains:"En bonne santé", alertes:"En alerte", critiques:"Critiques",
    tetes:"têtes", normal:"normal", alerte:"alerte", critique:"critique",
    charts:"Graphiques", repartition:"Répartition santé", confiance:"Confiance IA par animal",
    alertsTitle:"Alertes récentes", noAlerts:"Aucune alerte active", diag:"Diagnostic détaillé",
    all:"Tous", thAnimal:"Animal", thStatut:"Statut", thDiag:"Diagnostic", thConf:"Confiance",
    loading:"Chargement...", noData:"Aucune donnée", errApi:"Erreur API :",
    footer:"AgriBovin IA v3.0 · Auto-refresh 30s"
  },
  ar: {
    tagline:"صحة الحيوانات الذكية", online:"متصل · آخر تحديث :", source:"المصدر",
    overview:"نظرة عامة", total:"إجمالي الحيوانات", sains:"بصحة جيدة", alertes:"في حالة تنبيه", critiques:"حالات حرجة",
    tetes:"رأس", normal:"طبيعي", alerte:"تنبيه", critique:"حرج",
    charts:"الرسوم البيانية", repartition:"توزيع الحالات الصحية", confiance:"مستوى ثقة الذكاء الاصطناعي",
    alertsTitle:"التنبيهات الأخيرة", noAlerts:"لا توجد تنبيهات نشطة", diag:"التشخيص التفصيلي",
    all:"الكل", thAnimal:"الحيوان", thStatut:"الحالة", thDiag:"التشخيص", thConf:"الثقة",
    loading:"جارٍ التحميل...", noData:"لا توجد بيانات", errApi:"خطأ في API :",
    footer:"AgriBovin IA v3.0 · تحديث تلقائي كل 30 ثانية"
  },
  en: {
    tagline:"Intelligent animal health", online:"Online · Last update:", source:"Source",
    overview:"Overview", total:"Total animals", sains:"Healthy", alertes:"On alert", critiques:"Critical",
    tetes:"heads", normal:"normal", alerte:"alert", critique:"critical",
    charts:"Charts", repartition:"Health breakdown", confiance:"AI confidence per animal",
    alertsTitle:"Recent alerts", noAlerts:"No active alerts", diag:"Detailed diagnosis",
    all:"All", thAnimal:"Animal", thStatut:"Status", thDiag:"Diagnosis", thConf:"Confidence",
    loading:"Loading...", noData:"No data available", errApi:"API error:",
    footer:"AgriBovin IA v3.0 · Auto-refresh 30s"
  }
};

function t(k){ return T[currentLang][k] || k; }

function setLang(lang) {
  currentLang = lang;
  document.documentElement.lang = lang;
  document.body.classList.toggle('rtl', lang === 'ar');
  document.querySelectorAll('.lang-btn').forEach(b => b.classList.toggle('active', b.textContent === lang.toUpperCase()));
  applyTranslations();
}

function applyTranslations() {
  const ids = {
    'sub-tagline':'tagline','status-txt':'online','section-overview':'overview',
    'lbl-total':'total','lbl-sains':'sains','lbl-alertes':'alertes','lbl-critiques':'critiques',
    'b-sain':'normal','b-alert':'alerte','b-crit':'critique',
    'section-charts':'charts','lbl-repartition':'repartition','lbl-confiance':'confiance',
    'section-alerts':'alertsTitle','section-diag':'diag',
    'f-all':'all','th-animal':'thAnimal','th-statut':'thStatut','th-diag':'thDiag','th-conf':'thConf',
    'footer-txt':'footer'
  };
  Object.entries(ids).forEach(([id,key]) => {
    const el = document.getElementById(id);
    if(el) el.textContent = t(key);
  });
  document.getElementById('source-txt').textContent = t('source') + ': PHP';
  renderTable(allResults);
  renderAlerts(window._alertsData || []);
}

async function fetchData() {
  const r = await fetch(API_URL);
  return await r.json();
}

function renderMetrics(stats) {
  document.getElementById('m-total').textContent = stats.total ?? '—';
  document.getElementById('m-sains').textContent = stats.sains ?? '—';
  document.getElementById('m-alertes').textContent = stats.alertes ?? '—';
  document.getElementById('m-critiques').textContent = stats.critiques ?? '—';
  document.getElementById('b-total').textContent = (stats.total ?? 0) + ' ' + t('tetes');
}

function renderDonut(results) {
  const counts = {normal:0,alerte:0,critique:0};
  results.forEach(r => { if(counts[r.statut]!==undefined) counts[r.statut]++; });
  const labels = [t('normal'), t('alerte'), t('critique')];
  const colors = ['#4caf50','#ff9800','#f44336'];
  if(donutInst) donutInst.destroy();
  donutInst = new Chart(document.getElementById('donutChart'),{
    type:'doughnut',
    data:{ labels, datasets:[{ data:[counts.normal,counts.alerte,counts.critique], backgroundColor:colors, borderWidth:2, borderColor:'#fff', hoverOffset:4 }]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:ctx=>` ${ctx.label}: ${ctx.parsed}`}}},cutout:'58%'}
  });
  document.getElementById('donut-legend').innerHTML = labels.map((l,i)=>
    `<span class="legend-item"><span class="legend-dot" style="background:${colors[i]}"></span>${l}: ${[counts.normal,counts.alerte,counts.critique][i]}</span>`
  ).join('');
}

function renderBar(results) {
  const top = [...results].sort((a,b)=>b.confidence-a.confidence).slice(0,10);
  const colorMap = {normal:'#4caf50',alerte:'#ff9800',critique:'#f44336'};
  const h = Math.max(200, top.length*30+60);
  document.getElementById('bar-wrap').style.height = h+'px';
  if(barInst) barInst.destroy();
  barInst = new Chart(document.getElementById('barChart'),{
    type:'bar',
    data:{labels:top.map(r=>r.nom_animal),datasets:[{data:top.map(r=>r.confidence),backgroundColor:top.map(r=>colorMap[r.statut]||'#888'),borderRadius:4,borderSkipped:false}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:ctx=>` ${ctx.parsed.x}%`}}},scales:{x:{min:0,max:100,grid:{color:'rgba(0,0,0,0.04)'},ticks:{callback:v=>v+'%',font:{size:10}}},y:{grid:{display:false},ticks:{font:{size:10}}}}}
  });
}

function renderAlerts(alertes) {
  window._alertsData = alertes;
  const c = document.getElementById('alert-list');
  if(!alertes||!alertes.length){
    c.innerHTML = `<div class="alert-ok">${t('noAlerts')}</div>`; return;
  }
  c.innerHTML = alertes.slice(0,6).map(a=>`
    <div class="alert-item ${a.severite==='critique'?'alert-crit':'alert-warn'}">
      <div class="alert-name">${a.nom_animal}</div>
      <div>${a.message}</div>
    </div>`).join('');
}

let _activeFilter = 'all';
function filterTable(f, btn) {
  _activeFilter = f;
  document.querySelectorAll('.filter-pill').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  renderTable(allResults);
}

function renderTable(results) {
  const tbody = document.getElementById('diag-tbody');
  const filtered = _activeFilter==='all' ? results : results.filter(r=>r.statut===_activeFilter);
  if(!filtered.length){ tbody.innerHTML=`<tr><td colspan="4" style="color:#aaa;text-align:center;padding:16px">${t('noData')}</td></tr>`; return; }
  tbody.innerHTML = filtered.map(r=>`<tr>
    <td style="font-weight:600">${r.nom_animal}</td>
    <td><span class="pill pill-${r.statut}">${t(r.statut)}</span></td>
    <td style="color:#546e7a;font-size:12px">${r.maladie||'—'}</td>
    <td style="font-weight:600;color:#1b5e20">${r.confidence}%</td>
  </tr>`).join('');
}

async function refreshData() {
  const btn = document.getElementById('refreshBtn');
  btn.classList.add('spinning');
  document.getElementById('error-zone').innerHTML = '';
  try {
    const data = await fetchData();
    if(!data.success) throw new Error(data.error||'unknown');
    allResults = data.resultats_ia || [];
    renderMetrics(data.stats||{});
    if(allResults.length){ renderDonut(allResults); renderBar(allResults); }
    renderAlerts(data.alertes||[]);
    renderTable(allResults);
    document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
    document.getElementById('source-txt').textContent = t('source')+': '+(data.source_ia||'PHP');
  } catch(e) {
    document.getElementById('error-zone').innerHTML = `<div class="error-card">${t('errApi')} ${e.message}</div>`;
  }
  btn.classList.remove('spinning');
}

refreshData();
setInterval(refreshData, 30000);
</script>
</body>
</html>
