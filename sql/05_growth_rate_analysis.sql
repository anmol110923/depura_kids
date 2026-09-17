-- =====================================================================
-- 05_growth_rate_analysis.sql
-- ---------------------------------------------------------------------
-- BUSINESS QUESTION
--   How fast is the post-relaunch recovery moving, and is it still
--   accelerating, plateauing, or reversing? A growth-rate trend answers
--   "is momentum building" in a way a single revenue number cannot.
--
-- METHOD
--   Month-over-month and 3-month-over-prior-3-month growth on seasonally
--   adjusted revenue, using LAG and window frames, restricted to the
--   post-relaunch period (comparisons across the recall gap are
--   meaningless).
-- =====================================================================

WITH seasonality(month_num, seas_index) AS (
    VALUES (1,1.12),(2,1.10),(3,1.00),(4,0.97),(5,0.95),(6,0.95),
           (7,0.94),(8,0.95),(9,0.98),(10,1.02),(11,1.08),(12,1.12)
),
monthly AS (
    SELECT
        s.date,
        SUM(s.revenue) / se.seas_index AS revenue_sa
    FROM sales_active s
    JOIN seasonality se ON se.month_num = EXTRACT(MONTH FROM s.date)
    WHERE s.market_phase = 'post_relaunch'
    GROUP BY s.date, se.seas_index
),
growth AS (
    SELECT
        date,
        revenue_sa,
        LAG(revenue_sa, 1) OVER (ORDER BY date)   AS prev_month_sa,
        -- Trailing 3-month sum vs the 3-month sum immediately before it
        SUM(revenue_sa) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS trailing_3mo,
        SUM(revenue_sa) OVER (ORDER BY date ROWS BETWEEN 5 PRECEDING AND 3 PRECEDING) AS prior_3mo
    FROM monthly
)
SELECT
    date,
    ROUND(revenue_sa, 0)                                          AS revenue_sa,
    ROUND(100.0 * revenue_sa / NULLIF(prev_month_sa, 0) - 100, 1) AS mom_growth_pct,
    ROUND(trailing_3mo, 0)                                        AS trailing_3mo_revenue_sa,
    ROUND(100.0 * trailing_3mo / NULLIF(prior_3mo, 0) - 100, 1)   AS rolling_3mo_vs_prior_3mo_growth_pct
FROM growth
ORDER BY date;

-- Growth-phase classification: has recovery plateaued in the most recent
-- quarter? (Referenced directly in the relaunch strategy's "Phase 2/3"
-- gate criteria.)
WITH seasonality(month_num, seas_index) AS (
    VALUES (1,1.12),(2,1.10),(3,1.00),(4,0.97),(5,0.95),(6,0.95),
           (7,0.94),(8,0.95),(9,0.98),(10,1.02),(11,1.08),(12,1.12)
),
monthly AS (
    SELECT s.date, SUM(s.revenue) / se.seas_index AS revenue_sa
    FROM sales_active s
    JOIN seasonality se ON se.month_num = EXTRACT(MONTH FROM s.date)
    WHERE s.market_phase = 'post_relaunch'
    GROUP BY s.date, se.seas_index
)
SELECT
    ROUND(AVG(CASE WHEN date BETWEEN DATE '2025-09-01' AND DATE '2025-11-01' THEN revenue_sa END), 0) AS q1_post_relaunch_avg,
    ROUND(AVG(CASE WHEN date BETWEEN DATE '2026-06-01' AND DATE '2026-08-01' THEN revenue_sa END), 0) AS latest_quarter_avg,
    ROUND(100.0 * (
        AVG(CASE WHEN date BETWEEN DATE '2026-06-01' AND DATE '2026-08-01' THEN revenue_sa END)
        / NULLIF(AVG(CASE WHEN date BETWEEN DATE '2025-09-01' AND DATE '2025-11-01' THEN revenue_sa END), 0) - 1
    ), 1) AS pct_growth_first_to_latest_quarter
FROM monthly;
