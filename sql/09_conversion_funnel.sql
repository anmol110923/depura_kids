-- =====================================================================
-- 09_conversion_funnel.sql
-- ---------------------------------------------------------------------
-- BUSINESS QUESTION
--   How efficiently does each campaign audience move from impression to
--   conversion, and where in the funnel is the biggest drop-off?
--
-- METHOD
--   Impressions -> clicks -> leads -> conversions funnel by audience,
--   with stage-to-stage conversion rates. Because "conversion" means
--   something different for HCP vs parent audiences (see
--   data/DATA_DICTIONARY.md — conversion_definition column), the funnel
--   is built per audience rather than pooled, so the comparison stays
--   apples-to-apples.
-- =====================================================================

WITH funnel AS (
    SELECT
        audience,
        SUM(impressions)  AS impressions,
        SUM(clicks)       AS clicks,
        SUM(leads)        AS leads,
        SUM(conversions)  AS conversions,
        SUM(spend)        AS spend
    FROM campaign
    GROUP BY audience
)
SELECT
    audience,
    impressions,
    clicks,
    leads,
    conversions,
    ROUND(100.0 * clicks / NULLIF(impressions, 0), 2)      AS impression_to_click_pct,
    ROUND(100.0 * leads / NULLIF(clicks, 0), 2)             AS click_to_lead_pct,
    ROUND(100.0 * conversions / NULLIF(leads, 0), 2)        AS lead_to_conversion_pct,
    ROUND(100.0 * conversions / NULLIF(impressions, 0), 4)  AS overall_impression_to_conversion_pct,
    ROUND(spend / NULLIF(conversions, 0), 0)                AS blended_cac
FROM funnel
ORDER BY spend DESC;

-- Channel-level funnel within the "Parents" audience specifically, since
-- that is where budget reallocation choices are most numerous (6 channels
-- competing for the same audience, vs 3 for HCP and 1 for Pharmacist).
SELECT
    channel,
    SUM(impressions) AS impressions,
    SUM(clicks)       AS clicks,
    SUM(leads)        AS leads,
    SUM(conversions)  AS conversions,
    ROUND(100.0 * SUM(clicks) / NULLIF(SUM(impressions), 0), 2)   AS impression_to_click_pct,
    ROUND(100.0 * SUM(conversions) / NULLIF(SUM(leads), 0), 2)     AS lead_to_conversion_pct,
    ROUND(SUM(spend) / NULLIF(SUM(conversions), 0), 0)             AS cac
FROM campaign
WHERE audience IN ('Parents', 'Parents (existing)')
GROUP BY channel
ORDER BY cac ASC;
