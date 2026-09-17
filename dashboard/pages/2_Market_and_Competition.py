"""Page 2 — Market & Competition"""
import sys
from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.data import load_all, synthetic_banner, BRAND_COLOR, WARN_COLOR

st.set_page_config(page_title="Market & Competition", page_icon="🏆", layout="wide")

st.title("🏆 Market & Competition")
synthetic_banner()

data = load_all()
comp = data["competitor"]

st.markdown(
    "**Business question:** Where does DePURA Kids sit competitively, and on which basis can it credibly compete? "
    "Pack price is not comparable across brands with different strengths and sizes — see `research/competitor_analysis.md` "
    "— so this page compares **cost per equivalent 400 IU dose**."
)

# ---------------------------------------------------------------------------
# Price positioning
# ---------------------------------------------------------------------------
st.subheader("Cost per 400 IU dose, by brand")
comp_known = comp.dropna(subset=["cost_per_400iu_dose"]).sort_values("cost_per_400iu_dose")
comp_unknown = comp[comp.cost_per_400iu_dose.isna()]

colors = ["#dc2626" if b == "DePURA Kids" else "#94a3b8" for b in comp_known.brand]
fig = go.Figure(go.Bar(x=comp_known.cost_per_400iu_dose, y=comp_known.brand, orientation="h",
                        marker_color=colors, text=comp_known.cost_per_400iu_dose.round(2), textposition="outside"))
fig.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="₹ per 400 IU dose")
st.plotly_chart(fig, width='stretch')

if len(comp_unknown):
    st.caption(f"Excluded (strength unverified from a reliable source): {', '.join(comp_unknown.brand)}")

col1, col2 = st.columns(2)
with col1:
    st.metric("DePURA Kids cost per dose", f"₹{comp.loc[comp.brand=='DePURA Kids','cost_per_400iu_dose'].iloc[0]:.2f}")
with col2:
    cheapest = comp_known.iloc[0]
    st.metric(f"Cheapest verified option ({cheapest.brand})", f"₹{cheapest.cost_per_400iu_dose:.2f}",
              help="Ultra D3 — sugar-free, pineapple flavour, 30ml pack")

st.markdown("---")

# ---------------------------------------------------------------------------
# Competitive clusters
# ---------------------------------------------------------------------------
st.subheader("Competitive clusters")
cluster_map = {
    "DePURA Kids": "Premium nano", "Arachitol Kids / Nano": "Premium nano", "Kidrich D3 800 IU Nano": "Premium nano",
    "Uprise-D3 Drops": "Mid-price", "D3 Must Forte": "Mid-price",
}
comp["price_cluster"] = comp.brand.map(cluster_map).fillna("Value")
cluster_summary = comp.groupby("price_cluster").agg(
    brands=("brand", "count"), avg_cost=("cost_per_400iu_dose", "mean")
).reset_index()

left, right = st.columns([1, 1])
with left:
    fig2 = px.bar(cluster_summary.sort_values("avg_cost", ascending=False), x="price_cluster", y="avg_cost",
                  color="price_cluster", color_discrete_sequence=["#dc2626", "#f59e0b", "#16a34a"],
                  labels={"avg_cost": "Avg. ₹ per dose", "price_cluster": ""}, text_auto=".2f")
    fig2.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
    st.plotly_chart(fig2, width='stretch')

with right:
    st.markdown("""
**Reading the clusters:**
- **Premium nano** (DePURA Kids, Arachitol, Kidrich) compete on doctor trust and formulation credibility, not price.
- **Mid-price** (Uprise-D3, D3 Must Forte) cost ~52-58% of DePURA per dose, with strong T2/T3 field reach.
- **Value** brands (Ultra D3 and the long tail) are the pharmacist-substitution risk when DePURA is out of stock.

**Implication:** DePURA cannot win on price without abandoning its premium position. The premium has to be
justified at the point of prescription — reinforcing the case for HCP-first investment over price competition.
""")

st.markdown("---")

# ---------------------------------------------------------------------------
# Full competitor table
# ---------------------------------------------------------------------------
st.subheader("Full competitive matrix")
display_cols = ["brand", "manufacturer", "dosage", "pack_size", "price", "cost_per_400iu_dose",
                 "estimated_price_index", "positioning", "target_segment", "channel_presence"]
show = comp[display_cols].copy()
show.columns = ["Brand", "Manufacturer", "Dosage", "Pack", "MRP (₹)", "₹/400 IU dose", "Price Index",
                "Positioning", "Target Segment", "Channel Presence"]
st.dataframe(show, width='stretch', hide_index=True)
st.caption(
    "Positioning, Target Segment and Channel Presence are analyst assessments, not company statements. "
    "Price Index = 100 at DePURA Kids. See `research/competitor_analysis.md` for full sourcing."
)
