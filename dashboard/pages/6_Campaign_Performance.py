"""Page 6 — Campaign Performance"""
import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.data import load_all, synthetic_banner

st.set_page_config(page_title="Campaign Performance", page_icon="📣", layout="wide")

st.title("📣 Campaign Performance")
synthetic_banner()

data = load_all()
campaign = data["campaign"]

st.markdown(
    "**Business question:** Which channels deliver the best cost-per-conversion within each audience, and how "
    "much does spending more change that efficiency? Note: 'conversion' means something different per audience "
    "(HCP resuming recommendation vs. a parent's first purchase vs. a repeat purchase) — see `data/DATA_DICTIONARY.md`."
)

with st.expander("Filters", expanded=False):
    audiences = st.multiselect("Audience", sorted(campaign.audience.unique()), default=list(campaign.audience.unique()))

camp_f = campaign[campaign.audience.isin(audiences)]

# ---------------------------------------------------------------------------
# KPIs
# ---------------------------------------------------------------------------
total_spend = camp_f.spend.sum()
total_conversions = camp_f.conversions.sum()
blended_cac = total_spend / total_conversions
overall_ctr = camp_f.clicks.sum() / camp_f.impressions.sum()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total spend (12 months)", f"₹{total_spend/1e7:.2f} Cr")
c2.metric("Total conversions", f"{total_conversions:,.0f}")
c3.metric("Blended CAC", f"₹{blended_cac:,.0f}")
c4.metric("Overall CTR / engagement rate", f"{overall_ctr:.2%}")

st.markdown("---")

# ---------------------------------------------------------------------------
# CAC by channel, within audience
# ---------------------------------------------------------------------------
st.subheader("CAC by channel (within audience)")
by_channel = camp_f.groupby(["audience", "channel"]).agg(
    spend=("spend", "sum"), conversions=("conversions", "sum")
).reset_index()
by_channel["cac"] = by_channel.spend / by_channel.conversions

fig = px.bar(by_channel.sort_values("cac"), x="cac", y="channel", color="audience", orientation="h",
             labels={"cac": "CAC (₹)", "channel": ""}, color_discrete_sequence=px.colors.qualitative.Set2,
             log_x=True)
fig.update_layout(height=420, margin=dict(l=10, r=10, t=10, b=10), legend_title=None,
                   legend=dict(orientation="h", y=1.1))
st.plotly_chart(fig, width='stretch')
st.caption(
    "Log scale — CAC spans nearly 1000x across channels/audiences. Refill reminders (₹23) are far cheaper than "
    "new-parent acquisition (~₹908 blended) or HCP conversion (~₹19,400 blended)."
)

st.markdown("---")

# ---------------------------------------------------------------------------
# Funnel
# ---------------------------------------------------------------------------
st.subheader("Conversion funnel by audience")
funnel = camp_f.groupby("audience").agg(
    impressions=("impressions", "sum"), clicks=("clicks", "sum"), leads=("leads", "sum"), conversions=("conversions", "sum")
).reset_index()

audience_choice = st.selectbox("Select audience for funnel detail", funnel.audience.tolist())
row = funnel[funnel.audience == audience_choice].iloc[0]
fig2 = px.funnel(
    x=[row.impressions, row.clicks, row.leads, row.conversions],
    y=["Impressions", "Clicks", "Leads", "Conversions"],
)
fig2.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig2, width='stretch')

c1, c2, c3 = st.columns(3)
c1.metric("Impression → Click", f"{100*row.clicks/row.impressions:.2f}%")
c2.metric("Click → Lead", f"{100*row.leads/row.clicks:.2f}%")
c3.metric("Lead → Conversion", f"{100*row.conversions/row.leads:.2f}%")

st.markdown("---")

# ---------------------------------------------------------------------------
# Spend vs CAC — diminishing returns
# ---------------------------------------------------------------------------
st.subheader("Does more spend mean higher CAC? (diminishing returns check)")
channel_choice = st.selectbox("Select channel", sorted(camp_f.channel.unique()))
chan_data = camp_f[camp_f.channel == channel_choice].sort_values("month")

fig3 = px.scatter(chan_data, x="spend", y="cac",
                   labels={"spend": "Monthly spend (₹)", "cac": "CAC (₹)"},
                   color_discrete_sequence=["#1d4ed8"])
fig3.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig3, width='stretch')

corr = chan_data[["spend", "cac"]].corr().iloc[0, 1]
st.metric(f"Spend-vs-CAC correlation ({channel_choice})", f"{corr:.2f}",
          help="Positive = diminishing returns: CAC rises as spend rises within this channel")

st.markdown("---")

# ---------------------------------------------------------------------------
# Channel comparison table
# ---------------------------------------------------------------------------
st.subheader("Full channel comparison")
full = camp_f.groupby(["audience", "channel"]).agg(
    spend=("spend", "sum"), impressions=("impressions", "sum"), clicks=("clicks", "sum"),
    leads=("leads", "sum"), conversions=("conversions", "sum"),
).reset_index()
full["cac"] = full.spend / full.conversions
full["ctr"] = full.clicks / full.impressions
show = full[["audience", "channel", "spend", "conversions", "cac", "ctr"]].sort_values("cac")
show.columns = ["Audience", "Channel", "Total Spend (₹)", "Conversions", "CAC (₹)", "CTR"]
st.dataframe(
    show.style.format({"Total Spend (₹)": "{:,.0f}", "CAC (₹)": "{:,.0f}", "CTR": "{:.2%}"}),
    width='stretch', hide_index=True,
)
