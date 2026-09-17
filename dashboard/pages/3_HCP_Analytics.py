"""Page 3 — HCP Analytics"""
import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.data import load_all, synthetic_banner

st.set_page_config(page_title="HCP Analytics", page_icon="🩺", layout="wide")

st.title("🩺 HCP Analytics")
synthetic_banner()

data = load_all()
hcp = data["hcp"]

st.markdown(
    "**Business question:** Which HCPs should get priority engagement, and what actually drives their "
    "recommendation rate — not what merely correlates with it? (Patient volume is a confounder here — see below.)"
)

# ---------------------------------------------------------------------------
# Filters
# ---------------------------------------------------------------------------
with st.expander("Filters", expanded=False):
    specialties = st.multiselect("Specialty", sorted(hcp.specialty.unique()), default=list(hcp.specialty.unique()))
    tiers = st.multiselect("City tier", sorted(hcp.city_tier.unique()), default=list(hcp.city_tier.unique()))

hcp_f = hcp[hcp.specialty.isin(specialties) & hcp.city_tier.isin(tiers)]

# ---------------------------------------------------------------------------
# Segment overview
# ---------------------------------------------------------------------------
seg_order = ["High-volume advocate", "High-volume non/under-user", "Emerging", "Low-opportunity"]
seg_colors = {"High-volume advocate": "#16a34a", "High-volume non/under-user": "#dc2626",
              "Emerging": "#f59e0b", "Low-opportunity": "#94a3b8"}

seg_summary = hcp_f.groupby("hcp_segment").agg(
    hcp_count=("hcp_id", "size"), avg_rec=("recommendation_rate", "mean"),
    avg_volume=("monthly_patient_volume", "mean"), pct_prerecall=("pre_recall_prescriber", "mean"),
).reindex(seg_order).dropna(how="all")

c1, c2, c3, c4 = st.columns(4)
for col, seg in zip([c1, c2, c3, c4], seg_order):
    if seg in seg_summary.index:
        row = seg_summary.loc[seg]
        col.metric(seg, f"{int(row.hcp_count)} HCPs", help=f"Avg. recommendation rate: {row.avg_rec:.0%}")

st.markdown("---")

left, right = st.columns([1, 1])
with left:
    st.subheader("Segment sizes")
    fig = px.pie(seg_summary.reset_index(), names="hcp_segment", values="hcp_count", hole=0.45,
                 color="hcp_segment", color_discrete_map=seg_colors)
    fig.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10), showlegend=True)
    st.plotly_chart(fig, width='stretch')

with right:
    st.subheader("Avg. recommendation rate by segment")
    fig2 = px.bar(seg_summary.reset_index(), x="hcp_segment", y="avg_rec", color="hcp_segment",
                  color_discrete_map=seg_colors, labels={"avg_rec": "Avg. recommendation rate", "hcp_segment": ""})
    fig2.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10), showlegend=False, yaxis_tickformat=".0%")
    st.plotly_chart(fig2, width='stretch')

st.info(
    "💡 **High-volume non/under-users** are the single highest-value target: they see enough patients to matter "
    "but are not yet recommending DePURA. **High-volume advocates** need retention, not acquisition spend."
)

st.markdown("---")

# ---------------------------------------------------------------------------
# The confounder — volume vs recommendation, by specialty
# ---------------------------------------------------------------------------
st.subheader("Does patient volume actually predict recommendation?")
st.caption(
    "Pooled across specialties, volume looks correlated with recommendation. Within each specialty, that "
    "relationship nearly disappears — pediatricians simply have both higher volume and higher recommendation "
    "for reasons unrelated to volume itself."
)

vol_valid = hcp_f.dropna(subset=["monthly_patient_volume"])
fig3 = px.scatter(vol_valid, x="monthly_patient_volume", y="recommendation_rate", color="specialty",
                   opacity=0.4, labels={"monthly_patient_volume": "Monthly patient volume",
                                         "recommendation_rate": "Recommendation rate"})
fig3.update_layout(height=420, margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig3, width='stretch')

overall_corr = vol_valid[["recommendation_rate", "monthly_patient_volume"]].corr().iloc[0, 1]
within_corr = vol_valid.groupby("specialty").apply(
    lambda d: d.recommendation_rate.corr(d.monthly_patient_volume), include_groups=False
)
c1, c2 = st.columns(2)
c1.metric("Overall correlation (pooled)", f"{overall_corr:.2f}")
c2.metric("Max within-specialty correlation", f"{within_corr.abs().max():.2f}",
          help="Confirms the pooled correlation is confounded by specialty, not a real volume effect")

st.markdown("---")

# ---------------------------------------------------------------------------
# Specialty analysis
# ---------------------------------------------------------------------------
st.subheader("Specialty analysis: recommendation by pre-recall prescriber status")
spec_summary = hcp_f.groupby(["specialty", "pre_recall_prescriber"])["recommendation_rate"].mean().reset_index()
spec_summary["pre_recall_prescriber"] = spec_summary.pre_recall_prescriber.map(
    {True: "Prescribed pre-recall", False: "Did not prescribe pre-recall"})
fig4 = px.bar(spec_summary, x="specialty", y="recommendation_rate", color="pre_recall_prescriber", barmode="group",
              color_discrete_map={"Prescribed pre-recall": "#1d4ed8", "Did not prescribe pre-recall": "#94a3b8"},
              labels={"recommendation_rate": "Avg. recommendation rate", "specialty": ""})
fig4.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10), yaxis_tickformat=".0%",
                    legend_title=None, legend=dict(orientation="h", y=1.15))
st.plotly_chart(fig4, width='stretch')
st.caption(
    "Pediatricians recommend at roughly double the rate of other specialties, and within every specialty, "
    "pre-recall prescribers recommend far more than those who never prescribed DePURA — their habit was "
    "interrupted, not rejected."
)

st.markdown("---")

# ---------------------------------------------------------------------------
# Who's winning the HCPs DePURA is losing
# ---------------------------------------------------------------------------
st.subheader("Competitor preference among low-recommendation HCPs")
low_rec = hcp_f[hcp_f.recommendation_rate < 0.20]
comp_pref = low_rec.competitor_preference.value_counts(normalize=True).reset_index()
comp_pref.columns = ["competitor_preference", "share"]
fig5 = px.bar(comp_pref.sort_values("share", ascending=True), x="share", y="competitor_preference", orientation="h",
              labels={"share": "Share of low-recommendation HCPs", "competitor_preference": ""},
              color_discrete_sequence=["#1d4ed8"])
fig5.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10), xaxis_tickformat=".0%")
st.plotly_chart(fig5, width='stretch')
st.caption("Arachitol Kids — DePURA's closest like-for-like substitute — is the top alternative among HCPs DePURA is currently losing.")
