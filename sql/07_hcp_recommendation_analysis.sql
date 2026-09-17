-- =====================================================================
-- 07_hcp_recommendation_analysis.sql
-- ---------------------------------------------------------------------
-- BUSINESS QUESTION
--   What is associated with a higher HCP recommendation rate for DePURA
--   Kids — and, in particular, does raw patient volume matter once we
--   control for specialty? (This is the confounder flagged in
--   data/DATA_DICTIONARY.md §5: high-volume HCPs are disproportionately
--   pediatricians, who also recommend more for reasons unrelated to
--   volume itself.)
--
-- METHOD
--   1. Recommendation rate by specialty and by pre-recall-prescriber
--      status (categorical drivers).
--   2. Recommendation rate by brand-awareness quintile (a continuous
--      driver, bucketed for readability).
--   3. Correlation of recommendation rate with patient volume, computed
--      OVERALL and again WITHIN each specialty via a windowed CORR, to
--      make the confounding visible in the query itself rather than
--      requiring a separate notebook step.
-- =====================================================================

-- 1. Categorical drivers
SELECT
    specialty,
    pre_recall_prescriber,
    COUNT(*)                                        AS hcp_count,
    ROUND(AVG(recommendation_rate), 3)               AS avg_recommendation_rate
FROM hcp
GROUP BY specialty, pre_recall_prescriber
ORDER BY specialty, pre_recall_prescriber DESC;

-- 2. Recommendation rate by brand-awareness level
SELECT
    brand_awareness,
    COUNT(*)                                         AS hcp_count,
    ROUND(AVG(recommendation_rate), 3)                AS avg_recommendation_rate,
    ROUND(AVG(rep_visits_last_quarter), 1)            AS avg_rep_visits
FROM hcp
GROUP BY brand_awareness
ORDER BY brand_awareness;

-- 3a. Overall correlation between patient volume and recommendation rate
--     (this looks meaningful on its own — the confounding only shows up
--     once specialty is controlled for in 3b).
SELECT
    ROUND(CORR(recommendation_rate, monthly_patient_volume), 3) AS overall_corr_rec_vs_volume
FROM hcp
WHERE monthly_patient_volume IS NOT NULL;

-- 3b. Within-specialty correlation: the confounder check.
SELECT
    specialty,
    COUNT(*)                                                     AS hcp_count,
    ROUND(CORR(recommendation_rate, monthly_patient_volume), 3)  AS within_specialty_corr,
    ROUND(AVG(recommendation_rate), 3)                            AS avg_recommendation_rate,
    ROUND(AVG(monthly_patient_volume), 0)                         AS avg_patient_volume
FROM hcp
WHERE monthly_patient_volume IS NOT NULL
GROUP BY specialty
ORDER BY within_specialty_corr DESC;

-- 4. Competitor preference among low-recommendation HCPs — who is winning
--    the HCPs DePURA is losing?
SELECT
    competitor_preference,
    COUNT(*)                                          AS hcp_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_of_low_rec_hcps
FROM hcp
WHERE recommendation_rate < 0.20
GROUP BY competitor_preference
ORDER BY hcp_count DESC;
