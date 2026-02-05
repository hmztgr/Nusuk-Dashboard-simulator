"""
Compute dashboard metrics as of a given date.
All pipeline metrics are calculated by filtering date columns <= as_of_date.
"""

import pandas as pd
import numpy as np
from datetime import datetime


def compute_metrics(df, as_of_date, person_type_filter=None, nationality_filter=None, provider_filter=None):
    """
    Compute all dashboard metrics as of a specific date.

    Parameters:
        df: Full DataFrame
        as_of_date: datetime - metrics computed as of this date
        person_type_filter: list or None - filter by person types
        nationality_filter: list or None - filter by nationalities
        provider_filter: list or None - filter by service providers

    Returns:
        dict with all computed metrics
    """
    # Apply filters
    filtered = df.copy()

    if person_type_filter and len(person_type_filter) > 0:
        filtered = filtered[filtered["person_type"].isin(person_type_filter)]

    if nationality_filter and len(nationality_filter) > 0:
        filtered = filtered[filtered["nationality"].isin(nationality_filter)]

    if provider_filter and len(provider_filter) > 0:
        filtered = filtered[filtered["service_provider"].isin(provider_filter)]

    n = len(filtered)
    if n == 0:
        return _empty_metrics()

    # Convert date for comparison
    as_of = pd.Timestamp(as_of_date)

    # ── Visa / Permits ─────────────────────────────────────────────────
    visa_mask = pd.to_datetime(filtered["visa_issue_date"], errors="coerce") <= as_of
    total_visas = visa_mask.sum()

    # ── Groups Formed ──────────────────────────────────────────────────
    group_mask = pd.to_datetime(filtered["group_formation_date"], errors="coerce") <= as_of
    groups_formed = group_mask.sum()

    # ── Arrivals ───────────────────────────────────────────────────────
    arrival_mask = pd.to_datetime(filtered["arrival_date"], errors="coerce") <= as_of
    total_arrivals = arrival_mask.sum()
    arrival_pct = total_arrivals / max(total_visas, 1) * 100

    # ── Card Pipeline ──────────────────────────────────────────────────
    printed_mask = pd.to_datetime(filtered["card_printed_date"], errors="coerce") <= as_of
    cards_printed = printed_mask.sum()

    center_mask = pd.to_datetime(filtered["card_at_center_date"], errors="coerce") <= as_of
    cards_at_center = center_mask.sum()

    provider_mask = pd.to_datetime(filtered["card_at_provider_date"], errors="coerce") <= as_of
    cards_at_provider = provider_mask.sum()

    received_mask = pd.to_datetime(filtered["card_received_date"], errors="coerce") <= as_of
    cards_received = received_mask.sum()

    activated_mask = pd.to_datetime(filtered["card_activation_date"], errors="coerce") <= as_of
    cards_activated = activated_mask.sum()

    proof_mask = pd.to_datetime(filtered["proof_picture_date"], errors="coerce") <= as_of
    proof_pictures = proof_mask.sum()

    # Cards at provider but NOT delivered to pilgrims
    cards_not_delivered = cards_at_provider - cards_received

    # ── Percentages (each as % of previous stage) ─────────────────────
    formation_pct = groups_formed / max(total_visas, 1) * 100
    printed_pct = cards_printed / max(total_visas, 1) * 100
    center_pct = cards_at_center / max(cards_printed, 1) * 100
    provider_pct = cards_at_provider / max(cards_at_center, 1) * 100
    received_pct = cards_received / max(cards_at_provider, 1) * 100
    activated_pct = cards_activated / max(cards_received, 1) * 100

    # ── Health ─────────────────────────────────────────────────────────
    health_mask = (
        (filtered["health_status"] != "none") &
        (pd.to_datetime(filtered["health_date"], errors="coerce") <= as_of)
    )
    health_incidents = health_mask.sum()

    death_mask = (
        (filtered["death_status"] == True) &
        (pd.to_datetime(filtered["death_date"], errors="coerce") <= as_of)
    )
    deaths = death_mask.sum()

    # ── Daily arrivals for chart ───────────────────────────────────────
    arrival_dates = pd.to_datetime(filtered.loc[arrival_mask, "arrival_date"], errors="coerce")
    daily_arrivals = arrival_dates.dt.date.value_counts().sort_index()

    # ── Daily health incidents ─────────────────────────────────────────
    health_dates = pd.to_datetime(filtered.loc[health_mask, "health_date"], errors="coerce")
    daily_health = health_dates.dt.date.value_counts().sort_index()

    return {
        "total_records": n,
        "total_visas": int(total_visas),
        "groups_formed": int(groups_formed),
        "total_arrivals": int(total_arrivals),
        "arrival_pct": round(arrival_pct, 2),
        "cards_printed": int(cards_printed),
        "cards_at_center": int(cards_at_center),
        "cards_at_provider": int(cards_at_provider),
        "cards_received": int(cards_received),
        "cards_activated": int(cards_activated),
        "proof_pictures": int(proof_pictures),
        "cards_not_delivered": int(cards_not_delivered),
        "formation_pct": round(formation_pct, 2),
        "printed_pct": round(printed_pct, 2),
        "center_pct": round(center_pct, 2),
        "provider_pct": round(provider_pct, 2),
        "received_pct": round(received_pct, 2),
        "activated_pct": round(activated_pct, 2),
        "health_incidents": int(health_incidents),
        "deaths": int(deaths),
        "daily_arrivals": daily_arrivals,
        "daily_health": daily_health,
    }


def compute_metrics_by_type(df, as_of_date):
    """Compute pipeline metrics broken down by person type."""
    results = {}
    for ptype in ["pilgrim_external", "pilgrim_internal", "service_worker", "government", "healthcare"]:
        results[ptype] = compute_metrics(df, as_of_date, person_type_filter=[ptype])
    return results


def compute_provider_metrics(df, as_of_date):
    """Compute metrics per service provider."""
    as_of = pd.Timestamp(as_of_date)
    providers = df["service_provider"].dropna().unique()
    rows = []

    for provider in providers:
        if provider == "Government":
            continue
        prov_df = df[df["service_provider"] == provider]
        n = len(prov_df)
        if n == 0:
            continue

        at_provider = (pd.to_datetime(prov_df["card_at_provider_date"], errors="coerce") <= as_of).sum()
        received = (pd.to_datetime(prov_df["card_received_date"], errors="coerce") <= as_of).sum()
        activated = (pd.to_datetime(prov_df["card_activation_date"], errors="coerce") <= as_of).sum()

        delivery_rate = received / max(at_provider, 1) * 100

        # Avg delivery days (provider_date to received_date)
        valid_mask = prov_df["card_received_date"].notna() & prov_df["card_at_provider_date"].notna()
        if valid_mask.sum() > 0:
            prov_dates = pd.to_datetime(prov_df.loc[valid_mask, "card_at_provider_date"])
            recv_dates = pd.to_datetime(prov_df.loc[valid_mask, "card_received_date"])
            avg_days = (recv_dates - prov_dates).dt.days.mean()
        else:
            avg_days = 0

        health_count = (
            (prov_df["health_status"] != "none") &
            (pd.to_datetime(prov_df["health_date"], errors="coerce") <= as_of)
        ).sum()

        rows.append({
            "provider": provider,
            "pilgrims_assigned": n,
            "cards_at_provider": int(at_provider),
            "cards_received": int(received),
            "cards_activated": int(activated),
            "delivery_rate": round(delivery_rate, 1),
            "avg_delivery_days": round(avg_days, 1),
            "health_incidents": int(health_count),
        })

    return pd.DataFrame(rows).sort_values("pilgrims_assigned", ascending=False)


def _empty_metrics():
    """Return empty metrics dict."""
    return {
        "total_records": 0,
        "total_visas": 0, "groups_formed": 0,
        "total_arrivals": 0, "arrival_pct": 0,
        "cards_printed": 0, "cards_at_center": 0,
        "cards_at_provider": 0, "cards_received": 0,
        "cards_activated": 0, "proof_pictures": 0,
        "cards_not_delivered": 0,
        "formation_pct": 0, "printed_pct": 0,
        "center_pct": 0, "provider_pct": 0,
        "received_pct": 0, "activated_pct": 0,
        "health_incidents": 0, "deaths": 0,
        "daily_arrivals": pd.Series(dtype="int64"),
        "daily_health": pd.Series(dtype="int64"),
    }
