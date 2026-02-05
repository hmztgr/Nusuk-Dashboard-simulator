"""
Bilingual labels for Arabic (default) and English.
Usage: from utils.i18n import t, get_lang
"""

LABELS = {
    # ── App-wide ───────────────────────────────────────────────────────
    "app_title": {"ar": "لوحة معلومات نسك - إدارة بطاقات الحج", "en": "Nusuk Dashboard - Hajj Card Management"},
    "language": {"ar": "العربية", "en": "English"},
    "language_toggle": {"ar": "🌐 اللغة", "en": "🌐 Language"},

    # ── Sidebar ────────────────────────────────────────────────────────
    "sidebar_title": {"ar": "لوحة التحكم", "en": "Control Panel"},
    "season_phase": {"ar": "مرحلة الموسم", "en": "Season Phase"},
    "date_slider": {"ar": "التاريخ", "en": "Date"},
    "play_animation": {"ar": "▶ تشغيل الحركة", "en": "▶ Play Animation"},
    "stop_animation": {"ar": "⏹ إيقاف", "en": "⏹ Stop"},
    "person_type_filter": {"ar": "نوع الشخص", "en": "Person Type"},
    "nationality_filter": {"ar": "الجنسية", "en": "Nationality"},
    "provider_filter": {"ar": "مقدم الخدمة", "en": "Service Provider"},
    "all": {"ar": "الكل", "en": "All"},

    # ── Season Phases ──────────────────────────────────────────────────
    "phase_pre_season": {"ar": "ما قبل الموسم (15 أبريل)", "en": "Pre-Season (Apr 15)"},
    "phase_early_arrivals": {"ar": "الوصول المبكر (5 مايو)", "en": "Early Arrivals (May 5)"},
    "phase_peak_arrival": {"ar": "ذروة الوصول (20 مايو)", "en": "Peak Arrival (May 20)"},
    "phase_arrival_deadline": {"ar": "نهاية الوصول (31 مايو)", "en": "Arrival Deadline (May 31)"},
    "phase_arafah": {"ar": "يوم عرفة (5 يونيو)", "en": "Day of Arafah (Jun 5)"},
    "phase_post_hajj": {"ar": "بعد الحج (15 يونيو)", "en": "Post-Hajj (Jun 15)"},
    "phase_season_end": {"ar": "نهاية الموسم (30 يونيو)", "en": "Season End (Jun 30)"},

    # ── Person Types ───────────────────────────────────────────────────
    "pilgrim_external": {"ar": "حجاج الخارج", "en": "External Pilgrims"},
    "pilgrim_internal": {"ar": "حجاج الداخل", "en": "Internal Pilgrims"},
    "service_worker": {"ar": "العاملين", "en": "Service Workers"},
    "government": {"ar": "حكومي", "en": "Government"},
    "healthcare": {"ar": "صحي", "en": "Healthcare"},

    # ── Page Names ─────────────────────────────────────────────────────
    "page_executive_summary": {"ar": "الملخص التنفيذي", "en": "Executive Summary"},
    "page_card_pipeline": {"ar": "الملخص التنفيذي للبطاقات", "en": "Card Pipeline"},
    "page_card_tracking": {"ar": "تتبع البطاقات", "en": "Card Tracking"},
    "page_service_providers": {"ar": "شركات تقديم الخدمة", "en": "Service Providers"},
    "page_health_safety": {"ar": "الصحة والسلامة", "en": "Health & Safety"},
    "page_demographics": {"ar": "التركيبة السكانية", "en": "Demographics"},
    "page_reports": {"ar": "التقارير", "en": "Reports & Export"},

    # ── KPI Labels ─────────────────────────────────────────────────────
    "total_visas": {"ar": "إجمالي التأشيرات والتصاريح", "en": "Total Visas & Permits"},
    "total_arrivals": {"ar": "أعداد الواصلين", "en": "Total Arrivals"},
    "arrival_pct": {"ar": "نسبة الواصلين إلى الإجمالي", "en": "Arrival %"},
    "cards_active": {"ar": "البطاقات المفعلة", "en": "Cards Activated"},
    "cards_activated": {"ar": "البطاقات المفعلة", "en": "Cards Activated"},
    "health_incidents": {"ar": "الحالات الصحية", "en": "Health Incidents"},
    "deaths": {"ar": "الوفيات", "en": "Deaths"},

    # ── Card Pipeline Labels ───────────────────────────────────────────
    "total_visas_permits": {"ar": "إجمالي التأشيرات", "en": "Total Visas"},
    "groups_formed": {"ar": "إجمالي تكوين المجموعات", "en": "Groups Formed"},
    "cards_printed": {"ar": "إجمالي البطاقات المطبوعة", "en": "Cards Printed"},
    "cards_at_center": {"ar": "البطاقات الواصلة مركز التوزيع", "en": "Cards at Distribution Center"},
    "cards_at_provider": {"ar": "البطاقات المسلمة للشركات", "en": "Cards at Providers"},
    "cards_received": {"ar": "البطاقات المسلمة للحجاج", "en": "Cards Received by Pilgrims"},
    "cards_activated_delivered": {"ar": "البطاقات المفعلة والمسلمة للحجاج", "en": "Cards Activated & Delivered"},
    "formation_pct": {"ar": "نسبة التكوين إلى", "en": "Formation % of"},
    "printed_pct": {"ar": "نسبة المطبوعة إلى", "en": "Printed % of"},
    "center_pct": {"ar": "نسبة الواصلة إلى", "en": "At Center % of"},
    "provider_pct": {"ar": "نسبة المسلمة إلى", "en": "At Provider % of"},
    "activated_pct": {"ar": "نسبة المفعلة إلى", "en": "Activated % of"},
    "cards_not_delivered": {"ar": "عدد البطاقات المسلمة للشركة ولم تسلم", "en": "Cards at Company But NOT Delivered"},
    "b2b": {"ar": "B2B", "en": "B2B"},
    "b2c": {"ar": "B2C", "en": "B2C"},
    "pilgrim_type": {"ar": "نوع الحاج", "en": "Pilgrim Type"},

    # ── Card Tracking ──────────────────────────────────────────────────
    "search": {"ar": "بحث", "en": "Search"},
    "search_placeholder": {"ar": "ابحث بالاسم أو رقم النسك أو جواز السفر...", "en": "Search by name, Nusuk number, or passport..."},
    "advanced_filters": {"ar": "فلاتر متقدمة", "en": "Advanced Filters"},
    "card_status": {"ar": "حالة البطاقة", "en": "Card Status"},
    "date_range": {"ar": "نطاق التاريخ", "en": "Date Range"},
    "export_csv": {"ar": "تصدير CSV", "en": "Export CSV"},
    "export_excel": {"ar": "تصدير Excel", "en": "Export Excel"},
    "results": {"ar": "النتائج", "en": "Results"},
    "no_results": {"ar": "لا توجد نتائج", "en": "No results found"},
    "showing": {"ar": "عرض", "en": "Showing"},
    "of": {"ar": "من", "en": "of"},
    "records": {"ar": "سجل", "en": "records"},

    # ── Service Providers ──────────────────────────────────────────────
    "provider_name": {"ar": "اسم الشركة", "en": "Provider Name"},
    "pilgrims_assigned": {"ar": "الحجاج المخصصين", "en": "Pilgrims Assigned"},
    "delivery_rate": {"ar": "نسبة التسليم", "en": "Delivery Rate"},
    "avg_delivery_days": {"ar": "متوسط أيام التسليم", "en": "Avg. Delivery Days"},
    "provider_performance": {"ar": "أداء مقدمي الخدمة", "en": "Provider Performance"},

    # ── Health & Safety ────────────────────────────────────────────────
    "health_timeline": {"ar": "الجدول الزمني للحالات الصحية", "en": "Health Incident Timeline"},
    "severity_distribution": {"ar": "توزيع الشدة", "en": "Severity Distribution"},
    "incidents_by_nationality": {"ar": "الحالات حسب الجنسية", "en": "Incidents by Nationality"},
    "incidents_by_age": {"ar": "الحالات حسب الفئة العمرية", "en": "Incidents by Age Group"},
    "at_risk": {"ar": "مجموعة المخاطر العالية", "en": "At-Risk Group"},
    "elderly_no_card": {"ar": "حجاج 65+ بدون بطاقة مفعلة", "en": "Pilgrims 65+ Without Activated Card"},
    "minor": {"ar": "بسيطة", "en": "Minor"},
    "moderate": {"ar": "متوسطة", "en": "Moderate"},
    "severe": {"ar": "شديدة", "en": "Severe"},
    "critical": {"ar": "حرجة", "en": "Critical"},
    "death_summary": {"ar": "ملخص الوفيات", "en": "Death Summary"},

    # ── Demographics ───────────────────────────────────────────────────
    "world_map": {"ar": "خريطة أصول الحجاج", "en": "Pilgrim Origins Map"},
    "age_pyramid": {"ar": "الهرم العمري", "en": "Age/Sex Pyramid"},
    "family_patterns": {"ar": "أنماط السفر العائلي", "en": "Family Travel Patterns"},
    "b2b_b2c_by_nationality": {"ar": "B2B/B2C حسب الجنسية", "en": "B2B vs B2C by Nationality"},
    "arrival_by_nationality": {"ar": "الوصول حسب الجنسية", "en": "Arrival by Nationality"},

    # ── Reports ────────────────────────────────────────────────────────
    "daily_status_report": {"ar": "تقرير الحالة اليومي", "en": "Daily Status Report"},
    "overdue_cards_report": {"ar": "تقرير البطاقات المتأخرة", "en": "Overdue Cards Report"},
    "provider_report": {"ar": "تقرير مقدمي الخدمة", "en": "Provider Performance Report"},
    "health_report": {"ar": "تقرير الحالات الصحية", "en": "Health Incidents Report"},
    "weekly_comparison": {"ar": "المقارنة الأسبوعية", "en": "Weekly Comparison"},
    "export_data": {"ar": "تصدير البيانات", "en": "Export Data"},
    "generate_report": {"ar": "إنشاء التقرير", "en": "Generate Report"},

    # ── General ────────────────────────────────────────────────────────
    "total": {"ar": "الإجمالي", "en": "Total"},
    "percentage": {"ar": "النسبة", "en": "Percentage"},
    "count": {"ar": "العدد", "en": "Count"},
    "date": {"ar": "التاريخ", "en": "Date"},
    "name": {"ar": "الاسم", "en": "Name"},
    "status": {"ar": "الحالة", "en": "Status"},
    "details": {"ar": "التفاصيل", "en": "Details"},
    "daily": {"ar": "يومي", "en": "Daily"},
    "cumulative": {"ar": "تراكمي", "en": "Cumulative"},
    "male": {"ar": "ذكر", "en": "Male"},
    "female": {"ar": "أنثى", "en": "Female"},
    "reload_time": {"ar": "وقت التحديث", "en": "Reload Time"},
    "yes": {"ar": "نعم", "en": "Yes"},
    "no": {"ar": "لا", "en": "No"},
    "page": {"ar": "صفحة", "en": "Page"},
    "next": {"ar": "التالي", "en": "Next"},
    "previous": {"ar": "السابق", "en": "Previous"},
}


def get_lang():
    """Get current language from session state."""
    import streamlit as st
    return st.session_state.get("lang", "ar")


def t(key):
    """Translate a key to the current language."""
    lang = get_lang()
    if key in LABELS:
        return LABELS[key].get(lang, LABELS[key].get("en", key))
    return key
