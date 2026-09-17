# DePURA Kids Relaunch Strategy — Pharma Commercial Analytics Case Study

> **Independent case study based on publicly available information, with general industry perspective from a Sanofi professional.**
> This is **not** a Sanofi project, internship, consulting engagement, or Sanofi-approved strategy. No confidential, proprietary, internal or non-public information is used. All performance data is **synthetic**.

## The business question

> **How should DePURA Kids strengthen its post-relaunch growth in India's pediatric Vitamin D category?**

**Public context.** DePURA Kids (Vitamin D3 400 IU / 0.5 ml oral solution) is marketed by Sanofi Consumer Healthcare India Ltd. It was voluntarily recalled from March 2024 over microbiological contamination under investigation at the manufacturing site, and was back on shelves by September 2025. That is roughly 17–18 months in which doctors and parents had to use something else.

**Why this is an interesting problem.** The Indian Academy of Pediatrics recommends routine 400 IU/day supplementation in **infancy**, which makes this a doctor-initiated, habit-driven purchase with a clear 0–12 month target. It sits in a crowded category where a same-strength premium substitute (Arachitol Kids / Nano) and many cheaper 800 IU/ml drops are available. The relaunch problem is **winning back broken prescribing and purchasing habits**, not simply launching a product.

## Evidence rules

| Type | Where | Label used |
|---|---|---|
| Public facts | `research/` | FACT, with source ID |
| Directional public evidence | `research/market_research.md` | DIRECTIONAL |
| Analyst assumptions | `config/*.yaml` | ASSUMPTION |
| Hypotheses to test | `research/market_research.md` §5 | HYPOTHESIS |
| Simulated data | `data/` | SYNTHETIC |
| Industry perspective | `research/industry_perspective_policy.md` | General context only |

## Project status

| Stage | Deliverable | Status |
|---|---|---|
| 0 | Architecture, research plan, schema, framework, assumptions | ✅ |
| 1 | Research: market, competitors, sources, perspective policy | ✅ |
| 2 | Synthetic data generator, 6 CSVs, data dictionary, 27 validation checks | ✅ |
| 3 | SQL analysis (DuckDB) — 14 queries, all tested against the data | ✅ |
| 4 | Notebooks 01–03: cleaning, EDA, segmentation — all executed, 27+ checks, 8 charts | ✅ |
| 5 | Notebooks 04–05: territory scoring (with sensitivity test), scenario model | ✅ |
| 6 | Streamlit dashboard — 8 pages, all tested via Streamlit AppTest | ✅ |
| 7 | Strategy, GTM, KPI framework, case study — all cross-checked against the data | ✅ |
| 8 | Interview prep and resume bullets | ⏳ |

## Structure

```
depura-kids-relaunch/
├── README.md
├── requirements.txt
├── config/
│   └── data_generation.yaml     # every assumption behind the synthetic data
├── scripts/
│   ├── generate_data.py         # seeded, reproducible generator
│   └── validate_data.py         # schema, reconciliation & planted-effect checks
├── data/                        # SYNTHETIC
│   ├── DATA_DICTIONARY.md
│   ├── sales_data.csv           # 12,735 rows · month × territory × channel × SKU
│   ├── hcp_data.csv             # 2,500 HCPs
│   ├── consumer_data.csv        # 3,000 parents
│   ├── competitor_data.csv      # 8 brands (public fields + labelled assessments)
│   ├── campaign_data.csv        # 120 channel-months
│   └── territory_data.csv       # 36 territories
├── research/
│   ├── market_research.md
│   ├── competitor_analysis.md
│   ├── sources.md
│   └── industry_perspective_policy.md
├── sql/                          # 14 DuckDB queries + setup + README
├── notebooks/                    # 01-05: cleaning, EDA, segmentation, territory scoring, scenarios
├── dashboard/                    # 8-page Streamlit app (app.py + pages/ + utils/)
├── outputs/                      # tables + charts written by the notebooks
├── strategy/                     # relaunch_strategy.md, gtm_strategy.md, kpi_framework.md
└── presentation/                 # case_study.md — the consulting-style write-up
└── INTERVIEW_PREP.md                                                 # Stage 8
```

## Quickstart

```bash
python3 -m pip install -r requirements.txt
python3 scripts/generate_data.py     # regenerate all CSVs (seed 42)
     # expect 27/27 checks passed
# run notebooks/01 through 05 (in order) to populate outputs/tables/
cd dashboard && python3 -m streamlit run app.py
```

## Key public findings so far

1. **The target is infants, not "kids".** IAP guidance backs routine supplementation in infancy only. [S10]
2. **The closest threat is a like-for-like premium substitute.** Arachitol Kids / Nano matches DePURA Kids' strength and dosing volume at a ~5% higher cost per dose. [S15][S8]
3. **DePURA can't win on price.** Mid-price brands cost ~52–58% of DePURA per dose; the cheapest verified option costs 38%. [S8][S17][S18]
4. **The addressable market is a subset of births.** If ~96% of children get most vaccinations in public facilities (round to be verified), the private pediatrician visit is not universal. [S24]
5. **Retailer product copy is unreliable.** Retail pages disagree on DePURA Kids' dosing for ages 1–18, so only official documents are used for product facts. [S9]

## Key SQL findings so far (on synthetic data — see `sql/README.md`)

1. **Recovery has plateaued, not just slowed.** Month-over-month growth fell from +32% in the first post-relaunch month to ~0% by month 12; seasonally adjusted revenue sits at ~78% of the pre-recall run-rate.
2. **Patient volume does not predict HCP recommendation once specialty is controlled.** A seemingly meaningful correlation (0.28) collapses to near-zero within every specialty — a textbook confounder, not a real driver.
3. **Stock availability has a real, quantifiable effect on sales**, with a ~20% swing in the unit index between the lowest and highest stock bands.
4. **Adherence is far cheaper to win than acquisition.** Refill-reminder CAC (₹23) is two orders of magnitude below blended parent-acquisition CAC (₹908) and HCP-conversion CAC (₹19,434).
5. **Two large markets are hiding in plain sight.** Kolkata and Chennai are both top-3 by category potential but rank in the bottom half on penetration — invisible on a plain revenue leaderboard.

## Notebook findings (Stage 4, on synthetic data — see `notebooks/`)

- **01_data_cleaning.ipynb**: found and fixed 63 duplicate rows, 4 inconsistent state labels, 6 HCP data-entry errors, and ~1% missing discounts; reconciled cleaned sales to `territory_data.csv` to within 0.11%.
- **02_eda.ipynb**: 8 charts, each tied to a specific business question — including a visual demonstration of the volume/recommendation confounder (scatter by specialty) and the stock-availability effect on sales (~21% swing across bands).
- **03_segmentation.ipynb**: applies the HCP, consumer, and territory segmentation rules quantitatively; confirms every specialty is represented across all four HCP segments (ruling out the segmentation being a relabelled specialty split), and confirms Kolkata/Chennai land in "Grow" under both the SQL and notebook versions of the territory model.
- **04_territory_analysis.ipynb**: builds the full 6-factor weighted opportunity score (differentiating HCP behavioural opportunity from brand-awareness gap) and stress-tests it with 12 weight perturbations (±10pt on each factor). Chennai and Delhi North hold a top-4 rank under every perturbation tested; Kolkata does so in 10 of 12. The minimum Spearman correlation with the base ranking across all perturbations is 0.945 — the ranking is robust, not an artifact of the chosen weights.
- **05_scenario_model.ipynb**: builds Conservative/Base/Upside scenarios from five explicit, labelled levers. A genuinely useful finding: in the Base case, **adherence/retention is the single largest revenue driver (not HCP conversion)** — consistent with retention also being the cheapest channel (₹23 CAC) found in the SQL analysis. Even the Upside case doesn't fully close the gap to the pre-recall baseline within a year.

## Dashboard (Stage 6 — see `dashboard/`)

An 8-page Streamlit app (`dashboard/app.py` + `dashboard/pages/`) bringing together the SQL, EDA, segmentation, territory scoring and scenario model into one interactive view: Executive Overview, Market & Competition, HCP Analytics, Consumer Analytics, Territory Prioritization, Campaign Performance, an interactive Scenario Planner (live sliders reproducing notebook 05's model), and Strategic Recommendations. Every page carries a synthetic-data warning banner and was verified with Streamlit's `AppTest` framework before being considered done — see `dashboard/README.md` for design notes and the three real bugs that testing caught during development.

## Limitations

- No brand-level sales, share or prescription data is public. Every performance figure is synthetic and illustrative.
- Planted relationships in the synthetic data are documented; finding them demonstrates method, not market truth.
- Competitor prices are online MRP snapshots; two competitors' strengths remain unverified.
- Some official documents (image-only leaflet, BSE filing) need manual verification (see `research/market_research.md` §8).
- **Build-history note:** mid-project edits to `scripts/generate_data.py` (Stage 2) shifted the random-number sequence for `campaign_data.csv` specifically, so early campaign/CAC figures quoted in chat during Stage 3 no longer matched the data by the time Stage 7 began. Sales, HCP, consumer, competitor, and territory data were unaffected — the current `data/` and every notebook, table, and document in this repository are mutually consistent as of the final rebuild. If reproducing this project from scratch with `scripts/generate_data.py` unmodified, all figures will match what's written here.
