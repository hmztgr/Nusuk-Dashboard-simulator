"""
Page 4: Service Providers - شركات تقديم الخدمة
"""

import streamlit as st
import pandas as pd
from utils.i18n import t, get_lang
from utils.metrics import compute_provider_metrics
from utils.charts import provider_comparison_chart
lang = get_lang()
df = st.session_state.get("df")
filters = st.session_state.get("filters", {})
if df is None:
    st.stop()

as_of_date = filters.get("as_of_date")

st.markdown(f'<div class="nusuk-header"><h2>{t("page_service_providers")}</h2></div>', unsafe_allow_html=True)

provider_df = compute_provider_metrics(df, as_of_date)
if provider_df.empty:
    st.warning(t("no_results"))
    st.stop()

# ── KPIs ───────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("الشركات" if lang == "ar" else "Total Providers", f"{len(provider_df)}")
with col2:
    st.metric("متوسط التسليم" if lang == "ar" else "Avg Delivery Rate", f"{provider_df['delivery_rate'].mean():.1f}%")
with col3:
    under = (provider_df["delivery_rate"] < 60).sum()
    st.metric("أداء ضعيف (<60%)" if lang == "ar" else "Under-Performing", f"{under}", delta=f"-{under}" if under > 0 else "0", delta_color="inverse")
with col4:
    st.metric(t("health_incidents"), f"{provider_df['health_incidents'].sum():,}")

st.markdown("<br>", unsafe_allow_html=True)

# ── Chart ──────────────────────────────────────────────────────────────────
st.plotly_chart(provider_comparison_chart(provider_df), use_container_width=True)

# ── Table ──────────────────────────────────────────────────────────────────
st.subheader(t("provider_performance"))
display_df = provider_df.copy()
display_df.columns = [
    "الشركة" if lang == "ar" else "Provider",
    "الحجاج" if lang == "ar" else "Pilgrims",
    "بطاقات بالشركة" if lang == "ar" else "Cards at Provider",
    "بطاقات مستلمة" if lang == "ar" else "Cards Received",
    "بطاقات مفعلة" if lang == "ar" else "Cards Activated",
    "نسبة التسليم %" if lang == "ar" else "Delivery Rate %",
    "متوسط الأيام" if lang == "ar" else "Avg Days",
    "حالات صحية" if lang == "ar" else "Health Incidents",
]
st.dataframe(display_df, use_container_width=True, hide_index=True, height=600,
    column_config={display_df.columns[5]: st.column_config.ProgressColumn(display_df.columns[5], min_value=0, max_value=100, format="%.1f%%")})

# ── Drill-Down ─────────────────────────────────────────────────────────────
st.divider()
st.subheader("🔍 " + ("تفاصيل الشركة" if lang == "ar" else "Provider Detail"))

selected_provider = st.selectbox("اختر شركة" if lang == "ar" else "Select Provider", options=provider_df["provider"].tolist(), key="provider_detail")

if selected_provider:
    prov_data = df[df["service_provider"] == selected_provider]
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown("**" + ("توزيع الأنواع" if lang == "ar" else "Person Type Breakdown") + "**")
        for ptype, count in prov_data["person_type"].value_counts().items():
            st.write(f"  {t(ptype)}: {count:,}")
    with col_d2:
        st.markdown("**" + ("أعلى الجنسيات" if lang == "ar" else "Top Nationalities") + "**")
        for nat, count in prov_data["nationality"].value_counts().head(5).items():
            st.write(f"  {nat}: {count:,}")

    show_cols = ["person_id", "first_name", "last_name", "nationality", "person_type", "card_printed", "card_received", "card_activated"]
    st.dataframe(prov_data[show_cols].head(200), use_container_width=True, hide_index=True, height=400)
