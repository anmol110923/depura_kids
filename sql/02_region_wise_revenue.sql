-- =====================================================================
-- 02_region_wise_revenue.sql
-- ---------------------------------------------------------------------
-- BUSINESS QUESTION
--   How is post-relaunch revenue distributed across regions and city
--   tiers, and how does each region's share of revenue compare with its
--   share of the addressable category?
--
-- METHOD
--   Post-relaunch revenue by region joined to territory-level category
--   potential (data/territory_data.csv -> market_potential), so an
--   "over/under-indexed" view is possible without yet doing the full
--   territory scoring model (that comes in notebook 04).
-- =====================================================================

WITH region_revenue AS (
    SELECT
        region,
        SUM(revenue)                                        AS post_relaunch_revenue
    FROM sales_active
    WHERE market_phase = 'post_relaunch'
    GROUP BY region
),
region_potential AS (
    SELECT region, SUM(market_potential) * 1e5 AS market_potential_inr  -- lakh -> INR
    FROM territory
    GROUP BY region
),
combined AS (
    SELECT
        r.region,
        r.post_relaunch_revenue,
        p.market_potential_inr,
        r.post_relaunch_revenue / NULLIF(SUM(r.post_relaunch_revenue) OVER (), 0)   AS revenue_share,
        p.market_potential_inr  / NULLIF(SUM(p.market_potential_inr) OVER (), 0)    AS potential_share
    FROM region_revenue r
    JOIN region_potential p USING (region)
)
SELECT
    region,
    ROUND(post_relaunch_revenue, 0)                          AS post_relaunch_revenue,
    ROUND(market_potential_inr, 0)                            AS category_market_potential,
    ROUND(100.0 * revenue_share, 1)                           AS revenue_share_pct,
    ROUND(100.0 * potential_share, 1)                         AS potential_share_pct,
    ROUND(revenue_share / NULLIF(potential_share, 0), 2)      AS revenue_vs_potential_index,
    CASE
        WHEN revenue_share / NULLIF(potential_share, 0) >= 1.1 THEN 'Over-indexed (punching above potential)'
        WHEN revenue_share / NULLIF(potential_share, 0) <= 0.9 THEN 'Under-indexed (below potential)'
        ELSE 'In line with potential'
    END                                                        AS read
FROM combined
ORDER BY post_relaunch_revenue DESC;

-- Same view cut by city tier, which is often the more actionable axis for
-- channel and field-force planning.
SELECT
    city_tier,
    SUM(CASE WHEN market_phase = 'post_relaunch' THEN revenue END)              AS post_relaunch_revenue,
    ROUND(100.0 * SUM(CASE WHEN market_phase = 'post_relaunch' THEN revenue END)
        / SUM(SUM(CASE WHEN market_phase = 'post_relaunch' THEN revenue END)) OVER (), 1) AS revenue_share_pct
FROM sales_active
GROUP BY city_tier
ORDER BY post_relaunch_revenue DESC;
