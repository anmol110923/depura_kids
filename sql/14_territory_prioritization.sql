-- =====================================================================
-- 14_territory_prioritization.sql
-- ---------------------------------------------------------------------
-- BUSINESS QUESTION
--   Using the full segmentation framework (Defend / Grow / Build /
--   Deprioritize, defined in research/market_research.md and applied
--   quantitatively in notebooks/04_territory_analysis.ipynb), which
--   territories fall into each action category, and what should each
--   category's commercial motion be?
--
-- METHOD
--   Segmentation rule (median-split, matching the case-study framework):
--     Defend       : potential >= median AND penetration >= median
--     Grow         : potential >= median AND penetration <  median
--     Build        : potential <  median AND competitor_strength < median
--     Deprioritize : potential <  median AND competitor_strength >= median
--   This SQL file computes the segment membership directly from
--   territory_data so it can be run standalone; the notebook version
--   layers on the full opportunity_score from Q11/the weighted model.
-- =====================================================================

WITH med AS (
    SELECT
        MEDIAN(market_potential)                                 AS med_potential,
        MEDIAN(current_sales / NULLIF(market_potential, 0))       AS med_penetration,
        MEDIAN(competitor_strength)                                AS med_competitor
    FROM territory
),
segmented AS (
    SELECT
        t.*,
        t.current_sales / NULLIF(t.market_potential, 0)           AS penetration,
        CASE
            WHEN t.market_potential >= m.med_potential AND t.current_sales / NULLIF(t.market_potential,0) >= m.med_penetration THEN 'Defend'
            WHEN t.market_potential >= m.med_potential AND t.current_sales / NULLIF(t.market_potential,0) <  m.med_penetration THEN 'Grow'
            WHEN t.market_potential <  m.med_potential AND t.competitor_strength < m.med_competitor THEN 'Build'
            ELSE 'Deprioritize'
        END AS territory_segment
    FROM territory t CROSS JOIN med m
)
SELECT
    territory_segment,
    COUNT(*)                                          AS territory_count,
    ROUND(SUM(current_sales), 1)                       AS total_current_sales_inr_lakh,
    ROUND(SUM(market_potential), 1)                     AS total_market_potential_inr_lakh,
    ROUND(AVG(penetration) * 100, 1)                    AS avg_penetration_pct,
    ROUND(AVG(competitor_strength), 3)                  AS avg_competitor_strength,
    ROUND(AVG(sales_force_coverage), 3)                 AS avg_sales_force_coverage
FROM segmented
GROUP BY territory_segment
ORDER BY total_market_potential_inr_lakh DESC;

-- Full territory list with segment labels, for the dashboard's territory
-- prioritization page.
WITH med AS (
    SELECT
        MEDIAN(market_potential)                                 AS med_potential,
        MEDIAN(current_sales / NULLIF(market_potential, 0))       AS med_penetration,
        MEDIAN(competitor_strength)                                AS med_competitor
    FROM territory
)
SELECT
    t.territory, t.state, t.region, t.city_tier,
    ROUND(t.current_sales, 1)                          AS current_sales_inr_lakh,
    ROUND(t.market_potential, 1)                        AS market_potential_inr_lakh,
    ROUND(100.0 * t.current_sales / NULLIF(t.market_potential,0), 1) AS penetration_pct,
    CASE
        WHEN t.market_potential >= m.med_potential AND t.current_sales / NULLIF(t.market_potential,0) >= m.med_penetration THEN 'Defend'
        WHEN t.market_potential >= m.med_potential AND t.current_sales / NULLIF(t.market_potential,0) <  m.med_penetration THEN 'Grow'
        WHEN t.market_potential <  m.med_potential AND t.competitor_strength < m.med_competitor THEN 'Build'
        ELSE 'Deprioritize'
    END AS territory_segment
FROM territory t CROSS JOIN med m
ORDER BY territory_segment, market_potential_inr_lakh DESC;
