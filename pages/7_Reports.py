"""
Page 7: Reports & Export - التقارير
"""

import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import timedelta
from utils.i18n import t, get_lang
from utils.metrics import compute_metrics, compute_provider_metrics
lang = get_lang()
df = st.session_state.get("df")
filters = st.session_state.get("filters", {})
if df is None:
    st.stop()

as_of_date = filters.get("as_of_date")

st.markdown(f'<div class="nusuk-header"><h2>{t("page_reports")}</h2></div>', unsafe_allow_html=True)

m = compute_metrics(df, as_of_date)

# ── Daily Status Report ───────────────────────────────────────────────────
st.subheader("📋 " + t("daily_status_report"))

if lang == "ar":
    report = f"""### تقرير الحالة اليومي - {as_of_date}
**ملخص عام:**
- إجمالي التأشيرات والتصاريح: **{m['total_visas']:,}**
- إجمالي الواصلين: **{m['total_arrivals']:,}** ({m['arrival_pct']:.1f}%)
- البطاقات المطبوعة: **{m['cards_printed']:,}** ({m['printed_pct']:.1f}%)
- البطاقات المفعلة: **{m['cards_activated']:,}** ({m['activated_pct']:.1f}%)

**نقاط تحتاج اهتمام:**
- بطاقات عند الشركات لم تسلم: **{m['cards_not_delivered']:,}**
- حالات صحية: **{m['health_incidents']:,}**
- وفيات: **{m['deaths']:,}**"""
else:
    report = f"""### Daily Status Report - {as_of_date}
**Overall Summary:**
- Total Visas & Permits: **{m['total_visas']:,}**
- Total Arrivals: **{m['total_arrivals']:,}** ({m['arrival_pct']:.1f}%)
- Cards Printed: **{m['cards_printed']:,}** ({m['printed_pct']:.1f}%)
- Cards Activated: **{m['cards_activated']:,}** ({m['activated_pct']:.1f}%)

**Attention Required:**
- Cards NOT delivered: **{m['cards_not_delivered']:,}**
- Health incidents: **{m['health_incidents']:,}**
- Deaths: **{m['deaths']:,}**"""

st.markdown(report)

# ── Weekly Comparison ──────────────────────────────────────────────────────
st.divider()
st.subheader("📊 " + t("weekly_comparison"))

week_ago = as_of_date - timedelta(days=7)
m_prev = compute_metrics(df, week_ago)

labels = [t("total_arrivals"), t("cards_printed"), t("cards_at_center"), t("cards_at_provider"), t("cards_received"), t("cards_activated"), t("health_incidents")]
current_vals = [m["total_arrivals"], m["cards_printed"], m["cards_at_center"], m["cards_at_provider"], m["cards_received"], m["cards_activated"], m["health_incidents"]]
prev_vals = [m_prev["total_arrivals"], m_prev["cards_printed"], m_prev["cards_at_center"], m_prev["cards_at_provider"], m_prev["cards_received"], m_prev["cards_activated"], m_prev["health_incidents"]]

comp_df = pd.DataFrame({
    ("المؤشر" if lang == "ar" else "Metric"): labels,
    str(as_of_date): [f"{v:,}" for v in current_vals],
    str(week_ago): [f"{v:,}" for v in prev_vals],
    ("التغيير" if lang == "ar" else "Change"): [f"{c-p:+,}" for c, p in zip(current_vals, prev_vals)],
})
st.dataframe(comp_df, use_container_width=True, hide_index=True)

# ── Report Templates ──────────────────────────────────────────────────────
st.divider()
st.subheader("📄 " + ("قوالب التقارير" if lang == "ar" else "Report Templates"))

report_type = st.selectbox("اختر نوع التقرير" if lang == "ar" else "Select Report Type",
    options=[t("overdue_cards_report"), t("provider_report"), t("health_report")])

if st.button(t("generate_report"), type="primary"):
    as_of = pd.Timestamp(as_of_date)
    if report_type == t("overdue_cards_report"):
        has_prov = df["card_at_provider_date"].notna()
        not_recv = df["card_received"] == False
        overdue = df[has_prov & not_recv].copy()
        overdue["days_overdue"] = (as_of - overdue["card_at_provider_date"]).dt.days
        overdue = overdue[overdue["days_overdue"] > 7].sort_values("days_overdue", ascending=False)
        st.markdown(f"**{'بطاقات متأخرة (أكثر من 7 أيام)' if lang == 'ar' else 'Overdue Cards (>7 days)'}**: {len(overdue):,}")
        st.dataframe(overdue[["person_id", "first_name", "last_name", "nationality", "service_provider", "days_overdue"]].head(200),
            use_container_width=True, hide_index=True)
    elif report_type == t("provider_report"):
        st.dataframe(compute_provider_metrics(df, as_of_date), use_container_width=True, hide_index=True)
    elif report_type == t("health_report"):
        health_mask = (df["health_status"] != "none") & (df["health_date"] <= as_of)
        st.dataframe(df[health_mask][["person_id", "first_name", "last_name", "nationality", "age", "health_status", "health_date", "health_notes"]].sort_values("health_date", ascending=False).head(500),
            use_container_width=True, hide_index=True)

# ── Export ─────────────────────────────────────────────────────────────────
st.divider()
st.subheader("💾 " + t("export_data"))

col_e1, col_e2 = st.columns(2)
with col_e1:
    # Limit full export to 50K rows to avoid memory issues on Cloud
    csv_data = df.head(50000).to_csv(index=False).encode("utf-8-sig")
    st.download_button(f"📥 {t('export_csv')} ({('كامل' if lang == 'ar' else 'Full')} - 50K)",
        data=csv_data, file_name="hajj_nusuk_full.csv", mime="text/csv", use_container_width=True)

with col_e2:
    as_of = pd.Timestamp(as_of_date)
    filtered = df[df["visa_issue_date"] <= as_of]
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        filtered.head(50000).to_excel(writer, index=False, sheet_name="Data")
    st.download_button(f"📥 {t('export_excel')} ({('حتى التاريخ' if lang == 'ar' else 'To Date')})",
        data=buffer.getvalue(), file_name=f"hajj_nusuk_{as_of_date}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
