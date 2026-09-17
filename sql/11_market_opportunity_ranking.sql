-- =====================================================================
-- 11_market_opportunity_ranking.sql
-- ---------------------------------------------------------------------
-- BUSINESS QUESTION
--   If we could only act on a handful of territories next quarter, which
--   ones combine (a) real headroom, (b) a fixable reason for the
--   shortfall, and (c) low competitive resistance?
--
-- METHOD
--   A simplified opportunity score as a preview of the full weighted
--   model built in notebooks/04_territory_analysis.ipynb (documented in
--   full, with weight rationale and a sensitivity test, in
--   strategy/kpi_framework.md and the case study). Each component is
--   min-max normalised 0-1 so the SQL score can be reproduced without
--   Python. Weights match the case-study framework:
--     30% market potential, 20% HCP opportunity (1 - brand_awareness),
--     15% growth potential (1 - penetration), 15% brand gap
--     (1 - brand_awareness), 10% channel readiness (stock availability),
--     10% competitive opportunity (1 - competitor_strength).
--   NOTE: "HCP opportunity" and "brand gap" both use (1 - brand_awareness)
--   in this simplified SQL version because hcp-level digital/rep coverage
--   fields aren't joined here; the notebook version differentiates them
--   using hcp_data directly. This SQL version is intentionally the
--   coarser, quickly reproducible cut.
-- =====================================================================

WITH bounds AS (
    SELECT
        MIN(market_potential) AS mp_min, MAX(market_potential) AS mp_max,
        MIN(current_sales / NULLIF(market_potential,0)) AS pen_min, MAX(current_sales / NULLIF(market_potential,0)) AS pen_max,
        MIN(brand_awareness) AS aw_min, MAX(brand_awareness) AS aw_max,
        MIN(stock_availability_avg) AS stock_min, MAX(stock_availability_avg) AS stock_max,
        MIN(competitor_strength) AS comp_min, MAX(competitor_strength) AS comp_max
    FROM territory
),
norm AS (
    SELECT
        t.territory, t.state, t.region, t.city_tier,
        t.current_sales, t.market_potential, t.brand_awareness, t.competitor_strength,
        t.stock_availability_avg,
        (t.market_potential - b.mp_min) / NULLIF(b.mp_max - b.mp_min, 0)                             AS n_potential,
        1 - (t.brand_awareness - b.aw_min) / NULLIF(b.aw_max - b.aw_min, 0)                           AS n_hcp_opportunity,
        1 - ((t.current_sales / NULLIF(t.market_potential,0)) - b.pen_min) / NULLIF(b.pen_max - b.pen_min, 0) AS n_growth_potential,
        1 - (t.brand_awareness - b.aw_min) / NULLIF(b.aw_max - b.aw_min, 0)                           AS n_brand_gap,
        (t.stock_availability_avg - b.stock_min) / NULLIF(b.stock_max - b.stock_min, 0)               AS n_channel_readiness,
        1 - (t.competitor_strength - b.comp_min) / NULLIF(b.comp_max - b.comp_min, 0)                 AS n_competitive_opportunity
    FROM territory t CROSS JOIN bounds b
)
SELECT
    territory, state, region, city_tier,
    ROUND(current_sales, 1)     AS current_sales_inr_lakh,
    ROUND(market_potential, 1) AS market_potential_inr_lakh,
    ROUND(
        0.30 * n_potential + 0.20 * n_hcp_opportunity + 0.15 * n_growth_potential
        + 0.15 * n_brand_gap + 0.10 * n_channel_readiness + 0.10 * n_competitive_opportunity
    , 3) AS opportunity_score,
    RANK() OVER (ORDER BY
        0.30 * n_potential + 0.20 * n_hcp_opportunity + 0.15 * n_growth_potential
        + 0.15 * n_brand_gap + 0.10 * n_channel_readiness + 0.10 * n_competitive_opportunity
    DESC) AS opportunity_rank
FROM norm
ORDER BY opportunity_rank
LIMIT 10;
