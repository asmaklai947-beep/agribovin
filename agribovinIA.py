import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
from mysql.connector import Error
import time

st.set_page_config(page_title="AgriBovin IA", page_icon="🐄", layout="wide", initial_sidebar_state="expanded")

# --- Fonction de connexion robuste ---
@st.cache_resource
def init_connection():
    try:
        conn = mysql.connector.connect(
            host="fdb1034.awardspace.net",
            user="4734753_bovin",
            password="jbzgNnp2DRjKjE@",
            database="4734753_bovin",
            autocommit=True,
            connection_timeout=10
        )
        return conn
    except Error as e:
        st.error(f"❌ Erreur de connexion à la base de données : {e}")
        st.info("Vérifiez que l'accès distant MySQL est activé sur AwardSpace (Allow external connections).")
        return None

conn = init_connection()

def get_conn():
    if conn is None:
        return None
    try:
        conn.ping(reconnect=True, attempts=2, delay=1)
        return conn
    except Error:
        return None

# --- Chargement des données avec gestion d'erreur ---
@st.cache_data(ttl=600)
def load_animaux():
    conn_db = get_conn()
    if conn_db is None:
        return pd.DataFrame()
    return pd.read_sql("SELECT id, nom_animal, statut_sante, espece FROM animaux;", conn_db)

@st.cache_data(ttl=600)
def load_alertes():
    conn_db = get_conn()
    if conn_db is None:
        return pd.DataFrame()
    return pd.read_sql("""
        SELECT a.nom_animal, al.message, al.severite, al.created_at
        FROM alertes al JOIN animaux a ON al.animal_id = a.id
        WHERE al.type = 'sante' ORDER BY al.created_at DESC LIMIT 10;
    """, conn_db)

@st.cache_data(ttl=600)
def load_last_data():
    conn_db = get_conn()
    if conn_db is None:
        return pd.DataFrame()
    animaux_df = pd.read_sql("SELECT id, nom_animal FROM animaux;", conn_db)
    for col in ['temperature', 'bpm', 'spo2', 'acc_x', 'acc_y', 'acc_z']:
        animaux_df[col] = None
    for idx, row in animaux_df.iterrows():
        aid = row['id']
        try:
            t = pd.read_sql(f"SELECT valeur FROM temperature WHERE animal_id={aid} ORDER BY date_lecture DESC LIMIT 1;", conn_db)
            if not t.empty:
                animaux_df.at[idx, 'temperature'] = t['valeur'].iloc[0]
        except: pass
        try:
            b = pd.read_sql(f"SELECT bpm, spo2 FROM max30102 WHERE animal_id={aid} ORDER BY date_lecture DESC LIMIT 1;", conn_db)
            if not b.empty:
                animaux_df.at[idx, 'bpm'] = b['bpm'].iloc[0]
                animaux_df.at[idx, 'spo2'] = b['spo2'].iloc[0]
        except: pass
        try:
            a = pd.read_sql(f"SELECT acc_x, acc_y, acc_z FROM accelerometre_gy87 WHERE animal_id={aid} ORDER BY date_lecture DESC LIMIT 1;", conn_db)
            if not a.empty:
                animaux_df.at[idx, 'acc_x'] = a['acc_x'].iloc[0]
                animaux_df.at[idx, 'acc_y'] = a['acc_y'].iloc[0]
                animaux_df.at[idx, 'acc_z'] = a['acc_z'].iloc[0]
        except: pass
    return animaux_df

# --- Interface ---
st.title("🐄 AgriBovin : Tableau de Santé Intelligent")

if conn is None:
    st.stop()

try:
    animaux_stats = load_animaux()
    alertes_df = load_alertes()
    capteurs_df = load_last_data()

    if animaux_stats.empty:
        st.warning("Aucune donnée animale trouvée.")
        st.stop()

    capteurs_df = capteurs_df.merge(animaux_stats[['id','statut_sante','espece']], on='id', how='left')
    nb_total = len(animaux_stats)
    nb_critique = (animaux_stats['statut_sante'] == 'critique').sum()
    nb_alerte = (animaux_stats['statut_sante'] == 'alerte').sum()
    nb_sain = (animaux_stats['statut_sante'] == 'normal').sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🐄 Total Animaux", nb_total)
    col2.metric("🟢 En Bonne Santé", nb_sain)
    col3.metric("🟡 En Alerte", nb_alerte)
    col4.metric("🔴 État Critique", nb_critique)

    with st.sidebar:
        st.header("🔔 Alertes Récentes")
        if not alertes_df.empty:
            for _, row in alertes_df.iterrows():
                msg = f"**{row['nom_animal']}**: {row['message']}  \n_{row['created_at']}_"
                if row['severite'] == 'critique':
                    st.error(msg)
                elif row['severite'] == 'alerte':
                    st.warning(msg)
                else:
                    st.info(msg)
        else:
            st.success("✅ Aucune alerte")
        st.caption("AgriBovin v2.0")

    col_left, col_right = st.columns([2,1])
    with col_left:
        st.header("📊 Résultats du Diagnostic")
        display_df = capteurs_df[['nom_animal','statut_sante','temperature','bpm','spo2']].copy()
        display_df.columns = ['Animal','Statut','🌡️ Temp.','❤️ BPM','🫁 SpO2']
        st.dataframe(display_df, use_container_width=True)
    with col_right:
        if not capteurs_df['espece'].dropna().empty and not capteurs_df['temperature'].dropna().empty:
            temp_par_espece = capteurs_df.groupby('espece')['temperature'].mean().reset_index()
            fig = px.pie(temp_par_espece, values='temperature', names='espece', title='Température moyenne par espèce')
            st.plotly_chart(fig, use_container_width=True)
        st.metric("📳 Accélération x moyenne", f"{capteurs_df['acc_x'].mean():.3f}" if not capteurs_df['acc_x'].isna().all() else "N/A")
except Exception as e:
    st.error(f"Erreur : {e}")