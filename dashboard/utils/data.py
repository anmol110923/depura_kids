"""
Shared data-loading utilities for the DePURA Kids dashboard.

All data loaded here is SYNTHETIC / SIMULATED — see ../../data/DATA_DICTIONARY.md.
Cached with st.cache_data so switching pages doesn't re-read CSVs from disk.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]  # project root (depura-kids-relaunch/)
DATA = ROOT / "data"
TABLES = ROOT / "outputs" / "tables"

SEASONALITY = {1: 1.12, 2: 1.10, 3: 1.00, 4: 0.97, 5: 0.95, 6: 0.95,
               7: 0.94, 8: 0.95, 9: 0.98, 10: 1.02, 11: 1.08, 12: 1.12}

BRAND_COLOR = "#1d4ed8"
CONSERVATIVE_COLOR = "#94a3b8"
UPSIDE_COLOR = "#16a34a"
WARN_COLOR = "#dc2626"


@st.cache_data
def load_all():
    """Load every table the dashboard needs. Returns a dict of DataFrames."""
    sales = pd.read_csv(TABLES / "sales_active.csv", parse_dates=["date"])
    hcp = pd.read_csv(TABLES / "hcp_segmented.csv")
    hcp_raw = pd.read_csv(DATA / "hcp_data.csv", usecols=["hcp_id", "competitor_preference", "years_in_practice", "category_awareness", "brand_awareness"])
    hcp = hcp.merge(hcp_raw, on="hcp_id", how="left")
    consumer = pd.read_csv(TABLES / "consumer_segmented.csv")
    consumer_raw = pd.read_csv(DATA / "consumer_data.csv", usecols=[
        "consumer_id", "purchase_channel", "purchase_frequency", "recommendation_source",
        "aware_of_recall", "parent_age_group", "income_band", "child_age_group"])
    consumer = consumer.drop(columns=["child_age_group"]).merge(consumer_raw, on="consumer_id", how="left")
    territory_seg = pd.read_csv(TABLES / "territory_segmented.csv")
    territory_rank = pd.read_csv(TABLES / "territory_opportunity_ranked.csv")
    competitor = pd.read_csv(DATA / "competitor_data.csv")
    campaign = pd.read_csv(DATA / "campaign_data.csv", parse_dates=["month"])
    territory_full = pd.read_csv(DATA / "territory_data.csv")
    scenario_results = pd.read_csv(TABLES / "scenario_model_results.csv", index_col="scenario")
    lever_sensitivity = pd.read_csv(TABLES / "scenario_lever_sensitivity.csv")

    # Merge territory segment + rank + full attributes into one convenience table
    territory = (
        territory_full
        .merge(territory_seg[["territory_id", "penetration", "territory_segment"]], on="territory_id", how="left")
        .merge(territory_rank[["territory", "opportunity_rank", "opportunity_score"]], on="territory", how="left")
    )

    return dict(
        sales=sales, hcp=hcp, consumer=consumer, territory=territory,
        competitor=competitor, campaign=campaign,
        scenario_results=scenario_results, lever_sensitivity=lever_sensitivity,
    )


def seasonally_adjusted_monthly(sales: pd.DataFrame) -> pd.DataFrame:
    """Monthly revenue/units, seasonally adjusted, reindexed to the full
    calendar so off-market gaps render as genuine breaks rather than
    connecting lines (see notebooks/02_eda.ipynb for why this matters)."""
    monthly = sales.groupby("date").agg(revenue=("revenue", "sum"), units=("units_sold", "sum")).reset_index()
    monthly["seas_index"] = monthly.date.dt.month.map(SEASONALITY)
    monthly["revenue_sa"] = monthly.revenue / monthly.seas_index
    full_cal = pd.date_range(sales.date.min(), sales.date.max(), freq="MS")
    monthly = monthly.set_index("date").reindex(full_cal).rename_axis("date").reset_index()
    monthly["market_phase"] = np.where(
        (monthly.date >= "2024-03-01") & (monthly.date < "2025-09-01"), "off_market", "active"
    )
    return monthly


def recovery_pct(sales: pd.DataFrame) -> float:
    """Latest 3-month seasonally adjusted avg vs pre-recall seasonally adjusted avg."""
    m = seasonally_adjusted_monthly(sales)
    pre = m.loc[(m.date >= "2023-03-01") & (m.date < "2024-03-01"), "revenue_sa"].mean()
    latest = m.loc[m.date >= m.date.max() - pd.DateOffset(months=2), "revenue_sa"].mean()
    return 100 * latest / pre


def kpi_card(col, label, value, delta=None, help_text=None):
    col.metric(label, value, delta=delta, help=help_text)


def synthetic_banner():
    """Shared warning banner shown at the top of every dashboard page."""
    st.markdown(
        """
        <div style="background-color:#fef3c7; border-left:4px solid #d97706; padding:0.6rem 1rem;
                    border-radius:4px; margin-bottom:1rem; font-size:0.85rem;">
        ⚠️ <b>All figures on this page are SYNTHETIC / SIMULATED</b> — an independent case study based on
        public information, not Sanofi data. See <code>data/DATA_DICTIONARY.md</code> for provenance.
        </div>
        """,
        unsafe_allow_html=True,
    )
