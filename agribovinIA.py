import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime

# ═══════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════
st.set_page_config(
    page_title="AgriBovin IA",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://bovin.atwebpages.com/api/ia_data.php"

# ═══════════════════════════════════════
# CSS PERSONNALISÉ
# ═══════════════════════════════════════
st.markdown("""
<style>
    /* Fond principal */
    .stApp { background-color: #0f1a0f; }
    
    /* Titre principal */
    h1 { 
        color: #4caf50 !important; 
        font-size: 2.2rem !important;
        border-bottom: 2px solid #2d5a2d;
        padding-bottom: 10px;
    }
    
    /* Sous-titres */
    h2, h3 { color: #81c784 !important; }
    
    /* Cartes métriques */
    [data-testid="metric-container"] {
        background: #1a2e1a;
        border: 1px solid #2d5a2d;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    [data-testid="metric-container"] label {
        color: #81c784 !important;
        font-size: 13px !important;
    }
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #ffffff !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #111f11 !important;
        border-right: 1px solid #2d5a2d;
    }
    
    /* Bouton */
    .stButton button {
        background: #2d5a2d !important;
        color: #ffffff !important;
        border: 1px solid #4caf50 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        width: 100%;
        transition: all 0.3s;
    }
    .stButton button:hover {
        background: #4caf50 !important;
        color: #000000 !important;
    }
    
    /* Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid #2d5a2d !important;
        border-radius: 8px !important;
    }
    
    /* Badge statut */
    .badge-normal {
        background: #1b5e20; color: #69f0ae;
        padding: 3px 10px; border-radius: 12px;
        font-size: 12px; font-weight: bold;
    }
    .badge-alerte {
        background: #e65100; color: #ffcc02;
        padding: 3px 10px; border-radius: 12px;
        font-size: 12px; font-weight: bold;
    }
    .badge-critique {
        background: #b71c1c; color: #ff5252;
        padding: 3px 10px; border-radius: 12px;
        font-size: 12px; font-weight: bold;
    }
    
    /* Divider */
    hr { border-color: #2d5a2d !important; }
    
    /* Alert boxes */
    .alert-box {
        padding: 12px 16px;
        border-radius: 8px;
        margin: 6px 0;
        font-size: 13px;
    }
    .alert-critique {
        background: #1a0000;
        border-left: 4px solid #f44336;
        color: #ff8a80;
    }
    .alert-alerte {
        background: #1a1000;
        border-left: 4px solid #ff9800;
        color: #ffcc80;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════
# CHARGEMENT DES DONNÉES
# ═══════════════════════════════════════
@st.cache_data(ttl=30)
def load_data():
    try:
        r = requests.get(API_URL, timeout=10)
        return r.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

# ═══════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════
with st.sidebar:
    st.markdown("## 🐄 AgriBovin IA")
    st.markdown("---")

    # زر تحديث
    if st.button("🔄 Actualiser"):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")

    # آخر تحديث
    now = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"⏱️ **Dernière maj:** {now}")

    st.markdown("---")

    # معلومات النظام
    st.markdown("### 📡 Système")
    st.markdown("- **API:** PHP Expert")
    st.markdown("- **DB:** MySQL AwardSpace")
    st.markdown("- **Refresh:** 30s")

    st.markdown("---")
    st.markdown("### 🚨 Alertes récentes")

    data_sidebar = load_data()
    if data_sidebar.get("success"):
        alertes = data_sidebar.get("alertes", [])
        if alertes:
            for a in alertes[:5]:
                sev = a.get("severite", "")
                nom = a.get("nom_animal", "?")
                msg = a.get("message", "")
                if sev == "critique":
                    st.markdown(f'<div class="alert-box alert-critique">🔴 <b>{nom}</b><br>{msg}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="alert-box alert-alerte">🟡 <b>{nom}</b><br>{msg}</div>', unsafe_allow_html=True)
        else:
            st.success("✅ Aucune alerte")

# ═══════════════════════════════════════
# CONTENU PRINCIPAL
# ═══════════════════════════════════════
st.markdown("# 🐄 AgriBovin — Santé Animale Intelligente")

data = load_data()

if not data.get("success"):
    st.error(f"❌ Erreur API : {data.get('error', 'inconnue')}")
    st.info(f"Vérifiez : {API_URL}")
    st.stop()

stats  = data.get("stats", {})
result = data.get("resultats_ia", [])
alert  = data.get("alertes", [])

# ── MÉTRIQUES ──
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📦 Total animaux", stats.get("total", 0))
with col2:
    st.metric("✅ En bonne santé", stats.get("sains", 0))
with col3:
    delta_a = int(stats.get("alertes", 0))
    st.metric("⚠️ En alerte", delta_a, delta=f"+{delta_a}" if delta_a > 0 else None, delta_color="inverse")
with col4:
    delta_c = int(stats.get("critiques", 0))
    st.metric("🚨 Critiques", delta_c, delta=f"+{delta_c}" if delta_c > 0 else None, delta_color="inverse")

st.divider()

# ── GRAPHIQUES ──
if result:
    df = pd.DataFrame(result)

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        # Graphique camembert
        counts = df["statut"].value_counts().reset_index()
        counts.columns = ["Statut", "Nombre"]
        color_map = {
            "normal":   "#4caf50",
            "alerte":   "#ff9800",
            "critique": "#f44336"
        }
        fig_pie = px.pie(
            counts, values="Nombre", names="Statut",
            title="🥧 Répartition santé",
            color="Statut", color_discrete_map=color_map,
            hole=0.4
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#ffffff",
            title_font_color="#81c784"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_g2:
        # Graphique barres confiance
        df_sorted = df.sort_values("confidence", ascending=True).tail(15)
        colors = df_sorted["statut"].map({
            "normal": "#4caf50",
            "alerte": "#ff9800",
            "critique": "#f44336"
        })
        fig_bar = go.Figure(go.Bar(
            x=df_sorted["confidence"],
            y=df_sorted["nom_animal"],
            orientation="h",
            marker_color=colors,
            text=df_sorted["confidence"].astype(str) + "%",
            textposition="auto"
        ))
        fig_bar.update_layout(
            title="📊 Confiance par animal",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(26,46,26,0.5)",
            font_color="#ffffff",
            title_font_color="#81c784",
            xaxis=dict(gridcolor="#2d5a2d"),
            yaxis=dict(gridcolor="#2d5a2d")
        )
        st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# ── TABLEAU DIAGNOSTIC ──
st.markdown("### 📋 Diagnostic détaillé")

if result:
    df_display = pd.DataFrame(result)[["nom_animal", "statut", "maladie", "confidence"]]
    df_display.columns = ["🐄 Animal", "📊 Statut", "🔬 Diagnostic", "💯 Confiance %"]

    # فلتر
    filtre = st.selectbox("Filtrer par statut:", ["Tous", "normal", "alerte", "critique"])
    if filtre != "Tous":
        df_display = df_display[df_display["📊 Statut"] == filtre]

    st.dataframe(
        df_display,
        use_container_width=True,
        height=400,
        hide_index=True
    )
else:
    st.info("Aucune donnée disponible")

st.divider()

# ── FOOTER ──
source  = data.get("source_ia", "PHP")
dernier = data.get("dernier_analyse", "—")
st.markdown(f"""
<div style="text-align:center; color:#4a6a4a; font-size:12px; padding:10px">
    ⬡ AgriBovin IA v3.0 &nbsp;|&nbsp; 
    Source: {source} &nbsp;|&nbsp; 
    Dernière analyse: {dernier} &nbsp;|&nbsp;
    🔄 Auto-refresh: 30s
</div>
""", unsafe_allow_html=True)

# تحديث تلقائي
import time
time.sleep(30)
st.rerun()
