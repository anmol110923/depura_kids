-- =====================================================================
-- 08_customer_segmentation.sql
-- ---------------------------------------------------------------------
-- BUSINESS QUESTION
--   Which consumer segments (as defined in research/market_research.md
--   / the case study's segmentation framework) are the biggest and which
--   currently favour DePURA Kids the least?
--
-- METHOD
--   Applies the four consumer segmentation rules from the project
--   framework, in the stated priority order (a CASE statement evaluated
--   top-to-bottom so every parent lands in exactly one segment):
--     1. Low-awareness      : awareness <= 2
--     2. Price-sensitive    : price_sensitivity >= 4
--     3. Convenience-driven : buys via e-pharmacy or quick commerce
--     4. Health-conscious   : brand_trust >= 4 AND adherence_score >= 0.7
--     5. Mainstream         : everyone else
--   Then profiles each segment's size and current DePURA Kids share.
-- =====================================================================

WITH segmented AS (
    SELECT
        *,
        CASE
            WHEN awareness <= 2 THEN 'Low-awareness'
            WHEN price_sensitivity >= 4 THEN 'Price-sensitive'
            WHEN purchase_channel IN ('E-Pharmacy', 'Quick Commerce') THEN 'Convenience-driven'
            WHEN brand_trust >= 4 AND adherence_score >= 0.7 THEN 'Health-conscious'
            ELSE 'Mainstream'
        END AS consumer_segment
    FROM consumer
)
SELECT
    consumer_segment,
    COUNT(*)                                                          AS consumers,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)                 AS pct_of_total,
    ROUND(100.0 * SUM(CASE WHEN current_brand = 'DePURA Kids' THEN 1 ELSE 0 END)
        / COUNT(*), 1)                                                 AS depura_share_pct,
    ROUND(AVG(adherence_score), 3)                                     AS avg_adherence_score,
    ROUND(AVG(price_sensitivity), 2)                                   AS avg_price_sensitivity,
    ROUND(AVG(brand_trust), 2)                                         AS avg_brand_trust
FROM segmented
GROUP BY consumer_segment
ORDER BY consumers DESC;

-- Segment x recommendation source cross-tab: where does each segment get
-- its information, which tells us which channel to use to reach it.
WITH segmented AS (
    SELECT *,
        CASE
            WHEN awareness <= 2 THEN 'Low-awareness'
            WHEN price_sensitivity >= 4 THEN 'Price-sensitive'
            WHEN purchase_channel IN ('E-Pharmacy', 'Quick Commerce') THEN 'Convenience-driven'
            WHEN brand_trust >= 4 AND adherence_score >= 0.7 THEN 'Health-conscious'
            ELSE 'Mainstream'
        END AS consumer_segment
    FROM consumer
)
SELECT
    consumer_segment,
    recommendation_source,
    COUNT(*) AS consumers,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY consumer_segment), 1) AS pct_within_segment
FROM segmented
GROUP BY consumer_segment, recommendation_source
QUALIFY ROW_NUMBER() OVER (PARTITION BY consumer_segment ORDER BY COUNT(*) DESC) <= 2
ORDER BY consumer_segment, consumers DESC;
