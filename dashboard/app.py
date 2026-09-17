"""
DePURA Kids Relaunch Strategy — Executive Dashboard

⚠️ ALL DATA IS SYNTHETIC / SIMULATED. This is an independent case study based
on publicly available information, with general industry perspective from a
Sanofi professional. It is not a Sanofi project or Sanofi-approved strategy.
See ../data/DATA_DICTIONARY.md and ../research/ for full provenance.

Run with:  streamlit run app.py   (from the dashboard/ folder)
"""
import sys
from pathlib import Path

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.data import load_all, seasonally_adjusted_monthly, recovery_pct, synthetic_banner, BRAND_COLOR, WARN_COLOR

st.set_page_config(
    page_title="DePURA Kids Relaunch Strategy",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.sidebar.title("DePURA Kids")
st.sidebar.caption("Relaunch Strategy — Case Study")
st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Independent case study** based on publicly available information, "
    "with general industry perspective from a Sanofi professional. "
    "Not a Sanofi project or Sanofi-approved strategy."
)
st.sidebar.markdown("---")
st.sidebar.caption("Navigate using the pages above (Executive Overview, Market & Competition, HCP Analytics, "
                    "Consumer Analytics, Territory Prioritization, Campaign Performance, Scenario Planner, "
                    "Strategic Recommendations).")

data = load_all()
sales = data["sales"]
territory = data["territory"]
hcp = data["hcp"]
campaign = data["campaign"]

st.title("📊 Executive Overview")
synthetic_banner()

st.markdown(
    "**Business question:** How should DePURA Kids strengthen its post-relaunch growth in India's "
    "pediatric Vitamin D category, after ~17-18 months off shelves following a 2024 voluntary recall?"
)

# ---------------------------------------------------------------------------
# KPI row
# ---------------------------------------------------------------------------
monthly = seasonally_adjusted_monthly(sales)
post = sales[sales.market_phase == "post_relaunch"]
latest3 = post[post.date >= post.date.max() - pd.DateOffset(months=2)]

annual_revenue_runrate = latest3.groupby("date").revenue.sum().mean() * 12
annual_units_runrate = latest3.groupby("date").units_sold.sum().mean() * 12
recovery = recovery_pct(sales)
avg_stock = post.stock_availability.mean()
total_hcp_reach = len(hcp)
hcp_advocate_share = (hcp.hcp_segment == "High-volume advocate").mean()
blended_cac_parents = campaign.loc[campaign.audience.isin(["Parents", "Parents (existing)"]), "spend"].sum() / \
                       campaign.loc[campaign.audience.isin(["Parents", "Parents (existing)"]), "conversions"].sum()
avg_conversion_rate = campaign.conversions.sum() / campaign.leads.sum()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Annualised revenue run-rate", f"₹{annual_revenue_runrate/1e7:.1f} Cr",
          help="Latest 3-month average monthly revenue × 12")
c2.metric("Recovery vs pre-recall", f"{recovery:.0f}%",
          delta=f"{recovery-100:.0f} pts vs full recovery", delta_color="inverse",
          help="Seasonally adjusted, latest 3 months vs pre-recall 12-month average")
c3.metric("Annualised units run-rate", f"{annual_units_runrate/1e3:.0f}K packs")
c4.metric("Avg. distribution fill-rate", f"{avg_stock:.0%}", help="Post-relaunch average stock availability")

c5, c6, c7, c8 = st.columns(4)
c5.metric("HCPs reached (sample)", f"{total_hcp_reach:,}")
c6.metric("High-volume advocates", f"{hcp_advocate_share:.0%}", help="Share of sampled HCPs recommending strongly")
c7.metric("Blended parent CAC", f"₹{blended_cac_parents:,.0f}")
c8.metric("Overall conversion rate", f"{avg_conversion_rate:.1%}", help="Conversions ÷ leads, across all campaigns")

st.markdown("---")

# ---------------------------------------------------------------------------
# Revenue trend
# ---------------------------------------------------------------------------
left, right = st.columns([2, 1])

with left:
    st.subheader("Revenue trend: pre-recall → recall → relaunch")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly.date, y=monthly.revenue, name="Revenue (reported)",
                              line=dict(color="#94a3b8", width=1.5), mode="lines+markers", marker=dict(size=4)))
    fig.add_trace(go.Scatter(x=monthly.date, y=monthly.revenue_sa, name="Revenue (seasonally adjusted)",
                              line=dict(color=BRAND_COLOR, width=3), mode="lines+markers", marker=dict(size=4)))
    fig.add_vrect(x0="2024-04-01", x1="2025-08-01", fillcolor="#fecaca", opacity=0.4, line_width=0,
                  annotation_text="Off market", annotation_position="top left")
    fig.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", y=1.1),
                       yaxis_title="Revenue (₹)", xaxis_title=None)
    st.plotly_chart(fig, width='stretch')
    st.caption("Recovery has plateaued at ~78% of the pre-recall run-rate (see Scenario Planner for what closes the gap).")

with right:
    st.subheader("Regional performance")
    reg = territory.groupby("region").agg(current_sales=("current_sales", "sum"),
                                           market_potential=("market_potential", "sum")).reset_index()
    reg["index"] = 100 * (reg.current_sales / reg.current_sales.sum()) / (reg.market_potential / reg.market_potential.sum())
    fig2 = px.bar(reg.sort_values("current_sales", ascending=True), x="current_sales", y="region", orientation="h",
                  color="index", color_continuous_scale=["#dc2626", "#94a3b8", "#16a34a"], range_color=[70, 130],
                  labels={"current_sales": "Revenue (₹ lakh)", "index": "vs potential"})
    fig2.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10), coloraxis_colorbar=dict(title="Index"))
    st.plotly_chart(fig2, width='stretch')
    st.caption("Green = over-indexed vs category potential; red = under-indexed.")

st.markdown("---")

# ---------------------------------------------------------------------------
# Channel contribution + opportunity table
# ---------------------------------------------------------------------------
left2, right2 = st.columns([1, 1])

with left2:
    st.subheader("Channel contribution (post-relaunch)")
    ch = post.groupby("channel").revenue.sum().reset_index().sort_values("revenue", ascending=False)
    fig3 = px.pie(ch, names="channel", values="revenue", hole=0.45,
                  color_discrete_sequence=px.colors.qualitative.Set2)
    fig3.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig3, width='stretch')

with right2:
    st.subheader("Top 5 market opportunities")
    top5 = territory.sort_values("opportunity_rank").head(5)[
        ["territory", "city_tier", "current_sales", "market_potential", "opportunity_score"]
    ]
    top5.columns = ["Territory", "Tier", "Current Sales (₹L)", "Potential (₹L)", "Opportunity Score"]
    st.dataframe(top5.style.format({"Current Sales (₹L)": "{:.1f}", "Potential (₹L)": "{:.1f}",
                                     "Opportunity Score": "{:.3f}"}).background_gradient(
        subset=["Opportunity Score"], cmap="Greens"), width='stretch', hide_index=True)
    st.caption("Full ranking with sensitivity testing on the Territory Prioritization page.")

st.markdown("---")
st.caption(
    "DePURA Kids Relaunch Strategy — independent case study. Data: SYNTHETIC/SIMULATED. "
    "Product & market facts: public sources (see research/sources.md)."
)
