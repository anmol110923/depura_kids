"""
generate_data.py — SYNTHETIC DATA GENERATOR
===========================================

DePURA Kids Relaunch Strategy — independent case study.

Every row produced by this script is SIMULATED. It is not Sanofi or
Sanofi Consumer Healthcare India Ltd data and must never be presented as such.

Design principles
-----------------
1. Public facts shape the *structure* (recall timing, relaunch timing,
   15 ml MRP, directional regional/seasonal deficiency patterns).
2. Assumptions in config/data_generation.yaml set the *magnitudes*.
3. A small number of relationships are deliberately PLANTED so the
   analysis has something to find. Every planted relationship is listed in
   data/DATA_DICTIONARY.md so nobody mistakes a planted pattern for a
   real-world finding.
4. Realistic data-quality issues are injected on purpose for the cleaning
   notebook, and are also documented.

Run:  python scripts/generate_data.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
CONFIG = yaml.safe_load((ROOT / "config" / "data_generation.yaml").read_text())
RNG = np.random.default_rng(CONFIG["seed"])

# ---------------------------------------------------------------------------
# Territory master (36 synthetic sales territories named after real HQ cities)
# ---------------------------------------------------------------------------
TERRITORIES = [
    # territory, state, region, tier
    ("Delhi North", "Delhi", "North", "T1"),
    ("Delhi South", "Delhi", "North", "T1"),
    ("Noida-Ghaziabad", "Uttar Pradesh", "North", "T2"),
    ("Gurugram-Faridabad", "Haryana", "North", "T2"),
    ("Lucknow", "Uttar Pradesh", "North", "T2"),
    ("Kanpur-Agra", "Uttar Pradesh", "North", "T2"),
    ("Varanasi-Gorakhpur", "Uttar Pradesh", "North", "T3"),
    ("Chandigarh-Mohali", "Chandigarh", "North", "T2"),
    ("Ludhiana-Amritsar", "Punjab", "North", "T2"),
    ("Jaipur", "Rajasthan", "North", "T2"),
    ("Dehradun", "Uttarakhand", "North", "T3"),
    ("Mumbai West", "Maharashtra", "West", "T1"),
    ("Mumbai Thane", "Maharashtra", "West", "T1"),
    ("Pune", "Maharashtra", "West", "T1"),
    ("Nagpur", "Maharashtra", "West", "T2"),
    ("Ahmedabad", "Gujarat", "West", "T1"),
    ("Surat-Vadodara", "Gujarat", "West", "T2"),
    ("Rajkot", "Gujarat", "West", "T3"),
    ("Indore", "Madhya Pradesh", "Central", "T2"),
    ("Bhopal", "Madhya Pradesh", "Central", "T2"),
    ("Jabalpur", "Madhya Pradesh", "Central", "T3"),
    ("Raipur", "Chhattisgarh", "Central", "T3"),
    ("Bengaluru North", "Karnataka", "South", "T1"),
    ("Bengaluru South", "Karnataka", "South", "T1"),
    ("Mysuru-Mangaluru", "Karnataka", "South", "T3"),
    ("Chennai", "Tamil Nadu", "South", "T1"),
    ("Coimbatore-Madurai", "Tamil Nadu", "South", "T2"),
    ("Hyderabad", "Telangana", "South", "T1"),
    ("Vijayawada-Vizag", "Andhra Pradesh", "South", "T2"),
    ("Kochi-Trivandrum", "Kerala", "South", "T2"),
    ("Kolkata", "West Bengal", "East", "T1"),
    ("Siliguri-Durgapur", "West Bengal", "East", "T3"),
    ("Patna", "Bihar", "East", "T2"),
    ("Ranchi", "Jharkhand", "East", "T3"),
    ("Bhubaneswar", "Odisha", "East", "T2"),
    ("Guwahati", "Assam", "East", "T2"),
]


def u(lo: float, hi: float, size=None):
    """Uniform draw helper."""
    return RNG.uniform(lo, hi, size)


def clip01(x):
    return np.clip(x, 0.0, 1.0)


# ---------------------------------------------------------------------------
# 1. Latent territory attributes (drive everything downstream)
# ---------------------------------------------------------------------------
def build_territory_latents() -> pd.DataFrame:
    d = CONFIG["demand"]
    rows = []
    for i, (name, state, region, tier) in enumerate(TERRITORIES, start=1):
        cohort = u(*d["infant_cohort_thousands"][tier]) * 1000
        access = u(*d["private_access_share"][tier])
        supp = u(*d["supplementation_rate"]) * d["regional_deficiency_factor"][region]
        category_packs_year = cohort * access * supp * d["packs_per_supplemented_infant_year"]

        tier_density = {"T1": 1.0, "T2": 0.75, "T3": 0.55}[tier]
        hcp_universe = int(cohort / 1000 * u(4.5, 7.5) * tier_density + u(40, 120))
        pharmacy_count = int(cohort / 1000 * u(28, 45) * (1.15 - 0.2 * (tier == "T3")))

        # Commercial latents — drawn independently of potential on purpose,
        # so that some high-potential territories are under-served (PLANTED).
        coverage = u(0.25, 0.85)
        awareness_latent = clip01(RNG.normal(0.62 + 0.06 * (tier == "T1") - 0.05 * (tier == "T3"), 0.08))
        competitor_strength = clip01(RNG.normal(0.50 + 0.08 * (tier == "T1"), 0.15))
        pre_share = u(*CONFIG["brand_share"]["pre_recall_volume_share"]) * (0.8 + 0.4 * awareness_latent)

        # Post-relaunch recovery ceiling (share of pre-recall level regained)
        ceiling = np.clip(
            0.45 + 0.35 * coverage + 0.25 * (awareness_latent - 0.6)
            - 0.30 * (competitor_strength - 0.5) + RNG.normal(0, 0.05),
            0.35, 1.05,
        )
        speed = 0.20 + 0.30 * coverage
        distributors_base = int(np.clip(pharmacy_count / 300 + u(-1, 2), 3, 16))
        stock_pre = u(*CONFIG["supply"]["pre_recall_stock_mean"])
        stock_post = np.clip(
            u(*CONFIG["supply"]["post_relaunch_stock_mean"]) + 0.01 * (distributors_base - 8), 0.6, 0.97
        )

        rows.append(dict(
            territory_id=f"TR{i:02d}", territory=name, state=state, region=region, city_tier=tier,
            infant_cohort=cohort, category_packs_year=category_packs_year,
            hcp_count=hcp_universe, pharmacy_count=pharmacy_count,
            sales_force_coverage=round(coverage, 3), awareness_latent=awareness_latent,
            competitor_strength=round(competitor_strength, 3), pre_share=pre_share,
            recovery_ceiling=ceiling, recovery_speed=speed,
            distributors_base=distributors_base, stock_pre=stock_pre, stock_post=stock_post,
        ))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 2. Sales (month x territory x channel x product)
# ---------------------------------------------------------------------------
def build_sales(terr: pd.DataFrame) -> pd.DataFrame:
    cal = CONFIG["calendar"]
    months = pd.date_range(cal["start_month"], cal["end_month"], freq="MS")
    t_partial = pd.Timestamp(cal["recall_partial_month"])
    t_returns = pd.Timestamp(cal["recall_returns_month"])
    t_relaunch = pd.Timestamp(cal["relaunch_month"])
    ch = CONFIG["channels"]
    sup = CONFIG["supply"]
    seas = CONFIG["demand"]["seasonality"]
    net = CONFIG["pricing"]["net_realisation_of_mrp"]
    products = CONFIG["products"]

    records = []
    for _, t in terr.iterrows():
        cat_month = t.category_packs_year / 12
        tier = t.city_tier
        for m in months:
            months_from_start = (m.year - 2023) * 12 + m.month - 1
            growth = (1 + CONFIG["demand"]["pre_recall_yoy_growth"]) ** (months_from_start / 12)

            if m < t_partial:
                phase, share = "pre_recall", t.pre_share * growth
                stock_mean, dist = t.stock_pre, t.distributors_base
            elif m == t_partial:
                phase, share = "recall_partial", t.pre_share * growth * 0.55
                stock_mean, dist = t.stock_pre * 0.5, t.distributors_base
            elif m == t_returns:
                phase, share = "recall_returns", 0.0
                stock_mean, dist = 0.0, 0
            elif m < t_relaunch:
                phase, share = "off_market", 0.0
                stock_mean, dist = 0.0, 0
            else:
                k = (m.year - t_relaunch.year) * 12 + m.month - t_relaunch.month  # 0..11
                start = CONFIG["brand_share"]["relaunch_starting_recovery"]
                recovery = start + (t.recovery_ceiling - start) * (1 - np.exp(-t.recovery_speed * (k + 1)))
                phase, share = "post_relaunch", t.pre_share * growth * recovery
                stock_mean = t.stock_post * (0.78 + 0.22 * (1 - np.exp(-0.5 * (k + 1))))
                dist = int(round(t.distributors_base * (0.6 + 0.4 * (1 - np.exp(-0.4 * (k + 1))))))

            for c_idx, channel in enumerate(ch["names"]):
                c_share = ch["share_by_tier"][tier][c_idx]
                if phase == "post_relaunch" and channel == "E-Pharmacy":
                    c_share *= 1.25  # digital channel gains share post-relaunch (assumption)

                base_disc = ch["base_discount"][c_idx]
                for p_name, p in products.items():
                    sku_share = p["sku_share_t1"] if tier == "T1" else (
                        p["sku_share_t3"] if tier == "T3" else (p["sku_share_t1"] + p["sku_share_t3"]) / 2)

                    if phase in ("off_market",):
                        records.append((m, t, channel, p_name, 0, 0.0, np.nan, 0.0, 0))
                        continue
                    if phase == "recall_returns":
                        # Recalled stock returned: logged as negative units (realistic artefact)
                        if channel in ("Retail Chemist", "Pharmacy Chain"):
                            ret_units = -int(cat_month * t.pre_share * c_share * sku_share * u(0.25, 0.45))
                            records.append((m, t, channel, p_name, ret_units, ret_units * p["mrp"] * net,
                                            0.0, 0.0, 0))
                        else:
                            records.append((m, t, channel, p_name, 0, 0.0, np.nan, 0.0, 0))
                        continue

                    stock = clip01(stock_mean + RNG.normal(0, 0.035) + (0.03 if channel == "E-Pharmacy" else 0))
                    disc = base_disc + RNG.normal(0, 0.012)
                    if phase == "post_relaunch" and k < 4:
                        disc += ch["relaunch_trade_scheme_uplift"]
                    disc = float(np.clip(disc, 0, 0.30))

                    units = (cat_month * share * c_share * sku_share * seas[m.month]
                             * (stock ** sup["stock_units_elasticity"])
                             * (1 + ch["discount_units_elasticity"] * (disc - base_disc))
                             * RNG.lognormal(0, 0.12))
                    units = int(max(units, 0))
                    revenue = units * p["mrp"] * net * (1 - disc)
                    records.append((m, t, channel, p_name, units, revenue, disc, stock, dist))

    sales = pd.DataFrame([
        dict(date=r[0].strftime("%Y-%m-%d"), territory_id=r[1].territory_id, territory=r[1].territory,
             region=r[1].region, state=r[1].state, city_tier=r[1].city_tier, channel=r[2], product=r[3],
             units_sold=r[4], revenue=round(r[5], 2),
             discount_pct=None if (isinstance(r[6], float) and np.isnan(r[6])) else round(r[6], 4),
             stock_availability=round(r[7], 3), distributor_count=r[8])
        for r in records
    ])
    return sales


# ---------------------------------------------------------------------------
# 3. HCP sample (CRM / survey-style sample, not a census)
# ---------------------------------------------------------------------------
COMPETITOR_BRANDS = ["Arachitol Kids", "Kidrich D3 Nano", "Uprise-D3", "D3 Must Forte", "Ultra D3", "Other / Generic"]
COMP_PROBS = {
    "T1": [0.34, 0.16, 0.20, 0.12, 0.08, 0.10],
    "T2": [0.26, 0.10, 0.25, 0.17, 0.10, 0.12],
    "T3": [0.16, 0.05, 0.28, 0.22, 0.13, 0.16],
}


def build_hcp(terr: pd.DataFrame) -> pd.DataFrame:
    n = CONFIG["samples"]["hcp_rows"]
    weights = terr.hcp_count / terr.hcp_count.sum()
    t_idx = RNG.choice(len(terr), size=n, p=weights)
    specialties = RNG.choice(
        ["Pediatrician", "General Practitioner", "Obstetrician-Gynecologist", "Neonatologist"],
        size=n, p=[0.55, 0.25, 0.12, 0.08])
    vol_median = {"Pediatrician": 320, "General Practitioner": 140, "Obstetrician-Gynecologist": 110, "Neonatologist": 190}
    spec_boost = {"Pediatrician": 0.35, "General Practitioner": -0.45, "Obstetrician-Gynecologist": -0.25, "Neonatologist": 0.15}

    rows = []
    for i in range(n):
        t = terr.iloc[t_idx[i]]
        spec = specialties[i]
        years = int(np.clip(RNG.gamma(3.0, 5.0), 1, 40))
        volume = int(RNG.lognormal(np.log(vol_median[spec]), 0.45) * (1.1 if t.city_tier == "T1" else 1.0))

        cat_aw = int(np.clip(round(RNG.normal(4.3 if spec != "General Practitioner" else 3.4, 0.7)), 1, 5))
        brand_aw = int(np.clip(round(RNG.normal(1 + 4 * t.awareness_latent + (0.3 if spec == "Pediatrician" else -0.2), 0.8)), 1, 5))
        digital = clip01(RNG.normal(0.72 - 0.012 * years, 0.15))
        pre_prescriber = RNG.random() < (0.55 if spec in ("Pediatrician", "Neonatologist") else 0.30)

        # Rep visits: PLANTED weak link to volume (call plans poorly aligned to opportunity)
        rep_visits = int(np.clip(RNG.poisson(1 + 7 * t.sales_force_coverage + 0.002 * volume), 0, 15))

        # Recommendation-rate model (PLANTED). Patient volume intentionally has NO effect.
        comp_loyal = RNG.random() < 0.30 + 0.35 * t.competitor_strength
        logit = (-2.4 + 0.55 * (brand_aw - 3) + 0.95 * pre_prescriber
                 + 0.55 * np.log1p(rep_visits) / np.log1p(8)   # diminishing returns
                 + 0.35 * digital + spec_boost[spec]
                 - 0.80 * comp_loyal - 0.6 * (t.competitor_strength - 0.5)
                 + RNG.normal(0, 0.45))
        rec_rate = float(1 / (1 + np.exp(-logit)))

        if rec_rate >= 0.60 and RNG.random() < 0.5:
            comp_pref = "No alternative (DePURA loyal)"
        else:
            comp_pref = RNG.choice(COMPETITOR_BRANDS, p=COMP_PROBS[t.city_tier])

        rows.append(dict(
            hcp_id=f"HCP{i + 1:05d}", specialty=spec, territory_id=t.territory_id, region=t.region,
            city_tier=t.city_tier, years_in_practice=years, monthly_patient_volume=volume,
            category_awareness=cat_aw, brand_awareness=brand_aw, recommendation_rate=round(rec_rate, 3),
            digital_engagement=round(float(digital), 3), rep_visits_last_quarter=rep_visits,
            pre_recall_prescriber=bool(pre_prescriber), competitor_preference=comp_pref,
        ))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 4. Consumer (parent) survey sample
# ---------------------------------------------------------------------------
def build_consumers(terr: pd.DataFrame) -> pd.DataFrame:
    n = CONFIG["samples"]["consumer_rows"]
    weights = terr.infant_cohort / terr.infant_cohort.sum()
    t_idx = RNG.choice(len(terr), size=n, p=weights)
    rows = []
    for i in range(n):
        t = terr.iloc[t_idx[i]]
        tier = t.city_tier
        child_age = RNG.choice(["0-12 months", "1-5 years", "6-12 years", "13-18 years"], p=[0.46, 0.30, 0.19, 0.05])
        parent_age = RNG.choice(["18-24", "25-29", "30-34", "35-39", "40+"], p=[0.08, 0.30, 0.34, 0.19, 0.09])
        income = RNG.choice(["<25k", "25k-50k", "50k-1L", ">1L"],
                            p={"T1": [0.10, 0.25, 0.35, 0.30], "T2": [0.20, 0.35, 0.30, 0.15], "T3": [0.35, 0.38, 0.20, 0.07]}[tier])
        young = parent_age in ("18-24", "25-29")

        src_p = np.array([0.52, 0.14, 0.14, 0.16 if young else 0.08, 0.08])
        source = RNG.choice(["Pediatrician", "Pharmacist", "Family/Friends", "Online/Social media", "Gynecologist"],
                            p=src_p / src_p.sum())
        ch_p = {"T1": [0.34, 0.20, 0.08, 0.24, 0.14], "T2": [0.48, 0.14, 0.10, 0.18, 0.10], "T3": [0.66, 0.06, 0.12, 0.10, 0.06]}[tier]
        channel = RNG.choice(["Retail Chemist", "Pharmacy Chain", "Hospital Pharmacy", "E-Pharmacy", "Quick Commerce"], p=ch_p)

        aware_recall = RNG.random() < (0.12 + 0.10 * (tier == "T1") + 0.10 * (source == "Online/Social media")
                                       + 0.06 * (channel in ("E-Pharmacy", "Quick Commerce")))
        awareness = int(np.clip(round(RNG.normal(1.3 + 3.3 * t.awareness_latent + 0.6 * (source == "Pediatrician"), 0.9)), 1, 5))
        price_sens = int(np.clip(round(RNG.normal(3.0 + 0.8 * (income == "<25k") + 0.4 * (income == "25k-50k")
                                                  - 0.6 * (income == ">1L") + 0.3 * (tier == "T3"), 0.8)), 1, 5))
        trust = int(np.clip(round(RNG.normal(3.7 - 0.9 * aware_recall + 0.5 * (source == "Pediatrician"), 0.8)), 1, 5))
        # Adherence (PLANTED): pediatrician source and infants adhere better
        adherence = clip01(RNG.normal(0.52 + 0.14 * (source == "Pediatrician") + 0.10 * (child_age == "0-12 months")
                                      + 0.05 * (channel == "E-Pharmacy") - 0.03 * (price_sens - 3), 0.15))
        freq = ("Monthly" if adherence >= 0.70 else "Every 2-3 months" if adherence >= 0.50
                else "Occasionally" if adherence >= 0.30 else "One-time")

        logit = (-2.4 + 0.55 * (awareness - 3) + 0.45 * (trust - 3) - 0.35 * (price_sens - 3)
                 + 0.6 * (source == "Pediatrician") + RNG.normal(0, 0.5))
        p_depura = 1 / (1 + np.exp(-logit))
        r = RNG.random()
        current_brand = "DePURA Kids" if r < p_depura else ("Other brand" if r < p_depura + 0.75 * (1 - p_depura) else "Not currently buying")

        rows.append(dict(
            consumer_id=f"CON{i + 1:05d}", child_age_group=child_age, region=t.region, city_tier=tier,
            parent_age_group=parent_age, income_band=income, awareness=awareness, purchase_channel=channel,
            purchase_frequency=freq, price_sensitivity=price_sens, brand_trust=trust,
            recommendation_source=source, adherence_score=round(float(adherence), 3),
            aware_of_recall=bool(aware_recall), current_brand=current_brand,
        ))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 5. Competitor table — public fields + clearly separated analyst scores
# ---------------------------------------------------------------------------
def build_competitors() -> pd.DataFrame:
    # Public fields from research/competitor_analysis.md (snapshot, see sources).
    # iu_per_ml = None where not verified. differentiation_score is SYNTHETIC.
    rows = [
        # brand, manufacturer/marketer, dosage, formulation, pack_ml, mrp, iu_per_ml, verification,
        # positioning (assessment), target_segment (assessment), channel_presence (assessment), diff_score (synthetic)
        ("DePURA Kids", "Sanofi Consumer Healthcare India Ltd", "400 IU / 0.5 ml", "Oral solution drops (nano droplet claim)", 15, 190.00, 800,
         "Strength: official; MRP: pharmacy listing", "Premium, pediatrician-led infant supplementation", "Infants 0-12 m, urban", "Chemist + chains + e-pharmacy", 7.5),
        ("Arachitol Kids / Nano", "Abbott India Ltd", "400 IU / 0.5 ml", "Oral solution drops (nano droplet)", 15, 199.28, 800,
         "Strength: Abbott site; MRP: pharmacy listing", "Premium, pediatrician-led", "Infants and young children, urban", "Chemist + chains + e-pharmacy", 7.8),
        ("Kidrich D3 800 IU Nano", "Dr. Reddy's Laboratories Ltd", "800 IU / ml", "Oral drops (nano)", 15, 199.50, 800,
         "Strength & MRP: pharmacy listing", "Premium nano challenger", "Infants and young children, urban", "Chemist + e-pharmacy", 6.5),
        ("Uprise-D3 Drops", "Alkem Laboratories Ltd", "400 IU / 0.5 ml (retailer-reported)", "Oral drops", 15, 110.60, 800,
         "MRP: pharmacy listing; strength: retailer-reported, UNVERIFIED", "Mid-price, broad HCP reach", "Infants and children, T2/T3 reach", "Chemist-heavy", 6.0),
        ("D3 Must Forte", "Mankind Pharma Ltd", "800 IU / ml", "Oral drops", 15, 99.58, 800,
         "Strength & MRP: pharmacy listing", "Mid/value, mass reach", "Children, T2/T3", "Chemist-heavy", 5.5),
        ("D3 Must Drops", "Mankind Pharma Ltd", "UNVERIFIED", "Oral drops", 15, 43.84, None,
         "MRP: pharmacy listing (varies by site); strength UNVERIFIED", "Value", "Price-sensitive parents", "Chemist-heavy", 4.5),
        ("Ultra D3 Drops", "Meyer Organics Pvt Ltd", "400 IU / ml", "Oral drops, sugar-free, pineapple flavour", 30, 71.25, 400,
         "Strength & claims: Meyer site; MRP: pharmacy listing", "Value, taste & sugar-free claims", "Infants, price-conscious", "Chemist", 5.0),
        ("Oh D3 Drops", "Indoco Remedies Ltd", "UNVERIFIED", "Oral drops", 15, 33.86, None,
         "MRP: pharmacy listing; strength UNVERIFIED", "Value", "Price-sensitive parents", "Chemist", 4.0),
    ]
    df = pd.DataFrame(rows, columns=[
        "brand", "manufacturer", "dosage", "formulation", "pack_size_ml", "price", "iu_per_ml", "public_data_verification",
        "positioning", "target_segment", "channel_presence", "differentiation_score"])
    df["daily_400iu_doses_per_pack"] = (df.pack_size_ml * df.iu_per_ml / 400).round(0)
    df["cost_per_400iu_dose"] = (df.price / df.daily_400iu_doses_per_pack).round(2)
    ref = df.loc[df.brand == "DePURA Kids", "cost_per_400iu_dose"].iloc[0]
    df["estimated_price_index"] = (df.cost_per_400iu_dose / ref * 100).round(0)
    df["pack_size"] = df.pack_size_ml.astype(int).astype(str) + " ml"
    df["assessment_columns_note"] = "positioning/target_segment/channel_presence = analyst assessment; differentiation_score = SYNTHETIC"
    return df[["brand", "manufacturer", "dosage", "formulation", "pack_size", "pack_size_ml", "price", "iu_per_ml",
               "daily_400iu_doses_per_pack", "cost_per_400iu_dose", "estimated_price_index", "positioning",
               "target_segment", "channel_presence", "differentiation_score", "public_data_verification",
               "assessment_columns_note"]]


# ---------------------------------------------------------------------------
# 6. Campaigns (12 post-relaunch months x 10 channels)
# ---------------------------------------------------------------------------
CAMPAIGN_CHANNELS = [
    # channel, audience, monthly spend range (INR), impr per ₹, CTR, lead rate, conv rate, conversion definition
    # Spend ranges sized so 12-month total lands at roughly 12-18% of
    # annual post-relaunch revenue (a defensible relaunch-year marketing
    # intensity for a consumer healthcare brand) -- see
    # data/DATA_DICTIONARY.md for the reconciliation check.
    ("Field Rep Detailing", "HCP", (1.4e5, 2.1e5), 0.0012, 0.55, 0.30, 0.20, "HCP starts/resumes recommending"),
    ("HCP Digital Detailing & Webinars", "HCP", (4.0e4, 7.0e4), 0.02, 0.18, 0.22, 0.14, "HCP starts/resumes recommending"),
    ("CME / Medical Conferences", "HCP", (4.5e4, 9.0e4), 0.004, 0.40, 0.25, 0.12, "HCP starts/resumes recommending"),
    ("Pharmacist Trade Program", "Pharmacist", (3.0e4, 6.0e4), 0.010, 0.35, 0.40, 0.30, "Outlet re-stocks and recommends"),
    ("Paid Social (Meta)", "Parents", (6.5e4, 1.2e5), 9.0, 0.011, 0.07, 0.10, "First purchase"),
    ("YouTube / Video", "Parents", (4.5e4, 9.0e4), 11.0, 0.006, 0.05, 0.08, "First purchase"),
    ("Search Ads", "Parents", (2.2e4, 4.5e4), 1.6, 0.045, 0.12, 0.14, "First purchase"),
    ("E-Pharmacy Sponsored Listings", "Parents", (2.5e4, 5.0e4), 2.2, 0.030, 0.25, 0.28, "First purchase"),
    ("Parenting Communities & Creators", "Parents", (2.2e4, 5.0e4), 6.0, 0.014, 0.06, 0.09, "First purchase"),
    ("WhatsApp / CRM Refill Reminders", "Parents (existing)", (5.0e3, 1.3e4), 1.5, 0.22, 0.35, 0.40, "Repeat purchase (retention)"),
]


def build_campaigns() -> pd.DataFrame:
    months = pd.date_range(CONFIG["calendar"]["relaunch_month"], CONFIG["calendar"]["end_month"], freq="MS")
    rows, cid = [], 1
    for m in months:
        for ch, aud, spend_rng, impr_per_rupee, ctr, lead_rate, conv_rate, conv_def in CAMPAIGN_CHANNELS:
            spend = u(*spend_rng)
            # PLANTED diminishing returns: efficiency falls as spend rises within a channel
            spend_pos = (spend - spend_rng[0]) / (spend_rng[1] - spend_rng[0])
            eff = 1.15 - 0.30 * spend_pos
            impressions = int(spend * impr_per_rupee * RNG.lognormal(0, 0.10))
            clicks = int(impressions * ctr * RNG.lognormal(0, 0.12) * eff)
            leads = int(clicks * lead_rate * RNG.lognormal(0, 0.12))
            conversions = max(int(leads * conv_rate * RNG.lognormal(0, 0.15) * eff), 1)
            rows.append(dict(
                campaign_id=f"CMP{cid:04d}", month=m.strftime("%Y-%m-%d"), channel=ch, audience=aud,
                region="All-India", impressions=impressions, clicks=clicks, leads=leads, conversions=conversions,
                spend=round(spend, 0), engagement_rate=round(clicks / impressions, 4) if impressions else 0,
                conversion_rate=round(conversions / leads, 4) if leads else 0, cac=round(spend / conversions, 2),
                conversion_definition=conv_def,
            ))
            cid += 1
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 7. Territory table (derived from sales + HCP so joins reconcile)
# ---------------------------------------------------------------------------
def build_territory_table(terr: pd.DataFrame, sales: pd.DataFrame, hcp: pd.DataFrame) -> pd.DataFrame:
    s = sales.copy()
    s["date"] = pd.to_datetime(s["date"])
    post = s[s.date >= CONFIG["calendar"]["relaunch_month"]]
    current = post.groupby("territory_id").revenue.sum() / 1e5  # INR lakh, 12 post-relaunch months

    # Growth = last 3 months vs previous 3 months, on SEASONALLY ADJUSTED revenue
    # (revenue divided by the category seasonality index in the config).
    seas = CONFIG["demand"]["seasonality"]
    post = post.assign(rev_sa=post.revenue / post.date.dt.month.map(seas))
    recent = post[post.date >= "2026-06-01"].groupby("territory_id").rev_sa.sum()
    prior = post[(post.date >= "2026-03-01") & (post.date < "2026-06-01")].groupby("territory_id").rev_sa.sum()
    growth = (recent / prior - 1)

    stock = post.groupby("territory_id").stock_availability.mean()
    aw = hcp.groupby("territory_id").brand_awareness.mean() / 5

    p = CONFIG["pricing"]
    potential = terr.set_index("territory_id").category_packs_year * p["avg_category_mrp_per_pack"] * p["net_realisation_of_mrp"] / 1e5

    out = terr[["territory_id", "territory", "state", "region", "city_tier", "hcp_count", "pharmacy_count",
                "competitor_strength", "sales_force_coverage"]].set_index("territory_id")
    out["current_sales"] = current.round(2)
    out["market_potential"] = potential.round(2)
    out["brand_awareness"] = aw.round(3)
    out["growth_rate"] = growth.round(4)
    out["stock_availability_avg"] = stock.round(3)
    cols = ["territory", "state", "region", "city_tier", "hcp_count", "pharmacy_count", "current_sales",
            "market_potential", "brand_awareness", "competitor_strength", "sales_force_coverage",
            "growth_rate", "stock_availability_avg"]
    return out[cols].reset_index()


# ---------------------------------------------------------------------------
# 8. Deliberate data-quality issues (documented in DATA_DICTIONARY.md)
# ---------------------------------------------------------------------------
def inject_quality_issues(sales, hcp, consumers):
    q = CONFIG["data_quality_issues"]
    sales = sales.copy()
    active = sales.index[sales.units_sold > 0]
    miss = RNG.choice(active, int(len(sales) * q["sales_missing_discount_rate"]), replace=False)
    sales.loc[miss, "discount_pct"] = None
    label_noise = {"Delhi": "NCT of Delhi", "Tamil Nadu": "Tamil nadu", "Uttar Pradesh": "UP", "Maharashtra": "maharashtra"}
    noisy = RNG.choice(sales.index, int(len(sales) * q["sales_state_label_noise_rate"]), replace=False)
    sales.loc[noisy, "state"] = sales.loc[noisy, "state"].map(lambda s: label_noise.get(s, s))
    dups = sales.loc[RNG.choice(active, int(len(sales) * q["sales_duplicate_rate"]), replace=False)]
    sales = pd.concat([sales, dups]).sort_values(["date", "territory_id", "channel", "product"]).reset_index(drop=True)

    hcp = hcp.copy()
    hcp.loc[RNG.choice(hcp.index, int(len(hcp) * q["hcp_missing_digital_rate"]), replace=False), "digital_engagement"] = None
    hcp.loc[RNG.choice(hcp.index, q["hcp_volume_entry_errors"], replace=False), "monthly_patient_volume"] = 9999

    consumers = consumers.copy()
    consumers["price_sensitivity"] = consumers["price_sensitivity"].astype("Int64")
    consumers.loc[RNG.choice(consumers.index, int(len(consumers) * q["consumer_missing_price_sensitivity_rate"]),
                             replace=False), "price_sensitivity"] = pd.NA
    return sales, hcp, consumers


def main():
    DATA_DIR.mkdir(exist_ok=True)
    terr = build_territory_latents()
    sales_clean = build_sales(terr)
    hcp_clean = build_hcp(terr)
    consumers_clean = build_consumers(terr)
    territory = build_territory_table(terr, sales_clean, hcp_clean)  # derived BEFORE noise
    competitors = build_competitors()
    campaigns = build_campaigns()
    sales, hcp, consumers = inject_quality_issues(sales_clean, hcp_clean, consumers_clean)

    outputs = {
        "sales_data.csv": sales, "hcp_data.csv": hcp, "consumer_data.csv": consumers,
        "competitor_data.csv": competitors, "campaign_data.csv": campaigns, "territory_data.csv": territory,
    }
    for name, df in outputs.items():
        df.to_csv(DATA_DIR / name, index=False)
        print(f"  wrote data/{name:<22} {len(df):>6,} rows  {df.shape[1]:>2} cols")
    print("\nAll files are SYNTHETIC / SIMULATED. See data/DATA_DICTIONARY.md.")


if __name__ == "__main__":
    main()
