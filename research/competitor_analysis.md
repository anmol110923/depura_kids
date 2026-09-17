# Competitor Analysis — Pediatric Vitamin D3 Drops in India

**Independent case study based on publicly available information, with general industry perspective from a Sanofi professional.**
Source IDs refer to `sources.md`. Prices are online pharmacy MRP snapshots (17 Sep 2026) and vary by platform and GST revision.

**Business question:** *Which competitors most directly threaten DePURA Kids' recovery, and on what basis does DePURA compete?*

---

## 1. Why pack price is the wrong comparison

Brands sell different volumes at different concentrations. DePURA Kids delivers 400 IU in 0.5 ml, while Ultra D3 needs 1 ml for 400 IU. A 30 ml bottle is not "twice as much product" as a 15 ml bottle.

The parent actually pays for **daily 400 IU doses**, so everything is normalised to:

```
doses per pack      = pack_ml × IU_per_ml ÷ 400
cost per 400 IU dose = MRP ÷ doses per pack
price index          = cost per dose ÷ DePURA Kids cost per dose × 100
```

## 2. Public-data comparison

| Brand | Marketer | Strength | Pack | MRP (₹) | Doses/pack | ₹ per 400 IU dose | Price index | Evidence |
|---|---|---|---|---|---|---|---|---|
| **DePURA Kids** | Sanofi Consumer Healthcare India | 400 IU/0.5 ml | 15 ml | 190.00 | 30 | **6.33** | **100** | [S6][S7] |
| Arachitol Kids / Nano | Abbott India | 400 IU/0.5 ml (nano droplet) | 15 ml | 199.28 | 30 | 6.64 | 105 | [S15][S16][S8] |
| Kidrich D3 800 IU Nano | Dr. Reddy's | 800 IU/ml | 15 ml | 199.50 | 30 | 6.65 | 105 | [S18] |
| Uprise-D3 Drops | Alkem | 400 IU/0.5 ml *(unverified)* | 15 ml | 110.60 | 30* | 3.69* | 58* | [S8][S21] |
| D3 Must Forte | Mankind | 800 IU/ml | 15 ml | 99.58 | 30 | 3.32 | 52 | [S18][S19] |
| Ultra D3 Drops | Meyer Organics | 400 IU/ml; sugar-free; pineapple flavour | 30 ml | 71.25 | 30 | 2.38 | 38 | [S17][S8] |
| D3 Must Drops | Mankind | *not verified* | 15 ml | 43.84 | — | — | — | [S20] |
| Oh D3 Drops | Indoco | *not verified* | 15 ml | 33.86 | — | — | — | [S8] |

\* Depends on an unverified strength.

Beyond these eight, a single pharmacy listing shows **at least ten other 800 IU/ml drop brands** from different manufacturers, including Zuventus, Eris, Blue Cross and Brinton [S18]. The category is highly fragmented.

## 3. Competitive clusters

| Cluster | Brands | ₹/dose | How they compete |
|---|---|---|---|
| **Premium "nano" / pediatrician-led** | DePURA Kids, Arachitol Kids/Nano, Kidrich D3 Nano | ~6.3–6.7 | Brand trust, formulation claims, doctor familiarity |
| **Mid-price, broad reach** | Uprise-D3, D3 Must Forte | ~3.3–3.7 | Large field forces, T2/T3 reach, price roughly half of premium |
| **Value** | Ultra D3, D3 Must, Oh D3, long tail | ≤2.4 (where verifiable) | Price, taste/sugar-free claims, pharmacist substitution |

## 4. Positioning assessment

These columns are **analyst assessment**, inferred from pack claims and price tier. They are not public statements of the companies' strategies.

| Brand | Positioning (assessment) | Likely target | Key differentiator | HCP orientation | Digital presence |
|---|---|---|---|---|---|
| DePURA Kids | Premium, trusted infant supplement | Urban parents of infants | Legacy doctor familiarity; renewed marketing [S2] | High | Listed across major e-pharmacies [S7][S8] |
| Arachitol Kids / Nano | Premium nano, pediatrician-led | Urban infants and young children | Same strength as DePURA plus explicit nano claim [S15][S16] | High | Listed across major e-pharmacies |
| Kidrich D3 Nano | Premium nano challenger | Urban infants | Nano positioning from a large Indian pharma company | Medium–High | Listed online [S18] |
| Uprise-D3 | Mid-price mainstream | Broad, T2/T3 | Price at ~58% of DePURA with large reach | High | Listed online |
| D3 Must Forte | Mass-market value | T2/T3, price-sensitive | Price at ~52% of DePURA | Medium | Listed online |
| Ultra D3 | Value with taste/sugar-free claims | Price-conscious parents | Lowest verified ₹/dose (38% of DePURA); pineapple, sugar-free [S17] | Medium | Brand site plus listings |

Market share, HCP share of voice, sales-force size and digital spend: **UNAVAILABLE**. None are estimated.

## 5. Threat assessment

| Threat | Why | Severity | Evidence type |
|---|---|---|---|
| **Arachitol Kids / Nano** | Same strength, same dosing volume, near-identical price, overlapping nano claim. It is the closest like-for-like substitute a doctor could switch to during the absence | **Highest** | Public product facts [S15][S16]; switching behaviour is a HYPOTHESIS |
| **Mid-price brands (Uprise-D3, D3 Must Forte)** | Half the cost per dose, with the reach to hold T2/T3 prescribers who switched during the recall | High in T2/T3 | Public prices; reach is assessment |
| **Value long tail** | Pharmacist substitution when DePURA is out of stock; price-sensitive parents | Medium, driven by stock-outs | Public prices [S18]; substitution is a HYPOTHESIS |
| **Kidrich D3 Nano** | Premium nano entrant, same price tier | Medium | Public listing [S18] |

## 6. So what — implications for the strategy

1. **DePURA cannot win on price** in this category: it sits at the top with Arachitol and Kidrich, at roughly 1.7–1.9× the cost per dose of mid-price brands and about 2.7× the lowest verified value option. A price cut would give up premium positioning with no guarantee of volume, so pricing is treated as a scenario lever, not a recommendation.
2. **Formulation is not a clear differentiator** against Arachitol Kids, which has the same strength, dosing volume and a nano claim. The defensible advantages are the **doctor relationship and trust**, which are exactly what the recall damaged.
3. **The premium over mid-price brands has to be justified at the point of prescription.** That points to HCP engagement focused on pre-recall prescribers and high-volume pediatricians (tested in Stage 4).
4. **Being out of stock is a gift to the value tail.** With many same-strength alternatives on the shelf, a stock-out likely becomes a lost sale. Distribution fill-rate is a strategic KPI, not just an operational one (tested in Q7).
5. **Adherence is a trust lever.** One 15 ml pack is one month for an infant, so refill reminders and pediatrician follow-up protect revenue without discounting.

## 7. How this feeds `competitor_data.csv`

- Public fields (brand, marketer, strength, pack, MRP) come from the table above, with `public_data_verification` noting provenance.
- `iu_per_ml` is **left blank** where not verified. Cost per dose is only computed where strength is known.
- `positioning`, `target_segment` and `channel_presence` are **analyst assessments**.
- `differentiation_score` is **synthetic** (1–10) and labelled as such.
