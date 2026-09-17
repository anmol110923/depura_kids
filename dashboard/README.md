# Dashboard — DePURA Kids Relaunch Strategy

An 8-page Streamlit dashboard over the **SYNTHETIC** data in `../data/` and the derived tables in
`../outputs/tables/`. Every page carries a visible synthetic-data warning banner.

## Run it

```bash
pip install -r ../requirements.txt
cd dashboard
streamlit run app.py
```

Requires the notebooks in `../notebooks/` to have been run at least once, since several pages read
`../outputs/tables/*.csv` (segmented HCP/consumer/territory data, the territory opportunity ranking, and the
scenario model results) rather than the raw CSVs directly.

## Structure

```
dashboard/
├── app.py                          # Page 1 — Executive Overview (also the entry point)
├── pages/
│   ├── 2_Market_and_Competition.py
│   ├── 3_HCP_Analytics.py
│   ├── 4_Consumer_Analytics.py
│   ├── 5_Territory_Prioritization.py
│   ├── 6_Campaign_Performance.py
│   ├── 7_Scenario_Planner.py       # interactive — sliders re-run the model live
│   └── 8_Strategic_Recommendations.py
└── utils/
    └── data.py                     # shared, cached data loading + the synthetic-data banner
```

Streamlit's file-based routing means the sidebar page order follows the numeric prefixes above.

## Design notes

- **`utils/data.py` centralises loading.** `load_all()` is wrapped in `@st.cache_data` so every page shares one
  read of the CSVs rather than re-reading on every navigation. It also merges in a few raw-data columns
  (`competitor_preference`, `purchase_channel`, `recommendation_source`, `aware_of_recall`) that the segmented
  exports from `notebooks/03_segmentation.ipynb` don't carry, since those exports were trimmed to only the
  columns the notebook itself needed.
- **The off-market gap renders as a genuine break**, not a connecting line across 17 months of no data — the
  same fix applied in `notebooks/02_eda.ipynb` after the same bug showed up there first.
- **The Scenario Planner (page 7) is a live reimplementation of `notebooks/05_scenario_model.ipynb`'s model**,
  not a shortcut — same baseline calculation, same elasticities, same formula. At the Base-case preset it
  reproduces the notebook's saved output to within rounding (₹6.62 Cr vs. the notebook's ₹6,615,986; the
  driver breakdown matches to two decimal places). If you change the elasticities in the notebook, update
  the `ELASTICITIES` dict in `pages/7_Scenario_Planner.py` to match, or the two will drift apart silently.
- **Page 8's recommendations each cite the specific page/analysis they come from.** Every number quoted there
  was independently checked against the underlying data before being written down (see the project's build
  history for the specific verification queries).

## Testing

Every page was run through Streamlit's `AppTest` framework (which actually executes the script against a
test harness, not just an HTTP smoke test) before being considered done:

```bash
python3 -c "
from streamlit.testing.v1 import AppTest
at = AppTest.from_file('app.py', default_timeout=30)
at.run()
print(at.exception)
"
```

This caught three real issues during development: a debugging leftover in a conditional expression, two
missing-column errors where a segmented CSV didn't carry a field a page needed, and an undeclared
`statsmodels` dependency pulled in by a Plotly trendline option (removed rather than added to requirements).

## Known limitations

- No caching invalidation: if you re-run the notebooks with different assumptions, restart the Streamlit
  server (or clear its cache from the running app's menu) to pick up the new CSVs.
- The Scenario Planner's elasticities are hard-coded to match the notebook at time of writing; see the design
  note above if the notebook's assumptions change.
- Built for a single reviewer, not concurrent multi-user access — `st.cache_data` is process-wide, which is
  fine for a portfolio/interview demo but not how a production commercial dashboard would be architected.
