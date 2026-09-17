-- =====================================================================
-- 06_top_bottom_territories.sql
-- ---------------------------------------------------------------------
-- BUSINESS QUESTION
--   Which territories are the strongest and weakest performers today,
--   and — more usefully than a raw revenue ranking — which are
--   under-performing relative to their OWN category potential?
--
-- METHOD
--   Ranks territories by current_sales (raw performance) and separately
--   by penetration = current_sales / market_potential (relative
--   performance). A territory can be top-5 by revenue and still be
--   under-penetrated if it is simply a large market; the two rankings
--   are deliberately shown side by side so that distinction is visible.
-- =====================================================================

WITH scored AS (
    SELECT
        territory,
        state,
        region,
        city_tier,
        current_sales,
        market_potential,
        current_sales / NULLIF(market_potential, 0)               AS penetration,
        RANK() OVER (ORDER BY current_sales DESC)                  AS revenue_rank,
        RANK() OVER (ORDER BY current_sales / NULLIF(market_potential, 0) DESC) AS penetration_rank
    FROM territory
)
SELECT
    territory, state, region, city_tier,
    ROUND(current_sales, 1)                        AS current_sales_inr_lakh,
    ROUND(market_potential, 1)                      AS market_potential_inr_lakh,
    ROUND(100.0 * penetration, 1)                   AS penetration_pct,
    revenue_rank,
    penetration_rank
FROM scored
ORDER BY revenue_rank
LIMIT 5;

-- Bottom 5 by revenue
WITH scored AS (
    SELECT
        territory, state, region, city_tier, current_sales, market_potential,
        current_sales / NULLIF(market_potential, 0) AS penetration,
        RANK() OVER (ORDER BY current_sales DESC) AS revenue_rank,
        RANK() OVER (ORDER BY current_sales / NULLIF(market_potential, 0) DESC) AS penetration_rank
    FROM territory
)
SELECT territory, state, region, city_tier,
       ROUND(current_sales, 1) AS current_sales_inr_lakh,
       ROUND(market_potential, 1) AS market_potential_inr_lakh,
       ROUND(100.0 * penetration, 1) AS penetration_pct,
       revenue_rank, penetration_rank
FROM scored
ORDER BY revenue_rank DESC
LIMIT 5;

-- "Hidden large markets": territories with high market_potential (top
-- tercile) but low penetration (bottom tercile) — these would NOT surface
-- from a plain revenue ranking, which is exactly why they matter.
WITH scored AS (
    SELECT
        territory, state, region, city_tier, current_sales, market_potential,
        current_sales / NULLIF(market_potential, 0) AS penetration,
        NTILE(3) OVER (ORDER BY market_potential)   AS potential_tercile,
        NTILE(3) OVER (ORDER BY current_sales / NULLIF(market_potential, 0)) AS penetration_tercile
    FROM territory
)
SELECT territory, state, region, city_tier,
       ROUND(market_potential, 1) AS market_potential_inr_lakh,
       ROUND(100.0 * penetration, 1) AS penetration_pct
FROM scored
WHERE potential_tercile = 3 AND penetration_tercile = 1
ORDER BY market_potential DESC;
