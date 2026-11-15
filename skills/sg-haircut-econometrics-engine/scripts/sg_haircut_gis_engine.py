#!/usr/bin/env python3
"""Standalone CLI & GeoJSON Generator for Singapore Salon Spatio-Temporal GIS Engine."""

import argparse
import json
from sg_haircut_quant_mcp import (
    export_salon_geojson_layer,
    query_salon_gis_crowd_and_reservation_schedule,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Singapore Salon GIS Crowd & Reservation Scheduler")
    parser.add_argument("--day", type=int, default=5, help="Day of week (0=Mon .. 6=Sun)")
    parser.add_argument("--hour", type=int, default=14, help="Hour of day in SGT (10..21)")
    parser.add_argument("--days-elapsed", type=float, default=14.0, help="Days since last haircut")
    parser.add_argument("--income", type=float, default=5775.0, help="Monthly gross income in SGD")
    parser.add_argument("--profile", type=str, default="male", choices=["male", "female", "kid"])
    parser.add_argument("--occasion", type=str, default="normal", choices=["normal", "special"])
    parser.add_argument("--geojson-out", type=str, default="", help="Optional path to write GeoJSON file")
    args = parser.parse_args()

    res = query_salon_gis_crowd_and_reservation_schedule(
        day_of_week=args.day,
        hour_24=args.hour,
        days_since_last_cut=args.days_elapsed,
        monthly_income_sgd=args.income,
        profile=args.profile,
        occasion_type=args.occasion,
    )
    print(json.dumps(res["top_gis_recommendation"], indent=2))

    if args.geojson_out:
        gj = export_salon_geojson_layer(
            day_of_week=args.day,
            hour_24=args.hour,
            days_since_last_cut=args.days_elapsed,
            monthly_income_sgd=args.income,
            profile=args.profile,
            occasion_type=args.occasion,
        )
        with open(args.geojson_out, "w", encoding="utf-8") as f:
            json.dump(gj, f, indent=2)
        print(f"Saved GeoJSON FeatureCollection to {args.geojson_out}")


if __name__ == "__main__":
    main()
