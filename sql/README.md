# SQL Analysis — DePURA Kids Relaunch

All queries run against the **SYNTHETIC** data in `../data/` via DuckDB. Every file has been executed against the actual dataset; the numbers quoted below are real outputs of these queries on this synthetic data (not illustrative placeholders) — but they describe a simulated brand, not Sanofi's actual performance.

## Setup

```bash
pip install duckdb
python3 -c "
import duckdb
con = duckdb.connect('depura.db')
con.execute(open('00_setup.sql').read())
"
# then run any numbered file, e.g.:
python3 -c "
import duckdb
con = duckdb.connect('depura.db')
print(con.execute(open('05_growth_rate_analysis.sql').read().split(';')[0]).fetchdf())
"
```

`00_setup.sql` must run first — it loads the six CSVs into DuckDB tables and builds two cleaned views (`sales`, `sales_active`) that every other file depends on. Cleaning includes: de-duplicating 63 planted duplicate rows, canonicalising 4 state-label variants, nulling 6 planted HCP data-entry errors, and tagging each sales row with a `market_phase` (pre_recall / recall_partial / recall_returns / off_market / post_relaunch).

## Files and what each answers

| File | Business question | Headline output |
|---|---|---|
| `01_monthly_sales_trends.sql` | How has demand moved, and how close is recovery to baseline? | Seasonally adjusted post-relaunch run-rate is **~78% of the pre-recall baseline** |
| `02_region_wise_revenue.sql` | Which regions/tiers over- or under-index vs their category potential? | South is over-indexed (1.15×); East is under-indexed (0.83×); T1 alone is 62% of revenue |
| `03_product_wise_performance.sql` | Has the 15 ml / 10 ml pack mix shifted since relaunch? | No material shift (±0.4 pt) — pack preference is stable |
| `04_channel_contribution.sql` | Which channel gained share since relaunch? | E-Pharmacy +2.8 points; Retail Chemist -2.1 points |
| `05_growth_rate_analysis.sql` | Is the recovery still accelerating or has it plateaued? | MoM growth fell from **+32% (month 1) to ~0% (month 12)** — recovery has plateaued |
| `06_top_bottom_territories.sql` | Top/bottom by revenue, and which large markets look fine on revenue but are actually under-penetrated? | **Kolkata** is the #2 market by potential but ranks 30th of 36 on penetration |
| `07_hcp_recommendation_analysis.sql` | What drives HCP recommendation — and does patient volume actually matter? | Raw volume-recommendation correlation is 0.28, but drops to **~0 within every specialty** — a confounded, not causal, relationship |
| `08_customer_segmentation.sql` | Which consumer segments favour DePURA most/least? | Health-conscious segment: 39% DePURA share, 0.83 adherence; Low-awareness segment: 12% share |
| `09_conversion_funnel.sql` | Where does each audience's funnel leak? | Parent CAC ₹908 blended; HCP CAC ₹19,434; **refill-reminder CAC only ₹23** |
| `10_cac_analysis.sql` | Best CAC channel per audience; does spend correlate with rising CAC? | E-Pharmacy listings cheapest parent channel (₹242); 9 of 10 channels show positive spend-vs-CAC correlation (diminishing returns) |
| `11_market_opportunity_ranking.sql` | Top 10 territories on the weighted opportunity score | Chennai ranks #1 — high potential, low penetration, moderate competition |
| `12_stock_availability_vs_sales.sql` | Does stock availability actually move units? | Units index rises from **0.89 (stock <70%) to 1.08 (stock 90%+)** — a ~20% swing |
| `13_competitor_price_comparison.sql` | DePURA's position on price — pack MRP vs cost per equivalent dose | DePURA is 3rd-cheapest premium brand; mid-price brands cost ~52-58% per dose; value tier ~38% |
| `14_territory_prioritization.sql` | Defend / Grow / Build / Deprioritize segmentation | 12 Defend, 6 Grow (incl. Kolkata, Chennai), 8 Build, 10 Deprioritize |

## Techniques demonstrated

CTEs (every file) · window functions (`LAG`, `RANK`, `NTILE`, `QUALIFY`, rolling `SUM`/`AVG` with frame clauses) · `CASE` for segmentation logic · aggregations with `FILTER`-style conditional `SUM`/`AVG` · `CORR()` for confounder checks · self-normalising min-max scoring · median-split segmentation.

## Known confounders addressed in the SQL itself (not just discussed later)

- **07**: volume-vs-recommendation is checked both pooled and within-specialty in the same file, so the confounding is visible in the query output, not asserted separately.
- **12**: stock-vs-units is computed as a within-series index, not a raw pooled correlation, to avoid territory-size confounding.
- **13**: pack-price ranking and dose-cost ranking are shown side by side specifically to demonstrate why the metric choice matters.
