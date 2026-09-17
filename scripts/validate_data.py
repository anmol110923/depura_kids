"""
validate_data.py — checks that the SYNTHETIC datasets are internally consistent
and that each documented planted relationship is recoverable.

Why this exists: if the data were silently broken (a join key missing, the
recall window not zeroed, a planted effect not present) every downstream
insight would be wrong. A consulting team would run checks like these before
any analysis.

Run:  python scripts/validate_data.py
"""

from pathlib import Path
import sys

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"
results = []


def check(name: str, passed: bool, detail: str = ""):
    results.append(passed)
    print(f"  [{'PASS' if passed else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))


sales = pd.read_csv(DATA / "sales_data.csv", parse_dates=["date"])
hcp = pd.read_csv(DATA / "hcp_data.csv")
cons = pd.read_csv(DATA / "consumer_data.csv")
comp = pd.read_csv(DATA / "competitor_data.csv")
camp = pd.read_csv(DATA / "campaign_data.csv")
terr = pd.read_csv(DATA / "territory_data.csv")

print("\n1. Schema & keys")
required = {
    "sales": (sales, ["date", "region", "state", "city_tier", "channel", "product", "units_sold", "revenue",
                      "discount_pct", "stock_availability", "distributor_count", "territory_id"]),
    "hcp": (hcp, ["hcp_id", "specialty", "region", "city_tier", "monthly_patient_volume", "category_awareness",
                  "brand_awareness", "recommendation_rate", "digital_engagement", "competitor_preference", "territory_id"]),
    "consumer": (cons, ["consumer_id", "child_age_group", "region", "city_tier", "parent_age_group", "awareness",
                        "purchase_channel", "purchase_frequency", "price_sensitivity", "brand_trust",
                        "recommendation_source", "adherence_score"]),
    "competitor": (comp, ["brand", "manufacturer", "dosage", "formulation", "pack_size", "price",
                          "estimated_price_index", "positioning", "target_segment", "channel_presence",
                          "differentiation_score"]),
    "campaign": (camp, ["campaign_id", "channel", "audience", "impressions", "clicks", "leads", "conversions",
                        "spend", "engagement_rate", "conversion_rate", "cac"]),
    "territory": (terr, ["territory", "state", "city_tier", "hcp_count", "pharmacy_count", "current_sales",
                         "market_potential", "brand_awareness", "competitor_strength", "sales_force_coverage"]),
}
for name, (df, cols) in required.items():
    missing = [c for c in cols if c not in df.columns]
    check(f"{name}: all brief-specified columns present", not missing, f"missing={missing}" if missing else "")
check("sales.territory_id all exist in territory_data", set(sales.territory_id) <= set(terr.territory_id))
check("hcp.territory_id all exist in territory_data", set(hcp.territory_id) <= set(terr.territory_id))
check("hcp_id unique", hcp.hcp_id.is_unique)
check("consumer_id unique", cons.consumer_id.is_unique)

print("\n2. Public-fact structure (recall & relaunch timing)")
off = sales[(sales.date >= "2024-05-01") & (sales.date < "2025-09-01")]
check("zero units while off-market (May 2024 - Aug 2025)", (off.units_sold == 0).all())
apr = sales[sales.date == "2024-04-01"]
check("recall returns logged as negative units in Apr 2024", (apr.units_sold < 0).any())
check("sales resume in Sep 2025", sales[sales.date == "2025-09-01"].units_sold.sum() > 0)

print("\n3. Deliberate data-quality issues are present (for the cleaning notebook)")
key = ["date", "territory_id", "channel", "product"]
check("duplicate sales rows exist", sales.duplicated(key).sum() > 0, f"{sales.duplicated(key).sum()} dups")
check("state label inconsistencies exist", sales.state.isin(["NCT of Delhi", "Tamil nadu", "UP", "maharashtra"]).any())
check("HCP volume entry errors (9999) exist", (hcp.monthly_patient_volume == 9999).sum() > 0)

print("\n4. Reconciliation")
clean = sales.drop_duplicates(key)
post = clean[clean.date >= "2025-09-01"].groupby("territory_id").revenue.sum() / 1e5
merged = terr.set_index("territory_id").current_sales
check("territory current_sales reconciles to de-duplicated sales (±0.5%)",
      np.allclose(post.reindex(merged.index), merged, rtol=0.005))

print("\n5. Planted relationships are recoverable")
active = clean[(clean.units_sold > 0) & (clean.date >= "2025-09-01")].copy()
active["units_dm"] = active.units_sold / active.groupby(["territory_id", "channel", "product"]).units_sold.transform("mean")
r = active.stock_availability.corr(active.units_dm)
check("stock availability ↑ → units ↑ (within territory-channel-SKU)", r > 0.2, f"r={r:.2f}")

h = hcp[hcp.monthly_patient_volume < 9999]
r = h.brand_awareness.corr(h.recommendation_rate)
check("HCP brand awareness ↑ → recommendation ↑", r > 0.3, f"r={r:.2f}")
diff = h.groupby("pre_recall_prescriber").recommendation_rate.mean()
check("pre-recall prescribers recommend more", diff[True] > diff[False] + 0.1, f"{diff[True]:.2f} vs {diff[False]:.2f}")
within = h.groupby("specialty").apply(lambda d: d.recommendation_rate.corr(d.monthly_patient_volume), include_groups=False)
check("patient volume NOT related to recommendation within specialty (|r|<0.15)", within.abs().max() < 0.15,
      f"max |r|={within.abs().max():.2f}")
r = h.rep_visits_last_quarter.corr(h.monthly_patient_volume)
check("rep visits weakly aligned to patient volume (r<0.3)", r < 0.3, f"r={r:.2f}")

t = cons.groupby("aware_of_recall").brand_trust.mean()
check("recall-aware parents report lower trust", t[True] < t[False] - 0.5, f"{t[True]:.2f} vs {t[False]:.2f}")
a = cons.groupby("recommendation_source").adherence_score.mean()
check("pediatrician-sourced parents adhere better", a["Pediatrician"] == a.max(), f"{a['Pediatrician']:.2f}")

within_camp = camp.groupby("channel").apply(lambda d: d.spend.corr(d.cac), include_groups=False)
check("diminishing returns: CAC rises with spend in most channels", (within_camp > 0).mean() >= 0.7,
      f"{(within_camp > 0).mean():.0%} of channels")

print("\n6. Competitor normalisation")
ref = comp.loc[comp.brand == "DePURA Kids", "cost_per_400iu_dose"].iloc[0]
check("DePURA Kids cost per 400 IU dose = ₹190/30", abs(ref - 190 / 30) < 0.01, f"₹{ref}")
check("unverified strengths left blank, not guessed", comp.loc[comp.dosage == "UNVERIFIED", "iu_per_ml"].isna().all())

print("\n7. Cross-table plausibility (campaign spend vs revenue)")
annual_spend = camp.spend.sum()
annual_revenue = clean[(clean.date >= "2025-09-01") & (clean.units_sold > 0)].revenue.sum()
spend_ratio = annual_spend / annual_revenue
check("annual marketing spend is a plausible share of annual revenue (5%-30%)",
      0.05 <= spend_ratio <= 0.30, f"{spend_ratio:.1%}")

n_fail = results.count(False)
print(f"\n{len(results) - n_fail}/{len(results)} checks passed.")
sys.exit(1 if n_fail else 0)
