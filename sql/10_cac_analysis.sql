-- =====================================================================
-- 10_cac_analysis.sql
-- ---------------------------------------------------------------------
-- BUSINESS QUESTION
--   Which channels deliver the best cost-per-conversion within each
--   audience, and does spending more in a channel make it more or less
--   efficient (diminishing returns)?
--
-- METHOD
--   1. CAC ranking by channel, within audience (comparing HCP CAC to
--      parent CAC directly would be misleading — see 09's header note).
--   2. Month-over-month spend vs CAC correlation per channel: a positive
--      correlation means CAC rises as spend rises in that month, i.e.
--      diminishing returns within-channel (planted relationship P10 in
--      data/DATA_DICTIONARY.md).
-- =====================================================================

SELECT
    audience,
    channel,
    SUM(spend)                                       AS total_spend,
    SUM(conversions)                                 AS total_conversions,
    ROUND(SUM(spend) / NULLIF(SUM(conversions), 0), 0) AS cac,
    RANK() OVER (PARTITION BY audience ORDER BY SUM(spend) / NULLIF(SUM(conversions), 0)) AS cac_rank_within_audience
FROM campaign
GROUP BY audience, channel
ORDER BY audience, cac_rank_within_audience;

-- Diminishing-returns check: correlation between monthly spend and that
-- month's CAC, per channel. A reliably positive correlation means the
-- channel is already being pushed into its less-efficient range in some
-- months — useful evidence for "reallocate, don't just add more spend".
SELECT
    channel,
    COUNT(*)                                          AS months_observed,
    ROUND(CORR(spend, cac), 3)                         AS spend_vs_cac_corr,
    ROUND(MIN(spend), 0)                               AS min_monthly_spend,
    ROUND(MAX(spend), 0)                               AS max_monthly_spend,
    ROUND(MIN(cac), 0)                                 AS cac_at_min_spend_month,
    ROUND(MAX(cac), 0)                                 AS cac_at_max_spend_month
FROM campaign
GROUP BY channel
ORDER BY spend_vs_cac_corr DESC;
