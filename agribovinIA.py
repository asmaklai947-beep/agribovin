import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime
import time

st.set_page_config(
    page_title="AgriBovin IA",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://bovin.atwebpages.com/api/ia_data.php"

# ─── TRADUCTIONS ──────────────────────────────────────────────────────────────
TRANSLATIONS = {
    "FR": {
        "title": "🐄 AgriBovin — Santé Animale Intelligente",
        "caption": "Tableau de bord temps réel · IA diagnostique · Refresh automatique 30 s",
        "refresh_btn": "🔄 Actualiser les données",
        "last_update": "⏱️ **Dernière maj :**",
        "system": "📡 Système",
        "system_api": "**API :**",
        "system_db": "**DB :**",
        "system_refresh": "**Refresh :**",
        "system_btn": "📡 Informations Système",
        "recent_alerts": "🚨 Alertes récentes",
        "no_alert": "✅ Aucune alerte active",
        "alert_load_err": "❌ Impossible de charger les alertes",
        "overview": "### 📊 Vue d'ensemble",
        "total": "📦 Total animaux",
        "healthy": "✅ En bonne santé",
        "alert_count": "⚠️ En alerte",
        "critical": "🚨 Critiques",
        "charts": "### 📈 Visualisations",
        "pie_title": "Répartition des statuts de santé",
        "bar_title": "Score de confiance IA par animal",
        "diag_title": "### 📋 Diagnostic détaillé",
        "filter_label": "Filtrer par statut :",
        "filter_all": "Tous",
        "col_animal": "🐄 Animal",
        "col_status": "📊 Statut",
        "col_diag": "🔬 Diagnostic",
        "col_conf": "💯 Confiance %",
        "no_data": "ℹ️ Aucune donnée de diagnostic disponible.",
        "footer_source": "Source",
        "footer_last": "Dernière analyse",
        "footer_refresh": "Auto-refresh : 30 s",
        "api_err": "❌ Erreur API :",
        "api_check": "Vérifiez l'endpoint :",
        "lang_label": "🌐 Langue / Language",
        "statuts": {"normal": "normal", "alerte": "alerte", "critique": "critique"},
        "conf_suffix": "%",
    },
    "EN": {
        "title": "🐄 AgriBovin — Smart Animal Health",
        "caption": "Real-time dashboard · AI diagnostics · Auto-refresh every 30 s",
        "refresh_btn": "🔄 Refresh Data",
        "last_update": "⏱️ **Last update:**",
        "system": "📡 System",
        "system_api": "**API:**",
        "system_db": "**DB:**",
        "system_refresh": "**Refresh:**",
        "system_btn": "📡 System Information",
        "recent_alerts": "🚨 Recent Alerts",
        "no_alert": "✅ No active alerts",
        "alert_load_err": "❌ Could not load alerts",
        "overview": "### 📊 Overview",
        "total": "📦 Total animals",
        "healthy": "✅ Healthy",
        "alert_count": "⚠️ On alert",
        "critical": "🚨 Critical",
        "charts": "### 📈 Visualizations",
        "pie_title": "Health status distribution",
        "bar_title": "AI confidence score per animal",
        "diag_title": "### 📋 Detailed Diagnosis",
        "filter_label": "Filter by status:",
        "filter_all": "All",
        "col_animal": "🐄 Animal",
        "col_status": "📊 Status",
        "col_diag": "🔬 Diagnosis",
        "col_conf": "💯 Confidence %",
        "no_data": "ℹ️ No diagnostic data available.",
        "footer_source": "Source",
        "footer_last": "Last analysis",
        "footer_refresh": "Auto-refresh: 30 s",
        "api_err": "❌ API Error:",
        "api_check": "Check endpoint:",
        "lang_label": "🌐 Langue / Language",
        "statuts": {"normal": "normal", "alerte": "alert", "critique": "critical"},
        "conf_suffix": "%",
    },
    "AR": {
        "title": "🐄 أغريبوفان — الصحة الذكية للحيوانات",
        "caption": "لوحة تحكم فورية · تشخيص بالذكاء الاصطناعي · تحديث تلقائي كل 30 ث",
        "refresh_btn": "🔄 تحديث البيانات",
        "last_update": "⏱️ **آخر تحديث:**",
        "system": "📡 النظام",
        "system_api": "**API:**",
        "system_db": "**قاعدة البيانات:**",
        "system_refresh": "**التحديث:**",
        "system_btn": "📡 معلومات النظام",
        "recent_alerts": "🚨 التنبيهات الأخيرة",
        "no_alert": "✅ لا توجد تنبيهات نشطة",
        "alert_load_err": "❌ تعذّر تحميل التنبيهات",
        "overview": "### 📊 نظرة عامة",
        "total": "📦 إجمالي الحيوانات",
        "healthy": "✅ بصحة جيدة",
        "alert_count": "⚠️ في حالة تنبيه",
        "critical": "🚨 حالات حرجة",
        "charts": "### 📈 المخططات",
        "pie_title": "توزيع حالات الصحة",
        "bar_title": "درجة ثقة الذكاء الاصطناعي لكل حيوان",
        "diag_title": "### 📋 التشخيص التفصيلي",
        "filter_label": "تصفية حسب الحالة:",
        "filter_all": "الكل",
        "col_animal": "🐄 الحيوان",
        "col_status": "📊 الحالة",
        "col_diag": "🔬 التشخيص",
        "col_conf": "💯 نسبة الثقة %",
        "no_data": "ℹ️ لا توجد بيانات تشخيصية متاحة.",
        "footer_source": "المصدر",
        "footer_last": "آخر تحليل",
        "footer_refresh": "تحديث تلقائي: 30 ث",
        "api_err": "❌ خطأ في API:",
        "api_check": "تحقق من العنوان:",
        "lang_label": "🌐 Langue / Language",
        "statuts": {"normal": "طبيعي", "alerte": "تنبيه", "critique": "حرج"},
        "conf_suffix": "%",
    }
}

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main, .block-container,
[data-testid="stMainBlockContainer"] {
    background-color: #ffffff !important;
    color: #1a1a1a !important;
}
[data-testid="stApp"] { background-color: #ffffff !important; }

h1 {
    color: #1b5e20 !important;
    font-size: 1.9rem !important;
    font-weight: 700 !important;
    border-bottom: 2px solid #c8e6c9;
    padding-bottom: 10px;
    margin-bottom: 0 !important;
}
h2, h3 { color: #2e7d32 !important; font-weight: 600 !important; }

[data-testid="metric-container"] {
    background: #f1f8e9 !important;
    border: 1px solid #c8e6c9 !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
}
[data-testid="metric-container"] label {
    color: #388e3c !important; font-size: 13px !important;
    font-weight: 600 !important; letter-spacing: 0.03em !important;
}
[data-testid="metric-container"] [data-testid="metric-value"] {
    color: #1b5e20 !important; font-size: 2.2rem !important; font-weight: 800 !important;
}
[data-testid="stMetricDelta"] { font-size: 12px !important; }

[data-testid="stSidebar"] {
    background-color: #f9fdf6 !important;
    border-right: 1px solid #c8e6c9 !important;
}
[data-testid="stSidebar"] * { color: #2e7d32 !important; }

.stButton > button {
    background-color: #2e7d32 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 8px 16px !important;
    width: 100% !important;
    transition: background 0.2s ease !important;
}
.stButton > button:hover { background-color: #388e3c !important; color: #ffffff !important; }

[data-testid="stSelectbox"] > div > div {
    background-color: #f9fdf6 !important;
    border: 1px solid #c8e6c9 !important;
    border-radius: 8px !important;
    color: #1b5e20 !important;
}

[data-testid="stDataFrame"] {
    background-color: #ffffff !important;
    border: 1px solid #c8e6c9 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

hr { border-color: #c8e6c9 !important; margin: 12px 0 !important; }

.alert-box {
    padding: 10px 14px; border-radius: 8px;
    margin: 5px 0; font-size: 13px; line-height: 1.4;
}
.alert-critique {
    background-color: #ffebee; border-left: 4px solid #e53935; color: #b71c1c;
}
.alert-alerte {
    background-color: #fff8e1; border-left: 4px solid #fb8c00; color: #e65100;
}
.alert-normal {
    background-color: #e8f5e9; border-left: 4px solid #43a047; color: #1b5e20;
}

/* System info panel */
.system-panel {
    background: #f1f8e9;
    border: 1px solid #c8e6c9;
    border-radius: 10px;
    padding: 12px 16px;
    margin-top: 8px;
    font-size: 13px;
}
.system-panel p { margin: 4px 0; color: #2e7d32; }

.footer-bar {
    text-align: center; color: #81c784; font-size: 12px;
    padding: 10px; margin-top: 10px;
    border-top: 1px solid #e8f5e9; background-color: #ffffff;
}

[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"],
[data-testid="column"] { background-color: transparent !important; }

[data-testid="stInfo"], [data-testid="stWarning"],
[data-testid="stError"], [data-testid="stSuccess"] { border-radius: 8px !important; }

/* RTL support for Arabic */
.rtl { direction: rtl; text-align: right; }
</style>
""", unsafe_allow_html=True)


# ─── SESSION STATE ────────────────────────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "FR"
if "show_system" not in st.session_state:
    st.session_state.show_system = False


# ─── Chargement des données ───────────────────────────────────────────────────
@st.cache_data(ttl=30)
def load_data():
    try:
        r = requests.get(API_URL, timeout=10)
        return r.json()
    except Exception as e:
        return {"success": False, "error": str(e)}


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🐄 AgriBovin IA")
    st.markdown("---")

    # ── Sélecteur de langue ──
    lang_options = ["FR", "EN", "AR"]
    T = TRANSLATIONS[st.session_state.lang]

    selected_lang = st.selectbox(
        T["lang_label"],
        lang_options,
        index=lang_options.index(st.session_state.lang),
        key="lang_selector"
    )
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()

    T = TRANSLATIONS[st.session_state.lang]  # reload after possible change

    st.markdown("---")

    if st.button(T["refresh_btn"]):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    now_str = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
    st.markdown(f"{T['last_update']} `{now_str}`")
    st.markdown("---")

    # ── Bouton Système (toggle) ──
    if st.button(T["system_btn"]):
        st.session_state.show_system = not st.session_state.show_system

    if st.session_state.show_system:
        st.markdown(
            f"""<div class="system-panel">
                <p>🔌 {T['system_api']} PHP Expert</p>
                <p>🗄️ {T['system_db']} MySQL AwardSpace</p>
                <p>🔄 {T['system_refresh']} 30 s</p>
            </div>""",
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.markdown(f"### {T['recent_alerts']}")
    data_sb = load_data()
    if data_sb.get("success"):
        alertes_sb = data_sb.get("alertes", [])
        if alertes_sb:
            for a in alertes_sb[:5]:
                sev  = a.get("severite", "alerte")
                nom  = a.get("nom_animal", "?")
                msg  = a.get("message", "")
                cls  = "alert-critique" if sev == "critique" else "alert-alerte"
                icon = "🔴" if sev == "critique" else "🟡"
                st.markdown(
                    f'<div class="alert-box {cls}">{icon} <b>{nom}</b><br>{msg}</div>',
                    unsafe_allow_html=True
                )
        else:
            st.success(T["no_alert"])
    else:
        st.error(T["alert_load_err"])


# ─── EN-TÊTE ─────────────────────────────────────────────────────────────────
rtl_class = "rtl" if st.session_state.lang == "AR" else ""
st.markdown(f'<div class="{rtl_class}"><h1>{T["title"]}</h1></div>', unsafe_allow_html=True)
st.caption(T["caption"])

# ─── Chargement principal ─────────────────────────────────────────────────────
data = load_data()

if not data.get("success"):
    st.error(f"{T['api_err']} {data.get('error', '?')}")
    st.info(f"{T['api_check']} `{API_URL}`")
    st.stop()

stats   = data.get("stats", {})
results = data.get("resultats_ia", [])
alertes = data.get("alertes", [])


# ─── MÉTRIQUES ───────────────────────────────────────────────────────────────
st.markdown(T["overview"])
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(T["total"], stats.get("total", 0))
with col2:
    st.metric(T["healthy"], stats.get("sains", 0))
with col3:
    val_a = int(stats.get("alertes", 0))
    st.metric(T["alert_count"], val_a,
              delta=f"+{val_a}" if val_a > 0 else None, delta_color="inverse")
with col4:
    val_c = int(stats.get("critiques", 0))
    st.metric(T["critical"], val_c,
              delta=f"+{val_c}" if val_c > 0 else None, delta_color="inverse")

st.divider()


# ─── GRAPHIQUES ──────────────────────────────────────────────────────────────
color_map = {
    "normal":   "#4caf50",
    "alerte":   "#ff9800",
    "critique": "#f44336"
}

if results:
    df = pd.DataFrame(results)

    st.markdown(T["charts"])
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        counts = df["statut"].value_counts().reset_index()
        counts.columns = ["Statut", "Nombre"]
        # Translate statut labels for display
        counts["Statut_label"] = counts["Statut"].map(T["statuts"]).fillna(counts["Statut"])
        fig_pie = px.pie(
            counts, values="Nombre", names="Statut_label",
            title=T["pie_title"],
            color="Statut",
            color_discrete_map=color_map,
            hole=0.45
        )
        fig_pie.update_traces(
            textposition="inside", textinfo="percent+label",
            marker=dict(line=dict(color="#ffffff", width=2))
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#2e7d32", title_font_color="#1b5e20", title_font_size=15,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.15,
                        xanchor="center", x=0.5, font=dict(size=12)),
            margin=dict(t=50, b=30, l=10, r=10)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_g2:
        df_sorted = df.sort_values("confidence", ascending=True).tail(15)
        bar_colors = df_sorted["statut"].map(color_map).fillna("#888888")
        fig_bar = go.Figure(go.Bar(
            x=df_sorted["confidence"],
            y=df_sorted["nom_animal"],
            orientation="h",
            marker_color=bar_colors.tolist(),
            marker_line_width=0,
            text=df_sorted["confidence"].astype(str) + T["conf_suffix"],
            textposition="auto",
            textfont=dict(size=11, color="#ffffff")
        ))
        fig_bar.update_layout(
            title=T["bar_title"],
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(241,248,233,0.6)",
            font_color="#2e7d32", title_font_color="#1b5e20", title_font_size=15,
            xaxis=dict(range=[0, 105], gridcolor="#e8f5e9",
                       ticksuffix=T["conf_suffix"], title="Confiance (%)"),
            yaxis=dict(gridcolor="#e8f5e9", automargin=True),
            margin=dict(t=50, b=30, l=10, r=20), bargap=0.25
        )
        st.plotly_chart(fig_bar, use_container_width=True)

st.divider()


# ─── TABLEAU DIAGNOSTIC ───────────────────────────────────────────────────────
st.markdown(T["diag_title"])

if results:
    df_diag = pd.DataFrame(results)[["nom_animal", "statut", "maladie", "confidence"]]
    df_diag.columns = [T["col_animal"], T["col_status"], T["col_diag"], T["col_conf"]]

    col_f1, col_f2 = st.columns([1, 3])
    with col_f1:
        filter_options = [T["filter_all"], "normal", "alerte", "critique"]
        filtre = st.selectbox(T["filter_label"], filter_options, key="filtre_statut")

    if filtre != T["filter_all"]:
        df_diag = df_diag[df_diag[T["col_status"]] == filtre]

    st.dataframe(df_diag, use_container_width=True, height=400, hide_index=True)
else:
    st.info(T["no_data"])

st.divider()


# ─── FOOTER ──────────────────────────────────────────────────────────────────
source  = data.get("source_ia", "PHP")
dernier = data.get("dernier_analyse", "—")
st.markdown(
    f"""<div class="footer-bar">
        ⬡ AgriBovin IA v3.0 &nbsp;|&nbsp;
        {T['footer_source']} : <b>{source}</b> &nbsp;|&nbsp;
        {T['footer_last']} : <b>{dernier}</b> &nbsp;|&nbsp;
        🔄 {T['footer_refresh']}
    </div>""",
    unsafe_allow_html=True
)


# ─── AUTO-REFRESH ─────────────────────────────────────────────────────────────
time.sleep(30)
st.rerun()
