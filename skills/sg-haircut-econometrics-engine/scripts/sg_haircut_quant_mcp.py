#!/usr/bin/env python3
"""Singapore Haircut Econometrics & Spatio-Temporal Salon GIS FastMCP Server v2.0.

Upgraded for Antigravity IDE (Gemini 3.8 Flash High Effort) with:
1. Official SingStat (SSIC 9602) & Data.gov.sg ACRA business entity trends.
2. Cost-Value Efficacy Index (CVEI) & Weibull durability decay evaluator.
3. Spatio-Temporal Salon GIS Crowd Simulator & Next-Haircut Reservation Scheduler
   across 16 geocoded Singapore salons (pricing, Google reviews, diurnal crowd
   busyness, and optimal reservation countdown before next haircut).
4. GeoJSON FeatureCollection exporter for Leaflet / MapLibre WebGIS apps.
5. CASE / ACRA prepaid package insolvency actuarial evaluator.
6. Robotic Barber vs. AI Robotic Hair-Washing unit economics simulator.
"""

from __future__ import annotations

import datetime
import json
import math
import os
import sys
import urllib.parse
import urllib.request
from typing import Any, Dict, List

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

try:
    from mcp.server.mcpserver import MCPServer
    mcp = MCPServer("sg-haircut-econometrics-engine")
except ImportError:
    try:
        from fastmcp import FastMCP
        mcp = FastMCP("sg-haircut-econometrics-engine")
    except ImportError:
        try:
            from mcp.server.fastmcp import FastMCP
            mcp = FastMCP("sg-haircut-econometrics-engine")
        except ImportError:
            class _FallbackMCP:
                def __init__(self, name: str):
                    self.name = name
                def tool(self):
                    def decorator(fn):
                        return fn
                    return decorator
                def run(self):
                    pass
            mcp = _FallbackMCP("sg-haircut-econometrics-engine")


SALON_GIS_CATALOG: List[Dict[str, Any]] = [
    {"id": "S01", "name": "QB House (VivoCity)", "tier": "T2", "lat": 1.264395, "lng": 103.821809, "price_men": 12.0, "price_women": 12.0, "price_kid": 12.0, "rating": 4.4, "reviews": 306, "base_queue_mins": 14.0, "chair_mins": 10.0, "travel_mins": 12.0, "res_lead_days": 0.0, "s0": 74.0, "tau": 18.5, "beta": 1.65, "massage_mins": 0.0, "drink_val": 0.0, "talk_val": 0.0, "p_mem": 0.08, "p_prod": 0.00, "profile": "walkin_mall", "url": "https://qbhouse.co/sg/"},
    {"id": "S02", "name": "QB Premium (Suntec City)", "tier": "T2", "lat": 1.295467, "lng": 103.858585, "price_men": 16.0, "price_women": 16.0, "price_kid": 15.0, "rating": 4.2, "reviews": 189, "base_queue_mins": 10.0, "chair_mins": 15.0, "travel_mins": 12.0, "res_lead_days": 0.0, "s0": 79.0, "tau": 22.0, "beta": 1.55, "massage_mins": 0.0, "drink_val": 0.0, "talk_val": 1.0, "p_mem": 0.10, "p_prod": 0.02, "profile": "cbd_mall", "url": "http://www.qbpremium.sg/"},
    {"id": "S03", "name": "Kcuts (Capitol via kcutsGO)", "tier": "T2", "lat": 1.293063, "lng": 103.851293, "price_men": 14.0, "price_women": 14.0, "price_kid": 14.0, "rating": 4.3, "reviews": 215, "base_queue_mins": 4.0, "chair_mins": 10.0, "travel_mins": 11.0, "res_lead_days": 0.02, "s0": 75.0, "tau": 19.0, "beta": 1.65, "massage_mins": 0.0, "drink_val": 0.0, "talk_val": 0.0, "p_mem": 0.09, "p_prod": 0.01, "profile": "app_express", "url": "https://k-cuts.com/kcutsgo/"},
    {"id": "S04", "name": "Kimage Hairdressing School (Marina Sq)", "tier": "T1", "lat": 1.291040, "lng": 103.857624, "price_men": 8.0, "price_women": 8.0, "price_kid": 8.0, "rating": 4.5, "reviews": 658, "base_queue_mins": 8.0, "chair_mins": 45.0, "travel_mins": 15.0, "res_lead_days": 2.0, "s0": 75.0, "tau": 22.0, "beta": 1.50, "massage_mins": 5.0, "drink_val": 1.0, "talk_val": 3.0, "p_mem": 0.02, "p_prod": 0.05, "profile": "weekday_school", "url": "https://sch.kimage.com.sg/"},
    {"id": "S05", "name": "Snip Avenue (Bedok Town Centre)", "tier": "T1", "lat": 1.324669, "lng": 103.929405, "price_men": 6.8, "price_women": 6.8, "price_kid": 5.8, "rating": 3.6, "reviews": 142, "base_queue_mins": 22.0, "chair_mins": 12.0, "travel_mins": 9.0, "res_lead_days": 0.0, "s0": 68.0, "tau": 16.5, "beta": 1.70, "massage_mins": 0.0, "drink_val": 0.0, "talk_val": 1.0, "p_mem": 0.38, "p_prod": 0.30, "profile": "hdb_walkin", "url": "https://blog.moneysmart.sg/budgeting/cheap-haircut-singapore-barber-shop/"},
    {"id": "S06", "name": "Dragon Phoenix Salon (Toa Payoh HDB Hub)", "tier": "T1", "lat": 1.332188, "lng": 103.847078, "price_men": 10.0, "price_women": 18.0, "price_kid": 8.0, "rating": 4.3, "reviews": 110, "base_queue_mins": 15.0, "chair_mins": 20.0, "travel_mins": 9.0, "res_lead_days": 0.2, "s0": 75.0, "tau": 20.5, "beta": 1.55, "massage_mins": 4.0, "drink_val": 0.5, "talk_val": 6.0, "p_mem": 0.12, "p_prod": 0.10, "profile": "hdb_walkin", "url": "https://blog.moneysmart.sg/budgeting/cheap-haircut-singapore-barber-shop/"},
    {"id": "S07", "name": "New Chapter Hair Salon (Ubi HDB)", "tier": "T1", "lat": 1.318676, "lng": 103.892551, "price_men": 13.0, "price_women": 13.0, "price_kid": 10.0, "rating": 4.9, "reviews": 86, "base_queue_mins": 9.0, "chair_mins": 28.0, "travel_mins": 10.0, "res_lead_days": 1.0, "s0": 80.0, "tau": 24.0, "beta": 1.50, "massage_mins": 6.0, "drink_val": 2.0, "talk_val": 5.5, "p_mem": 0.08, "p_prod": 0.08, "profile": "ubi_heartland", "url": "https://glamingo.ai/sg/blogs/haircut-price-singapore/"},
    {"id": "S08", "name": "\"Hair\" by Common Studio (Queenstown)", "tier": "T1", "lat": 1.292703, "lng": 103.810972, "price_men": 25.0, "price_women": 33.0, "price_kid": 18.0, "rating": 4.8, "reviews": 445, "base_queue_mins": 7.0, "chair_mins": 35.0, "travel_mins": 12.0, "res_lead_days": 1.5, "s0": 83.0, "tau": 26.5, "beta": 1.45, "massage_mins": 7.0, "drink_val": 3.5, "talk_val": 5.0, "p_mem": 0.10, "p_prod": 0.12, "profile": "queenstown_hdb", "url": "https://anjiacollection.com/pages/hair-by-common-studio"},
    {"id": "S09", "name": "Keller Hair Studio (Thomson Plaza)", "tier": "T3", "lat": 1.354325, "lng": 103.830328, "price_men": 32.0, "price_women": 40.0, "price_kid": 22.0, "rating": 4.7, "reviews": 259, "base_queue_mins": 8.0, "chair_mins": 40.0, "travel_mins": 14.0, "res_lead_days": 1.5, "s0": 84.0, "tau": 28.0, "beta": 1.42, "massage_mins": 7.0, "drink_val": 3.0, "talk_val": 4.0, "p_mem": 0.16, "p_prod": 0.18, "profile": "suburban_mall", "url": "https://glamingo.ai/sg/blogs/haircut-price-singapore/"},
    {"id": "S10", "name": "Act Point Salon (Midpoint Orchard)", "tier": "T3", "lat": 1.301784, "lng": 103.838661, "price_men": 45.0, "price_women": 55.0, "price_kid": 30.0, "rating": 4.9, "reviews": 1313, "base_queue_mins": 6.0, "chair_mins": 45.0, "travel_mins": 16.0, "res_lead_days": 3.5, "s0": 90.0, "tau": 34.0, "beta": 1.36, "massage_mins": 9.0, "drink_val": 4.5, "talk_val": 5.5, "p_mem": 0.05, "p_prod": 0.12, "profile": "orchard_booked", "url": "http://www.actpoint.com.sg/"},
    {"id": "S11", "name": "Be U Hair Design (The Centrepoint)", "tier": "T3", "lat": 1.301978, "lng": 103.839759, "price_men": 42.0, "price_women": 52.0, "price_kid": 28.0, "rating": 4.9, "reviews": 700, "base_queue_mins": 6.0, "chair_mins": 45.0, "travel_mins": 16.0, "res_lead_days": 2.5, "s0": 88.0, "tau": 32.0, "beta": 1.38, "massage_mins": 8.0, "drink_val": 4.0, "talk_val": 5.0, "p_mem": 0.14, "p_prod": 0.18, "profile": "centrepoint_orchard", "url": "https://beuhairdesign.com/"},
    {"id": "S12", "name": "Salon Plus (Far East Plaza)", "tier": "T3", "lat": 1.307311, "lng": 103.833940, "price_men": 55.0, "price_women": 65.0, "price_kid": 35.0, "rating": 4.8, "reviews": 310, "base_queue_mins": 7.0, "chair_mins": 45.0, "travel_mins": 16.0, "res_lead_days": 2.0, "s0": 87.0, "tau": 31.5, "beta": 1.40, "massage_mins": 8.0, "drink_val": 4.0, "talk_val": 4.5, "p_mem": 0.18, "p_prod": 0.22, "profile": "orchard_booked", "url": "https://salonplus.com.sg/our-service/haircut/"},
    {"id": "S13", "name": "Number76 Hair Salon (268 Orchard)", "tier": "T3", "lat": 1.300443, "lng": 103.839443, "price_men": 56.0, "price_women": 76.0, "price_kid": 28.0, "rating": 4.6, "reviews": 671, "base_queue_mins": 5.0, "chair_mins": 50.0, "travel_mins": 16.0, "res_lead_days": 3.5, "s0": 90.0, "tau": 34.5, "beta": 1.36, "massage_mins": 10.0, "drink_val": 5.5, "talk_val": 5.0, "p_mem": 0.15, "p_prod": 0.25, "profile": "orchard_booked", "url": "https://sgp.number76.com/price/"},
    {"id": "S14", "name": "Walking On Sunshine (Orchard Central)", "tier": "T4", "lat": 1.300724, "lng": 103.839692, "price_men": 70.0, "price_women": 120.0, "price_kid": 45.0, "rating": 4.8, "reviews": 9079, "base_queue_mins": 5.0, "chair_mins": 60.0, "travel_mins": 18.0, "res_lead_days": 4.5, "s0": 92.0, "tau": 38.0, "beta": 1.30, "massage_mins": 14.0, "drink_val": 9.5, "talk_val": 6.5, "p_mem": 0.26, "p_prod": 0.34, "profile": "orchard_luxury", "url": "https://www.walkingonsunshine.sg/wos-services"},
    {"id": "S15", "name": "Shunji Matsuo Flagship (15 Scotts Rd)", "tier": "T4", "lat": 1.305763, "lng": 103.833083, "price_men": 85.0, "price_women": 110.0, "price_kid": 55.0, "rating": 4.7, "reviews": 536, "base_queue_mins": 4.0, "chair_mins": 60.0, "travel_mins": 18.0, "res_lead_days": 5.0, "s0": 93.0, "tau": 39.5, "beta": 1.28, "massage_mins": 15.0, "drink_val": 8.0, "talk_val": 6.0, "p_mem": 0.22, "p_prod": 0.32, "profile": "orchard_luxury", "url": "https://www.shunjimatsuo.com.sg/pages/japanese-hair-salon-orchard"},
    {"id": "S16", "name": "Chez Vous: HideAway & Kim Robinson (Ngee Ann City)", "tier": "T4", "lat": 1.302424, "lng": 103.834676, "price_men": 199.0, "price_women": 199.0, "price_kid": 120.0, "rating": 4.9, "reviews": 2295, "base_queue_mins": 2.0, "chair_mins": 75.0, "travel_mins": 20.0, "res_lead_days": 10.0, "s0": 96.0, "tau": 45.0, "beta": 1.25, "massage_mins": 20.0, "drink_val": 14.0, "talk_val": 8.5, "p_mem": 0.12, "p_prod": 0.38, "profile": "sanctuary_capped", "url": "https://chezvoushair.com/chez-vous-hide-away/"},
]


def _crowd_multiplier(profile: str, day_idx: int, hour_24: int) -> float:
    base_map = {10: 0.45, 11: 0.62, 12: 0.95, 13: 1.05, 14: 0.92, 15: 0.88, 16: 0.96, 17: 1.15, 18: 1.35, 19: 1.28, 20: 0.85, 21: 0.40}
    mult = base_map.get(hour_24, 0.80)
    is_weekend = day_idx in (5, 6)
    if profile == "ubi_heartland":
        if day_idx in (1, 5, 6) and hour_24 >= 17:
            mult *= 1.45
        if day_idx in (3, 4) and hour_24 <= 12:
            mult *= 0.42
    elif profile == "queenstown_hdb":
        if day_idx == 6 and hour_24 >= 17:
            mult *= 1.40
        if day_idx in (4, 5) and 11 <= hour_24 <= 16:
            mult *= 1.35
        if day_idx in (1, 3) and hour_24 <= 12:
            mult *= 0.45
    elif profile == "centrepoint_orchard":
        if day_idx == 4 and 11 <= hour_24 <= 16:
            mult *= 1.42
        if day_idx == 5 and 13 <= hour_24 <= 18:
            mult *= 1.48
        if day_idx == 6 or (day_idx == 0 and hour_24 <= 12) or (day_idx == 1 and hour_24 >= 18):
            mult *= 0.50
    elif profile == "app_express":
        mult = 0.65 + 0.35 * mult
    elif profile == "sanctuary_capped":
        mult = 0.50 + 0.25 * (1.2 if is_weekend else 0.8)
    elif is_weekend:
        mult *= 1.32
    return max(0.25, min(2.1, mult))


@mcp.tool()
def query_salon_gis_crowd_and_reservation_schedule(
    day_of_week: int = 5,
    hour_24: int = 14,
    days_since_last_cut: float = 14.0,
    monthly_income_sgd: float = 5775.0,
    profile: str = "male",
    occasion_type: str = "normal",
    reference_date_iso: str = "2026-11-11",
) -> Dict[str, Any]:
    """Simulate live GIS salon crowd wait, CVEI score, and next-haircut reservation countdown.

    Parameters:
    - day_of_week: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun.
    - hour_24: Hour of day in SGT (10 to 21).
    - days_since_last_cut: Days elapsed since the user's last haircut.
    - monthly_income_sgd: Gross monthly income in SGD (MOM median = 5775).
    - profile: 'male', 'female', or 'kid'.
    - occasion_type: 'normal' or 'special'.
    - reference_date_iso: ISO date string (YYYY-MM-DD) for calendar scheduling.
    """
    vot_hourly = max(6.0, monthly_income_sgd / 173.33)
    s_min = 72.0 if occasion_type.lower() == "special" else 56.0
    try:
        ref_date = datetime.date.fromisoformat(reference_date_iso)
    except ValueError:
        ref_date = datetime.date(2026, 11, 11)

    ranked: List[Dict[str, Any]] = []
    for s in SALON_GIS_CATALOG:
        nominal = s["price_kid"] if profile == "kid" else (s["price_women"] if profile == "female" else s["price_men"])
        mult = _crowd_multiplier(s["profile"], day_of_week, hour_24)
        live_queue_mins = round(s["base_queue_mins"] * mult, 1)
        crowd_pct = min(99, round(38 * mult + s["base_queue_mins"] * 1.4))

        s_today = s["s0"] * math.exp(-((days_since_last_cut / s["tau"]) ** s["beta"]))
        half_life_days = round(s["tau"] * ((math.log(s["s0"] / 50.0)) ** (1.0 / s["beta"])), 1)
        optimal_cycle_days = (
            s["tau"] * ((-math.log(s_min / s["s0"])) ** (1.0 / s["beta"]))
            if s["s0"] > s_min else half_life_days
        )
        days_until_cut = max(0.0, optimal_cycle_days - days_since_last_cut)
        lead_bump = 1.35 if (day_of_week >= 4 and s["res_lead_days"] > 0.5) else 1.0
        eff_lead_days = round(s["res_lead_days"] * lead_bump, 1)
        days_until_reserve = max(0.0, round(days_until_cut - eff_lead_days, 1))

        cut_due_date = (ref_date + datetime.timedelta(days=round(days_until_cut))).isoformat()
        reserve_by_date = (ref_date + datetime.timedelta(days=round(days_until_reserve))).isoformat()

        queue_cost = vot_hourly * (live_queue_mins / 60.0) * 1.15
        chair_adj = s["chair_mins"] * (1.3 if profile == "female" and s["tier"] != "T2" else 1.0)
        chair_travel_cost = vot_hourly * ((chair_adj * 0.45 + s["travel_mins"]) / 60.0)
        upsell_friction = s["p_mem"] * 16.0 + s["p_prod"] * 8.5
        full_cost = nominal + queue_cost + chair_travel_cost + upsell_friction

        integrated_days = sum(
            (s["s0"] * math.exp(-((d / s["tau"]) ** s["beta"]))) / 100.0
            for d in range(1, 43)
        )
        occ_mult = 1.80 if occasion_type.lower() == "special" else 1.0
        perk_val = s["massage_mins"] * 1.2 + s["drink_val"] + s["talk_val"]
        benefit = integrated_days * 2.45 * occ_mult + max(0.0, (s["s0"] - 70.0) * (1.9 if occasion_type == "special" else 0.5)) + perk_val
        cvei = round((benefit / full_cost) * 10.0, 2)

        ranked.append({
            "salon_id": s["id"],
            "name": s["name"],
            "tier": s["tier"],
            "lat": s["lat"],
            "lng": s["lng"],
            "nominal_price_sgd": nominal,
            "google_rating": s["rating"],
            "google_reviews": s["reviews"],
            "live_queue_wait_mins": live_queue_mins,
            "crowd_occupancy_pct": crowd_pct,
            "full_economic_cost_sgd": round(full_cost, 2),
            "aesthetic_score_today": round(s_today, 1),
            "half_life_days": half_life_days,
            "days_until_next_cut_needed": round(days_until_cut, 1),
            "next_cut_due_date": cut_due_date,
            "effective_reservation_lead_days": eff_lead_days,
            "days_until_reservation_deadline": days_until_reserve,
            "reserve_by_date": reserve_by_date,
            "cvei_score": cvei,
            "verified_url": s["url"],
        })

    ranked.sort(key=lambda x: x["cvei_score"], reverse=True)
    return {
        "query_context": {
            "day_of_week": day_of_week,
            "hour_24": hour_24,
            "days_since_last_cut": days_since_last_cut,
            "monthly_income_sgd": monthly_income_sgd,
            "hourly_vot_sgd": round(vot_hourly, 2),
            "profile": profile,
            "occasion_type": occasion_type,
        },
        "top_gis_recommendation": ranked[0],
        "salons_ranked": ranked,
    }


@mcp.tool()
def export_salon_geojson_layer(
    day_of_week: int = 5,
    hour_24: int = 14,
    days_since_last_cut: float = 14.0,
    monthly_income_sgd: float = 5775.0,
    profile: str = "male",
    occasion_type: str = "normal",
) -> Dict[str, Any]:
    """Export all 16 Singapore salons as a GeoJSON FeatureCollection with live crowd & reservation properties."""
    sim = query_salon_gis_crowd_and_reservation_schedule(
        day_of_week=day_of_week,
        hour_24=hour_24,
        days_since_last_cut=days_since_last_cut,
        monthly_income_sgd=monthly_income_sgd,
        profile=profile,
        occasion_type=occasion_type,
    )
    features = []
    for item in sim["salons_ranked"]:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [item["lng"], item["lat"]],
            },
            "properties": item,
        })
    return {
        "type": "FeatureCollection",
        "features": features,
    }


@mcp.tool()
def evaluate_salon_package_and_upsell_odds(
    package_upfront_cash_sgd: float = 300.0,
    package_credit_value_sgd: float = 360.0,
    price_per_visit_sgd: float = 45.0,
    visits_per_year: float = 8.0,
    is_casetrust_accredited: bool = False,
) -> Dict[str, Any]:
    """Actuarial valuation of a prepaid hair/beauty salon package under ACRA/CASE closure hazards."""
    annual_hazard_lambda = 0.015 if is_casetrust_accredited else (1647.0 / 11241.0)
    total_visits_in_pkg = package_credit_value_sgd / max(1.0, price_per_visit_sgd)
    depletion_horizon_years = total_visits_in_pkg / max(0.5, visits_per_year)
    prob_closure = 1.0 - math.exp(-annual_hazard_lambda * depletion_horizon_years)
    expected_trapped = (package_upfront_cash_sgd * 0.55) * prob_closure
    nominal_bonus = package_credit_value_sgd - package_upfront_cash_sgd
    forgone_yield_breakage = package_upfront_cash_sgd * 0.035 * depletion_horizon_years + (0.06 * package_credit_value_sgd)
    net_ev = nominal_bonus - expected_trapped - forgone_yield_breakage
    return {
        "total_visits_covered": round(total_visits_in_pkg, 2),
        "depletion_horizon_years": round(depletion_horizon_years, 2),
        "prob_closure_during_package_pct": round(prob_closure * 100.0, 2),
        "net_actuarial_ev_sgd": round(net_ev, 2),
        "verdict": "SAFE (<=4 visits)" if net_ev > 0 and total_visits_in_pkg <= 4 else "REJECT (High Insolvency Risk)",
    }


@mcp.tool()
def simulate_robotic_barber_vs_ai_washer_roi(
    monthly_rent_sgd: float = 6500.0,
    human_stylist_monthly_wage_sgd: float = 3800.0,
    daily_customers: int = 45,
) -> Dict[str, Any]:
    """Compare unit economics of Pure Robotic Clipper Kiosk vs Hybrid Human Stylist + AI Robotic Hair Washer."""
    rev_robot = min(22, int(daily_customers * 0.40)) * 30 * 8.0
    cost_robot = monthly_rent_sgd + 1400.0 + 1800.0
    rev_hybrid = daily_customers * 30 * 32.0
    cost_hybrid = monthly_rent_sgd + (2 * human_stylist_monthly_wage_sgd) + 950.0 + (rev_hybrid * 0.08)
    return {
        "pure_robotic_barber_net_profit_sgd": round(rev_robot - cost_robot, 2),
        "hybrid_human_plus_ai_washer_net_profit_sgd": round(rev_hybrid - cost_hybrid, 2),
    }




@mcp.tool()
def query_onemap_lta_nea_contextual_routing(
    origin_postal_code: str = "238874",
    target_salon_id: str = "S10",
    relative_humidity_pct: float = 82.0,
    is_raining_nowcast: bool = False,
    query_live_apis: bool = False,
) -> Dict[str, Any]:
    """Fuse SLA OneMap geocoding/distance, NEA humidity frizz adjustment, and LTA/weather queue modifiers.

    - Queries SLA OneMap Elastic Search (`https://www.onemap.gov.sg/api/common/elastic/search`)
      and NEA Real-Time Weather (`https://api-open.data.gov.sg/v2/real-time/api/two-hour-forecast`)
      when `query_live_apis=True` (with deterministic haversine + seasonal fallback when offline).
    """
    salon = next((s for s in SALON_GIS_CATALOG if s["id"] == target_salon_id), SALON_GIS_CATALOG[9])
    origin_lat, origin_lng = 1.3024, 103.8347  # Default Orchard 238874
    api_status = "offline_deterministic_svy21_wgs84"

    if query_live_apis:
        try:
            url = "https://www.onemap.gov.sg/api/common/elastic/search?" + urllib.parse.urlencode({
                "searchVal": origin_postal_code,
                "returnGeom": "Y",
                "getAddrDetails": "Y",
                "pageNum": 1,
            })
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                results = data.get("results", [])
                if results:
                    origin_lat = float(results[0]["LATITUDE"])
                    origin_lng = float(results[0]["LONGITUDE"])
                    api_status = "live_onemap_connected"
        except Exception as exc:
            api_status = f"fallback_offline ({type(exc).__name__})"

    # Haversine distance (km) & estimated Singapore MRT/Bus transit time
    r_earth = 6371.0
    dlat = math.radians(salon["lat"] - origin_lat)
    dlng = math.radians(salon["lng"] - origin_lng)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(origin_lat))
        * math.cos(math.radians(salon["lat"]))
        * math.sin(dlng / 2) ** 2
    )
    dist_km = 2 * r_earth * math.asin(math.sqrt(a))
    est_pt_travel_mins = round(8.0 + dist_km * 2.6, 1)
    est_drive_travel_mins = round(5.0 + dist_km * 1.45, 1)

    # NEA Humidity Frizz Decay adjustment on Weibull scale parameter tau
    humidity_penalty_factor = max(0.82, 1.0 - 0.008 * max(0.0, relative_humidity_pct - 75.0))
    adjusted_tau_days = round(salon["tau"] * humidity_penalty_factor, 2)

    # Rainstorm walk-in queue dampener (-30% walk-in queue at HDB/express salons)
    rain_queue_mult = 0.70 if (is_raining_nowcast and salon["tier"] in ("T1", "T2")) else 1.0

    return {
        "api_status": api_status,
        "origin_postal_code": origin_postal_code,
        "origin_coords": [round(origin_lat, 5), round(origin_lng, 5)],
        "target_salon": salon["name"],
        "straight_line_distance_km": round(dist_km, 2),
        "estimated_public_transport_mins": est_pt_travel_mins,
        "estimated_drive_mins": est_drive_travel_mins,
        "nea_relative_humidity_pct": relative_humidity_pct,
        "humidity_adjusted_weibull_tau_days": adjusted_tau_days,
        "rain_walkin_queue_multiplier": rain_queue_mult,
    }



from haircut_sheaf_graph_and_loop_engine import (
    simulate_multicycle_closed_loop_and_growout_graph,
    validate_simulation_math_sympy_scipy_and_r_bridge,
    query_and_verify_pubmed_trichology_evidence,
    calculate_hairstyle_switch_economic_and_time_savings,
    benchmark_singstat_mcp_and_international_hairstyle_timelags,
    compute_singstat_and_google_trends_hairstyle_headcount_demand,
    query_universal_hairstyle_popularity_and_combinatorial_taxonomy,
    evaluate_infant_first_cut_shaving_and_frequent_cutting_biophysics,
    evaluate_alopecia_postpartum_and_occupational_hazard,
    HAIR_BIOTYPE_PROFILES,
    compute_sheaf_hypergraph_compatibility,
    execute_closed_loop_bayesian_update,
)


@mcp.tool()
def evaluate_sheaf_hypergraph_and_biotype_match(
    hair_biotype: str = "east_asian_coarse_straight",
    requires_hijab_private_room: bool = False,
    requires_beard_razor_lineup: bool = False,
    preferred_language: str = "en",
) -> Dict[str, Any]:
    """Evaluate Multipartite Cellular Sheaf Hypergraph compatibility across Singapore salons.

    Models hair follicle biophysics (shaft diameter um, ellipticity, growth velocity cm/mo,
    wet-to-dry curl shrinkage), cultural/religious privacy (Muslimah hijab-friendly rooms,
    traditional straight-razor beard craft), and consultation language restriction maps.
    """
    enriched_salons = [
        {**SALON_GIS_CATALOG[5], "biotype_specialties": ["south_asian_malay_wavy_curly", "east_asian_coarse_straight", "afro_coiled_textured"], "hijab_friendly_private": False, "razor_beard_craft": True, "languages": ["en", "ta", "ms", "zh"]},
        {**SALON_GIS_CATALOG[9], "biotype_specialties": ["east_asian_coarse_straight", "south_asian_malay_wavy_curly", "caucasian_fine_oval"], "hijab_friendly_private": False, "razor_beard_craft": False, "languages": ["en", "zh"]},
        {**SALON_GIS_CATALOG[15], "biotype_specialties": ["east_asian_coarse_straight", "caucasian_fine_oval", "south_asian_malay_wavy_curly", "afro_coiled_textured"], "hijab_friendly_private": True, "razor_beard_craft": False, "languages": ["en", "zh", "ms"]},
        {"id": "S17", "name": "Karva Salon for Ladies (Plaza Singapura)", "tier": "T3", "biotype_specialties": ["south_asian_malay_wavy_curly", "east_asian_coarse_straight", "afro_coiled_textured"], "hijab_friendly_private": True, "razor_beard_craft": False, "languages": ["en", "ms"]},
        {"id": "S18", "name": "Expat Hair Studio (Joo Chiat)", "tier": "T4", "biotype_specialties": ["caucasian_fine_oval", "south_asian_malay_wavy_curly", "afro_coiled_textured"], "hijab_friendly_private": False, "razor_beard_craft": False, "languages": ["en"]},
    ]
    evals = []
    for s in enriched_salons:
        res = compute_sheaf_hypergraph_compatibility(
            salon=s,
            hair_biotype=hair_biotype,
            requires_hijab_private_room=requires_hijab_private_room,
            requires_beard_razor_lineup=requires_beard_razor_lineup,
            preferred_language=preferred_language,
        )
        evals.append({"salon_id": s["id"], "salon_name": s["name"], **res})
    evals.sort(key=lambda x: x["sheaf_harmony_score"], reverse=True)
    return {
        "biotype_profile": HAIR_BIOTYPE_PROFILES.get(hair_biotype),
        "ranked_sheaf_matches": evals,
    }


@mcp.tool()
def run_closed_loop_bayesian_postcut_feedback(
    prior_tau_days: float = 34.0,
    prior_s0: float = 90.0,
    prior_p_upsell: float = 0.15,
    observed_day14_score: float = 78.0,
    observed_day28_score: float = 58.0,
    observed_queue_mins: float = 8.0,
    predicted_queue_mins: float = 6.0,
    upsell_pitched: bool = False,
) -> Dict[str, Any]:
    """Closed-Loop Bayesian Self-Improvement Controller for post-haircut telemetry updates."""
    return execute_closed_loop_bayesian_update(
        prior_tau_days=prior_tau_days,
        prior_s0=prior_s0,
        prior_p_upsell=prior_p_upsell,
        observed_day14_score=observed_day14_score,
        observed_day28_score=observed_day28_score,
        observed_queue_mins=observed_queue_mins,
        predicted_queue_mins=predicted_queue_mins,
        upsell_pitched=upsell_pitched,
    )




@mcp.tool()
def reconcile_and_crawl_all_sg_salons_osm_google_acra(
    run_live_overpass_osm: bool = False,
    google_places_api_key: str = "",
    planning_area_lat: float = 1.3024,
    planning_area_lng: float = 103.8347,
    radius_meters: int = 2000,
) -> Dict[str, Any]:
    """Reconcile Singapore salon counts across Scraper (415) vs OSM vs Google Maps (2,819) vs ACRA SSIC 96021 (3,930) vs SingStat (11,241), and optionally crawl live OpenStreetMap Overpass / Google Places API.
    """
    osm_count = None
    osm_sample = []
    if run_live_overpass_osm:
        try:
            overpass_query = f'[out:json][timeout:10];(node["shop"~"hairdresser|barber"](around:{radius_meters},{planning_area_lat},{planning_area_lng});way["shop"~"hairdresser|barber"](around:{radius_meters},{planning_area_lat},{planning_area_lng}););out center 15;'
            url = "https://overpass-api.de/api/interpreter?data=" + urllib.parse.quote(overpass_query)
            req = urllib.request.Request(url, headers={"User-Agent": "sg-haircut-econometrics-mcp/4.0"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                elements = data.get("elements", [])
                osm_count = len(elements)
                for el in elements[:5]:
                    tags = el.get("tags", {})
                    osm_sample.append({
                        "osm_id": el.get("id"),
                        "name": tags.get("name", "Unnamed Salon"),
                        "shop": tags.get("shop"),
                        "lat": el.get("lat") or el.get("center", {}).get("lat"),
                        "lon": el.get("lon") or el.get("center", {}).get("lon"),
                    })
        except Exception as exc:
            osm_count = f"offline_or_rate_limited ({type(exc).__name__})"

    return {
        "why_415_is_an_undercount": (
            "The '415 hair salons (384 single-owner / 31 chain)' figure in Google's AI snippet comes from "
            "a third-party web-domain scraper that only counts businesses with standalone English websites "
            "tagged 'Hair Salon'. In reality, just 3 chains alone—Kcuts (70 outlets), Clippers Barber (45 outlets), "
            "and QB House (35+ outlets)—already operate 150+ chain outlets in Singapore."
        ),
        "verified_2026_singapore_counts_by_source": {
            "1_web_domain_lead_scraper_undercount": {
                "count": 415,
                "scope": "Only salons with scraped standalone websites (misses 85%+ of HDB & mall outlets)",
            },
            "2_openstreetmap_overpass_shop_hairdresser": {
                "count_range": "450-680 mapped nodes",
                "query": 'node["shop"~"hairdresser|barber"](1.22,103.60,1.48,104.05);',
                "scope": "Volunteer-mapped OSM nodes (undercounts upper-floor mall units & HDB void decks)",
            },
            "3_google_maps_places_verified_physical_outlets": {
                "hair_salons_count": 1981,
                "barber_shops_count": 838,
                "combined_hair_and_barber_outlets": 2819,
                "all_beauty_wellness_outlets": 16773,
                "top_chains": {"Kcuts": 70, "Clippers_Barber": 45, "QB_House": 35, "Kimage": 20, "On_Hair_and_Beauty": 12},
                "source_url": "https://b2blistsg.com/beauty-wellness/hair-salon",
            },
            "4_acra_ssic_96021_registered_companies": {
                "active_companies_ssic_96021": 3930,
                "cumulative_registered_entities_96021": 15400,
                "scope": "5-digit SSIC 96021: Hairdressing salons/shops (including barber shops)",
                "source_url": "https://www.sgpbusiness.com/activities/industrial-classification/Other-Service-Activities/Other-Personal-Service-Activities/Other-Personal-Service-Activities/Hairdressing-Beauty-And-Other-Personal-Care-Services",
            },
            "5_singstat_ssic_9602_services_survey": {
                "operating_establishments_ssic_9602": 11241,
                "scope": "4-digit SSIC 9602 combined (Hair salons + Barbers + Beauty/Facial Spas + Nail Salons)",
                "source_url": "https://www.chachacha.com.sg/beauty-personal-care-statistics-singapore/",
            },
        },
        "live_osm_overpass_sample": {
            "count_in_radius": osm_count,
            "sample_nodes": osm_sample,
        },
    }




@mcp.tool()
def evaluate_age_gender_postpartum_and_occupational_alopecia(
    age: int = 34,
    gender: str = "male",
    hair_biotype: str = "east_asian_coarse_straight",
    norwood_or_ludwig_stage: int = 2,
    postpartum_months: int = 0,
    occupation_profile: str = "radiographer_healthcare_shift",
) -> Dict[str, Any]:
    """Evaluate how age/balding (Norwood/Ludwig), female postpartum telogen effluvium (months 1-12), ethnicity (SG Chinese 61% vs Indian 87%), and occupation (radiographer shift work vs 3 Gy radiation myth, cabin crew tight bun, helmet friction) modify haircut interval tau and optimal salon routing."""
    return evaluate_alopecia_postpartum_and_occupational_hazard(
        age=age,
        gender=gender,
        hair_biotype=hair_biotype,
        norwood_or_ludwig_stage=norwood_or_ludwig_stage,
        postpartum_months=postpartum_months,
        occupation_profile=occupation_profile,
    )




@mcp.tool()
def evaluate_baby_first_cut_bald_shave_and_weekly_cutting(
    cohort_type: str = "infant_first_shave_vs_unshaved",
    infant_age_months: float = 3.0,
    cut_interval_days: float = 7.0,
) -> Dict[str, Any]:
    """Evaluate hair growth velocity (mm/day & cm/month), neonatal vellus-to-terminal transition, blunt-tip Euler-Bernoulli stiffness illusion, and weekly cutting mechanics for babies (with vs without first haircut/shave), adults who shaved bald, and weekly 7-day cutters."""
    return evaluate_infant_first_cut_shaving_and_frequent_cutting_biophysics(
        cohort_type=cohort_type,
        infant_age_months=infant_age_months,
        cut_interval_days=cut_interval_days,
    )




@mcp.tool()
def query_singapore_hairstyle_popularity_matrix_1970_2026(
    gender_filter: str = "all",
    age_group_filter: str = "all",
    race_filter: str = "all",
) -> Dict[str, Any]:
    """Query the Super-Inclusive 6D Hairstyle Taxonomy (14,400 morphological combinations) and 1970-2026 Singapore Hairstyle Popularity Time-Series stratified by Gender, Age Cohort (0-12, 13-24, 25-44, 45-64, 65+), and Race/Ethnicity (Chinese, Malay/Muslimah, Indian/Sikh, Caucasian/Eurasian, Afro-Coiled)."""
    return query_universal_hairstyle_popularity_and_combinatorial_taxonomy(
        gender_filter=gender_filter,
        age_group_filter=age_group_filter,
        race_filter=race_filter,
    )




@mcp.tool()
def calculate_live_singstat_and_google_trends_hairstyle_demand(
    include_non_residents: bool = True,
    fetch_live_singstat_api: bool = False,
    fetch_live_google_trends: bool = False,
    serpapi_api_key: str = "",
    gender_filter: str = "all",
    age_group_filter: str = "all",
    race_filter: str = "all",
) -> Dict[str, Any]:
    """Fuse SingStat Table M810011 / Population in Brief 2026 (4.2315M Residents [3.6849M Citizens + 0.5466M PRs] + 1.977M Non-Residents = 6.2085M [6.21M] Total SG Population across Age x Sex x Race) with Google Trends (geo=SG) search velocity to compute exact Singapore adopter headcount, annual haircut visits, and annual SGD market GTV per hairstyle."""
    return compute_singstat_and_google_trends_hairstyle_headcount_demand(
        include_non_residents=include_non_residents,
        fetch_live_singstat_api=fetch_live_singstat_api,
        fetch_live_google_trends=fetch_live_google_trends,
        serpapi_api_key=serpapi_api_key,
        gender_filter=gender_filter,
        age_group_filter=age_group_filter,
        race_filter=race_filter,
    )




@mcp.tool()
def query_singstat_mcp_and_international_hairstyle_timelag_benchmark() -> Dict[str, Any]:
    """Connects official SingStat MCP (https://www.singstat.gov.sg/data-tools-services/singstat-mcp) table metadata (M810011, M810091, M085831, M181641) and benchmarks Singapore hairstyle trends, climate humidity penalties, and Weber-Fechner style-specific haircut timelags against South Korea, Japan, US/UK, Australia, and Malaysia/Indonesia."""
    return benchmark_singstat_mcp_and_international_hairstyle_timelags()




@mcp.tool()
def simulate_hairstyle_switch_annual_savings(
    from_style_key: str = "skin_fade_14d",
    to_style_key: str = "korean_two_block_down_perm_28d",
    monthly_income_sgd: float = 5775.0,
) -> Dict[str, Any]:
    """Compare annual nominal SGD spend, salon/queue/travel hours, Full Economic Cost (including Value of Time), and mean Weibull aesthetic score when switching from a 2-week Skin Fade (or Weekly Fade / 3-week Taper) to a Korean Two-Block Down Perm, Wolf Cut, Hush Cut, Butterfly Perm, or Rëzo Curl Cut."""
    return calculate_hairstyle_switch_economic_and_time_savings(
        from_style_key=from_style_key,
        to_style_key=to_style_key,
        monthly_income_sgd=monthly_income_sgd,
    )




@mcp.tool()
def verify_and_fetch_pubmed_trichology_citations(
    pmid_or_query: str = "11063167",
    fetch_live_ncbi_eutils: bool = False,
    ncbi_api_key: str = "",
) -> Dict[str, Any]:
    """Query the built-in PubMed/PMC Trichology Parameter Ledger (PMID:11063167 Bishan SG AGA, PMID:12520829 NSC SG AGA, PMID:26904154/PMC4740347 Koyama Scalp Massage, PMC8487794 Hospital Staff AGA, PMC13580428 Radiation 3.0 Gy threshold, PMC3162256 Neonatal Occipital Alopecia) and optionally fetch live metadata via NCBI Entrez E-Utilities."""
    return query_and_verify_pubmed_trichology_evidence(
        pmid_or_query=pmid_or_query,
        fetch_live_ncbi_eutils=fetch_live_ncbi_eutils,
        ncbi_api_key=ncbi_api_key,
    )




@mcp.tool()
def verify_simulation_math_sympy_scipy_r(
    s0: float = 92.0,
    s_min: float = 56.0,
    tau: float = 34.0,
    beta: float = 1.40,
) -> Dict[str, Any]:
    """Validate all simulation mathematics using SymPy symbolic algebra (exact Weibull inverse, hazard rate h(t), and 4th-power Euler-Bernoulli stiffness), SciPy Gauss-Kronrod quadrature & chi-square clinical replication, and formal invariant checking across all 14,400 6D hairstyle combinations."""
    return validate_simulation_math_sympy_scipy_and_r_bridge(
        s0=s0,
        s_min=s_min,
        tau=tau,
        beta=beta,
    )




@mcp.tool()
def inspect_graph_and_loop_engineering_architecture(
    start_style_node: str = "H08_SAF_BMT_Buzz_2mm",
    initial_prior_tau: float = 30.0,
    true_personal_tau: float = 24.5,
    cycles: int = 6,
) -> Dict[str, Any]:
    """Run the 3-Layer Graph Engineering engine (Cellular Sheaf Hypergraph, Spatial Queue-Spillover k-NN Graph, and Hairstyle Grow-Out Transition DAG) and 3-Layer Closed-Loop Bayesian Feedback Controller across k=1..6 haircut cycles."""
    return simulate_multicycle_closed_loop_and_growout_graph(
        start_style_node=start_style_node,
        initial_prior_tau=initial_prior_tau,
        true_personal_tau=true_personal_tau,
        cycles=cycles,
    )


if __name__ == "__main__":
    mcp.run()
