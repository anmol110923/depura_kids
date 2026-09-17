-- =====================================================================
-- 04_channel_contribution.sql
-- ---------------------------------------------------------------------
-- BUSINESS QUESTION
--   Which sales channels drive revenue today, and which channel gained
--   the most ground since relaunch (a signal for where to invest trade
--   and digital spend)?
--
-- METHOD
--   Revenue and unit share by channel, pre-recall vs post-relaunch,
--   plus average discount and stock availability per channel (context
--   for why a channel might be under- or over-performing).
-- =====================================================================

WITH channel_phase AS (
    SELECT
        channel,
        market_phase,
        SUM(units_sold)                                    AS units,
        SUM(revenue)                                       AS revenue,
        AVG(discount_pct)                                  AS avg_discount,
        AVG(stock_availability)                             AS avg_stock_availability
    FROM sales_active
    WHERE market_phase IN ('pre_recall', 'post_relaunch')
    GROUP BY channel, market_phase
),
shares AS (
    SELECT
        *,
        revenue / SUM(revenue) OVER (PARTITION BY market_phase) AS revenue_share
    FROM channel_phase
)
SELECT
    channel,
    market_phase,
    units,
    ROUND(revenue, 0)                                       AS revenue,
    ROUND(100.0 * revenue_share, 1)                          AS revenue_share_pct,
    ROUND(100.0 * avg_discount, 1)                           AS avg_discount_pct,
    ROUND(100.0 * avg_stock_availability, 1)                 AS avg_stock_availability_pct
FROM shares
ORDER BY channel, market_phase;

-- Channel share-point change, pre-recall -> post-relaunch (the "who gained
-- ground" summary a category lead would ask for first).
WITH channel_phase AS (
    SELECT channel, market_phase, SUM(revenue) AS revenue
    FROM sales_active
    WHERE market_phase IN ('pre_recall', 'post_relaunch')
    GROUP BY channel, market_phase
),
shares AS (
    SELECT channel, market_phase, revenue,
           revenue / SUM(revenue) OVER (PARTITION BY market_phase) AS share
    FROM channel_phase
)
SELECT
    channel,
    ROUND(100.0 * MAX(CASE WHEN market_phase = 'pre_recall' THEN share END), 1)     AS pre_recall_share_pct,
    ROUND(100.0 * MAX(CASE WHEN market_phase = 'post_relaunch' THEN share END), 1)  AS post_relaunch_share_pct,
    ROUND(100.0 * (MAX(CASE WHEN market_phase = 'post_relaunch' THEN share END)
                 - MAX(CASE WHEN market_phase = 'pre_recall' THEN share END)), 1)   AS share_pt_change
FROM shares
GROUP BY channel
ORDER BY share_pt_change DESC;
