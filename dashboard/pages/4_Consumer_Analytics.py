"""Page 4 — Consumer Analytics"""
import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.data import load_all, synthetic_banner

st.set_page_config(page_title="Consumer Analytics", page_icon="👨‍👩‍👧", layout="wide")

st.title("👨‍👩‍👧 Consumer Analytics")
synthetic_banner()

data = load_all()
consumer = data["consumer"]

st.markdown(
    "**Business question:** Which parent segments currently favour DePURA Kids, which represent the biggest "
    "growth gap, and where does each segment get its information?"
)

seg_order = ["Price-sensitive", "Mainstream", "Convenience-driven", "Low-awareness", "Health-conscious"]
seg_colors = {"Price-sensitive": "#f59e0b", "Mainstream": "#94a3b8", "Convenience-driven": "#3b82f6",
              "Low-awareness": "#dc2626", "Health-conscious": "#16a34a"}

with st.expander("Filters", expanded=False):
    tiers = st.multiselect("City tier", sorted(consumer.city_tier.unique()), default=list(consumer.city_tier.unique()))
    regions = st.multiselect("Region", sorted(consumer.region.unique()), default=list(consumer.region.unique()))

cons_f = consumer[consumer.city_tier.isin(tiers) & consumer.region.isin(regions)]

# ---------------------------------------------------------------------------
# Segment distribution & DePURA share
# ---------------------------------------------------------------------------
seg_summary = cons_f.groupby("consumer_segment").agg(
    consumers=("consumer_id", "size"),
    pct_depura=("current_brand", lambda s: 100 * (s == "DePURA Kids").mean()),
    avg_adherence=("adherence_score", "mean"),
).reindex(seg_order).dropna(how="all")
seg_summary["pct_of_total"] = 100 * seg_summary.consumers / seg_summary.consumers.sum()

c1, c2, c3, c4, c5 = st.columns(5)
for col, seg in zip([c1, c2, c3, c4, c5], seg_order):
    if seg in seg_summary.index:
        row = seg_summary.loc[seg]
        col.metric(seg, f"{row.pct_of_total:.0f}% of parents", help=f"DePURA share: {row.pct_depura:.0f}%")

st.markdown("---")

left, right = st.columns([1, 1])
with left:
    st.subheader("Segment size")
    fig = px.bar(seg_summary.reset_index().sort_values("consumers"), x="consumers", y="consumer_segment",
                 orientation="h", color="consumer_segment", color_discrete_map=seg_colors,
                 labels={"consumers": "Parents surveyed", "consumer_segment": ""})
    fig.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
    st.plotly_chart(fig, width='stretch')

with right:
    st.subheader("DePURA Kids share, by segment")
    fig2 = px.bar(seg_summary.reset_index().sort_values("pct_depura"), x="pct_depura", y="consumer_segment",
                  orientation="h", color="consumer_segment", color_discrete_map=seg_colors,
                  labels={"pct_depura": "% currently buying DePURA Kids", "consumer_segment": ""})
    fig2.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
    st.plotly_chart(fig2, width='stretch')

st.info(
    "💡 **Health-conscious** parents have both the highest DePURA share and highest adherence — the brand's core. "
    "**Low-awareness** parents have the *lowest* share — the clearest growth pool, fixed by education, not price."
)

st.markdown("---")

# ---------------------------------------------------------------------------
# Awareness
# ---------------------------------------------------------------------------
st.subheader("Awareness distribution")
aware_dist = cons_f.awareness.value_counts().sort_index().reset_index()
aware_dist.columns = ["awareness", "count"]
fig3 = px.bar(aware_dist, x="awareness", y="count", labels={"awareness": "Awareness (1-5)", "count": "Parents"},
              color_discrete_sequence=["#1d4ed8"])
fig3.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig3, width='stretch')

st.markdown("---")

# ---------------------------------------------------------------------------
# Purchase behavior & price sensitivity
# ---------------------------------------------------------------------------
left2, right2 = st.columns([1, 1])
with left2:
    st.subheader("Purchase channel mix")
    ch = cons_f.purchase_channel.value_counts(normalize=True).reset_index()
    ch.columns = ["channel", "share"]
    fig4 = px.pie(ch, names="channel", values="share", hole=0.45, color_discrete_sequence=px.colors.qualitative.Set2)
    fig4.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig4, width='stretch')

with right2:
    st.subheader("Price sensitivity distribution")
    ps = cons_f.price_sensitivity.dropna().value_counts().sort_index().reset_index()
    ps.columns = ["price_sensitivity", "count"]
    fig5 = px.bar(ps, x="price_sensitivity", y="count", labels={"price_sensitivity": "Price sensitivity (1-5)"},
                  color_discrete_sequence=["#f59e0b"])
    fig5.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig5, width='stretch')

st.markdown("---")

# ---------------------------------------------------------------------------
# Recommendation source by segment
# ---------------------------------------------------------------------------
st.subheader("Where each segment gets its information")
source_cross = (
    cons_f.groupby(["consumer_segment", "recommendation_source"]).size().reset_index(name="count")
)
source_cross["pct"] = source_cross.groupby("consumer_segment")["count"].transform(lambda s: 100 * s / s.sum())
fig6 = px.bar(source_cross, x="consumer_segment", y="pct", color="recommendation_source", barmode="stack",
              category_orders={"consumer_segment": seg_order},
              labels={"pct": "% of segment", "consumer_segment": ""},
              color_discrete_sequence=px.colors.qualitative.Set3)
fig6.update_layout(height=420, margin=dict(l=10, r=10, t=10, b=10), legend_title=None,
                    legend=dict(orientation="h", y=1.15))
st.plotly_chart(fig6, width='stretch')
st.caption(
    "Health-conscious and Convenience-driven parents lean heavily on their pediatrician — reinforcing that "
    "HCP-channel investment reaches the segments that already favour the brand. Low-awareness parents rely "
    "more on pharmacists and family/friends, pointing to a different channel mix for that segment."
)

st.markdown("---")

# ---------------------------------------------------------------------------
# Recall impact
# ---------------------------------------------------------------------------
st.subheader("Recall awareness and brand trust")
trust = cons_f.groupby("aware_of_recall")["brand_trust"].mean().reset_index()
trust["aware_of_recall"] = trust.aware_of_recall.map({True: "Aware of recall", False: "Not aware of recall"})
c1, c2 = st.columns([1, 2])
with c1:
    fig7 = px.bar(trust, x="aware_of_recall", y="brand_trust", color="aware_of_recall",
                  color_discrete_map={"Aware of recall": "#dc2626", "Not aware of recall": "#1d4ed8"},
                  labels={"brand_trust": "Avg. brand trust (1-5)", "aware_of_recall": ""})
    fig7.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10), showlegend=False, yaxis_range=[0, 5])
    st.plotly_chart(fig7, width='stretch')
with c2:
    pct_aware = cons_f.aware_of_recall.mean()
    st.metric("Share of parents aware of the 2024 recall", f"{pct_aware:.0%}")
    st.markdown(
        "Parents aware of the recall report meaningfully lower brand trust — roughly a full point lower on a "
        "5-point scale. Pediatrician reassurance at the point of recommendation is likely a more effective "
        "lever than mass-market messaging trying to overwrite the recall memory directly."
    )
