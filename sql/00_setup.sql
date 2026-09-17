-- =====================================================================
-- 00_setup.sql — load the SYNTHETIC CSVs into DuckDB and build clean views
-- =====================================================================
-- Run first. Every other .sql file in this folder assumes these views exist.
-- Usage (from project root):
--   duckdb depura.db < sql/00_setup.sql
--   duckdb depura.db < sql/01_monthly_sales_trends.sql
--   ... etc, or open depura.db in any DuckDB client / notebook.
--
-- Design note: raw tables keep the data exactly as generated, including the
-- deliberate duplicates, label noise and off-market zero rows. All cleaning
-- happens in named VIEWs, so every downstream query can be run against
-- either the raw table (to demonstrate the issue) or the clean view
-- (to analyse correctly) and the difference is auditable.
-- =====================================================================

CREATE OR REPLACE TABLE raw_sales        AS SELECT * FROM read_csv_auto('data/sales_data.csv');
CREATE OR REPLACE TABLE raw_hcp          AS SELECT * FROM read_csv_auto('data/hcp_data.csv');
CREATE OR REPLACE TABLE raw_consumer     AS SELECT * FROM read_csv_auto('data/consumer_data.csv');
CREATE OR REPLACE TABLE raw_competitor   AS SELECT * FROM read_csv_auto('data/competitor_data.csv');
CREATE OR REPLACE TABLE raw_campaign     AS SELECT * FROM read_csv_auto('data/campaign_data.csv');
CREATE OR REPLACE TABLE raw_territory    AS SELECT * FROM read_csv_auto('data/territory_data.csv');

-- ---------------------------------------------------------------------
-- sales: de-duplicate, canonicalise state labels, tag market phase
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW sales AS
WITH deduped AS (
    SELECT DISTINCT * FROM raw_sales
),
labelled AS (
    SELECT
        *,
        CASE state
            WHEN 'NCT of Delhi' THEN 'Delhi'
            WHEN 'Tamil nadu'   THEN 'Tamil Nadu'
            WHEN 'UP'           THEN 'Uttar Pradesh'
            WHEN 'maharashtra'  THEN 'Maharashtra'
            ELSE state
        END AS state_clean,
        CASE
            WHEN date < DATE '2024-03-01'                          THEN 'pre_recall'
            WHEN date = DATE '2024-03-01'                          THEN 'recall_partial'
            WHEN date = DATE '2024-04-01'                          THEN 'recall_returns'
            WHEN date >  DATE '2024-04-01' AND date < DATE '2025-09-01' THEN 'off_market'
            ELSE 'post_relaunch'
        END AS market_phase
    FROM deduped
)
SELECT
    date, territory_id, territory, region, state_clean AS state, city_tier,
    channel, product, units_sold, revenue, discount_pct, stock_availability,
    distributor_count, market_phase
FROM labelled;

-- Active-demand view: excludes off-market zero rows and the one-off returns
-- month, since neither represents ordinary demand. Used for trend/average
-- calculations; the full `sales` view is used when the recall period itself
-- is the subject of analysis.
CREATE OR REPLACE VIEW sales_active AS
SELECT * FROM sales
WHERE market_phase IN ('pre_recall', 'recall_partial', 'post_relaunch')
  AND units_sold > 0;

-- ---------------------------------------------------------------------
-- hcp: null out the known entry errors (patient volume = 9999)
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW hcp AS
SELECT
    hcp_id, specialty, territory_id, region, city_tier, years_in_practice,
    CASE WHEN monthly_patient_volume = 9999 THEN NULL ELSE monthly_patient_volume END AS monthly_patient_volume,
    category_awareness, brand_awareness, recommendation_rate, digital_engagement,
    rep_visits_last_quarter, pre_recall_prescriber, competitor_preference
FROM raw_hcp;

CREATE OR REPLACE VIEW consumer   AS SELECT * FROM raw_consumer;
CREATE OR REPLACE VIEW competitor AS SELECT * FROM raw_competitor;
CREATE OR REPLACE VIEW campaign   AS SELECT * FROM raw_campaign;
CREATE OR REPLACE VIEW territory  AS SELECT * FROM raw_territory;

-- Quick reconciliation check: row counts before/after cleaning
SELECT 'raw_sales' AS tbl, COUNT(*) AS rows FROM raw_sales
UNION ALL SELECT 'sales (deduped)', COUNT(*) FROM sales
UNION ALL SELECT 'sales_active', COUNT(*) FROM sales_active;
