"""
Reusable Plotly chart builders for the Hajj Nusuk Dashboard.
All charts follow the Nusuk brown/gold/cream aesthetic.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils.i18n import t, get_lang

# ── Color Palette ──────────────────────────────────────────────────────────
NUSUK_COLORS = {
    "brown_dark": "#4A3728",
    "brown": "#5C4033",
    "brown_light": "#8B6914",
    "gold": "#B8860B",
    "gold_light": "#DAA520",
    "cream": "#FAF6F0",
    "cream_dark": "#F0E6D4",
    "green": "#2E7D32",
    "green_light": "#4CAF50",
    "yellow": "#F9A825",
    "red": "#C62828",
    "red_light": "#E53935",
    "blue": "#1565C0",
}

PIPELINE_COLORS = [
    "#5C4033", "#8B6914", "#B8860B", "#DAA520", "#E8C547", "#4CAF50", "#2E7D32"
]

SEVERITY_COLORS = {
    "minor": "#4CAF50",
    "moderate": "#F9A825",
    "severe": "#E53935",
    "critical": "#880E4F",
}


def _chart_layout(fig, title="", rtl=False):
    """Apply consistent layout to all charts."""
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=NUSUK_COLORS["brown_dark"])),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Segoe UI, Tahoma, sans-serif", color=NUSUK_COLORS["brown_dark"]),
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    if rtl:
        fig.update_layout(xaxis=dict(autorange="reversed" if rtl else True))
    return fig


def arrival_trend_chart(daily_arrivals, title=None):
    """Line chart showing daily and cumulative arrivals."""
    if daily_arrivals.empty:
        return go.Figure()

    df = pd.DataFrame({
        "date": daily_arrivals.index,
        "daily": daily_arrivals.values,
    })
    df["cumulative"] = df["daily"].cumsum()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df["date"], y=df["daily"],
        name=t("daily"),
        marker_color=NUSUK_COLORS["gold"],
        opacity=0.6,
    ))

    fig.add_trace(go.Scatter(
        x=df["date"], y=df["cumulative"],
        name=t("cumulative"),
        line=dict(color=NUSUK_COLORS["brown"], width=3),
        yaxis="y2",
    ))

    fig.update_layout(
        yaxis=dict(title=t("daily"), side="left"),
        yaxis2=dict(title=t("cumulative"), side="right", overlaying="y"),
        legend=dict(x=0.01, y=0.99),
        barmode="overlay",
    )

    return _chart_layout(fig, title or t("total_arrivals"))


def pipeline_funnel_chart(metrics, title=None):
    """Funnel chart showing card pipeline stages."""
    lang = get_lang()

    stages = [
        ("total_visas", metrics["total_visas"]),
        ("groups_formed", metrics["groups_formed"]),
        ("cards_printed", metrics["cards_printed"]),
        ("cards_at_center", metrics["cards_at_center"]),
        ("cards_at_provider", metrics["cards_at_provider"]),
        ("cards_received", metrics["cards_received"]),
        ("cards_activated", metrics["cards_activated"]),
    ]

    fig = go.Figure(go.Funnel(
        y=[t(s[0]) for s in stages],
        x=[s[1] for s in stages],
        textinfo="value+percent initial",
        marker=dict(color=PIPELINE_COLORS),
        connector=dict(line=dict(color=NUSUK_COLORS["cream_dark"], width=2)),
    ))

    return _chart_layout(fig, title or t("page_card_pipeline"))


def nationality_bar_chart(df, as_of_date, top_n=10, title=None):
    """Horizontal bar chart of top nationalities."""
    as_of = pd.Timestamp(as_of_date)
    visa_mask = df["visa_issue_date"] <= as_of
    filtered = df[visa_mask]

    nat_counts = filtered["nationality"].value_counts().head(top_n)

    fig = go.Figure(go.Bar(
        y=nat_counts.index,
        x=nat_counts.values,
        orientation="h",
        marker_color=NUSUK_COLORS["gold"],
        text=nat_counts.values,
        textposition="auto",
    ))

    fig.update_layout(yaxis=dict(autorange="reversed"))

    return _chart_layout(fig, title or t("arrival_by_nationality"))


def health_timeline_chart(daily_health, title=None):
    """Bar chart showing daily health incidents."""
    if daily_health.empty:
        return go.Figure()

    fig = go.Figure(go.Bar(
        x=daily_health.index,
        y=daily_health.values,
        marker_color=NUSUK_COLORS["red_light"],
        opacity=0.8,
    ))

    return _chart_layout(fig, title or t("health_timeline"))


def severity_pie_chart(df, as_of_date, title=None):
    """Pie chart of health severity distribution."""
    as_of = pd.Timestamp(as_of_date)
    health_mask = (
        (df["health_status"] != "none") &
        (df["health_date"] <= as_of)
    )
    health_df = df[health_mask]

    if health_df.empty:
        return go.Figure()

    counts = health_df["health_status"].value_counts()
    labels = [t(s) for s in counts.index]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=counts.values,
        marker=dict(colors=[SEVERITY_COLORS.get(s, "#999") for s in counts.index]),
        hole=0.4,
        textinfo="label+percent",
    ))

    return _chart_layout(fig, title or t("severity_distribution"))


def age_sex_pyramid(df, as_of_date, title=None):
    """Population pyramid by age and sex."""
    as_of = pd.Timestamp(as_of_date)
    visa_mask = df["visa_issue_date"] <= as_of
    filtered = df[visa_mask]

    if filtered.empty:
        return go.Figure()

    bins = list(range(15, 95, 5))
    labels = [f"{b}-{b+4}" for b in bins[:-1]]
    filtered = filtered.copy()
    filtered["age_group"] = pd.cut(filtered["age"], bins=bins, labels=labels, right=False)

    male = filtered[filtered["sex"] == "M"]["age_group"].value_counts().sort_index()
    female = filtered[filtered["sex"] == "F"]["age_group"].value_counts().sort_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=male.index, x=-male.values,
        name=t("male"), orientation="h",
        marker_color=NUSUK_COLORS["blue"],
    ))
    fig.add_trace(go.Bar(
        y=female.index, x=female.values,
        name=t("female"), orientation="h",
        marker_color=NUSUK_COLORS["red_light"],
    ))

    max_val = max(male.max(), female.max()) if not male.empty else 1000
    fig.update_layout(
        barmode="overlay",
        xaxis=dict(
            title=t("count"),
            tickvals=[-max_val, -max_val//2, 0, max_val//2, max_val],
            ticktext=[f"{max_val:,}", f"{max_val//2:,}", "0", f"{max_val//2:,}", f"{max_val:,}"],
        ),
        bargap=0.05,
    )

    return _chart_layout(fig, title or t("age_pyramid"))


def world_map_chart(df, as_of_date, title=None):
    """Choropleth map of pilgrim origins."""
    as_of = pd.Timestamp(as_of_date)
    ext_mask = (
        (df["person_type"] == "pilgrim_external") &
        (df["visa_issue_date"] <= as_of)
    )
    ext_df = df[ext_mask]

    if ext_df.empty:
        return go.Figure()

    # Country name to ISO-3 mapping (simplified)
    country_iso = {
        "Indonesia": "IDN", "Pakistan": "PAK", "India": "IND", "Bangladesh": "BGD",
        "Nigeria": "NGA", "Iran": "IRN", "Algeria": "DZA", "Turkey": "TUR",
        "Egypt": "EGY", "Sudan": "SDN", "Malaysia": "MYS", "Morocco": "MAR",
        "Iraq": "IRQ", "Yemen": "YEM", "Jordan": "JOR", "Syria": "SYR",
        "Tunisia": "TUN", "Libya": "LBY", "Somalia": "SOM", "Afghanistan": "AFG",
        "Uzbekistan": "UZB", "Senegal": "SEN", "Tanzania": "TZA", "Niger": "NER",
        "Mali": "MLI", "Ethiopia": "ETH", "Philippines": "PHL", "China": "CHN",
        "United Kingdom": "GBR", "France": "FRA", "USA": "USA", "Germany": "DEU",
        "Russia": "RUS", "Bosnia": "BIH", "Thailand": "THA", "Cameroon": "CMR",
        "Ghana": "GHA", "Guinea": "GIN", "Ivory Coast": "CIV", "Kenya": "KEN",
        "Sri Lanka": "LKA", "Myanmar": "MMR", "Tajikistan": "TJK",
        "Saudi Arabia": "SAU",
    }

    nat_counts = ext_df["nationality"].value_counts().reset_index()
    nat_counts.columns = ["country", "count"]
    nat_counts["iso"] = nat_counts["country"].map(country_iso)
    nat_counts = nat_counts.dropna(subset=["iso"])

    fig = px.choropleth(
        nat_counts,
        locations="iso",
        color="count",
        hover_name="country",
        color_continuous_scale=[
            NUSUK_COLORS["cream"], NUSUK_COLORS["gold"],
            NUSUK_COLORS["brown_light"], NUSUK_COLORS["brown"]
        ],
    )

    fig.update_geos(
        showcoastlines=True, coastlinecolor=NUSUK_COLORS["brown_dark"],
        showland=True, landcolor=NUSUK_COLORS["cream_dark"],
        showocean=True, oceancolor="#E8F4F8",
        projection_type="natural earth",
        center=dict(lat=25, lon=45),
    )

    fig.update_layout(height=500, margin=dict(l=0, r=0, t=50, b=0))

    return _chart_layout(fig, title or t("world_map"))


def provider_comparison_chart(provider_df, title=None):
    """Bar chart comparing provider performance."""
    if provider_df.empty:
        return go.Figure()

    top = provider_df.head(20)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=top["provider"], y=top["delivery_rate"],
        name=t("delivery_rate"),
        marker_color=[
            NUSUK_COLORS["green"] if r >= 80
            else NUSUK_COLORS["yellow"] if r >= 60
            else NUSUK_COLORS["red_light"]
            for r in top["delivery_rate"]
        ],
        text=[f"{r:.0f}%" for r in top["delivery_rate"]],
        textposition="auto",
    ))

    fig.update_layout(xaxis=dict(tickangle=45))

    return _chart_layout(fig, title or t("provider_performance"))


def b2b_b2c_nationality_chart(df, as_of_date, title=None):
    """Stacked bar chart of B2B/B2C by top nationalities."""
    as_of = pd.Timestamp(as_of_date)
    visa_mask = df["visa_issue_date"] <= as_of
    filtered = df[visa_mask]

    if filtered.empty:
        return go.Figure()

    top_nats = filtered["nationality"].value_counts().head(10).index
    subset = filtered[filtered["nationality"].isin(top_nats)]

    cross = pd.crosstab(subset["nationality"], subset["b2b_b2c"])
    cross = cross.loc[top_nats]

    fig = go.Figure()
    if "B2B" in cross.columns:
        fig.add_trace(go.Bar(
            x=cross.index, y=cross["B2B"],
            name="B2B", marker_color=NUSUK_COLORS["brown"],
        ))
    if "B2C" in cross.columns:
        fig.add_trace(go.Bar(
            x=cross.index, y=cross["B2C"],
            name="B2C", marker_color=NUSUK_COLORS["gold"],
        ))

    fig.update_layout(barmode="stack", xaxis=dict(tickangle=45))

    return _chart_layout(fig, title or t("b2b_b2c_by_nationality"))
