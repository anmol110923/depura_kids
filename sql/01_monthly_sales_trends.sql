-- =====================================================================
-- 01_monthly_sales_trends.sql
-- ---------------------------------------------------------------------
-- BUSINESS QUESTION
--   How has DePURA Kids' demand moved month over month, and how close is
--   the post-relaunch run-rate to the pre-recall baseline?
--
-- METHOD
--   Monthly units/revenue from sales_active (off-market and returns
--   months excluded — see sql/00_setup.sql). A seasonally adjusted
--   revenue is added because vitamin D demand is directionally higher in
--   winter [research/market_research.md §3.2], so raw month-over-month
--   comparisons would confuse seasonality with real recovery.
--   Seasonality index values are the same ones used to generate the data
--   (config/data_generation.yaml -> demand.seasonality), applied here as
--   a lookup so the query does not need to re-derive them from the data
--   it is trying to measure.
-- =====================================================================

WITH seasonality(month_num, seas_index) AS (
    VALUES (1,1.12),(2,1.10),(3,1.00),(4,0.97),(5,0.95),(6,0.95),
           (7,0.94),(8,0.95),(9,0.98),(10,1.02),(11,1.08),(12,1.12)
),
monthly AS (
    SELECT
        date,
        market_phase,
        SUM(units_sold)                                   AS units,
        SUM(revenue)                                       AS revenue
    FROM sales_active
    GROUP BY date, market_phase
)
SELECT
    m.date,
    m.market_phase,
    m.units,
    ROUND(m.revenue, 0)                                    AS revenue,
    ROUND(m.revenue / s.seas_index, 0)                     AS revenue_seasonally_adjusted,
    ROUND(
        100.0 * m.revenue / NULLIF(LAG(m.revenue) OVER (ORDER BY m.date), 0) - 100, 1
    )                                                        AS mom_revenue_growth_pct,
    -- 3-month rolling seasonally adjusted revenue: smooths month-to-month
    -- noise so the recovery trajectory is readable at a glance.
    ROUND(AVG(m.revenue / s.seas_index) OVER (
        ORDER BY m.date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 0)                                                    AS revenue_sa_3mo_rolling
FROM monthly m
JOIN seasonality s ON s.month_num = EXTRACT(MONTH FROM m.date)
ORDER BY m.date;

-- Headline recovery metric referenced throughout the case study:
-- seasonally adjusted post-relaunch run-rate (last 3 available months)
-- vs seasonally adjusted pre-recall run-rate (last 12 pre-recall months).
WITH seasonality(month_num, seas_index) AS (
    VALUES (1,1.12),(2,1.10),(3,1.00),(4,0.97),(5,0.95),(6,0.95),
           (7,0.94),(8,0.95),(9,0.98),(10,1.02),(11,1.08),(12,1.12)
),
sa AS (
    SELECT date, market_phase, SUM(revenue) / s.seas_index AS revenue_sa
    FROM sales_active s2
    JOIN seasonality s ON s.month_num = EXTRACT(MONTH FROM s2.date)
    GROUP BY date, market_phase, s.seas_index
)
SELECT
    ROUND(AVG(CASE WHEN market_phase = 'pre_recall' AND date >= DATE '2023-03-01' AND date < DATE '2024-03-01'
                   THEN revenue_sa END), 0)                AS pre_recall_avg_monthly_revenue_sa,
    ROUND(AVG(CASE WHEN date >= DATE '2026-06-01' THEN revenue_sa END), 0) AS latest_3mo_avg_monthly_revenue_sa,
    ROUND(100.0 *
        AVG(CASE WHEN date >= DATE '2026-06-01' THEN revenue_sa END) /
        NULLIF(AVG(CASE WHEN market_phase = 'pre_recall' AND date >= DATE '2023-03-01' AND date < DATE '2024-03-01'
                        THEN revenue_sa END), 0), 1)         AS pct_of_pre_recall_runrate
FROM sa;
