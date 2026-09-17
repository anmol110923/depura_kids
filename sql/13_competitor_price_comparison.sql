-- =====================================================================
-- 13_competitor_price_comparison.sql
-- ---------------------------------------------------------------------
-- BUSINESS QUESTION
--   Where does DePURA Kids sit on price, and does it matter which metric
--   you use — pack MRP or cost per equivalent 400 IU dose? (Comparing
--   pack MRP directly is the wrong comparison — see
--   research/competitor_analysis.md §1 — because pack sizes and
--   strengths differ across brands.)
--
-- METHOD
--   Ranks competitors on raw pack price AND on the normalised cost-per-
--   dose metric side by side, so the difference in ranking is visible.
--   Brands with unverified strength are shown but excluded from the
--   dose-based ranking (their cost_per_400iu_dose is NULL by
--   construction — see data/DATA_DICTIONARY.md).
-- =====================================================================

SELECT
    brand,
    manufacturer,
    dosage,
    pack_size,
    price                                                       AS pack_mrp_inr,
    RANK() OVER (ORDER BY price DESC)                            AS pack_price_rank,
    cost_per_400iu_dose,
    estimated_price_index,
    RANK() OVER (ORDER BY cost_per_400iu_dose DESC)              AS dose_cost_rank,
    CASE WHEN cost_per_400iu_dose IS NULL THEN 'Strength unverified — excluded from dose-based ranking'
         ELSE NULL END                                            AS caveat
FROM competitor
ORDER BY dose_cost_rank NULLS LAST;

-- DePURA Kids' position relative to each cluster average (premium / mid /
-- value), using the clusters defined in research/competitor_analysis.md.
WITH clustered AS (
    SELECT *,
        CASE
            WHEN brand IN ('DePURA Kids', 'Arachitol Kids / Nano', 'Kidrich D3 800 IU Nano') THEN 'Premium nano'
            WHEN brand IN ('Uprise-D3 Drops', 'D3 Must Forte') THEN 'Mid-price'
            ELSE 'Value'
        END AS price_cluster
    FROM competitor
)
SELECT
    price_cluster,
    COUNT(*)                                          AS brands,
    ROUND(AVG(cost_per_400iu_dose), 2)                 AS avg_cost_per_400iu_dose,
    ROUND(MIN(cost_per_400iu_dose), 2)                 AS min_cost_per_400iu_dose,
    ROUND(MAX(cost_per_400iu_dose), 2)                 AS max_cost_per_400iu_dose
FROM clustered
GROUP BY price_cluster
ORDER BY avg_cost_per_400iu_dose DESC;
