# DePURA Kids — Post-Relaunch Commercial Strategy

**Independent case study based on publicly available information, with general industry perspective from a Sanofi professional.** Not a Sanofi project or Sanofi-approved strategy. All performance figures are **SYNTHETIC** — see `../data/DATA_DICTIONARY.md`. Every recommendation below traces to a specific analysis; sources are cited in brackets.

---

## 1. Business problem

DePURA Kids (Vitamin D3 400 IU/0.5 ml oral solution) was voluntarily recalled from March 2024 over microbiological contamination and was back on shelves by September 2025 [research/sources.md, S3, S5] — roughly 17-18 months off the market. In a category where the purchase is doctor-initiated, that absence broke prescribing habits: pediatricians and parents had to form new relationships with competing brands.

The synthetic analysis shows what that break costs even a year after relaunch: seasonally adjusted revenue has recovered to only **~78% of the pre-recall run-rate** [`sql/01_monthly_sales_trends.sql`], and month-over-month growth has fallen from +32% in the first post-relaunch month to roughly flat by month 12 [`sql/05_growth_rate_analysis.sql`, `notebooks/02_eda.ipynb` §2.2]. This is a **plateau**, not a slow continued climb — closing the remaining gap needs new levers, not more time.

## 2. Target segment

**Primary: infants aged 0-12 months**, reached through their pediatrician. The Indian Academy of Pediatrics' 2021 guideline recommends routine 400 IU/day supplementation specifically during infancy; older children are guided toward diet and sunlight for prevention [research/market_research.md §3.1]. A 400 IU/0.5 ml drop is a poor fit for "kids" broadly — its natural moment is the pediatrician visit in an infant's first year.

**Secondary, by consumer segment** [`notebooks/03_segmentation.ipynb` §B]:
- **Health-conscious** (10.5% of surveyed parents): already the brand's core — 39% DePURA share, 0.83 adherence score. Priority: **retain**, not acquire.
- **Low-awareness** (10.5%): lowest DePURA share (11.8%) of any segment — the clearest growth pool, fixed by education rather than price or product changes.
- **Price-sensitive** (32.0%, the largest segment): below-average DePURA share, consistent with the brand's premium cost-per-dose position. Not a near-term priority — winning this segment on price would undercut the brand.
- **Convenience-driven** (17.9%): above-average DePURA share (28.9%) — e-pharmacy/quick-commerce buyers are not simply chasing the cheapest option.

## 3. Positioning

**Hold the premium position; do not compete on price.** DePURA Kids costs ~₹6.33 per equivalent 400 IU dose, in a "premium nano" cluster with Arachitol Kids/Nano (₹6.64) and Kidrich D3 Nano (₹6.65) [research/competitor_analysis.md]. Mid-price brands (Uprise-D3, D3 Must Forte) cost 52-58% of that; the cheapest verified option (Ultra D3) costs 38%. Arachitol Kids/Nano is an exact strength-and-pack match at a near-identical price — the nearest like-for-like substitute, and the top alternative among HCPs currently recommending DePURA least [`sql/07_hcp_recommendation_analysis.sql`, query 4].

Since formulation is not a clear differentiator against Arachitol, **the defensible advantage is the doctor relationship and trust that the recall damaged.** Positioning should lean on rebuilt HCP engagement and product-quality reassurance, not new claims that a nearly-identical competitor could match.

## 4. HCP strategy

**Priority target: "High-volume non/under-user" pediatricians who prescribed DePURA before the recall.** This segment (616 of 2,500 sampled HCPs, 24.6%) sees enough patients to matter but is not yet recommending the brand [`notebooks/03_segmentation.ipynb` §A]. Within every specialty, pre-recall prescribers recommend at roughly 1.5-2x the rate of non-prescribers [`notebooks/02_eda.ipynb` §2.5] — their habit was interrupted, not rejected, making them the fastest, highest-probability re-engagement target.

**Do not target on raw patient volume alone.** Volume looks correlated with recommendation rate (r ≈ 0.28) only because pediatricians have both higher volume and higher recommendation for reasons unrelated to volume itself; within each specialty that correlation collapses to near zero [`sql/07_hcp_recommendation_analysis.sql`, query 3b; `notebooks/02_eda.ipynb` §2.4]. A call plan built on volume alone would waste effort on high-volume GPs and OB-GYNs who were never going to be strong DePURA advocates.

**Channel mix by HCP segment:**
| Segment | Approach | Rationale |
|---|---|---|
| High-volume advocate (140 HCPs, 5.6%) | Retain — protect from stock-outs, no acquisition spend | Already recommending at 54.7% avg. rate |
| High-volume non/under-user (616, 24.6%) | Field rep detailing, prioritizing pre-recall prescribers | Highest-value conversion target |
| Emerging (300, 12.0%) | HCP digital detailing & webinars | High digital engagement, growing volume — cheapest HCP-audience CAC (₹10,757) [`sql/10_cac_analysis.sql`] |
| Low-opportunity (1,444, 57.8%) | Deprioritize for expensive one-to-one channels | Lowest yield per HCP |

## 5. Consumer strategy

- **Health-conscious segment:** retention infrastructure (refill reminders) — the single cheapest channel measured (₹23 CAC) [`sql/09_conversion_funnel.sql`] and, per the scenario model, the largest driver of Base-case revenue lift [`notebooks/05_scenario_model.ipynb` §4].
- **Low-awareness segment:** education content, delivered through the channels this segment actually uses — more reliant on pharmacists (21.3%) and family/friends (17.8%) than other segments, and less on pediatricians (31.5% vs. 86.0% for Health-conscious) [`notebooks/03_segmentation.ipynb` §B.1].
- **Price-sensitive segment:** not a near-term priority; a value-tier sub-brand or price move is a longer-term strategic question outside this project's scope, not a relaunch-phase action.
- **Recall-aware parents** (19.4% of surveyed parents) report brand trust roughly a full point lower (of 5) than unaware parents [`notebooks/02_eda.ipynb` §2.8]. Pediatrician reassurance at the point of recommendation is likely more effective than mass-market messaging trying to overwrite the recall memory directly.

## 6. Channel strategy

Post-relaunch, E-Pharmacy gained ~2.8 points of revenue share at Retail Chemist's expense [`sql/04_channel_contribution.sql`], and E-Pharmacy sponsored listings are the cheapest new-parent acquisition channel measured (₹242 CAC vs. ₹1,381 for Paid Social, ₹3,432 for YouTube) [`sql/10_cac_analysis.sql`]. Continue shifting incremental digital spend toward E-Pharmacy listings and Search over broad-reach video/social, while maintaining Retail Chemist as the largest volume channel (54% of post-relaunch revenue).

## 7. Digital strategy

- **HCP digital detailing & webinars** for the Emerging HCP segment — cheapest HCP-audience CAC.
- **WhatsApp/CRM refill reminders** for existing customers — cheapest channel overall by two orders of magnitude, and the largest Base-case revenue driver.
- **E-Pharmacy sponsored listings** for new-parent acquisition — cheapest parent-audience channel.
- Marketing spend should scale sub-linearly: the scenario model applies diminishing returns to marketing spend specifically, consistent with the positive spend-vs-CAC correlation found in 9 of 10 channels tested [`sql/10_cac_analysis.sql`]. The Upside scenario leans more on operational execution (HCP, stock, adherence) than on outspending the problem [`notebooks/05_scenario_model.ipynb` §6].

## 8. Distribution strategy

**Treat stock availability as a tracked commercial KPI, not just an operations metric.** Units sold swing ~21% between the lowest (<70%) and highest (90%+) stock-availability bands, in a within-series comparison that controls for territory size [`notebooks/02_eda.ipynb` §2.6]. Several T1/T2 territories with strong underlying demand — Pune, Delhi South, Indore, Kanpur-Agra — sit meaningfully below the network median (80.6%) on stock availability [territory_data.csv]. This is the fastest lever available: unlike rebuilding doctor trust, distribution fill-rate can be fixed within a single quarter.

## 9. Territory strategy

Full quantitative model in `notebooks/04_territory_analysis.ipynb` and Section "Territory Prioritization" of the dashboard. Summary:

| Segment | Territories | Action |
|---|---|---|
| **Defend** | 12 (incl. Delhi North, Bengaluru South, Hyderabad, Pune) | Protect share — high potential, already well-penetrated |
| **Grow** | 6 (incl. **Kolkata, Chennai**) | Prioritize incremental resourcing — high potential, under-penetrated |
| **Build** | 8 | Selective investment — lower potential, low competitive intensity |
| **Deprioritize** | 10 | Minimal near-term resourcing — lower potential, high competitive intensity |

**Kolkata and Chennai deserve specific call-out:** both rank top-3 by category potential but land in the bottom half on penetration — invisible on a plain revenue leaderboard, and confirmed as top-4 opportunities under a weighted, sensitivity-tested scoring model (Chennai: top-4 under all 12 weight perturbations tested; Kolkata: 10 of 12) [`notebooks/04_territory_analysis.ipynb` §4].

## 10. Measurement framework

See `kpi_framework.md` for the full KPI tree, targets, and cadence. Headline metrics: seasonally adjusted revenue recovery %, HCP recommendation rate among pre-recall prescribers, distribution fill-rate, and blended CAC by audience.

---

## Three-phase plan

### Phase 1 — Rebuild (0-90 days)
| | |
|---|---|
| **Objective** | Stop the plateau; fix the fastest-moving levers |
| **Actions** | Fix distribution fill-rate in under-stocked T1/T2 territories (Pune, Delhi South, Indore); launch refill-reminder/retention program for existing customers; begin field-rep re-engagement of pre-recall pediatricians |
| **Target segment** | High-volume non/under-user pediatricians (pre-recall prescribers first); Health-conscious consumers |
| **Channel** | Field rep detailing; WhatsApp/CRM |
| **KPI** | Stock availability ≥ network median in priority territories; retention-channel CAC held under ₹50 |
| **Expected outcome** | Recovery moves from ~78% toward the Conservative-case trajectory (~79% of pre-recall baseline annualised) [`notebooks/05_scenario_model.ipynb`] |

### Phase 2 — Accelerate (90-180 days)
| | |
|---|---|
| **Objective** | Convert the re-engaged HCP base into sustained volume; open the awareness gap |
| **Actions** | Scale HCP digital detailing to the Emerging segment; expand field coverage in Grow territories (Kolkata, Chennai); launch awareness content for Low-awareness consumers via pharmacist and family-network channels |
| **Target segment** | Emerging HCPs; Low-awareness parents |
| **Channel** | HCP digital detailing & webinars; pharmacist trade program; E-Pharmacy sponsored listings |
| **KPI** | HCP recommendation rate among the non-user segment trending up; Kolkata/Chennai penetration narrowing toward the Defend-segment average |
| **Expected outcome** | Base-case trajectory (~90% of pre-recall baseline annualised) |

### Phase 3 — Scale (180-365 days)
| | |
|---|---|
| **Objective** | Reassess against the scenario checkpoints; expand what's working |
| **Actions** | Compare realised recovery against Conservative/Base/Upside; expand the territory playbook from Grow to Build-segment territories where the model validated; re-tune channel mix based on realised (not modelled) CAC |
| **Target segment** | Full funnel, reweighted by what Phase 1-2 data shows is working |
| **Channel** | Reallocate based on realised CAC and conversion data |
| **KPI** | Full KPI framework (see `kpi_framework.md`) |
| **Expected outcome** | Even the Upside case does not fully close the gap to pre-recall levels within a year [`notebooks/05_scenario_model.ipynb`] — Phase 3 sets the stage for continued recovery into year 2, not a declared "done" |

---

**Explicit disclaimer:** this strategy is built from a synthetic dataset and stated assumptions, sense-checked against general industry perspective. It demonstrates a commercial-analytics method — segment, prioritize, model trade-offs, measure — and is not a Sanofi-endorsed plan. See `research/industry_perspective_policy.md` for what the industry input was and was not.
