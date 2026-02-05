"""
Page 5: Health & Safety - الصحة والسلامة
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.i18n import t, get_lang
from utils.metrics import compute_metrics
from utils.charts import health_timeline_chart, severity_pie_chart, NUSUK_COLORS
lang = get_lang()
df = st.session_state.get("df")
filters = st.session_state.get("filters", {})
if df is None:
    st.stop()

as_of_date = filters.get("as_of_date")
m = compute_metrics(df, as_of_date)

st.markdown(f'<div class="nusuk-header"><h2>{t("page_health_safety")}</h2></div>', unsafe_allow_html=True)

# ── Filter health data ────────────────────────────────────────────────────
as_of = pd.Timestamp(as_of_date)
health_mask = (df["health_status"] != "none") & (df["health_date"] <= as_of)
health_df = df[health_mask]
death_mask = (df["death_status"] == True) & (df["death_date"] <= as_of)

# ── KPIs ───────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(t("health_incidents"), f"{len(health_df):,}")
with col2:
    st.metric(t("critical"), f"{(health_df['health_status'] == 'critical').sum():,}")
with col3:
    st.metric(t("severe"), f"{(health_df['health_status'] == 'severe').sum():,}")
with col4:
    st.metric(t("deaths"), f"{death_mask.sum():,}")

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts Row 1 ──────────────────────────────────────────────────────────
col_c1, col_c2 = st.columns(2)
with col_c1:
    st.plotly_chart(health_timeline_chart(m["daily_health"]), use_container_width=True)
with col_c2:
    st.plotly_chart(severity_pie_chart(df, as_of_date), use_container_width=True)

# ── Charts Row 2 ──────────────────────────────────────────────────────────
col_c3, col_c4 = st.columns(2)
with col_c3:
    if not health_df.empty:
        nat_inc = health_df["nationality"].value_counts().head(10)
        fig = go.Figure(go.Bar(x=nat_inc.values, y=nat_inc.index, orientation="h",
            marker_color=NUSUK_COLORS["red_light"], text=nat_inc.values, textposition="auto"))
        fig.update_layout(title=t("incidents_by_nationality"), yaxis=dict(autorange="reversed"),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=NUSUK_COLORS["brown_dark"]), margin=dict(l=40,r=40,t=50,b=40))
        st.plotly_chart(fig, use_container_width=True)

with col_c4:
    if not health_df.empty:
        bins = [0, 30, 40, 50, 60, 65, 70, 75, 80, 100]
        labels = ["<30", "30-39", "40-49", "50-59", "60-64", "65-69", "70-74", "75-79", "80+"]
        hdf = health_df.copy()
        hdf["age_group"] = pd.cut(hdf["age"], bins=bins, labels=labels, right=False)
        age_inc = hdf["age_group"].value_counts().sort_index()
        fig = go.Figure(go.Bar(x=age_inc.index.astype(str), y=age_inc.values,
            marker_color=[NUSUK_COLORS["gold"] if i < 4 else NUSUK_COLORS["yellow"] if i < 6 else NUSUK_COLORS["red_light"] for i in range(len(age_inc))],
            text=age_inc.values, textposition="auto"))
        fig.update_layout(title=t("incidents_by_age"), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=NUSUK_COLORS["brown_dark"]), margin=dict(l=40,r=40,t=50,b=40))
        st.plotly_chart(fig, use_container_width=True)

# ── At-Risk ────────────────────────────────────────────────────────────────
st.divider()
st.subheader("⚠️ " + t("at_risk"))

at_risk = df[
    df["person_type"].isin(["pilgrim_external", "pilgrim_internal"]) &
    (df["age"] >= 65) & (df["arrival_status"] == True) & (df["card_activated"] == False)
]

st.markdown(f"""<div class="alert-card alert-card-red">
    <strong>{"⚠️ " + t("elderly_no_card")}</strong><br>
    <span style="font-size:28px; font-weight:bold; color:#C62828;">{len(at_risk):,}</span><br>
    <span style="font-size:12px; color:#5C4033;">{"حجاج كبار السن وصلوا بدون بطاقة مفعلة" if lang == "ar" else "Elderly pilgrims arrived without activated card"}</span>
</div>""", unsafe_allow_html=True)

# ── Death Summary ──────────────────────────────────────────────────────────
st.divider()
st.subheader(t("death_summary"))
death_df = df[death_mask]
if not death_df.empty:
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        st.metric(t("total"), f"{len(death_df)}")
    with col_d2:
        st.metric("متوسط العمر" if lang == "ar" else "Average Age", f"{death_df['age'].mean():.0f}")
    with col_d3:
        top_nat = death_df["nationality"].value_counts().index[0] if len(death_df) > 0 else "-"
        st.metric("أكثر الجنسيات" if lang == "ar" else "Most Common Nationality", top_nat)
    if "health_notes" in death_df.columns:
        st.markdown("**" + ("أسباب الوفاة الرئيسية" if lang == "ar" else "Primary Causes") + "**")
        for note, count in death_df["health_notes"].value_counts().head(5).items():
            st.write(f"  {note}: {count}")
else:
    st.info("لا توجد حالات وفاة مسجلة حتى هذا التاريخ" if lang == "ar" else "No deaths recorded up to this date.")
