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

# ─── CSS : fond blanc, pas de changement de couleur ───────────────────────────
st.markdown("""
<style>
/* ── Reset global ── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main, .block-container,
[data-testid="stMainBlockContainer"] {
    background-color: #ffffff !important;
    color: #1a1a1a !important;
}

/* Empêche Streamlit de mettre un fond gris sur la page */
[data-testid="stApp"] {
    background-color: #ffffff !important;
}

/* ── Typographie ── */
h1 {
    color: #1b5e20 !important;
    font-size: 1.9rem !important;
    font-weight: 700 !important;
    border-bottom: 2px solid #c8e6c9;
    padding-bottom: 10px;
    margin-bottom: 0 !important;
}
h2, h3 {
    color: #2e7d32 !important;
    font-weight: 600 !important;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: #f1f8e9 !important;
    border: 1px solid #c8e6c9 !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
}
[data-testid="metric-container"] label {
    color: #388e3c !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
}
[data-testid="metric-container"] [data-testid="metric-value"] {
    color: #1b5e20 !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
}
[data-testid="stMetricDelta"] {
    font-size: 12px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #f9fdf6 !important;
    border-right: 1px solid #c8e6c9 !important;
}
[data-testid="stSidebar"] * {
    color: #2e7d32 !important;
}

/* ── Boutons ── */
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
.stButton > button:hover {
    background-color: #388e3c !important;
    color: #ffffff !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background-color: #f9fdf6 !important;
    border: 1px solid #c8e6c9 !important;
    border-radius: 8px !important;
    color: #1b5e20 !important;
}

/* ── DataFrame / Table ── */
[data-testid="stDataFrame"] {
    background-color: #ffffff !important;
    border: 1px solid #c8e6c9 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ── Divider ── */
hr {
    border-color: #c8e6c9 !important;
    margin: 12px 0 !important;
}

/* ── Alertes custom ── */
.alert-box {
    padding: 10px 14px;
    border-radius: 8px;
    margin: 5px 0;
    font-size: 13px;
    line-height: 1.4;
}
.alert-critique {
    background-color: #ffebee;
    border-left: 4px solid #e53935;
    color: #b71c1c;
}
.alert-alerte {
    background-color: #fff8e1;
    border-left: 4px solid #fb8c00;
    color: #e65100;
}
.alert-normal {
    background-color: #e8f5e9;
    border-left: 4px solid #43a047;
    color: #1b5e20;
}

/* ── Footer ── */
.footer-bar {
    text-align: center;
    color: #81c784;
    font-size: 12px;
    padding: 10px;
    margin-top: 10px;
    border-top: 1px solid #e8f5e9;
    background-color: #ffffff;
}

/* ── Suppression fond sombre sur certains composants ── */
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"],
[data-testid="column"] {
    background-color: transparent !important;
}

/* ── Info/warning boxes ── */
[data-testid="stInfo"],
[data-testid="stWarning"],
[data-testid="stError"],
[data-testid="stSuccess"] {
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)


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

    if st.button("🔄 Actualiser les données"):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    now_str = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
    st.markdown(f"⏱️ **Dernière maj :** `{now_str}`")
    st.markdown("---")

    st.markdown("### 📡 Système")
    st.markdown("- **API :** PHP Expert")
    st.markdown("- **DB :** MySQL AwardSpace")
    st.markdown("- **Refresh :** 30 s")
    st.markdown("---")

    st.markdown("### 🚨 Alertes récentes")
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
            st.success("✅ Aucune alerte active")
    else:
        st.error("❌ Impossible de charger les alertes")


# ─── EN-TÊTE ─────────────────────────────────────────────────────────────────
st.markdown("# 🐄 AgriBovin — Santé Animale Intelligente")
st.caption("Tableau de bord temps réel · IA diagnostique · Refresh automatique 30 s")

# ─── Chargement principal ─────────────────────────────────────────────────────
data = load_data()

if not data.get("success"):
    st.error(f"❌ Erreur API : {data.get('error', 'inconnue')}")
    st.info(f"Vérifiez l'endpoint : `{API_URL}`")
    st.stop()

stats   = data.get("stats", {})
results = data.get("resultats_ia", [])
alertes = data.get("alertes", [])


# ─── MÉTRIQUES ───────────────────────────────────────────────────────────────
st.markdown("### 📊 Vue d'ensemble")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📦 Total animaux", stats.get("total", 0))
with col2:
    st.metric("✅ En bonne santé", stats.get("sains", 0))
with col3:
    val_a = int(stats.get("alertes", 0))
    st.metric(
        "⚠️ En alerte", val_a,
        delta=f"+{val_a}" if val_a > 0 else None,
        delta_color="inverse"
    )
with col4:
    val_c = int(stats.get("critiques", 0))
    st.metric(
        "🚨 Critiques", val_c,
        delta=f"+{val_c}" if val_c > 0 else None,
        delta_color="inverse"
    )

st.divider()


# ─── GRAPHIQUES ──────────────────────────────────────────────────────────────
if results:
    df = pd.DataFrame(results)

    st.markdown("### 📈 Visualisations")
    col_g1, col_g2 = st.columns(2)

    # --- Donut : répartition santé ---
    with col_g1:
        counts = df["statut"].value_counts().reset_index()
        counts.columns = ["Statut", "Nombre"]
        color_map = {
            "normal":   "#4caf50",
            "alerte":   "#ff9800",
            "critique": "#f44336"
        }
        fig_pie = px.pie(
            counts,
            values="Nombre",
            names="Statut",
            title="Répartition des statuts de santé",
            color="Statut",
            color_discrete_map=color_map,
            hole=0.45
        )
        fig_pie.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(line=dict(color="#ffffff", width=2))
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#2e7d32",
            title_font_color="#1b5e20",
            title_font_size=15,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.15,
                xanchor="center",
                x=0.5,
                font=dict(size=12)
            ),
            margin=dict(t=50, b=30, l=10, r=10)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- Bar horizontal : confiance IA ---
    with col_g2:
        df_sorted = df.sort_values("confidence", ascending=True).tail(15)
        bar_colors = df_sorted["statut"].map(color_map).fillna("#888888")

        fig_bar = go.Figure(go.Bar(
            x=df_sorted["confidence"],
            y=df_sorted["nom_animal"],
            orientation="h",
            marker_color=bar_colors.tolist(),
            marker_line_width=0,
            text=df_sorted["confidence"].astype(str) + "%",
            textposition="auto",
            textfont=dict(size=11, color="#ffffff")
        ))
        fig_bar.update_layout(
            title="Score de confiance IA par animal",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(241,248,233,0.6)",
            font_color="#2e7d32",
            title_font_color="#1b5e20",
            title_font_size=15,
            xaxis=dict(
                range=[0, 105],
                gridcolor="#e8f5e9",
                ticksuffix="%",
                title="Confiance (%)"
            ),
            yaxis=dict(
                gridcolor="#e8f5e9",
                automargin=True
            ),
            margin=dict(t=50, b=30, l=10, r=20),
            bargap=0.25
        )
        st.plotly_chart(fig_bar, use_container_width=True)

st.divider()


# ─── TABLEAU DIAGNOSTIC ───────────────────────────────────────────────────────
st.markdown("### 📋 Diagnostic détaillé")

if results:
    df_diag = pd.DataFrame(results)[["nom_animal", "statut", "maladie", "confidence"]]
    df_diag.columns = ["🐄 Animal", "📊 Statut", "🔬 Diagnostic", "💯 Confiance %"]

    col_f1, col_f2 = st.columns([1, 3])
    with col_f1:
        filtre = st.selectbox(
            "Filtrer par statut :",
            ["Tous", "normal", "alerte", "critique"],
            key="filtre_statut"
        )

    if filtre != "Tous":
        df_diag = df_diag[df_diag["📊 Statut"] == filtre]

    st.dataframe(
        df_diag,
        use_container_width=True,
        height=400,
        hide_index=True
    )
else:
    st.info("ℹ️ Aucune donnée de diagnostic disponible.")

st.divider()


# ─── FOOTER ──────────────────────────────────────────────────────────────────
source   = data.get("source_ia", "PHP")
dernier  = data.get("dernier_analyse", "—")
st.markdown(
    f"""<div class="footer-bar">
        ⬡ AgriBovin IA v3.0 &nbsp;|&nbsp;
        Source : <b>{source}</b> &nbsp;|&nbsp;
        Dernière analyse : <b>{dernier}</b> &nbsp;|&nbsp;
        🔄 Auto-refresh : 30 s
    </div>""",
    unsafe_allow_html=True
)


# ─── AUTO-REFRESH ─────────────────────────────────────────────────────────────
time.sleep(30)
st.rerun()
