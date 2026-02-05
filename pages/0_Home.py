"""
Home / Landing Page - الرئيسية
Quick overview with KPIs, funnel, and arrival trend.
"""

import streamlit as st
from utils.i18n import t, get_lang
from utils.metrics import compute_metrics
from utils.charts import pipeline_funnel_chart, arrival_trend_chart

lang = get_lang()
df = st.session_state.get("df")
filters = st.session_state.get("filters", {})

if df is None:
    st.error("Data not loaded.")
    st.stop()

as_of_date = filters.get("as_of_date")
m = compute_metrics(df, as_of_date)

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="nusuk-header">
    <h2>{"🕋 لوحة معلومات نسك - إدارة بطاقات الحج ٢٠٢٥" if lang == "ar" else "🕋 Nusuk Dashboard - Hajj 2025 Card Management"}</h2>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ──────────────────────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(t("total_visas"), f"{m['total_visas']:,}")
with col2:
    st.metric(t("total_arrivals"), f"{m['total_arrivals']:,}", f"{m['arrival_pct']:.1f}%")
with col3:
    st.metric(t("cards_activated"), f"{m['cards_activated']:,}", f"{m['activated_pct']:.1f}%")
with col4:
    st.metric(t("health_incidents"), f"{m['health_incidents']:,}")
with col5:
    st.metric(t("deaths"), f"{m['deaths']:,}")

st.divider()

# ── Alert Cards ────────────────────────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    not_delivered = m["cards_not_delivered"]
    st.markdown(f"""
    <div class="alert-card">
        <strong>{"⚠️ " + t("cards_not_delivered")}</strong><br>
        <span style="font-size: 24px; font-weight: bold; color: #E65100;">{not_delivered:,}</span>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    not_activated_pct = 100 - m["activated_pct"]
    st.markdown(f"""
    <div class="alert-card {"alert-card-red" if not_activated_pct > 50 else ""}">
        <strong>{"⚠️ " + ("نسبة غير المفعلة" if lang == "ar" else "Not Activated Rate")}</strong><br>
        <span style="font-size: 24px; font-weight: bold; color: #C62828;">{not_activated_pct:.1f}%</span>
    </div>
    """, unsafe_allow_html=True)

# ── Charts ─────────────────────────────────────────────────────────────────
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.plotly_chart(pipeline_funnel_chart(m), use_container_width=True)

with col_chart2:
    st.plotly_chart(arrival_trend_chart(m["daily_arrivals"]), use_container_width=True)

# ── Navigation hint ────────────────────────────────────────────────────────
if lang == "ar":
    st.info("👈 استخدم القائمة الجانبية للتنقل بين الصفحات")
else:
    st.info("👉 Use the sidebar to navigate between pages")
