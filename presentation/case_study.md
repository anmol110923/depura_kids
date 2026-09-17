# DePURA Kids Relaunch Strategy — Case Study

**Independent case study based on publicly available information, with general industry perspective from a Sanofi professional. Not a Sanofi project, internship, consulting engagement, or Sanofi-approved strategy. All performance data is SYNTHETIC / SIMULATED — see `data/DATA_DICTIONARY.md`.**

---

## 01. Executive Summary

**What should the company do, why, where, and how will we measure success?**

DePURA Kids returned to shelves in September 2025 after an ~17-18 month voluntary recall. A year later, seasonally adjusted revenue has recovered to only **~78% of its pre-recall run-rate**, and growth has decelerated from +32% month-over-month in the first post-relaunch month to roughly flat — a **plateau**, not a slow continued climb.

**What:** Prioritize five levers, ranked by what the analysis shows actually moves revenue: retention/adherence infrastructure, HCP re-engagement (specifically pre-recall prescribers), distribution fill-rate, sustained premium positioning, and targeted expansion in two under-penetrated large markets.

**Why:** A driver-based scenario model shows retention/adherence is, counter-intuitively, the single largest revenue lever in the Base case — and it is also the cheapest channel measured (₹23 CAC vs. ₹908 for new-parent acquisition). HCP conversion remains strategically necessary as the upstream driver that creates new adherent customers, even though its direct contribution is smaller. Stock availability is the fastest-acting lever, with a measured ~21% swing in units between poorly- and well-stocked observations.

**Where:** Defend the 12 large, already-penetrated territories; prioritize incremental investment in the 6 Grow territories, especially **Kolkata and Chennai** — both rank top-3 by category potential but bottom-half on penetration, a gap invisible on a plain revenue leaderboard.

**How we'll measure success:** The KPI framework (`kpi_framework.md`) ties every metric to a specific analysis and reviews progress against Conservative/Base/Upside scenario checkpoints, not a single-point forecast. Even the Upside case does not fully close the gap to the pre-recall baseline within a year — this is set as an 18-24 month recovery, not a one-quarter fix.

---

## 02. Business Context

DePURA Kids (Vitamin D3 400 IU/0.5 ml oral solution) is marketed by Sanofi Consumer Healthcare India Ltd, formed from Sanofi India's 2023 consumer-healthcare demerger. DePURA was named among the demerged entity's top brands at that time [research/sources.md, S1]. In July 2024, the company's circular confirmed a voluntary precautionary recall of DePURA Kids (letter dated 26 March 2024) due to microbiological contamination under investigation at the manufacturing site [S3]. The product, along with Allegra Suspension, was back on shelves by September 2025 [S5]; SCHIL's FY2025 annual report notes this was the first time in over a decade the brand received focused consumer and HCP-directed marketing [S2].

## 03. Problem Statement

*See Executive Summary.* The core analytical question this project answers: **why has recovery plateaued at ~78%, and which levers close the remaining gap fastest and most cheaply?**

## 04. Market Landscape

The Indian Academy of Pediatrics' 2021 guideline recommends routine 400 IU/day Vitamin D supplementation specifically **during infancy**; older children are guided toward diet and sunlight for prevention [S10]. This makes DePURA Kids' natural target the **0-12 month infant, reached through a pediatrician**, not "kids" broadly. Deficiency prevalence is meaningful and regionally uneven: 13.7-23.9% across age bands in the CNNS 2016-18 survey, with materially higher odds in North India specifically [S11, S12]. India registered ~2.55 crore births in 2024 [S13], but the addressable market for a privately-recommended premium product is a subset of that cohort — most vaccinations happen through public facilities [S23, S24], so the private pediatrician visit is not a universal touchpoint. Full sizing logic and its stated uncertainty are in `research/market_research.md` §4.

## 05. Competitive Landscape

DePURA Kids sits in a "premium nano" cluster at ~₹6.33 per equivalent 400 IU dose, alongside **Arachitol Kids/Nano** (Abbott, ~₹6.64) — an exact strength-and-pack match at a near-identical price, making it the closest like-for-like substitute — and Kidrich D3 Nano (Dr. Reddy's, ~₹6.65). Mid-price brands (Uprise-D3, D3 Must Forte) cost 52-58% of DePURA's dose price; the cheapest verified option (Ultra D3) costs 38%. Full comparison and sourcing in `research/competitor_analysis.md`.

## 06. Data & Methodology

Given no public brand-level sales, share, or prescription data exists for DePURA Kids, this project builds a **synthetic dataset** (six CSVs: sales, HCP, consumer, competitor, campaign, territory) whose *structure* reflects public facts (recall/relaunch timing, product pricing, directional regional/seasonal deficiency patterns) and whose *magnitudes* are stated, changeable assumptions (`config/data_generation.yaml`). The data includes deliberately planted relationships (documented in `data/DATA_DICTIONARY.md`) so the analysis has genuine confounders and effects to find — and deliberately injected data-quality issues (duplicates, label inconsistencies, entry errors) so the cleaning stage has real problems to solve. Analysis stack: SQL (DuckDB, 14 queries), Python (pandas/matplotlib/seaborn across 5 notebooks), and a Streamlit dashboard.

## 07. Key Insights

1. Recovery has **plateaued** at ~78% of pre-recall run-rate, not merely slowed — month-over-month growth fell from +32% to ~0% over 12 months [`sql/05_growth_rate_analysis.sql`].
2. Patient volume is a **confounded**, not causal, predictor of HCP recommendation — a pooled correlation of 0.28 collapses to near-zero within every specialty once controlled for [`sql/07_hcp_recommendation_analysis.sql`].
3. **Pre-recall prescribers** recommend at roughly 1.5-2x the rate of non-prescribers, within every specialty — their habit was interrupted, not rejected [`notebooks/02_eda.ipynb`].
4. Stock availability has a real, quantifiable effect: **~21% swing** in units sold between the least- and best-stocked observations [`notebooks/02_eda.ipynb` §2.6].
5. **Retention is both the cheapest lever and, in the Base case, the largest revenue driver** — a rare case where lowest-cost and highest-leverage coincide [`notebooks/05_scenario_model.ipynb`].
6. Two large markets, **Kolkata and Chennai**, rank top-3 by category potential but bottom-half on penetration — invisible on a plain revenue leaderboard [`sql/06_top_bottom_territories.sql`].

## 08. Customer/HCP Segmentation

**HCP** (4 segments, within-specialty volume percentile × recommendation rate × digital engagement): High-volume advocate (5.6%, retain), High-volume non/under-user (24.6%, highest-priority conversion target), Emerging (12.0%, digital-first), Low-opportunity (57.8%, deprioritize for expensive channels).

**Consumer** (5 segments, priority-ordered rules): Price-sensitive (32.0%, largest, below-average DePURA share), Mainstream (29.1%), Convenience-driven (17.9%, above-average share), Low-awareness (10.5%, lowest share — clearest growth pool), Health-conscious (10.5%, highest share and adherence — the brand's core).

Full method and quantitative thresholds in `notebooks/03_segmentation.ipynb`.

## 09. Territory Opportunity

A six-factor weighted score (30% market potential, 20% HCP opportunity, 15% growth potential, 15% brand gap, 10% channel readiness, 10% competitive opportunity) ranks all 36 synthetic territories. **Chennai and Delhi North hold a top-4 rank under every one of 12 tested weight perturbations** (±10pt on each factor); Kolkata does so in 10 of 12 — the top of this ranking is a weight-independent conclusion, not an artifact of the specific weights chosen [`notebooks/04_territory_analysis.ipynb`].

## 10. Relaunch Strategy

Full detail in `relaunch_strategy.md`. Summary: hold premium positioning (don't compete on price against a fragmented, many-competitor field); prioritize pre-recall-prescriber HCP re-engagement over volume-based targeting; fix distribution fill-rate as a fast Phase 1 lever; fund retention infrastructure as the highest-leverage, lowest-cost investment.

## 11. GTM Strategy

Full detail in `gtm_strategy.md`. Two parallel motions — HCP-led (trust rebuilding) and consumer-led (acquisition/retention) — with channel sequencing based on measured CAC: HCP Digital Detailing (₹10,757) before Field Rep Detailing (₹24,874) for the Emerging segment; WhatsApp/CRM retention (₹23) funded before any new-acquisition channel.

## 12. Scenario Analysis

Three scenarios (Conservative/Base/Upside) built from five explicit, labelled levers (HCP conversion, stock availability, awareness, adherence, marketing spend), each grounded in a specific prior finding. **Base case:** ~90% of pre-recall baseline within 12 months, driven most by adherence/retention (8.0 of 22.2 lift points) and stock availability (6.4 points) — ahead of marketing spend (3.5) and HCP conversion (3.4). **Even the Upside case (~105%) does not fully close the gap within a year**, consistent with rebuilding doctor trust after a recall being an 18-24 month process. Full model, elasticity rationale, and lever-sensitivity ranking in `notebooks/05_scenario_model.ipynb`.

## 13. KPI Framework

Full detail in `kpi_framework.md`. North Star: seasonally adjusted revenue recovery %. Supporting trees: HCP engagement, distribution, consumer, and territory — every metric traces to a specific chart or query in this project, reviewed at cadences from weekly (stock) to quarterly (segment conversion, scenario re-check).

## 14. Risks & Limitations

- **No public brand-level data exists** for DePURA Kids' actual sales, share, or prescription volume. Every performance figure in this project is synthetic and illustrative — the method (segment, prioritize, model trade-offs, measure) is the transferable output, not the specific numbers.
- **Planted relationships in the synthetic data** are documented in `data/DATA_DICTIONARY.md`; finding them demonstrates analytical method, not a real-world market finding.
- **Competitor prices are online MRP snapshots** (17 Sep 2026); two competitors' strengths (D3 Must Drops, Oh D3) remain unverified from a reliable source and are excluded from dose-cost comparisons.
- **The scenario model's elasticities are stated judgements**, not derived from a regression — clearly labelled as such, and would need real data or subject-matter sign-off before informing an actual budget decision.
- **Some official source documents need manual verification**: the DePURA Kids leaflet PDF returned no machine-readable text, and one relevant BSE filing blocked automated fetching — see `research/market_research.md` §8 for the full list of open items.

## 15. Final Recommendation

Fund retention/adherence infrastructure first — it is simultaneously the cheapest channel measured and the largest modelled revenue driver. In parallel, redirect HCP engagement toward pre-recall prescribers specifically (not volume-sorted call lists, which the analysis shows target the wrong variable), fix distribution fill-rate in under-stocked but high-potential territories within the first 90 days, and open incremental investment in Kolkata and Chennai. Hold the premium price position throughout — the brand's defensible advantage is doctor trust, not formulation or price, and both of DePURA's nearest competitors match it on the latter two. Communicate an 18-24 month recovery horizon to stakeholders from the outset, using the Conservative case as the floor expectation.

---

*Prepared as an independent case study for interview and portfolio purposes. See `research/industry_perspective_policy.md` for the scope and limits of the general industry input used, and `README.md` for the full project structure and reproducibility instructions.*
