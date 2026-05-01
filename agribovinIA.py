import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(
    page_title="AgriBovin IA",
    page_icon="🐄",
    layout="wide"
)

# ── رابط API ──
API_URL = "http://bovin.atwebpages.com/api/ia_data.php"

# ── جلب البيانات ──
@st.cache_data(ttl=60)
def load_data():
    try:
        r = requests.get(API_URL, timeout=10)
        return r.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

# ── واجهة ──
st.title("🐄 AgriBovin : Tableau de Santé Intelligent")

data = load_data()

if not data.get("success"):
    st.error(f"❌ Erreur API : {data.get('error', 'inconnue')}")
    st.info("Vérifiez que l'API répond sur : " + API_URL)
    st.stop()

# ── إحصائيات ──
stats = data.get("stats", {})
col1, col2, col3, col4 = st.columns(4)
col1.metric("🐄 Total", stats.get("total", 0))
col2.metric("✅ Sains", stats.get("sains", 0))
col3.metric("⚠️ Alertes", stats.get("alertes", 0))
col4.metric("🚨 Critiques", stats.get("critiques", 0))

st.divider()

col_left, col_right = st.columns([2, 1])

# ── جدول الحيوانات ──
with col_left:
    st.subheader("📊 Diagnostic des animaux")
    resultats = data.get("resultats_ia", [])
    if resultats:
        df = pd.DataFrame(resultats)
        df = df[["nom_animal", "statut", "maladie", "confidence"]]
        df.columns = ["Animal", "Statut", "Diagnostic", "Confiance %"]

        def color_statut(val):
            colors = {
                "normal":   "background-color: #d4edda; color: #155724",
                "alerte":   "background-color: #fff3cd; color: #856404",
                "critique": "background-color: #f8d7da; color: #721c24"
            }
            return colors.get(val, "")

        st.dataframe(
           df.style.map(color_statut, subset=["Statut"])
            use_container_width=True
        )
    else:
        st.info("Aucun résultat IA disponible")

# ── الإنذارات ──
with col_right:
    st.subheader("🚨 Dernières alertes")
    alertes = data.get("alertes", [])
    if alertes:
        for a in alertes[:8]:
            sev = a.get("severite", "info")
            msg = f"**{a.get('nom_animal', '?')}**: {a.get('message', '')}"
            if sev == "critique":
                st.error(msg)
            elif sev in ["alerte", "danger"]:
                st.warning(msg)
            else:
                st.info(msg)
    else:
        st.success("✅ Aucune alerte")

st.divider()

# ── رسم بياني ──
if resultats:
    df2 = pd.DataFrame(resultats)
    if "statut" in df2.columns:
        counts = df2["statut"].value_counts().reset_index()
        counts.columns = ["Statut", "Nombre"]
        color_map = {
            "normal":   "#28a745",
            "alerte":   "#ffc107",
            "critique": "#dc3545"
        }
        fig = px.pie(
            counts, values="Nombre", names="Statut",
            title="Répartition de la santé",
            color="Statut", color_discrete_map=color_map
        )
        st.plotly_chart(fig, use_container_width=True)

# ── معلومات ──
source = data.get("source_ia", "PHP")
dernier = data.get("dernier_analyse", "—")
st.caption(f"⬡ Source IA: {source} | 🕐 Dernière analyse: {dernier}")

# ── زر تحديث ──
if st.button("🔄 Actualiser les données"):
    st.cache_data.clear()
    st.rerun()
