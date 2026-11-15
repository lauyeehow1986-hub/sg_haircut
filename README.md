# Singapore Haircut Econometrics & Spatio-Temporal GIS Engine

An interactive Singapore salon econometrics, clinical trichology, and demographic analysis toolkit built around **defensible official benchmarks** and a **qualitative 19-archetype inclusive hairstyle taxonomy**.

## Visual Explorers
- **`webgis/sg_haircut_gis_explorer.html`** — Spatio-temporal 102-outlet Singapore salon GIS visualizer, queue vs. reservation opportunity cost, and Bayesian post-cut loop simulator.
- **`webgis/sg_hairstyle_demographics_explorer.html`** — Refactored **Strictly Defensible Data** explorer:
  1. **19 Inclusive Qualitative Archetypes** (`H01`–`H19`, adding `H19` Everyday Express & Classic Functional Trim) with biotype mechanics (`PMC6894537`), cultural/institutional compliance, typical maintenance cadence ranges, and verified SG price bands.
  2. **Qualitative Demographic & Biotype Compatibility Matrix** (Age × Community × Observed Price — intentionally omits unmeasured `%` style shares).
  3. **Official SingStat / Population in Brief (2016–2026)** demographic series (`5.61M` → `6.21M` total pop, `12.4%` → `19.5%` residents `65+`, `21.4%` citizens `65+` super-aged threshold, CMIO `73.9% / 13.5% / 9.0% / 3.6%`, Census 2020 `12,051` Sikhs `15+`).
  4. **SSIC 9602 Industry & HES 2023 Economics + Verified Price Ladder** (`11,241` establishments, `~S$2.17B` in `2019` → `~S$3.38B` recent revenue across Hairdressing/Beauty/Spa/Nail services; `S$6.80` *Snip Avenue* to `S$438` Korean digital perms).

## Data Provenance Policy
- **Empirical Data:** Demographic totals, aging curves, CMIO proportions, Census 2020 Sikh figures, SSIC 9602 totals, HES 2023 spending (`S$5,931/mo`), and published chain/salon prices come from official SingStat / NPTD *Population in Brief* releases and published retail menus.
- **Heuristic Priors:** In `skills/sg-haircut-econometrics-engine/scripts/haircut_sheaf_graph_and_loop_engine.py`, offline `eras_pct`, offline search indices, and the `0.42` scaling factor remain explicitly flagged under `data_provenance` as uncalibrated scenario priors unless live SingStat/SerpApi feeds are connected.
- **Credentials & Local Configs:** `.antigravity/`, `mcp_config.json`, `mcp.json`, and `.env*` are excluded via `.gitignore`.
