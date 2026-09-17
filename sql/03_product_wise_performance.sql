-- =====================================================================
-- 03_product_wise_performance.sql
-- ---------------------------------------------------------------------
-- BUSINESS QUESTION
--   How do the 15 ml and 10 ml SKUs compare, and has the mix shifted
--   since relaunch? A shift toward the smaller pack could signal
--   affordability pressure or trial behaviour among new/returning buyers.
--
-- METHOD
--   Units, revenue and average realised price (net of discount) per SKU,
--   split pre-recall vs post-relaunch, with a mix-shift column.
-- =====================================================================

WITH product_phase AS (
    SELECT
        product,
        market_phase,
        SUM(units_sold)                                        AS units,
        SUM(revenue)                                           AS revenue,
        SUM(revenue) / NULLIF(SUM(units_sold), 0)               AS avg_net_realisation_per_unit
    FROM sales_active
    WHERE market_phase IN ('pre_recall', 'post_relaunch')
    GROUP BY product, market_phase
),
mix AS (
    SELECT
        market_phase,
        product,
        units,
        revenue,
        avg_net_realisation_per_unit,
        units / SUM(units) OVER (PARTITION BY market_phase)     AS unit_mix_share
    FROM product_phase
)
SELECT
    product,
    market_phase,
    units,
    ROUND(revenue, 0)                                          AS revenue,
    ROUND(avg_net_realisation_per_unit, 1)                      AS avg_net_realisation_per_unit,
    ROUND(100.0 * unit_mix_share, 1)                            AS unit_mix_share_pct
FROM mix
ORDER BY product, market_phase;

-- Mix-shift summary: has the 10 ml pack gained share since relaunch?
WITH mix AS (
    SELECT
        market_phase,
        product,
        SUM(units_sold) AS units
    FROM sales_active
    WHERE market_phase IN ('pre_recall', 'post_relaunch')
    GROUP BY market_phase, product
),
share AS (
    SELECT
        market_phase, product, units,
        units / SUM(units) OVER (PARTITION BY market_phase) AS share
    FROM mix
)
SELECT
    product,
    ROUND(100.0 * MAX(CASE WHEN market_phase = 'pre_recall' THEN share END), 1)    AS pre_recall_share_pct,
    ROUND(100.0 * MAX(CASE WHEN market_phase = 'post_relaunch' THEN share END), 1) AS post_relaunch_share_pct,
    ROUND(100.0 * (MAX(CASE WHEN market_phase = 'post_relaunch' THEN share END)
                 - MAX(CASE WHEN market_phase = 'pre_recall' THEN share END)), 1)  AS share_pt_change
FROM share
GROUP BY product
ORDER BY product;
