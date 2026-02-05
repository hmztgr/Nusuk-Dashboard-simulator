"""
Page 6: Demographics - التركيبة السكانية
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.i18n import t, get_lang
from utils.charts import world_map_chart, age_sex_pyramid, b2b_b2c_nationality_chart, nationality_bar_chart, NUSUK_COLORS
lang = get_lang()
df = st.session_state.get("df")
filters = st.session_state.get("filters", {})
if df is None:
    st.stop()

as_of_date = filters.get("as_of_date")

st.markdown(f'<div class="nusuk-header"><h2>{t("page_demographics")}</h2></div>', unsafe_allow_html=True)

# ── Note about data (issue #8) ────────────────────────────────────────────
st.caption("ℹ️ " + ("الخريطة تعرض الحجاج الخارجيين فقط. الجدول أدناه يشمل جميع الأنواع بما في ذلك الحجاج الداخل والعاملين."
    if lang == "ar" else "Map shows external pilgrims only. Charts below include all types including internal pilgrims and workers."))

# ── World Map ──────────────────────────────────────────────────────────────
st.plotly_chart(world_map_chart(df, as_of_date), use_container_width=True)

# ── Age Pyramid + Nationality ──────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(age_sex_pyramid(df, as_of_date), use_container_width=True)
with col2:
    st.plotly_chart(nationality_bar_chart(df, as_of_date, top_n=15), use_container_width=True)

# ── B2B vs B2C ─────────────────────────────────────────────────────────────
st.divider()
st.plotly_chart(b2b_b2c_nationality_chart(df, as_of_date), use_container_width=True)

# ── Family Patterns ────────────────────────────────────────────────────────
st.divider()
st.subheader(t("family_patterns"))

as_of = pd.Timestamp(as_of_date)
visa_mask = pd.to_datetime(df["visa_issue_date"], errors="coerce") <= as_of
pilgrims = df[visa_mask & df["person_type"].isin(["pilgrim_external", "pilgrim_internal"])]

total = len(pilgrims)
with_spouse = pilgrims["spouse_id"].notna().sum()
with_father = pilgrims["father_id"].notna().sum()
solo = total - with_spouse - with_father

col_f1, col_f2, col_f3, col_f4 = st.columns(4)
with col_f1:
    st.metric("إجمالي الحجاج" if lang == "ar" else "Total Pilgrims", f"{total:,}")
with col_f2:
    st.metric("مع زوج/ة" if lang == "ar" else "With Spouse", f"{with_spouse:,}", f"{with_spouse/max(total,1)*100:.1f}%")
with col_f3:
    st.metric("مع والد" if lang == "ar" else "With Parent", f"{with_father:,}", f"{with_father/max(total,1)*100:.1f}%")
with col_f4:
    st.metric("فردي" if lang == "ar" else "Solo", f"{solo:,}", f"{solo/max(total,1)*100:.1f}%")

# ── Arrival by Nationality ─────────────────────────────────────────────────
st.divider()
st.subheader(t("arrival_by_nationality"))

filtered = df[visa_mask]
top5 = filtered["nationality"].value_counts().head(5).index
arrived = filtered[filtered["arrival_status"] == True]
colors = [NUSUK_COLORS["brown"], NUSUK_COLORS["gold"], NUSUK_COLORS["blue"], NUSUK_COLORS["green"], NUSUK_COLORS["red_light"]]

fig = go.Figure()
for i, nat in enumerate(top5):
    nat_arr = arrived[arrived["nationality"] == nat]
    if not nat_arr.empty:
        daily = pd.to_datetime(nat_arr["arrival_date"]).dt.date.value_counts().sort_index()
        fig.add_trace(go.Scatter(x=daily.cumsum().index, y=daily.cumsum().values,
            name=nat, line=dict(color=colors[i % len(colors)], width=2)))

fig.update_layout(title=t("arrival_by_nationality"), xaxis_title=t("date"), yaxis_title=t("cumulative"),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color=NUSUK_COLORS["brown_dark"]), margin=dict(l=40,r=40,t=50,b=40))
st.plotly_chart(fig, use_container_width=True)

# ── Travel Mode ────────────────────────────────────────────────────────────
st.divider()
st.subheader("✈️ " + ("وسيلة السفر" if lang == "ar" else "Travel Mode"))

travel = filtered["travel_mode"].value_counts()
icons = {"air": "✈️", "land": "🚌", "sea": "🚢"}
cols = st.columns(len(travel))
for i, (mode, count) in enumerate(travel.items()):
    with cols[i]:
        st.metric(f"{icons.get(mode, '')} {mode.capitalize()}", f"{count:,}", f"{count/len(filtered)*100:.1f}%")
