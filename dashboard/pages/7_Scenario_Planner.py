"""Page 7 — Scenario Planner (interactive)

Reproduces the driver-based model from notebooks/05_scenario_model.ipynb so
the sliders compute live. The elasticities and baseline are identical to the
notebook — this page is an interactive front-end on the same model, not a
different one.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.data import load_all, synthetic_banner, seasonally_adjusted_monthly

st.set_page_config(page_title="Scenario Planner", page_icon="🎛️", layout="wide")

st.title("🎛️ Scenario Planner")
synthetic_banner()

st.markdown(
    "**Illustrative scenario model based on synthetic assumptions — not a Sanofi forecast.** "
    "Adjust the five levers below to see the implied revenue and unit impact. The elasticities connecting "
    "each lever to revenue are stated judgements (see `notebooks/05_scenario_model.ipynb` for the full "
    "reasoning and grounding for each one), not derived from a regression."
)

data = load_all()
sales = data["sales"]
hcp = data["hcp"]
consumer = data["consumer"]
campaign = data["campaign"]

# ---------------------------------------------------------------------------
# Baseline (identical calculation to notebook 05)
# ---------------------------------------------------------------------------
post = sales[sales.market_phase == "post_relaunch"]
latest3 = post[post.date >= post.date.max() - pd.DateOffset(months=2)]
baseline_annual_revenue = latest3.groupby("date").revenue.sum().mean() * 12
baseline_annual_units = latest3.groupby("date").units_sold.sum().mean() * 12
baseline_annual_spend = campaign.spend.sum()

hcp_nonuser_share = (hcp.hcp_segment == "High-volume non/under-user").mean()
consumer_low_awareness_share = (consumer.consumer_segment == "Low-awareness").mean()

monthly = seasonally_adjusted_monthly(sales)
pre_recall_annual = monthly.loc[
    (monthly.date >= "2023-03-01") & (monthly.date < "2024-03-01"), "revenue_sa"
].mean() * 12

ELASTICITIES = {
    "hcp_conversion_to_revenue": 0.55,
    "stock_pt_to_units": 0.008,
    "awareness_conversion_to_revenue": 0.35,
    "adherence_packs_to_revenue": 0.10,
    "marketing_spend_elasticity": 0.25,
}

PRESETS = {
    "Conservative": dict(hcp_conversion_pct=0.10, stock_availability_pts=3, awareness_conversion_pct=0.10,
                          adherence_packs_delta=0.3, marketing_spend_change=0.00),
    "Base": dict(hcp_conversion_pct=0.25, stock_availability_pts=8, awareness_conversion_pct=0.25,
                 adherence_packs_delta=0.8, marketing_spend_change=0.15),
    "Upside": dict(hcp_conversion_pct=0.45, stock_availability_pts=14, awareness_conversion_pct=0.45,
                   adherence_packs_delta=1.5, marketing_spend_change=0.35),
}


def run_scenario(inputs):
    hcp_effect = inputs["hcp_conversion_pct"] * hcp_nonuser_share * ELASTICITIES["hcp_conversion_to_revenue"]
    stock_effect = inputs["stock_availability_pts"] * ELASTICITIES["stock_pt_to_units"]
    awareness_effect = inputs["awareness_conversion_pct"] * consumer_low_awareness_share * ELASTICITIES["awareness_conversion_to_revenue"]
    adherence_effect = inputs["adherence_packs_delta"] * ELASTICITIES["adherence_packs_to_revenue"]
    marketing_effect = np.log1p(inputs["marketing_spend_change"]) * ELASTICITIES["marketing_spend_elasticity"]
    total_lift = hcp_effect + stock_effect + awareness_effect + adherence_effect + marketing_effect

    revenue = baseline_annual_revenue * (1 + total_lift)
    units = baseline_annual_units * (1 + total_lift)
    spend = baseline_annual_spend * (1 + inputs["marketing_spend_change"])

    return dict(
        hcp_effect=100*hcp_effect, stock_effect=100*stock_effect, awareness_effect=100*awareness_effect,
        adherence_effect=100*adherence_effect, marketing_effect=100*marketing_effect, total_lift=100*total_lift,
        revenue=revenue, units=units, spend=spend, pct_of_pre_recall=100*revenue/pre_recall_annual,
    )


# ---------------------------------------------------------------------------
# Preset selector + sliders
# ---------------------------------------------------------------------------
preset_choice = st.radio("Start from a preset", ["Custom", "Conservative", "Base", "Upside"], horizontal=True, index=2)
defaults = PRESETS.get(preset_choice, PRESETS["Base"])

st.subheader("Adjust the levers")
c1, c2 = st.columns(2)
with c1:
    hcp_conversion_pct = st.slider("HCP conversion: % of non-user HCPs who become active recommenders",
                                    0.0, 1.0, defaults["hcp_conversion_pct"], 0.05, key="hcp")
    stock_availability_pts = st.slider("Distribution: +points of average stock availability",
                                        0, 25, defaults["stock_availability_pts"], 1, key="stock")
    awareness_conversion_pct = st.slider("Awareness: % of low-awareness consumers reached",
                                          0.0, 1.0, defaults["awareness_conversion_pct"], 0.05, key="awareness")
with c2:
    adherence_packs_delta = st.slider("Adherence: +packs/year for existing customers",
                                       0.0, 3.0, defaults["adherence_packs_delta"], 0.1, key="adherence")
    marketing_spend_change = st.slider("Marketing spend: % change vs current annual run-rate",
                                        0.0, 1.0, defaults["marketing_spend_change"], 0.05, key="marketing")

inputs = dict(hcp_conversion_pct=hcp_conversion_pct, stock_availability_pts=stock_availability_pts,
              awareness_conversion_pct=awareness_conversion_pct, adherence_packs_delta=adherence_packs_delta,
              marketing_spend_change=marketing_spend_change)
result = run_scenario(inputs)

st.markdown("---")

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
st.subheader("Simulated impact")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Projected annual revenue", f"₹{result['revenue']/1e7:.2f} Cr",
          delta=f"{result['total_lift']:.1f}% vs current run-rate")
c2.metric("Projected annual units", f"{result['units']/1e3:.0f}K packs")
c3.metric("% of pre-recall baseline", f"{result['pct_of_pre_recall']:.0f}%")
c4.metric("Annual marketing spend", f"₹{result['spend']/1e7:.2f} Cr",
          help=f"{result['spend']/result['revenue']:.1%} of projected revenue")

left, right = st.columns([1, 1])
with left:
    st.markdown("**Revenue lift by driver**")
    drivers = pd.DataFrame({
        "driver": ["HCP conversion", "Stock availability", "Awareness", "Adherence/retention", "Marketing spend"],
        "contribution": [result["hcp_effect"], result["stock_effect"], result["awareness_effect"],
                          result["adherence_effect"], result["marketing_effect"]],
    })
    fig = go.Figure(go.Bar(x=drivers.contribution, y=drivers.driver, orientation="h", marker_color="#1d4ed8"))
    fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="Contribution to revenue lift (%)")
    st.plotly_chart(fig, width='stretch')

with right:
    st.markdown("**vs current run-rate & pre-recall baseline**")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=["Current run-rate", "Your scenario", "Pre-recall baseline"],
                           y=[baseline_annual_revenue, result["revenue"], pre_recall_annual],
                           marker_color=["#94a3b8", "#1d4ed8", "#dc2626"]))
    fig2.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), yaxis_title="Annual revenue (₹)")
    st.plotly_chart(fig2, width='stretch')

st.info(
    "💡 In the Base case, **adherence/retention and stock availability are the largest revenue drivers** — "
    "not HCP conversion. Retention is also the cheapest channel (₹23 CAC vs ~₹908 for new-parent acquisition), "
    "making it a rare case where the highest-leverage and lowest-cost lever are the same one. HCP conversion "
    "remains strategically necessary as the upstream driver that creates new adherent customers in the first place."
)

st.markdown("---")

# ---------------------------------------------------------------------------
# Compare all three presets
# ---------------------------------------------------------------------------
st.subheader("Compare the three standard scenarios")
compare_rows = []
for name, preset_inputs in PRESETS.items():
    r = run_scenario(preset_inputs)
    compare_rows.append({"Scenario": name, "Annual Revenue (₹Cr)": r["revenue"]/1e7,
                          "Annual Units (K)": r["units"]/1e3, "% of Pre-recall Baseline": r["pct_of_pre_recall"],
                          "Marketing Spend (₹Cr)": r["spend"]/1e7})
compare_df = pd.DataFrame(compare_rows).set_index("Scenario")
st.dataframe(compare_df.style.format("{:.1f}"), width='stretch')

st.caption(
    "Even the Upside case does not fully close the gap to the pre-recall baseline within a year — consistent "
    "with rebuilding doctor trust after a recall being an 18-24 month process, not a one-quarter fix."
)
