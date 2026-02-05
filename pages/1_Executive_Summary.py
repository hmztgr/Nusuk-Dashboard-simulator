"""
Page 1: Executive Summary - الملخص التنفيذي
"""

import streamlit as st
import pandas as pd
from datetime import date
from utils.i18n import t, get_lang
from utils.metrics import compute_metrics
from utils.charts import (
    arrival_trend_chart, pipeline_funnel_chart,
    nationality_bar_chart, health_timeline_chart
)
lang = get_lang()
df = st.session_state.get("df")
filters = st.session_state.get("filters", {})
if df is None:
    st.error("يرجى تحميل لوحة المعلومات من الصفحة الرئيسية أولاً." if lang == "ar" else "Please load the dashboard from the main page first.")
    st.stop()

as_of_date = filters.get("as_of_date")

# Apply filters (no .copy() needed — filtering creates new DataFrames)
filtered_df = df
if filters.get("person_types"):
    filtered_df = filtered_df[filtered_df["person_type"].isin(filters["person_types"])]
if filters.get("nationalities"):
    filtered_df = filtered_df[filtered_df["nationality"].isin(filters["nationalities"])]
if filters.get("providers"):
    filtered_df = filtered_df[filtered_df["service_provider"].isin(filters["providers"])]

m = compute_metrics(filtered_df, as_of_date)

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown(f'<div class="nusuk-header"><h2>{t("page_executive_summary")}</h2></div>', unsafe_allow_html=True)

# ── KPI Cards ──────────────────────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)

# Benchmark colors
def _benchmark_color(actual, metric_type):
    benchmarks = {
        "arrivals": {date(2025,4,15):0, date(2025,5,5):15, date(2025,5,20):60, date(2025,5,31):90, date(2025,6,5):95, date(2025,6,30):95},
        "activated": {date(2025,4,15):0, date(2025,5,5):5, date(2025,5,20):30, date(2025,5,31):55, date(2025,6,5):75, date(2025,6,30):90},
    }
    target = 0
    for bdate, bval in sorted(benchmarks.get(metric_type, {}).items()):
        if as_of_date >= bdate:
            target = bval
    if actual >= target: return "#2E7D32"
    elif actual >= target * 0.7: return "#F9A825"
    else: return "#C62828"

arr_color = _benchmark_color(m["arrival_pct"], "arrivals")
act_color = _benchmark_color(m["activated_pct"], "activated")

with col1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{m["total_visas"]:,}</div><div class="kpi-label">{t("total_visas")}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{m["total_arrivals"]:,}</div><div class="kpi-label">{t("total_arrivals")}</div><div class="kpi-delta" style="color:{arr_color};">{m["arrival_pct"]:.1f}%</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{m["cards_activated"]:,}</div><div class="kpi-label">{t("cards_active")}</div><div class="kpi-delta" style="color:{act_color};">{m["activated_pct"]:.1f}%</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{m["health_incidents"]:,}</div><div class="kpi-label">{t("health_incidents")}</div></div>', unsafe_allow_html=True)
with col5:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{m["deaths"]:,}</div><div class="kpi-label">{t("deaths")}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Alert Cards ────────────────────────────────────────────────────────────
col_a1, col_a2, col_a3 = st.columns(3)

with col_a1:
    st.markdown(f"""<div class="alert-card">
        <strong>{"⚠️ " + t("cards_not_delivered")}</strong><br>
        <span style="font-size:28px; font-weight:bold; color:#E65100;">{m["cards_not_delivered"]:,}</span><br>
        <span style="font-size:12px; color:#5C4033;">{"بطاقات عند الشركات لم تسلم للحجاج" if lang == "ar" else "Cards at providers but not delivered"}</span>
    </div>""", unsafe_allow_html=True)

with col_a2:
    not_act = 100 - m["activated_pct"]
    st.markdown(f"""<div class="alert-card {"alert-card-red" if not_act > 50 else ""}">
        <strong>{"⚠️ " + ("نسبة غير المفعلة" if lang == "ar" else "Not Activated Rate")}</strong><br>
        <span style="font-size:28px; font-weight:bold; color:#C62828;">{not_act:.1f}%</span><br>
        <span style="font-size:12px; color:#5C4033;">{"من البطاقات المسلمة لم يتم تفعيلها" if lang == "ar" else "of delivered cards not activated"}</span>
    </div>""", unsafe_allow_html=True)

with col_a3:
    not_printed = m["total_visas"] - m["cards_printed"]
    st.markdown(f"""<div class="alert-card">
        <strong>{"⚠️ " + ("بطاقات لم تطبع" if lang == "ar" else "Cards Not Printed")}</strong><br>
        <span style="font-size:28px; font-weight:bold; color:#E65100;">{not_printed:,}</span><br>
        <span style="font-size:12px; color:#5C4033;">{"تأشيرات صادرة بدون بطاقة مطبوعة" if lang == "ar" else "Visas issued without printed card"}</span>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts ─────────────────────────────────────────────────────────────────
col_c1, col_c2 = st.columns(2)
with col_c1:
    st.plotly_chart(pipeline_funnel_chart(m), use_container_width=True)
with col_c2:
    st.plotly_chart(arrival_trend_chart(m["daily_arrivals"]), use_container_width=True)

col_c3, col_c4 = st.columns(2)
with col_c3:
    st.plotly_chart(nationality_bar_chart(filtered_df, as_of_date), use_container_width=True)
with col_c4:
    st.plotly_chart(health_timeline_chart(m["daily_health"]), use_container_width=True)
