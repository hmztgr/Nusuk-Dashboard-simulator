"""
Page 3: Card Tracking - تتبع البطاقات
Search, filters, paginated results, individual lookup, export.
"""

import streamlit as st
import pandas as pd
from io import BytesIO
from utils.i18n import t, get_lang
lang = get_lang()
df = st.session_state.get("df")
filters = st.session_state.get("filters", {})
if df is None:
    st.stop()

as_of_date = filters.get("as_of_date")

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown(f'<div class="nusuk-header"><h2>{t("page_card_tracking")}</h2></div>', unsafe_allow_html=True)

# ── Search ─────────────────────────────────────────────────────────────────
search_query = st.text_input(t("search"), placeholder=t("search_placeholder"), key="search_input")

# ── Advanced Filters ───────────────────────────────────────────────────────
with st.expander(t("advanced_filters"), expanded=False):
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)

    with col_f1:
        selected_nationality = st.selectbox(
            t("nationality_filter"),
            options=[t("all")] + sorted(df["nationality"].unique().tolist()),
            key="track_nationality")

    with col_f2:
        selected_person_type = st.selectbox(
            t("person_type_filter"),
            options=[t("all")] + df["person_type"].unique().tolist(),
            key="track_person_type")

    with col_f3:
        status_options = [
            t("all"),
            "مطبوعة" if lang == "ar" else "Printed",
            "بالمركز" if lang == "ar" else "At Center",
            "بالشركة" if lang == "ar" else "At Provider",
            "مستلمة" if lang == "ar" else "Received",
            "مفعلة" if lang == "ar" else "Activated",
            "لم تطبع" if lang == "ar" else "Not Printed",
        ]
        selected_card_status = st.selectbox(t("card_status"), options=status_options, key="track_card_status")

    with col_f4:
        selected_provider = st.selectbox(
            t("provider_filter"),
            options=[t("all")] + sorted(df["service_provider"].dropna().unique().tolist()),
            key="track_provider")

# ── Apply Filters ──────────────────────────────────────────────────────────
as_of = pd.Timestamp(as_of_date)

# Timeline filter (no .copy() needed — filtering creates new DataFrames)
results = df[df["visa_issue_date"] <= as_of]

# Search (all columns are already string from app.py load_data)
if search_query:
    q = search_query.lower()
    results = results[
        results["first_name"].str.lower().str.contains(q, na=False) |
        results["last_name"].str.lower().str.contains(q, na=False) |
        results["nusuk_number"].str.lower().str.contains(q, na=False) |
        results["id_number"].str.lower().str.contains(q, na=False) |
        results["passport_number"].str.lower().str.contains(q, na=False)
    ]

if selected_nationality != t("all"):
    results = results[results["nationality"] == selected_nationality]
if selected_person_type != t("all"):
    results = results[results["person_type"] == selected_person_type]
if selected_provider != t("all"):
    results = results[results["service_provider"] == selected_provider]

# Card status
status_col_map = {
    "Printed": "card_printed", "مطبوعة": "card_printed",
    "At Center": "card_at_center", "بالمركز": "card_at_center",
    "At Provider": "card_at_provider", "بالشركة": "card_at_provider",
    "Received": "card_received", "مستلمة": "card_received",
    "Activated": "card_activated", "مفعلة": "card_activated",
}
if selected_card_status in ("Not Printed", "لم تطبع"):
    results = results[results["card_printed"] == False]
elif selected_card_status in status_col_map:
    results = results[results[status_col_map[selected_card_status]] == True]

# ── Results ────────────────────────────────────────────────────────────────
total_results = len(results)
st.markdown(f"**{t('showing')} {min(total_results, 50)} {t('of')} {total_results:,} {t('records')}**")

PAGE_SIZE = 50
total_pages = max(1, (total_results + PAGE_SIZE - 1) // PAGE_SIZE)
current_page = st.number_input(t("page"), min_value=1, max_value=total_pages, value=1, step=1, key="page_num")

start_idx = (current_page - 1) * PAGE_SIZE
page_results = results.iloc[start_idx:start_idx + PAGE_SIZE]

display_cols = [
    "person_id", "first_name", "last_name", "nationality", "person_type",
    "nusuk_number", "card_printed", "card_at_center", "card_at_provider",
    "card_received", "card_activated", "arrival_status", "service_provider",
]

col_labels = {
    "person_id": "ID",
    "first_name": "الاسم الأول" if lang == "ar" else "First Name",
    "last_name": "اسم العائلة" if lang == "ar" else "Last Name",
    "nationality": "الجنسية" if lang == "ar" else "Nationality",
    "person_type": "النوع" if lang == "ar" else "Type",
    "nusuk_number": "رقم النسك" if lang == "ar" else "Nusuk #",
    "card_printed": "مطبوعة" if lang == "ar" else "Printed",
    "card_at_center": "بالمركز" if lang == "ar" else "At Center",
    "card_at_provider": "بالشركة" if lang == "ar" else "At Provider",
    "card_received": "مستلمة" if lang == "ar" else "Received",
    "card_activated": "مفعلة" if lang == "ar" else "Activated",
    "arrival_status": "وصل" if lang == "ar" else "Arrived",
    "service_provider": "الشركة" if lang == "ar" else "Provider",
}

display_df = page_results[display_cols].copy()
display_df.columns = [col_labels.get(c, c) for c in display_cols]
st.dataframe(display_df, use_container_width=True, hide_index=True, height=500)

# ── Individual Record Lookup ───────────────────────────────────────────────
st.divider()
st.subheader("🔎 " + t("details"))

lookup_id = st.text_input("Person ID" if lang == "en" else "رقم الشخص", key="lookup_id")

if lookup_id:
    try:
        pid = int(lookup_id)
        person = df[df["person_id"] == pid]
        if len(person) > 0:
            p = person.iloc[0]
            col_d1, col_d2, col_d3 = st.columns(3)

            with col_d1:
                st.markdown("**" + ("معلومات شخصية" if lang == "ar" else "Personal Info") + "**")
                st.write(f"{'الاسم' if lang == 'ar' else 'Name'}: {p['first_name']} {p['last_name']}")
                st.write(f"{'الجنسية' if lang == 'ar' else 'Nationality'}: {p['nationality']}")
                st.write(f"{'العمر' if lang == 'ar' else 'Age'}: {p['age']}")
                st.write(f"{'الجنس' if lang == 'ar' else 'Sex'}: {p['sex']}")
                st.write(f"{'النوع' if lang == 'ar' else 'Type'}: {t(p['person_type'])}")

            with col_d2:
                st.markdown("**" + ("حالة البطاقة" if lang == "ar" else "Card Status") + "**")
                st.write(f"{'رقم النسك' if lang == 'ar' else 'Nusuk #'}: {p['nusuk_number']}")
                for col_name, label in [
                    ("card_printed", "مطبوعة" if lang == "ar" else "Printed"),
                    ("card_at_center", "بالمركز" if lang == "ar" else "At Center"),
                    ("card_at_provider", "بالشركة" if lang == "ar" else "At Provider"),
                    ("card_received", "مستلمة" if lang == "ar" else "Received"),
                    ("card_activated", "مفعلة" if lang == "ar" else "Activated"),
                ]:
                    st.write(f"{'✅' if p[col_name] else '❌'} {label}")

            with col_d3:
                st.markdown("**" + ("معلومات السفر" if lang == "ar" else "Travel Info") + "**")
                st.write(f"{'الشركة' if lang == 'ar' else 'Provider'}: {p['service_provider']}")
                st.write(f"{'وصل' if lang == 'ar' else 'Arrived'}: {'✅' if p['arrival_status'] else '❌'}")
                if pd.notna(p['arrival_date']):
                    st.write(f"{'تاريخ الوصول' if lang == 'ar' else 'Arrival Date'}: {p['arrival_date']}")
                st.write(f"{'ميناء الوصول' if lang == 'ar' else 'Port'}: {p['arrival_port']}")
                st.write(f"{'طريقة السفر' if lang == 'ar' else 'Travel Mode'}: {p['travel_mode']}")
        else:
            st.warning(t("no_results"))
    except ValueError:
        st.warning("يرجى إدخال رقم صحيح." if lang == "ar" else "Please enter a valid numeric ID.")

# ── Export ─────────────────────────────────────────────────────────────────
st.divider()
col_exp1, col_exp2, _ = st.columns([1, 1, 3])

with col_exp1:
    csv_data = results[display_cols].head(50000).to_csv(index=False).encode("utf-8-sig")
    st.download_button(t("export_csv"), data=csv_data, file_name="hajj_card_tracking.csv", mime="text/csv", use_container_width=True)

with col_exp2:
    buffer = BytesIO()
    results[display_cols].head(10000).to_excel(buffer, index=False, engine="openpyxl")
    st.download_button(t("export_excel"), data=buffer.getvalue(), file_name="hajj_card_tracking.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
