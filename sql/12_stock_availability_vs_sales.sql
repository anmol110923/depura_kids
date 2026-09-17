-- =====================================================================
-- 12_stock_availability_vs_sales.sql
-- ---------------------------------------------------------------------
-- BUSINESS QUESTION
--   Does poor stock availability actually cost sales, and if so, how
--   much? This underpins the recommendation to treat distribution
--   fill-rate as a KPI, not just an operational metric (see
--   research/competitor_analysis.md §6).
--
-- METHOD
--   Correlation of stock_availability with units_sold, computed WITHIN
--   each territory-channel-SKU series (raw pooled correlation would be
--   confounded by territory size — see data/DATA_DICTIONARY.md §5,
--   confounder #2). Units are converted to an index (unit / series mean)
--   before pooling across series, so a small territory's low absolute
--   volume doesn't get outweighed by a large territory's — every series
--   contributes on the same 1.0-centred scale.
-- =====================================================================

WITH post_relaunch AS (
    SELECT * FROM sales_active WHERE market_phase = 'post_relaunch'
),
series_avg AS (
    SELECT
        territory_id, channel, product,
        AVG(units_sold) AS series_mean_units
    FROM post_relaunch
    GROUP BY territory_id, channel, product
),
indexed AS (
    SELECT
        p.*,
        p.units_sold / NULLIF(s.series_mean_units, 0) AS units_index
    FROM post_relaunch p
    JOIN series_avg s USING (territory_id, channel, product)
)
SELECT
    ROUND(CORR(stock_availability, units_index), 3) AS within_series_corr_stock_vs_units,
    COUNT(*)                                          AS observations
FROM indexed;

-- Bucketed view for an intuitive chart: average unit index by stock band.
WITH post_relaunch AS (
    SELECT * FROM sales_active WHERE market_phase = 'post_relaunch'
),
series_avg AS (
    SELECT territory_id, channel, product, AVG(units_sold) AS series_mean_units
    FROM post_relaunch GROUP BY territory_id, channel, product
),
indexed AS (
    SELECT p.*, p.units_sold / NULLIF(s.series_mean_units, 0) AS units_index
    FROM post_relaunch p JOIN series_avg s USING (territory_id, channel, product)
)
SELECT
    CASE
        WHEN stock_availability < 0.70 THEN '1. <70%'
        WHEN stock_availability < 0.80 THEN '2. 70-80%'
        WHEN stock_availability < 0.90 THEN '3. 80-90%'
        ELSE '4. 90%+'
    END                                            AS stock_availability_band,
    COUNT(*)                                       AS observations,
    ROUND(AVG(units_index), 3)                      AS avg_units_index
FROM indexed
GROUP BY stock_availability_band
ORDER BY stock_availability_band;

-- Estimated revenue left on the table: territories whose average
-- post-relaunch stock availability is below the network median, scaled
-- by the within-series elasticity implied above (illustrative, not a
-- precise revenue-recovery forecast).
WITH med AS (
    SELECT MEDIAN(stock_availability_avg) AS median_stock FROM territory
)
SELECT
    t.territory,
    ROUND(t.stock_availability_avg, 3)  AS stock_availability_avg,
    ROUND(m.median_stock, 3)            AS network_median_stock,
    ROUND(t.current_sales, 1)           AS current_sales_inr_lakh,
    ROUND(t.current_sales * (m.median_stock / NULLIF(t.stock_availability_avg,0) - 1), 1) AS illustrative_upside_inr_lakh
FROM territory t CROSS JOIN med m
WHERE t.stock_availability_avg < m.median_stock
ORDER BY illustrative_upside_inr_lakh DESC
LIMIT 10;
