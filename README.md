# Singapore Haircut Econometrics & Spatio-Temporal Salon Dashboard

Live GitHub Pages site: **https://lauyeehow1986-hub.github.io/sg_haircut/**

## What Is Included
- **`index.html`** (and **`webgis/sg_hairstyle_demographics_explorer.html`**) — Defensible empirical dashboard covering:
  1. **Yearly Trend in Singapore (`2016–2026`):** Official **SingStat SSIC 9602** Services Survey operating revenue (`S$2,173.8M` in `2019` → `S$3,381.1M` in `2024`, `+55.5%`) and establishment count (`8,453` → `11,241`, `+33.0%`), paired with **Population in Brief (`2016–2026`)** mid-year population (`5.61M` → `5.45M` → `6.21M`), Resident `65+` aging (`12.4%` → `19.5%`), `HES 2023` (`S$5,931/mo`), and an interactive annual haircut demand sensitivity curve.
  2. **Cost at Different Places & Outlet Count Reconciliation (Salons + Barbers):** Shows why our **`102`** geo-verified outlets are only a price-audited sample (`S$5.80–S$280` across `T1` Heartland/Barbers, `T2` Express chains, `T3` Mid-Tier & *Karva* Muslimah Suites, and `T4` Luxury Directors), reconciled live against **SLA OneMap** (`0` commercial retail themes out of `166`; `1–7` Elastic Search address/building hits), **OpenStreetMap Overpass** (`492` mapped nodes/ways for `hairdresser|barber`), **Google Maps directory totals** (`2,819` physical outlets = `1,981` hair salons + `838` barber shops), **ACRA SSIC `96021`** (`~3,930` active entities, explicitly *including barber shops*), and **SingStat SSIC `9602`** (`11,241` combined Hairdressing/Beauty/Spa/Nail establishments).
  3. **Annual Money Spent & SingStat `CMIO` / Age Context:** Transparent **Visits/Year × Audited Tier Ticket + Add-Ons** calculator with zero fabricated biological/racial cadence multipliers, paired with **SingStat 2026 Resident `CMIO` & Age** context (`4.23M` residents: `73.9%` Chinese, `13.5%` Malay, `9.0%` Indian, `3.6%` Others; `19.5%` aged `65+`) and verified Singapore cultural service rules (Muslimah hijab-private cabins and Sikh Sacred *Kesh* `S$0` haircut fees; `Census 2020`: `12,051` aged `15+`).
- **`webgis/sg_haircut_gis_explorer.html`** — Interactive Leaflet Spatio-Temporal Map across the 102 Singapore outlets.

## Privacy & Credentials
- Local Antigravity MCP configurations and credentials (`.antigravity/`, `mcp_config.json`, `mcp.json`, `.env*`) are excluded via `.gitignore`.
