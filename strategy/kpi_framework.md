# DePURA Kids — KPI Framework

**Independent case study; all figures SYNTHETIC.** This framework defines what to measure, why, at what cadence, and against what target — so the relaunch strategy (`relaunch_strategy.md`) is auditable, not just aspirational.

---

## 1. Design principles

1. **Every KPI traces to an analysis.** No metric here is included because it's generically "good practice" — each one is here because a specific chart or query in this project showed it matters.
2. **Leading and lagging metrics are separated.** Revenue recovery is a lagging outcome; HCP recommendation rate and stock availability are leading indicators that move first and predict it.
3. **Targets are ranges tied to the scenario model**, not single-point promises — consistent with the Conservative/Base/Upside framing in `notebooks/05_scenario_model.ipynb`.

## 2. The KPI tree

```
North Star: Seasonally adjusted revenue recovery (% of pre-recall baseline)
│
├── HCP engagement
│   ├── Recommendation rate among pre-recall prescribers (leading)
│   ├── High-volume non/under-user → advocate conversion rate (leading)
│   └── Field/digital detailing CAC by segment (efficiency)
│
├── Distribution
│   ├── Stock availability % (leading — fastest-moving lever)
│   └── Active distributor count by territory (leading)
│
├── Consumer
│   ├── Adherence score / refill rate among existing customers (leading)
│   ├── Awareness % among Low-awareness segment (leading)
│   └── Blended CAC by audience (efficiency)
│
└── Territory
    ├── Penetration % in Grow-segment territories (Kolkata, Chennai priority)
    └── Opportunity-score rank stability (model health check)
```

## 3. Metric definitions, targets, and cadence

### North Star

| Metric | Definition | Current (synthetic) | Target | Cadence | Source |
|---|---|---|---|---|---|
| Revenue recovery % | Seasonally adjusted monthly revenue ÷ pre-recall 12-month average | ~78% | Conservative: 79% · Base: 90% · Upside: 105%, annualised | Monthly | `sql/01_monthly_sales_trends.sql` |

### HCP engagement

| Metric | Definition | Current (synthetic) | Target | Cadence | Source |
|---|---|---|---|---|---|
| Pre-recall prescriber recommendation rate | Avg. recommendation rate among HCPs who prescribed DePURA before March 2024 | Pediatricians: 41.6% (vs 23.1% for non-prescribers) | Directional increase quarter-over-quarter | Quarterly (HCP survey/CRM cycle) | `sql/07_hcp_recommendation_analysis.sql` |
| Non-user → advocate conversion | Share of "High-volume non/under-user" HCPs (24.6% of sample) reclassified as advocates | Baseline: 0% converted (relaunch just occurred) | Base case assumes 25% converted within 12 months | Quarterly | `notebooks/03_segmentation.ipynb`, `notebooks/05_scenario_model.ipynb` |
| HCP-audience blended CAC | Total HCP-channel spend ÷ HCP conversions | ₹19,434 blended (Field Rep: ₹24,874 · CME: ₹21,747 · Digital: ₹10,757) | Shift mix toward Digital Detailing; hold blended CAC flat or falling as volume scales | Monthly | `sql/10_cac_analysis.sql` |

### Distribution

| Metric | Definition | Current (synthetic) | Target | Cadence | Source |
|---|---|---|---|---|---|
| Stock availability % | Share of outlet-days in stock, post-relaunch average | Network median: 80.6%; several T1/T2 territories below 70% | ≥ network median in all Defend/Grow territories within Phase 1 (90 days) | Weekly (ops), monthly (reporting) | `notebooks/02_eda.ipynb` §2.6, `data/territory_data.csv` |
| Active distributor count | Distributors actively carrying DePURA per territory | Ramping since Sep 2025 relaunch | Full pre-recall distributor count restored in Defend territories by end of Phase 1 | Monthly | `data/sales_data.csv` (`distributor_count`) |

### Consumer

| Metric | Definition | Current (synthetic) | Target | Cadence | Source |
|---|---|---|---|---|---|
| Adherence score | Share of recommended dosing days actually given, existing customers | Health-conscious segment: 0.83; overall: ~0.60 | +0.3 to +0.8 packs/year per existing customer (Conservative → Base) | Quarterly (survey-based) | `notebooks/03_segmentation.ipynb` |
| Low-awareness segment awareness % | Share of Low-awareness consumers reached with education content | Baseline: 10.5% of parents in this segment | 10-45% of this segment reached over 12 months (Conservative → Upside) | Quarterly | `notebooks/05_scenario_model.ipynb` |
| Parent-audience blended CAC | Total parent-channel spend ÷ parent conversions | New acquisition: ₹908 blended · Retention (refill reminders): ₹23 | Shift incremental spend toward retention; hold new-acquisition CAC flat as channel mix optimizes | Monthly | `sql/09_conversion_funnel.sql`, `sql/10_cac_analysis.sql` |

### Territory

| Metric | Definition | Current (synthetic) | Target | Cadence | Source |
|---|---|---|---|---|---|
| Grow-territory penetration | Current sales ÷ market potential, Kolkata & Chennai | Kolkata: ~12.4% · Chennai: ~14.3% | Narrow gap toward the Defend-segment average (~20%) within 12 months | Quarterly | `outputs/tables/territory_segmented.csv` |
| Opportunity-rank stability | Spearman correlation of the top-10 territory ranking under weight perturbation | 0.945 minimum (validated once; re-check if underlying data changes materially) | Maintain ≥0.90 if the model is re-weighted or re-run on updated data | Ad hoc (on model refresh) | `notebooks/04_territory_analysis.ipynb` |

## 4. What this framework deliberately excludes

- **Brand market share.** Not publicly available and not modelled with confidence at brand level; tracking it would require real audit data (IQVIA/Pharmarack), not this project's synthetic dataset.
- **Vanity metrics** (impressions, followers) that don't map to a conversion or business outcome — every metric above ties to either revenue, a segment conversion, or an operational lever.
- **Single-point revenue forecasts.** The North Star target is deliberately a range (Conservative/Base/Upside), not a promised number — the scenario model explicitly does not claim forecasting precision (`notebooks/05_scenario_model.ipynb`).

## 5. Review cadence

| Review | Frequency | Owner (illustrative) | Key question |
|---|---|---|---|
| Distribution & stock check | Weekly | Field/ops | Are priority territories at or above target stock availability? |
| HCP & consumer CAC review | Monthly | Marketing | Is spend shifting toward the cheapest-CAC channels validated in this analysis? |
| Segment conversion review | Quarterly | Commercial lead | Are non-user HCPs and low-awareness consumers moving segments? |
| Full scenario re-check | Quarterly | Commercial lead | Is realised recovery tracking Conservative, Base, or Upside — and does the plan need to shift phase? |
| Territory model refresh | Semi-annual or on major data change | Analytics | Re-run the opportunity score and sensitivity test; confirm top territories are still stable |
