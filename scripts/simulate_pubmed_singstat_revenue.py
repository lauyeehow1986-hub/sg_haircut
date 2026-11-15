"""PubMed-grounded Hair Growth, SingStat 2026 Demographic Demand,
and SSIC 9602 / ACRA Establishment-Driver Simulation for Singapore.

Reads:
  - data/singstat_and_acra_facts_2026.json
  - skills/sg-haircut-econometrics-engine/assets/sg_haircut_salons_2026_catalog.csv
Writes:
  - data/pubmed_singstat_revenue_2026.json
"""

from __future__ import annotations

import csv
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FACTS_PATH = ROOT / "data" / "singstat_and_acra_facts_2026.json"
CATALOG_PATH = ROOT / "skills" / "sg-haircut-econometrics-engine" / "assets" / "sg_haircut_salons_2026_catalog.csv"
OUT_PATH = ROOT / "data" / "pubmed_singstat_revenue_2026.json"

PUBMED_STUDIES = [
    {"pmid": "16187948", "cite": "Loussouarn et al. (2005)", "journal": "Int J Dermatol", "scope": "Race velocity", "finding": "Asian 411 ± 43 µm/day (1.000×), Caucasian 367 ± 56 µm/day (0.893×), African 280 ± 50 µm/day (0.681×)."},
    {"pmid": "11531795", "cite": "Loussouarn (2001)", "journal": "Br J Dermatol", "scope": "Sex invariance & curl", "finding": "African 256 ± 44 vs Caucasian 396 ± 55 µm/day; zero significant linear growth difference by gender or scalp site."},
    {"pmid": "25065943", "cite": "Liu et al. (2014)", "journal": "Int J Cosmet Sci", "scope": "Chinese 1-yr phototrichogram", "finding": "N=41 Chinese adults: confirms fastest terminal growth rate among studied ethnic groups with minor Aug–Sep seasonal telogen bump."},
    {"pmid": "27019510", "cite": "Loussouarn et al. (2016)", "journal": "Eur J Dermatol", "scope": "Multi-ethnic N=2,249", "finding": "Ages 18–35 across 24 groups: Asian hair shows thickest diameter and fastest growth; Caucasian highest density."},
    {"pmid": "29543618", "cite": "Ingprasert et al. (2018)", "journal": "Dermatol Surg", "scope": "SE Asian women (N=101)", "finding": "Donor density 98.9–152.2 hairs/cm² and thick shaft diameter 76.8–81.1 µm; declines with age."},
    {"pmid": "37667034", "cite": "Ruiz et al. (2024)", "journal": "Pediatr Res", "scope": "Infants & preschoolers (N=266)", "finding": "Infants <1y grow slower (287.9 ± 60.7 µm/day) vs 3y (345.1 µm/day); Asian kids (355.6 µm/d) > White (332.1, p=0.016); sex p=0.71."},
    {"pmid": "24185569", "cite": "Kim et al. (2013)", "journal": "Eur J Dermatol", "scope": "East Asian aging (N=1,357)", "finding": "Ages 10–69 phototrichogram: no gender gap in density/thickness; density peaks in 20s then declines; greying spikes >40y."},
    {"pmid": "17161939", "cite": "Tajima et al. (2007)", "journal": "J Dermatol Sci", "scope": "Age >40 slowdown (N=159)", "finding": "Diameter rises age 10→40, then both anagen ratio and anagen growth rate decline significantly after the 40s."},
    {"pmid": "22524482", "cite": "Robbins et al. (2012)", "journal": "Br J Dermatol", "scope": "Lifespan peak (N=1,414)", "finding": "Density peaks 20–30y, parietal diameter rises to 40–45y, composite hair mass peaks ~35y."},
    {"pmid": "14965792", "cite": "Van Neste (2004)", "journal": "Eur J Dermatol", "scope": "Age & white hair paradox", "finding": "Pigmented hair slows with age (0.34–0.35 mm/day) while unpigmented white hair grows ~10% faster (0.38 mm/day, p=0.0001)."},
    {"pmid": "8003330", "cite": "Courtois et al. (1994)", "journal": "Skin Pharmacol", "scope": "15-yr longitudinal cycle", "finding": "Aging progressively shortens anagen duration, thins shafts, and prolongs telogen-to-anagen latency (~10,000 cycles tracked)."},
    {"pmid": "11063167", "cite": "Tang et al. (2000)", "journal": "Singapore Med J", "scope": "SG Male AGA (Bishan East, N=254)", "finding": "63% overall male AGA (32% aged 17–26 → 100% aged 80s); Indian 87% vs Chinese 61%; 74% of treatment-seekers use non-medical centers."},
    {"pmid": "12520829", "cite": "Goh (2002)", "journal": "Ann Acad Med Singap", "scope": "NSC SG AGA clinic (N=256)", "finding": "Mean presentation age 33.7y (31.2 mo prior loss); 96.4% distressed, 90.5% cosmetic demand across Chinese/Malay/Indian patients."},
    {"pmid": "20105167", "cite": "Wang et al. (2010)", "journal": "Br J Dermatol", "scope": "Chinese M/F AGA (N=15,257)", "finding": "Female AGA age-curve: 1.3% (18–29), 2.3% (30–39), 5.4% (40–49), 7.5% (50–59), 10.3% (60–69), 11.8% (70+); overall M 21.3%, F 6.0%."},
    {"pmid": "24981717", "cite": "Ishino et al. (2014)", "journal": "Br J Dermatol", "scope": "Crown vs occipital (n=369)", "finding": "AGA depletes thick >80 µm vertex hairs into <40 µm vellus hairs while sides/occipital perimeter preserve growth."},
    {"pmid": "23682615", "cite": "Gizlenti & Ekmekci (2014)", "journal": "JEADV", "scope": "Postpartum TE (N=116)", "finding": "Pregnancy prolongs anagen; significant month-4 postpartum anagen drop & telogen spike (p=0.045/0.038), normalizing by year 1."},
    {"pmid": "39462180", "cite": "Hirose et al. (2024)", "journal": "BMJ Open", "scope": "Postpartum psychological distress", "finding": "N=331 mothers: heavy postpartum hair loss carries AOR=4.58 for GAD-2 anxiety, reinforcing scalp-care demand."},
    {"pmid": "33541773", "cite": "Chien Yin et al. (2021)", "journal": "J Dermatol Sci", "scope": "NSC Singapore TE review", "finding": "Summarizes clinical precipitants, cycle disruption, and absence of targeted pharmacotherapy for telogen effluvium."},
]


def run_simulation() -> dict:
    facts = json.loads(FACTS_PATH.read_text(encoding="utf-8"))
    cells = facts["resident_cells_2026"]
    asfr_2025 = facts["asfr_2025_per_1000"]
    tot_pop = facts["total_pop_2026"]

    # Audited 102 catalog price statistics
    cat = list(csv.DictReader(CATALOG_PATH.open(encoding="utf-8")))
    med_all = {
        "men": round(statistics.median(float(r["price_men_sgd"]) for r in cat), 2),
        "women": round(statistics.median(float(r["price_women_sgd"]) for r in cat), 2),
        "kid": round(statistics.median(float(r["price_kid_sgd"]) for r in cat), 2),
    }
    tier_weights = {"T1": 0.35, "T2": 0.45, "T3": 0.15, "T4": 0.05}
    tier_meds = {}
    for tc in tier_weights:
        sub = [r for r in cat if r["tier_code"] == tc]
        tier_meds[tc] = {
            "men": statistics.median(float(r["price_men_sgd"]) for r in sub),
            "women": statistics.median(float(r["price_women_sgd"]) for r in sub),
            "kid": statistics.median(float(r["price_kid_sgd"]) for r in sub),
        }
    blend = {
        k: round(sum(tier_weights[tc] * tier_meds[tc][k] for tc in tier_weights), 2)
        for k in ("men", "women", "kid")
    }

    pop = {(c["race"], c["sex"], c["age"]): c["pop_2026"] for c in cells}
    tot_res = sum(pop.values())

    race_bio = {"Chinese": 1.000, "Malay": 0.980, "Indian": 0.946, "Others": 0.900}
    age_bio = {
        "0 - 4 Years": 0.832, "5 - 9 Years": 0.930, "10 - 14 Years": 0.960, "15 - 19 Years": 0.985,
        "20 - 24 Years": 1.000, "25 - 29 Years": 1.000, "30 - 34 Years": 1.000, "35 - 39 Years": 1.000,
        "40 - 44 Years": 0.955, "45 - 49 Years": 0.930, "50 - 54 Years": 0.905, "55 - 59 Years": 0.880,
        "60 - 64 Years": 0.855, "65 - 69 Years": 0.835, "70 - 74 Years": 0.815, "75 - 79 Years": 0.795,
        "80 - 84 Years": 0.775, "85 - 89 Years": 0.755, "90 Years & Over": 0.740,
    }
    male_aga_base = {
        "0 - 4 Years": 0.00, "5 - 9 Years": 0.00, "10 - 14 Years": 0.00, "15 - 19 Years": 0.10,
        "20 - 24 Years": 0.30, "25 - 29 Years": 0.38, "30 - 34 Years": 0.46, "35 - 39 Years": 0.54,
        "40 - 44 Years": 0.60, "45 - 49 Years": 0.66, "50 - 54 Years": 0.72, "55 - 59 Years": 0.78,
        "60 - 64 Years": 0.84, "65 - 69 Years": 0.88, "70 - 74 Years": 0.92, "75 - 79 Years": 0.95,
        "80 - 84 Years": 0.98, "85 - 89 Years": 0.99, "90 Years & Over": 0.99,
    }
    male_sev_share = {
        "0 - 4 Years": 0.00, "5 - 9 Years": 0.00, "10 - 14 Years": 0.00, "15 - 19 Years": 0.02,
        "20 - 24 Years": 0.05, "25 - 29 Years": 0.10, "30 - 34 Years": 0.15, "35 - 39 Years": 0.22,
        "40 - 44 Years": 0.28, "45 - 49 Years": 0.35, "50 - 54 Years": 0.42, "55 - 59 Years": 0.48,
        "60 - 64 Years": 0.54, "65 - 69 Years": 0.60, "70 - 74 Years": 0.65, "75 - 79 Years": 0.70,
        "80 - 84 Years": 0.75, "85 - 89 Years": 0.80, "90 Years & Over": 0.85,
    }
    female_fphl = {
        "0 - 4 Years": 0.000, "5 - 9 Years": 0.000, "10 - 14 Years": 0.000, "15 - 19 Years": 0.005,
        "20 - 24 Years": 0.013, "25 - 29 Years": 0.013, "30 - 34 Years": 0.023, "35 - 39 Years": 0.023,
        "40 - 44 Years": 0.054, "45 - 49 Years": 0.054, "50 - 54 Years": 0.075, "55 - 59 Years": 0.075,
        "60 - 64 Years": 0.103, "65 - 69 Years": 0.103, "70 - 74 Years": 0.118, "75 - 79 Years": 0.118,
        "80 - 84 Years": 0.118, "85 - 89 Years": 0.118, "90 Years & Over": 0.118,
    }
    male_style = {
        "0 - 4 Years": 0.56, "5 - 9 Years": 0.74, "10 - 14 Years": 0.86, "15 - 19 Years": 0.95,
        "20 - 24 Years": 1.00, "25 - 29 Years": 1.00, "30 - 34 Years": 1.00, "35 - 39 Years": 1.00,
        "40 - 44 Years": 0.98, "45 - 49 Years": 0.96, "50 - 54 Years": 0.94, "55 - 59 Years": 0.92,
        "60 - 64 Years": 0.90, "65 - 69 Years": 0.88, "70 - 74 Years": 0.84, "75 - 79 Years": 0.80,
        "80 - 84 Years": 0.75, "85 - 89 Years": 0.70, "90 Years & Over": 0.65,
    }
    female_style = {
        "0 - 4 Years": 0.30, "5 - 9 Years": 0.34, "10 - 14 Years": 0.36, "15 - 19 Years": 0.38,
        "20 - 24 Years": 0.38, "25 - 29 Years": 0.38, "30 - 34 Years": 0.38, "35 - 39 Years": 0.38,
        "40 - 44 Years": 0.37, "45 - 49 Years": 0.37, "50 - 54 Years": 0.36, "55 - 59 Years": 0.35,
        "60 - 64 Years": 0.35, "65 - 69 Years": 0.34, "70 - 74 Years": 0.33, "75 - 79 Years": 0.32,
        "80 - 84 Years": 0.30, "85 - 89 Years": 0.28, "90 Years & Over": 0.26,
    }

    def raw_rate(rc: str, sx: str, ag: str) -> float:
        rb, ab = race_bio[rc], age_bio[ag]
        if sx == "Male":
            aga_s = 1.00 if rc in ("Chinese", "Malay", "Others") else 1.426
            p_aga = min(0.98, male_aga_base[ag] * aga_s)
            p_sev = male_sev_share[ag] * p_aga
            aga_f = (1.0 - p_aga) * 1.00 + (p_aga - p_sev) * 0.92 + p_sev * 0.42
            cult_f = (1.0 - 0.035) if (rc == "Indian" and ag not in ("0 - 4 Years", "5 - 9 Years")) else 1.0
            return rb * ab * aga_f * cult_f * male_style[ag]
        p_f = female_fphl[ag]
        aga_f = (1.0 - p_f) * 1.00 + p_f * 0.85
        pp_addon = (asfr_2025[ag] / 1000.0) * 0.21 if ag in asfr_2025 else 0.0
        cult_f = 1.0
        if rc == "Indian" and ag not in ("0 - 4 Years", "5 - 9 Years"):
            cult_f = 1.0 - 0.030
        elif rc == "Malay" and ag not in ("0 - 4 Years", "5 - 9 Years", "10 - 14 Years"):
            cult_f = 0.82
        return rb * ab * aga_f * cult_f * (female_style[ag] * (1.0 + pp_addon))

    anchor_ages = ("20 - 24 Years", "25 - 29 Years", "30 - 34 Years", "35 - 39 Years")
    m2039_pop = sum(pop[(rc, "Male", ag)] for rc in race_bio for ag in anchor_ages)
    m2039_raw = sum(pop[(rc, "Male", ag)] * raw_rate(rc, "Male", ag) for rc in race_bio for ag in anchor_ages)
    k_5wk = 10.40 / (m2039_raw / m2039_pop)

    cell_cuts = {
        (rc, sx, ag): (n, k_5wk * raw_rate(rc, sx, ag), n * k_5wk * raw_rate(rc, sx, ag))
        for (rc, sx, ag), n in pop.items()
    }
    tot_cuts_res = sum(v[2] for v in cell_cuts.values())

    by_gender = []
    for sx in ("Male", "Female"):
        p_sx = sum(v[0] for (r, s, a), v in cell_cuts.items() if s == sx)
        c_sx = sum(v[2] for (r, s, a), v in cell_cuts.items() if s == sx)
        by_gender.append({
            "sex": sx, "pop": p_sx, "pop_pct": round(p_sx / tot_res * 100, 1),
            "cuts": round(c_sx), "cuts_pct": round(c_sx / tot_cuts_res * 100, 1),
            "avg_cuts": round(c_sx / p_sx, 2),
        })

    by_race = []
    for rc in ("Chinese", "Malay", "Indian", "Others"):
        rp = sum(v[0] for (r, s, a), v in cell_cuts.items() if r == rc)
        rc_tot = sum(v[2] for (r, s, a), v in cell_cuts.items() if r == rc)
        mp = sum(v[0] for (r, s, a), v in cell_cuts.items() if r == rc and s == "Male")
        mc = sum(v[2] for (r, s, a), v in cell_cuts.items() if r == rc and s == "Male")
        fp = sum(v[0] for (r, s, a), v in cell_cuts.items() if r == rc and s == "Female")
        fc = sum(v[2] for (r, s, a), v in cell_cuts.items() if r == rc and s == "Female")
        m20 = sum(cell_cuts[(rc, "Male", a)][2] for a in anchor_ages) / sum(cell_cuts[(rc, "Male", a)][0] for a in anchor_ages)
        f20 = sum(cell_cuts[(rc, "Female", a)][2] for a in anchor_ages) / sum(cell_cuts[(rc, "Female", a)][0] for a in anchor_ages)
        by_race.append({
            "race": rc, "bio_idx": race_bio[rc], "pop": rp, "pop_pct": round(rp / tot_res * 100, 1),
            "cuts": round(rc_tot), "cuts_pct": round(rc_tot / tot_cuts_res * 100, 1),
            "avg_cuts": round(rc_tot / rp, 2), "male_avg": round(mc / mp, 2), "female_avg": round(fc / fp, 2),
            "male_20_39": round(m20, 2), "female_20_39": round(f20, 2),
        })

    cohorts = [
        ("0–4 Preschool & Infants", ["0 - 4 Years"]),
        ("5–14 School Children", ["5 - 9 Years", "10 - 14 Years"]),
        ("15–19 Teens / Tertiary / NS", ["15 - 19 Years"]),
        ("20–39 Prime Adults (Anchor)", ["20 - 24 Years", "25 - 29 Years", "30 - 34 Years", "35 - 39 Years"]),
        ("40–59 Midlife Adults", ["40 - 44 Years", "45 - 49 Years", "50 - 54 Years", "55 - 59 Years"]),
        ("60–79 Seniors", ["60 - 64 Years", "65 - 69 Years", "70 - 74 Years", "75 - 79 Years"]),
        ("80+ Oldest-Old", ["80 - 84 Years", "85 - 89 Years", "90 Years & Over"]),
    ]
    by_age = []
    for lbl, ags in cohorts:
        ap = sum(v[0] for (r, s, a), v in cell_cuts.items() if a in ags)
        ac = sum(v[2] for (r, s, a), v in cell_cuts.items() if a in ags)
        mp = sum(v[0] for (r, s, a), v in cell_cuts.items() if a in ags and s == "Male")
        mc = sum(v[2] for (r, s, a), v in cell_cuts.items() if a in ags and s == "Male")
        fp = sum(v[0] for (r, s, a), v in cell_cuts.items() if a in ags and s == "Female")
        fc = sum(v[2] for (r, s, a), v in cell_cuts.items() if a in ags and s == "Female")
        by_age.append({
            "cohort": lbl, "pop": ap, "pop_pct": round(ap / tot_res * 100, 1),
            "cuts": round(ac), "cuts_pct": round(ac / tot_cuts_res * 100, 1),
            "avg_cuts": round(ac / ap, 2), "male_avg": round(mc / mp, 2), "female_avg": round(fc / fp, 2),
        })

    # Non-resident working-age complement (55% M @ 10.2/yr, 45% F @ 3.6/yr at 5-wk anchor)
    nr_pop = tot_pop - tot_res
    nr_m_cuts = round(nr_pop * 0.55 * 10.2)
    nr_f_cuts = round(nr_pop * 0.45 * 3.6)

    kid_ages = ("0 - 4 Years", "5 - 9 Years", "10 - 14 Years")
    res_kid_cuts = round(sum(v[2] for (r, s, a), v in cell_cuts.items() if a in kid_ages))
    res_men_cuts = round(sum(v[2] for (r, s, a), v in cell_cuts.items() if s == "Male" and a not in kid_ages))
    res_wom_cuts = round(sum(v[2] for (r, s, a), v in cell_cuts.items() if s == "Female" and a not in kid_ages))

    output = {
        "meta": {
            "anchor_default_weeks": 5.0,
            "anchor_default_cuts_yr": 10.40,
            "residents_2026": tot_res,
            "non_residents_est": nr_pop,
            "total_pop_2026": tot_pop,
            "implied_resident_births_yr": round(sum(
                sum(pop[(rc, "Female", ag)] for rc in race_bio) * rate / 1000.0
                for ag, rate in asfr_2025.items()
            )),
            "calibration_scalar_k": round(k_5wk, 4),
            "denominators": {"acra_96021": 3933, "google_retail": 2819, "ssic_9602": 11241},
        },
        "tickets": {
            "median_express": med_all,
            "tier_blend": blend,
            "tier_weights": tier_weights,
        },
        "cuts_5wk": {
            "res_total": round(tot_cuts_res),
            "res_kid": res_kid_cuts,
            "res_men": res_men_cuts,
            "res_women": res_wom_cuts,
            "nr_men": nr_m_cuts,
            "nr_women": nr_f_cuts,
            "all_total": round(tot_cuts_res + nr_m_cuts + nr_f_cuts),
        },
        "by_gender": by_gender,
        "by_race": by_race,
        "by_age": by_age,
        "pubmed_studies": PUBMED_STUDIES,
        "pubmed_gaps": [
            "No standalone phototrichogram linear velocity (um/day) clinical trial exists on Singapore Malays or Singapore Indians; SE Asian donor-site data (PMID 29543618) and South Asian clinical AGA cohorts (PMID 11063167, 39312769) anchor our proxy parameters.",
            "Gender haircut frequency divergence (~7.90 vs ~3.57 cuts/yr) is primarily behavioral (style-length tolerance) + higher male AGA/SS16 short-cut norms, because healthy human linear velocity shows zero significant gender difference (PMID 11531795, 37667034, 24185569).",
        ],
        "ssic_9602_pnl": facts["ssic_9602_pnl"],
        "ssic_9602_formations_cessations": facts["ssic_9602_formations_cessations"],
        "acra_comparison": facts["acra_comparison"],
    }

    OUT_PATH.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_PATH} | Res cuts (5-wk): {output['cuts_5wk']['res_total']:,} | All 6.21M cuts (5-wk): {output['cuts_5wk']['all_total']:,}")


if __name__ == "__main__":
    run_simulation()
