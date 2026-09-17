# Market Research — Pediatric Vitamin D in India & DePURA Kids

**Independent case study based on publicly available information, with general industry perspective from a Sanofi professional.**
Not a Sanofi project or Sanofi-approved strategy. Source IDs in [brackets] refer to `sources.md`.

### Evidence labels used throughout

| Label | Meaning |
|---|---|
| **FACT** | Stated in a Tier A/B public source |
| **DIRECTIONAL** | Public evidence supports the direction, not the magnitude |
| **ASSUMPTION** | Analyst assumption for modelling; changeable in `config/` |
| **HYPOTHESIS** | A claim to be tested against (synthetic) data — not a finding |

---

## 1. Business question and why it matters

> *How should DePURA Kids strengthen its post-relaunch growth in India's pediatric Vitamin D category?*

The product was absent from shelves for roughly 17–18 months (recall letter March 2024 [S3]; back on shelves by September 2025 [S5]). In a category where the purchase is usually triggered by a doctor's recommendation, an absence that long means prescribers and parents had to form new habits with competing brands. The relaunch problem is therefore not "launch a product" but **win back habits that were broken**, while rebuilding trust after a quality-related recall.

---

## 2. DePURA Kids — what is publicly known

### 2.1 Product facts

| Attribute | What public sources say | Status |
|---|---|---|
| Owner / marketer | Sanofi Consumer Healthcare India Ltd (SCHIL), the demerged consumer healthcare entity; DePURA was named among its top brands [S1] | **FACT** |
| Active | Cholecalciferol (Vitamin D3) [S6][S7] | **FACT** |
| Strength | 400 IU per 0.5 ml oral solution (drops) [S6 title][S7] | **FACT** — confirm on printed leaflet |
| Packs | 15 ml (MRP ₹190 snapshot) and a 10 ml pack listed [S7][S8] | **FACT** (price is a snapshot) |
| Doses per 15 ml pack at 0.5 ml/day | 30 → one month for an infant | Derived arithmetic |
| Infant dose | 400 IU (0.5 ml) daily for 0–1 year, aligned to IAP [S9][S10] | **FACT** (IAP); label to be confirmed |
| Dose for 1–18 years | Retailer pages conflict: 0.75 ml vs 1 ml for 600 IU [S9] | **CONFLICT** — use only the official PI |
| "Nano" formulation & absorption claims | Appear in retailer copy [S26]; not yet seen in an official Sanofi document | **UNVERIFIED** — do not cite |

**Interview note:** the dosing conflict is a small but real example of why a commercial analytics team validates secondary data before building on it.

### 2.2 Positioning (historical and current)

- **FACT:** At the 2023 demerger, Sanofi described DePURA as a top consumer healthcare brand and a leader in its category [S1]. No brand-level share or sales figure is public.
- **FACT:** SCHIL's 2025 annual report says that DePURA and sister brands received focused consumer and healthcare-practitioner marketing for the first time in over a decade [S2].
- **Implication:** before the recall, the brand's strength likely rested on long-standing doctor familiarity rather than active promotion. After relaunch, that familiarity has to be rebuilt deliberately, which makes HCP engagement the central lever. (**HYPOTHESIS**, tested in Stage 4.)

### 2.3 Recall timeline

| Date | Event | Source |
|---|---|---|
| 26 Mar 2024 | Letter initiating voluntary precautionary recall of DePURA Kids | [S3] |
| 26 Jun 2024 | Letter for Depura Sugar Free recall | [S3] |
| Jul 2024 | Allegra and Combiflam Suspension recalls, described as a continuation of the DePURA recalls; reason given as microbiological contamination under investigation at the manufacturing site; same facility | [S3] |
| By Sep 2025 | DePURA Kids back on shelves | [S5] |
| Q1 CY2026 | Company revenue +32.8% YoY; first quarter with all three relaunched products fully in play | [S5] |

Company results are **company-level**. They do not show how DePURA Kids specifically is recovering; that is what the synthetic analysis simulates.

### 2.4 What is not public

Brand revenue, units, market share, prescriber counts, rep coverage, marketing spend, and distribution coverage are all unavailable (see `sources.md`). Every number of that kind in this project is **synthetic**.

---

## 3. Clinical and epidemiological context

### 3.1 Who should be supplemented — the IAP guideline

The Indian Academy of Pediatrics 2021 revision [S10]:

- recommends **400 IU/day supplementation during infancy**;
- says older children and adolescents should meet their requirement (400–600 IU/day) from **diet and sunlight**, not routine supplements;
- recommends treating deficiency/rickets with **daily cholecalciferol at higher doses** (2,000 IU below 1 year; 3,000 IU in older children) for 12 weeks;
- uses cut-offs of <12 ng/mL (deficiency), 12–20 (insufficiency), >20 (sufficiency).

**Strategic implication (the most important finding in this file):**
A 400 IU/0.5 ml drop is primarily an **infant prevention product**. Its natural decision point is a doctor visit in the first year of life. "Kids" as a broad target is misleading: for children over 1, guidelines favour diet and sunlight for prevention, and treatment uses higher-strength products where DePURA Kids is less natural. The core segment is **parents of infants aged 0–12 months, reached through the doctors who see them**.

### 3.2 Deficiency burden

- **FACT:** CNNS 2016–18 secondary analysis: VDD prevalence of 13.7% (1–4 y), 18.2% (5–9 y), 23.9% (10–19 y) [S11].
- **FACT:** Significant correlates include age, urban residence and winter [S11]; North Indian children have substantially higher odds of deficiency [S12]; among adolescents, Punjab, Haryana and Uttarakhand stand out [S25].
- **DIRECTIONAL use in this project:** synthetic territory potential is modestly higher in North India and demand is modestly higher in winter months. Magnitudes are **ASSUMPTIONS**.

---

## 4. Demand base — top-down sizing logic

### 4.1 Public anchors

| Anchor | Value | Source |
|---|---|---|
| Registered births, 2024 | 2,54,73,389 | [S13] |
| Institutional births | 89% (NFHS-5) | [S23] |
| Full immunisation, 12–23 months | 76.8% (NFHS-5) | [S22] |
| Children receiving most vaccinations in public facilities | 95.6% (round to be verified) | [S24] |

### 4.2 Why the public-facility figure matters

If almost all vaccinations happen in public facilities, the private pediatrician visit is **not** a universal touchpoint, even though most births are institutional. The addressable market for a premium, privately recommended drop is therefore a **subset** of the birth cohort. This is the single biggest uncertainty in sizing and is handled as a range.

### 4.3 Illustrative funnel (ASSUMPTIONS — not a market estimate)

| Step | Low | High | Basis |
|---|---|---|---|
| Annual infant cohort | 2.55 cr | 2.55 cr | [S13] |
| × infants with regular private pediatric access | 35% | 50% | ASSUMPTION |
| × supplemented with a vitamin D drop | 45% | 65% | ASSUMPTION |
| = supplemented infants | ~40 lakh | ~83 lakh | derived |
| × packs per infant-year (of a possible 12) | 6 | 6 | ASSUMPTION (adherence gap) |
| × blended category MRP per pack | ₹110 | ₹110 | ASSUMPTION |
| **= infant D3 drops category at MRP** | **~₹265 cr** | **~₹547 cr** | illustrative |

This excludes older-child treatment demand and higher-strength products. It is used only to set the **scale** of the synthetic data and scenario model, and to show the method. Validating it would require pharmacy audit data (IQVIA/Pharmarack) or a primary survey.

---

## 5. Behaviour: HCPs, pharmacists, parents

These are **HYPOTHESES** grounded in category logic and general industry perspective. They are not public facts, and are tested against synthetic data in later stages.

| # | Hypothesis | Why it is plausible | Tested in |
|---|---|---|---|
| H1 | The doctor's recommendation is the main purchase trigger for infant D3 drops | IAP guidance is directed at pediatricians; infants cannot self-select | Q3, Q4, consumer `recommendation_source` |
| H2 | Pre-recall prescribers are the fastest win-back pool; their habit was interrupted, not rejected | Long brand familiarity [S1][S2] | HCP `pre_recall_prescriber` |
| H3 | High patient volume does not automatically mean advocacy | Volume reflects practice size, not brand preference | Q4, within-specialty analysis |
| H4 | Stock-outs after relaunch cause silent substitution at the pharmacy | Fragmented chemist retail, >90% unorganised [S14]; many same-strength alternatives exist | Q7 |
| H5 | Parents who know about the recall trust the brand less, and a doctor's reassurance offsets it | Recall was widely reported [S3] | Consumer `aware_of_recall` × `brand_trust` |
| H6 | Adherence (packs per infant-year) is a larger value lever than new-parent acquisition | 12 possible packs per year; assumed actual ~6 | Scenario model |

---

## 6. Market trends, growth drivers and barriers

| Growth drivers | Barriers |
|---|---|
| Clear IAP guidance for infant supplementation [S10] | Most vaccinations in public facilities, limiting private touchpoints [S24] |
| Material deficiency burden, higher in North India and in winter [S11][S12] | Many low-priced same-strength alternatives [S8][S18] |
| Rising institutional births, creating early contact with the health system [S23] | Pharmacist substitution in unorganised retail [S14] |
| Growth of organised and online pharmacy channels [S14] (magnitude dated) | Trust damage from a quality-related recall [S3] |
| Company re-investing in HCP and consumer marketing [S2] | ~17–18 months of lost prescribing habit [S3][S5] |

---

## 7. How the research shapes the analysis

| Research finding | Design decision |
|---|---|
| Infant (0–12 m) is the guideline-backed segment | Consumer data uses IAP-aligned age groups; strategy prioritises the infant pathway |
| Doctor-led demand | HCP dataset carries recommendation drivers; HCP opportunity is weighted 20% in territory scoring |
| Recall broke habits | `pre_recall_prescriber` flag; recall-aware trust modelled |
| Fragmented, price-varied competition | Competitor comparison normalised to cost per 400 IU dose |
| Regional and seasonal deficiency differences | Directional territory and seasonality effects in synthetic data |
| No public brand data | All brand performance data synthetic; scenario ranges, not point forecasts |

## 8. Open items to verify manually

1. Official DePURA Kids leaflet/PI: dosing for ages 1–18, pack sizes, any absorption claims [S6].
2. SCHIL BSE filing wording on the relaunch quarter [S4].
3. CRS 2024 primary report from ORGI [S13].
4. Survey round behind the 95.6% public-facility vaccination figure [S24].
5. Uprise-D3 strength from an Alkem source [S21].
