"""Page 8 — Strategic Recommendations

Recommendations here are traced directly back to the analysis on the other
7 pages — no recommendation appears without a source. Full narrative
version will live in strategy/ (Stage 7); this page summarises for the
dashboard audience.
"""
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.data import load_all, synthetic_banner, recovery_pct

st.set_page_config(page_title="Strategic Recommendations", page_icon="🎯", layout="wide")

st.title("🎯 Strategic Recommendations")
synthetic_banner()

data = load_all()
recovery = recovery_pct(data["sales"])

st.markdown(f"""
### The problem, in one line
DePURA Kids has recovered to **~{recovery:.0f}% of its pre-recall revenue run-rate**, and month-over-month
growth has fallen from +32% in the first post-relaunch month to roughly flat — the recovery has **plateaued**,
not merely slowed. Closing the remaining gap requires new levers, not more time.
""")

st.markdown("---")

recommendations = [
    {
        "title": "1. Prioritize retention infrastructure — it's the cheapest lever AND the largest driver",
        "evidence": "Scenario Planner: adherence/retention contributes the most to Base-case revenue lift (8.0 of 22.2 points). "
                    "Campaign Performance: refill-reminder CAC is ₹23, vs ~₹908 blended for new-parent acquisition.",
        "action": "Fund WhatsApp/CRM refill reminders and adherence programs for existing DePURA customers, "
                  "especially the Health-conscious consumer segment (already 39% DePURA share, 0.83 adherence).",
    },
    {
        "title": "2. Re-engage pre-recall pediatricians before chasing new HCPs",
        "evidence": "HCP Analytics: pre-recall prescribers recommend far more than non-prescribers within every "
                    "specialty. Pediatricians recommend at ~2x the rate of other specialties. Patient volume, by "
                    "contrast, is a confounded (not causal) predictor once specialty is controlled for.",
        "action": "Target field rep and digital detailing at 'High-volume non/under-user' pediatricians who "
                  "prescribed DePURA before March 2024 — their habit was interrupted, not rejected.",
    },
    {
        "title": "3. Fix distribution fill-rate — a fast, operational lever",
        "evidence": "Territory Prioritization / EDA: units sold swing ~21% between the lowest and highest stock-"
                    "availability bands. Several T1/T2 territories (Delhi South, Indore, Pune) sit meaningfully "
                    "below the network median on stock availability despite strong underlying demand.",
        "action": "Treat distributor onboarding and stock availability as a tracked KPI in Phase 1 (0-90 days), "
                  "not just an operations metric — it is a direct, quantifiable revenue lever.",
    },
    {
        "title": "4. Defend the doctor-trust premium; don't compete on price",
        "evidence": "Market & Competition: DePURA sits in the premium cluster at ~1.7-2.7x the cost-per-dose of "
                    "mid-price and value competitors. Arachitol Kids/Nano is an exact strength/pack match at a "
                    "similar price — the nearest like-for-like substitute.",
        "action": "Invest in HCP trust and formulation credibility messaging, not discounting. A price cut would "
                  "give up premium positioning without a guaranteed volume payoff against a fragmented, "
                  "many-competitor field.",
    },
    {
        "title": "5. Target two under-penetrated large markets: Kolkata and Chennai",
        "evidence": "Territory Prioritization: both territories rank top-3 by category potential but land in the "
                    "bottom half on penetration — invisible on a plain revenue leaderboard. Both hold a top-4 "
                    "opportunity-score rank under most weight perturbations tested (Chennai: 12/12, Kolkata: 10/12).",
        "action": "Prioritize incremental field and marketing resourcing in these two 'Grow' territories ahead of "
                  "smaller, better-penetrated markets.",
    },
    {
        "title": "6. Set an 18-24 month recovery expectation, not a one-quarter fix",
        "evidence": "Scenario Planner: even the Upside case (aggressive execution on all five levers) does not "
                    "fully close the gap to the pre-recall baseline within a year.",
        "action": "Communicate the Conservative case explicitly to stakeholders to avoid over-promising if HCP "
                  "re-engagement — which depends on rebuilding trust after a quality-related recall — takes "
                  "longer than hoped.",
    },
]

for rec in recommendations:
    with st.container(border=True):
        st.markdown(f"#### {rec['title']}")
        st.markdown(f"**Evidence:** {rec['evidence']}")
        st.markdown(f"**Action:** {rec['action']}")

st.markdown("---")

st.subheader("Three-phase roadmap")
phase_col1, phase_col2, phase_col3 = st.columns(3)
with phase_col1:
    st.markdown("""
**Phase 1 — Rebuild (0-90 days)**
- Fix distribution fill-rate in under-stocked territories
- Launch refill-reminder / retention program
- Re-engage pre-recall pediatricians
""")
with phase_col2:
    st.markdown("""
**Phase 2 — Accelerate (90-180 days)**
- Scale HCP digital detailing to Emerging segment
- Expand field coverage in Grow territories (Kolkata, Chennai)
- Launch awareness content for Low-awareness consumer segment
""")
with phase_col3:
    st.markdown("""
**Phase 3 — Scale (180-365 days)**
- Reassess penetration vs Base-case scenario checkpoint
- Expand successful territory playbook to Build-segment territories
- Re-evaluate marketing mix based on realised CAC by channel
""")

st.info(
    "📄 A fully narrative version of this strategy — with phase-by-phase KPIs, target segments, and channel "
    "detail — is being developed in `strategy/relaunch_strategy.md`, `strategy/gtm_strategy.md`, and "
    "`strategy/kpi_framework.md` (Stage 7)."
)

st.caption(
    "Every recommendation above traces to a specific chart or table elsewhere in this dashboard. "
    "All figures are SYNTHETIC — see data/DATA_DICTIONARY.md."
)
