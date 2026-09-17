"""Page 5 — Territory Prioritization"""
import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.data import load_all, synthetic_banner

st.set_page_config(page_title="Territory Prioritization", page_icon="🗺️", layout="wide")

st.title("🗺️ Territory Prioritization")
synthetic_banner()

data = load_all()
territory = data["territory"]

st.markdown(
    "**Business question:** Given limited field and marketing resources, which territories should get priority "
    "next quarter? Uses the full six-factor weighted opportunity model (see `notebooks/04_territory_analysis.ipynb`), "
    "stress-tested against 12 different weight choices to confirm the ranking isn't an artefact of the specific weights used."
)

seg_colors = {"Defend": "#16a34a", "Grow": "#f59e0b", "Build": "#3b82f6", "Deprioritize": "#94a3b8"}

# ---------------------------------------------------------------------------
# Segment overview
# ---------------------------------------------------------------------------
seg_summary = territory.groupby("territory_segment").agg(
    territories=("territory", "size"), current_sales=("current_sales", "sum"),
    market_potential=("market_potential", "sum"),
).reindex(["Defend", "Grow", "Build", "Deprioritize"])

c1, c2, c3, c4 = st.columns(4)
for col, seg in zip([c1, c2, c3, c4], ["Defend", "Grow", "Build", "Deprioritize"]):
    row = seg_summary.loc[seg]
    col.metric(seg, f"{int(row.territories)} territories", help=f"₹{row.market_potential:.0f}L potential")

st.markdown("---")

# ---------------------------------------------------------------------------
# Quadrant chart
# ---------------------------------------------------------------------------
st.subheader("Potential vs penetration")
med_potential = territory.market_potential.median()
med_penetration = territory.penetration.median()

fig = px.scatter(territory, x="market_potential", y="penetration", color="territory_segment",
                  color_discrete_map=seg_colors, hover_name="territory",
                  hover_data={"market_potential": ":.1f", "penetration": ":.1%", "current_sales": ":.1f"},
                  labels={"market_potential": "Market potential (₹ lakh)", "penetration": "Penetration"})
fig.update_traces(marker=dict(size=11, line=dict(width=1, color="white")))
fig.add_vline(x=med_potential, line_dash="dash", line_color="gray")
fig.add_hline(y=med_penetration, line_dash="dash", line_color="gray")
fig.update_layout(height=480, margin=dict(l=10, r=10, t=10, b=10), yaxis_tickformat=".0%",
                   legend_title=None, legend=dict(orientation="h", y=1.1))
st.plotly_chart(fig, width='stretch')
st.caption(
    "Dashed lines mark the median. Kolkata and Chennai sit in **Grow**: large markets by potential, but "
    "under-penetrated — invisible on a plain revenue leaderboard."
)

st.markdown("---")

# ---------------------------------------------------------------------------
# Opportunity ranking
# ---------------------------------------------------------------------------
st.subheader("Top territories by opportunity score")
top_n = st.slider("Show top N territories", 5, 36, 15)
ranked = territory.sort_values("opportunity_rank").head(top_n)

fig2 = px.bar(ranked.sort_values("opportunity_score"), x="opportunity_score", y="territory", orientation="h",
              color="opportunity_score", color_continuous_scale="RdYlGn",
              labels={"opportunity_score": "Opportunity score", "territory": ""})
fig2.update_layout(height=max(340, top_n * 22), margin=dict(l=10, r=10, t=10, b=10), coloraxis_showscale=False)
st.plotly_chart(fig2, width='stretch')

st.markdown("**Weighting used:** 30% Market Potential + 20% HCP Opportunity + 15% Growth Potential + "
            "15% Brand Gap + 10% Channel Readiness + 10% Competitive Opportunity")

st.markdown("---")

# ---------------------------------------------------------------------------
# Sensitivity note
# ---------------------------------------------------------------------------
st.subheader("Is this ranking robust to the chosen weights?")
col1, col2, col3 = st.columns(3)
col1.metric("Min. Spearman correlation across 12 weight perturbations", "0.945",
            help="±10pt perturbation on each of the 6 weights, vs the base ranking")
col2.metric("Chennai & Delhi North top-4 stability", "12 / 12", help="Held a top-4 rank under every perturbation tested")
col3.metric("Kolkata top-4 stability", "10 / 12")
st.markdown(
    "**Takeaway:** the top 2-3 territories are effectively weight-independent conclusions. Rank order from "
    "roughly #5 downward is more sensitive to specific weight choices and should be treated as directional. "
    "Full methodology and chart in `notebooks/04_territory_analysis.ipynb`."
)

st.markdown("---")

# ---------------------------------------------------------------------------
# Full table
# ---------------------------------------------------------------------------
st.subheader("Full territory table")
show = territory[["opportunity_rank", "territory", "state", "region", "city_tier", "current_sales",
                   "market_potential", "penetration", "territory_segment", "opportunity_score"]].sort_values("opportunity_rank")
show.columns = ["Rank", "Territory", "State", "Region", "Tier", "Current Sales (₹L)", "Potential (₹L)",
                "Penetration", "Segment", "Opp. Score"]
st.dataframe(
    show.style.format({"Current Sales (₹L)": "{:.1f}", "Potential (₹L)": "{:.1f}",
                        "Penetration": "{:.1%}", "Opp. Score": "{:.3f}"}),
    width='stretch', hide_index=True, height=420,
)
