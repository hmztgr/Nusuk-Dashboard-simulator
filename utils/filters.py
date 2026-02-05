"""
Shared sidebar filter components.
Used across all pages for consistent filtering.
"""

import streamlit as st
from datetime import datetime, date, timedelta
from utils.i18n import t, get_lang
import time


# Season phase presets
PHASE_DATES = {
    "phase_pre_season": date(2025, 4, 15),
    "phase_early_arrivals": date(2025, 5, 5),
    "phase_peak_arrival": date(2025, 5, 20),
    "phase_arrival_deadline": date(2025, 5, 31),
    "phase_arafah": date(2025, 6, 5),
    "phase_post_hajj": date(2025, 6, 15),
    "phase_season_end": date(2025, 6, 30),
}

SEASON_START = date(2025, 4, 1)
SEASON_END = date(2025, 6, 30)


def render_sidebar(df):
    """Render the shared sidebar with all filter controls."""

    # Advance animation BEFORE any widget reads the state
    if st.session_state.get("playing", False):
        current = st.session_state.get("date_slider", SEASON_START)
        if current < SEASON_END:
            st.session_state["date_slider"] = current + timedelta(days=1)
        else:
            st.session_state["playing"] = False

    with st.sidebar:
        # ── Nusuk Logo / Branding ──────────────────────────────────────
        lang = get_lang()

        st.markdown(f"""
        <div style="text-align: center; padding: 10px; margin-bottom: 15px;
                    background: linear-gradient(135deg, #5C4033, #8B6914);
                    border-radius: 12px; color: white;">
            <div style="font-size: 28px; font-weight: bold; font-family: 'Segoe UI', Tahoma;">
                {"نسك" if lang == "ar" else "nusuk"}
            </div>
            <div style="font-size: 11px; margin-top: 4px; opacity: 0.85;">
                {"لوحة معلومات غرفة التحكم - منصة بطاقة" if lang == "ar" else "Control Room Dashboard - Card Platform"}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Language Toggle ────────────────────────────────────────────
        col1, col2 = st.columns(2)
        with col1:
            if st.button("العربية", use_container_width=True,
                         type="primary" if lang == "ar" else "secondary"):
                st.session_state["lang"] = "ar"
                st.rerun()
        with col2:
            if st.button("English", use_container_width=True,
                         type="primary" if lang == "en" else "secondary"):
                st.session_state["lang"] = "en"
                st.rerun()

        st.divider()

        # ── Season Phase Selector ──────────────────────────────────────
        phase_options = list(PHASE_DATES.keys())

        # Default to arrival deadline
        default_idx = phase_options.index("phase_arrival_deadline")

        selected_phase = st.selectbox(
            t("season_phase"),
            options=phase_options,
            format_func=lambda x: t(x),
            index=default_idx,
            key="phase_selector"
        )

        # ── Date Slider ───────────────────────────────────────────────
        # If slider already has a value in session state, use it; otherwise use phase date
        if "date_slider" not in st.session_state:
            st.session_state["date_slider"] = PHASE_DATES[selected_phase]

        selected_date = st.slider(
            t("date_slider"),
            min_value=SEASON_START,
            max_value=SEASON_END,
            format="YYYY-MM-DD",
            key="date_slider"
        )

        # ── Play/Animation Button ──────────────────────────────────────
        col_play, col_stop = st.columns(2)
        with col_play:
            play_btn = st.button(t("play_animation"), use_container_width=True)
        with col_stop:
            stop_btn = st.button(t("stop_animation"), use_container_width=True)

        if play_btn:
            st.session_state["playing"] = True
        if stop_btn:
            st.session_state["playing"] = False

        st.divider()

        # ── Person Type Filter ─────────────────────────────────────────
        person_types = df["person_type"].unique().tolist()
        person_type_labels = {pt: t(pt) for pt in person_types}

        selected_types = st.multiselect(
            t("person_type_filter"),
            options=person_types,
            format_func=lambda x: person_type_labels.get(x, x),
            default=person_types,
            key="person_type_filter"
        )

        # ── Nationality Filter ─────────────────────────────────────────
        top_nationalities = df["nationality"].value_counts().head(15).index.tolist()

        selected_nationalities = st.multiselect(
            t("nationality_filter"),
            options=top_nationalities,
            default=[],
            key="nationality_filter",
            placeholder=t("all")
        )

        # ── Provider Filter ────────────────────────────────────────────
        providers = sorted(df["service_provider"].dropna().unique().tolist())
        selected_providers = st.multiselect(
            t("provider_filter"),
            options=providers,
            default=[],
            key="provider_filter",
            placeholder=t("all")
        )

        # ── Reload Time ───────────────────────────────────────────────
        st.divider()
        now = datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
        st.caption(f"{t('reload_time')}: {now}")

    return {
        "as_of_date": selected_date,
        "person_types": selected_types,
        "nationalities": selected_nationalities,
        "providers": selected_providers,
    }


def animate_slider():
    """Trigger a rerun to keep the animation going.
    Uses 2.0s sleep to reduce memory pressure on Streamlit Cloud.
    """
    if st.session_state.get("playing", False):
        time.sleep(2.0)
        st.rerun()
