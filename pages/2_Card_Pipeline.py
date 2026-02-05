"""
Page 2: Card Pipeline - الملخص التنفيذي للبطاقات
Centerpiece page replicating the Nusuk screenshot layout.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.i18n import t, get_lang
from utils.metrics import compute_metrics

lang = get_lang()
df = st.session_state.get("df")
filters = st.session_state.get("filters", {})
if df is None:
    st.stop()

as_of_date = filters.get("as_of_date")

# ── B2B / B2C Toggle ──────────────────────────────────────────────────────
b2b_b2c = st.radio(
    t("pilgrim_type"),
    ["B2B", "B2C"],
    horizontal=True,
    label_visibility="collapsed",
    help=("B2B: حجاج عن طريق شركات الطوافة | B2C: حجاج مسجلين مباشرة"
          if lang == "ar" else
          "B2B: Pilgrims via authorized travel companies | B2C: Direct registration on Nusuk"),
)

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown(f'<div class="nusuk-header"><h2>{t("page_card_pipeline")}</h2></div>', unsafe_allow_html=True)

# ── Overall Metrics (cached — pass filter params instead of pre-filtered df) ──
m = compute_metrics(df, as_of_date, b2b_b2c_filter=b2b_b2c)

# ── Top Alert Bar ──────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background: linear-gradient(90deg, #5C4033, #8B6914);
            color: white; padding: 10px 20px; border-radius: 8px; margin-bottom: 15px;
            display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; gap: 15px;">
    <span>👤 {t("total_arrivals")}: <strong>{m['total_arrivals']:,}</strong></span>
    <span>📊 {t("arrival_pct")}: <strong>{m['arrival_pct']:.2f}%</strong></span>
    <span>⚠️ {t("cards_not_delivered")}: <strong>{m['cards_not_delivered']:,}</strong></span>
</div>
""", unsafe_allow_html=True)


# ── Pipeline Row Builder (using st.columns) ──────────────────────────────
def _pipeline_row(metrics, label, show_groups=True):
    """Render one pipeline row using native Streamlit columns."""
    st.markdown(f"**{label}**")

    if show_groups:
        stages = [
            ("🪪", t("total_visas_permits"), metrics["total_visas"], ""),
            ("👥", t("groups_formed"), metrics["groups_formed"], f'{metrics["formation_pct"]:.2f}%'),
            ("🖨️", t("cards_printed"), metrics["cards_printed"], f'{metrics["printed_pct"]:.2f}%'),
            ("🏢", t("cards_at_center"), metrics["cards_at_center"], f'{metrics["center_pct"]:.2f}%'),
            ("🚚", t("cards_at_provider"), metrics["cards_at_provider"], f'{metrics["provider_pct"]:.2f}%'),
            ("✅", t("cards_activated_delivered"), metrics["cards_activated"], f'{metrics["activated_pct"]:.2f}%'),
        ]
    else:
        stages = [
            ("🪪", t("total_visas_permits"), metrics["total_visas"], ""),
            ("🖨️", t("cards_printed"), metrics["cards_printed"], f'{metrics["printed_pct"]:.2f}%'),
            ("🏢", t("cards_at_center"), metrics["cards_at_center"], f'{metrics["center_pct"]:.2f}%'),
            ("🚚", t("cards_at_provider"), metrics["cards_at_provider"], f'{metrics["provider_pct"]:.2f}%'),
            ("✅", t("cards_activated_delivered"), metrics["cards_activated"], f'{metrics["activated_pct"]:.2f}%'),
        ]

    # For Arabic RTL, reverse column order
    if lang == "ar":
        stages = list(reversed(stages))

    cols = st.columns(len(stages))
    for i, (icon, stage_label, value, pct) in enumerate(stages):
        with cols[i]:
            pct_html = f'<div class="step-pct">{pct}</div>' if pct else ""
            st.markdown(f'<div class="pipeline-step"><div style="font-size:22px;">{icon}</div><div class="step-value">{value:,}</div><div class="step-label">{stage_label}</div>{pct_html}</div>', unsafe_allow_html=True)


# ── Top Summary (all combined) ─────────────────────────────────────────────
direction = "row-reverse" if lang == "ar" else "row"
st.markdown(f"""
<div style="background:linear-gradient(90deg,#F0E6D4,#FAF6F0); border-radius:10px; padding:15px; margin:10px 0;">
    <div style="display:flex; flex-direction:{direction};
                justify-content:space-around; align-items:flex-start; flex-wrap:wrap; gap:10px;">
        <div style="text-align:center;">
            <div style="font-size:11px;color:#5C4033;">{t("total_visas_permits")}</div>
            <div style="font-size:24px;font-weight:bold;color:#4A3728;">{m['total_visas']:,}</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:11px;color:#5C4033;">{t("groups_formed")}</div>
            <div style="font-size:24px;font-weight:bold;color:#4A3728;">{m['groups_formed']:,}</div>
            <div style="font-size:11px;color:#8B6914;">{m['formation_pct']:.2f}%</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:11px;color:#5C4033;">{t("cards_printed")}</div>
            <div style="font-size:24px;font-weight:bold;color:#4A3728;">{m['cards_printed']:,}</div>
            <div style="font-size:11px;color:#8B6914;">{m['printed_pct']:.2f}%</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:11px;color:#5C4033;">{t("cards_at_center")}</div>
            <div style="font-size:24px;font-weight:bold;color:#4A3728;">{m['cards_at_center']:,}</div>
            <div style="font-size:11px;color:#8B6914;">{m['center_pct']:.2f}%</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:11px;color:#5C4033;">{t("cards_at_provider")}</div>
            <div style="font-size:24px;font-weight:bold;color:#4A3728;">{m['cards_at_provider']:,}</div>
            <div style="font-size:11px;color:#8B6914;">{m['provider_pct']:.2f}%</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:11px;color:#5C4033;">{t("cards_activated_delivered")}</div>
            <div style="font-size:24px;font-weight:bold;color:#4A3728;">{m['cards_activated']:,}</div>
            <div style="font-size:11px;color:#8B6914;">{m['activated_pct']:.2f}%</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Per-type rows ──────────────────────────────────────────────────────────
for ptype, label, show_g in [
    ("pilgrim_external", "حجاج الخارج" if lang == "ar" else "External Pilgrims", True),
    ("pilgrim_internal", "حجاج الداخل" if lang == "ar" else "Internal Pilgrims", True),
    ("service_worker", "العاملين" if lang == "ar" else "Service Workers", False),
]:
    st.divider()
    pm = compute_metrics(df, as_of_date, person_type_filter=[ptype], b2b_b2c_filter=b2b_b2c)
    _pipeline_row(pm, label, show_g)

# ── Reload timestamp ──────────────────────────────────────────────────────
st.caption(f"{t('reload_time')}: {datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')}")
