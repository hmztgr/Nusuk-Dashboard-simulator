"""
Hajj Nusuk Dashboard - Main Entry Point
Bilingual (Arabic RTL / English) Streamlit multi-page app
simulating the Nusuk card management system for Hajj 2025.
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ── Page Config (must be first Streamlit call) ─────────────────────────────
st.set_page_config(
    page_title="Nusuk Dashboard | لوحة نسك",
    page_icon="🕋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Initialize Session State ───────────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state["lang"] = "ar"
if "playing" not in st.session_state:
    st.session_state["playing"] = False

lang = st.session_state["lang"]

# ── CSS Injection ──────────────────────────────────────────────────────────
SHARED_CSS = """
<style>
    .stApp {
        font-family: 'Segoe UI', Tahoma, 'Arial', sans-serif;
    }
    h1, h2, h3, h4, h5, h6, p, label {
        font-family: 'Segoe UI', Tahoma, 'Arial', sans-serif !important;
    }
    /* Metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #FAF6F0, #F0E6D4);
        border-radius: 12px;
        padding: 15px;
        border-left: 4px solid #B8860B;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    [data-testid="stMetricLabel"] { font-size: 14px !important; color: #5C4033 !important; }
    [data-testid="stMetricValue"] { font-size: 28px !important; color: #4A3728 !important; font-weight: bold !important; }

    /* Sidebar - force readable colors regardless of theme */
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
    section[data-testid="stSidebar"] small,
    section[data-testid="stSidebar"] caption {
        color: #4A3728 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] span {
        color: #4A3728 !important;
        font-weight: 500;
    }
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-selected="true"] {
        background-color: #B8860B !important;
    }
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-selected="true"] span {
        color: white !important;
    }

    /* Alert cards */
    .alert-card {
        background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
        border-radius: 10px; padding: 15px; margin: 8px 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }
    .alert-card-red {
        background: linear-gradient(135deg, #FFEBEE, #FFCDD2);
    }
    .alert-card-green {
        background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
    }
    /* alert border side depends on direction */
    .alert-card, .alert-card-red, .alert-card-green {
        border-right: 4px solid #E65100;
    }
    .alert-card-red { border-right-color: #C62828; }
    .alert-card-green { border-right-color: #2E7D32; }

    /* KPI card */
    .kpi-card {
        background: linear-gradient(135deg, #FAF6F0, #F0E6D4);
        border-radius: 12px; padding: 20px; text-align: center;
        border-bottom: 4px solid #B8860B;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        color: #4A3728;
    }
    .kpi-value { font-size: 32px; font-weight: bold; color: #4A3728; }
    .kpi-label { font-size: 13px; color: #5C4033; margin-top: 6px; }
    .kpi-delta { font-size: 14px; margin-top: 4px; }

    /* Pipeline step */
    .pipeline-step {
        background: linear-gradient(135deg, #FAF6F0, #F0E6D4);
        border-radius: 10px; padding: 12px 8px; text-align: center;
        border-top: 3px solid #B8860B; min-height: 120px;
    }
    .pipeline-step .step-value { font-size: 22px; font-weight: bold; color: #4A3728; }
    .pipeline-step .step-label { font-size: 11px; color: #5C4033; margin-top: 4px; }
    .pipeline-step .step-pct { font-size: 12px; color: #8B6914; margin-top: 2px; }

    /* Header bar */
    .nusuk-header {
        background: linear-gradient(135deg, #5C4033, #8B6914);
        color: white; padding: 12px 20px; border-radius: 10px;
        margin-bottom: 15px; text-align: center;
    }
    .nusuk-header h2 { color: white !important; margin: 0; }

    /* Pipeline rows */
    .pipeline-row { background: #F5F0E8; border-radius: 10px; padding: 15px; margin: 10px 0; }
    .pipeline-row-dark { background: #E8E0D0; }
    .pipeline-row-workers { background: #D5CEC3; }

    /* Reduce loading flash during animation */
    .stApp [data-testid="stAppViewBlockContainer"] {
        transition: opacity 0.05s !important;
    }
</style>
"""

RTL_EXTRA = """
<style>
    .main .block-container { direction: rtl; text-align: right; }
    .stSidebar .block-container { direction: rtl; text-align: right; }
    .alert-card, .alert-card-red, .alert-card-green {
        border-right: none; border-left: 4px solid #E65100;
    }
    .alert-card-red { border-left-color: #C62828; }
    .alert-card-green { border-left-color: #2E7D32; }
</style>
"""

LTR_EXTRA = """
<style>
    .main .block-container { direction: ltr; text-align: left; }
    .stSidebar .block-container { direction: ltr; text-align: left; }
</style>
"""

st.markdown(SHARED_CSS, unsafe_allow_html=True)
st.markdown(RTL_EXTRA if lang == "ar" else LTR_EXTRA, unsafe_allow_html=True)

# ── Data Loading ───────────────────────────────────────────────────────────
@st.cache_resource
def load_data():
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    gz_path = os.path.join(data_dir, "hajj_data.csv.gz")
    csv_path = os.path.join(data_dir, "hajj_data.csv")

    if os.path.exists(gz_path):
        df = pd.read_csv(gz_path, compression="gzip", low_memory=False)
    elif os.path.exists(csv_path):
        df = pd.read_csv(csv_path, low_memory=False)
    else:
        # Auto-generate if neither file exists
        import subprocess, sys
        gen_script = os.path.join(data_dir, "generate_data.py")
        subprocess.run([sys.executable, gen_script], check=True)
        df = pd.read_csv(csv_path, low_memory=False)
    date_cols = [
        "visa_issue_date", "group_formation_date", "travel_date", "arrival_date",
        "card_printed_date", "card_at_center_date", "card_at_provider_date",
        "card_received_date", "card_activation_date", "proof_picture_date",
        "health_date", "death_date",
    ]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    bool_cols = [
        "arrival_status", "card_printed", "card_at_center", "card_at_provider",
        "card_received", "card_activated", "proof_picture_received", "death_status",
    ]
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].fillna(False).astype(bool)
    # Ensure string columns for search
    for col in ["id_number", "passport_number", "nusuk_number", "first_name", "last_name"]:
        if col in df.columns:
            df[col] = df[col].astype(str).replace("nan", "")
    return df


df = load_data()
st.session_state["df"] = df

# ── Sidebar ────────────────────────────────────────────────────────────────
from utils.filters import render_sidebar, animate_slider
from utils.i18n import t

filters = render_sidebar(df)
st.session_state["filters"] = filters

# ── Navigation (bilingual page labels) ─────────────────────────────────────
home_page = st.Page("pages/0_Home.py",
    title="الرئيسية" if lang == "ar" else "Home", icon="🕋")
exec_page = st.Page("pages/1_Executive_Summary.py",
    title="الملخص التنفيذي" if lang == "ar" else "Executive Summary", icon="📊")
pipeline_page = st.Page("pages/2_Card_Pipeline.py",
    title="الملخص التنفيذي للبطاقات" if lang == "ar" else "Card Pipeline", icon="🪪")
tracking_page = st.Page("pages/3_Card_Tracking.py",
    title="تتبع البطاقات" if lang == "ar" else "Card Tracking", icon="🔍")
providers_page = st.Page("pages/4_Service_Providers.py",
    title="شركات تقديم الخدمة" if lang == "ar" else "Service Providers", icon="🏢")
health_page = st.Page("pages/5_Health_Safety.py",
    title="الصحة والسلامة" if lang == "ar" else "Health & Safety", icon="🏥")
demo_page = st.Page("pages/6_Demographics.py",
    title="التركيبة السكانية" if lang == "ar" else "Demographics", icon="🌍")
reports_page = st.Page("pages/7_Reports.py",
    title="التقارير" if lang == "ar" else "Reports & Export", icon="📑")

nav = st.navigation([
    home_page, exec_page, pipeline_page, tracking_page,
    providers_page, health_page, demo_page, reports_page,
])
nav.run()

# Animation: rerun AFTER page has fully rendered so user sees updated numbers
animate_slider()
