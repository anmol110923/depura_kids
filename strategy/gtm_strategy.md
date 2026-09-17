# DePURA Kids — Go-to-Market Strategy

**Independent case study; all figures SYNTHETIC.** This document translates the relaunch strategy (`relaunch_strategy.md`) into a concrete channel and resourcing plan. See that document for the underlying evidence and citations — this file focuses on execution mechanics.

---

## 1. GTM structure: two parallel motions

DePURA Kids' relaunch requires two distinct go-to-market motions running in parallel, because the category has two different buying triggers:

1. **HCP-led motion** — the pediatrician's recommendation initiates the purchase (infant prevention, per IAP guidance). This motion is about **trust rebuilding**, not new-customer acquisition in the usual sense.
2. **Consumer-led motion** — parents who already know the brand, or are reached through non-HCP channels (pharmacist, e-pharmacy, family). This motion is closer to a conventional acquisition/retention funnel.

Treating these as one funnel would misallocate spend: an HCP "conversion" (a doctor resuming recommendation) is worth an entirely different amount, and costs an entirely different amount to achieve, than a single parent's first purchase.

## 2. Channel plan by motion

### HCP-led motion

| Channel | Audience | CAC (synthetic) | Role |
|---|---|---|---|
| Field Rep Detailing | All HCP segments, prioritizing pre-recall prescribers | ₹24,874 | Highest-touch, reserved for the highest-value non-user segment |
| HCP Digital Detailing & Webinars | Emerging segment | ₹10,757 | Cheapest HCP channel — scale here before scaling field reps |
| CME / Medical Conferences | Broad HCP awareness | ₹21,747 | Category credibility and awareness, not direct conversion |
| Pharmacist Trade Program | Retail chemists | ₹2,586 | Protects against pharmacist-led substitution when DePURA is in stock |

*CAC figures from `sql/10_cac_analysis.sql` on synthetic campaign data — illustrative of relative ordering, not real spend levels.*

**Sequencing:** digital detailing scales fastest and cheapest; field rep capacity should follow the HCP segmentation, concentrated on pre-recall prescribers in the "High-volume non/under-user" segment (616 HCPs in the sample, 24.6%) rather than spread evenly across the full territory HCP universe.

### Consumer-led motion

| Channel | CAC (synthetic) | Role |
|---|---|---|
| WhatsApp / CRM Refill Reminders | ₹23 | Retention — the highest-priority channel by cost and by modelled revenue contribution |
| E-Pharmacy Sponsored Listings | ₹242 | Cheapest new-parent acquisition channel |
| Search Ads | ₹854 | Captures existing intent (parents already searching) |
| Paid Social (Meta) | ₹1,381 | Broad awareness, particularly for the Low-awareness segment |
| Parenting Communities & Creators | ₹2,261 | Trust-building content, secondary priority |
| YouTube / Video | ₹3,432 | Most expensive tested channel — lowest priority for incremental spend |

**Sequencing:** fund retention first (cheapest, largest modelled driver), then E-Pharmacy and Search (efficient acquisition), then use Paid Social specifically to reach Low-awareness parents rather than as a general-purpose channel.

## 3. Territory rollout sequencing

Following the Defend/Grow/Build/Deprioritize segmentation (`relaunch_strategy.md` §9):

1. **Defend territories first** (12 territories, incl. Delhi North, Bengaluru South, Hyderabad) — protect the existing base; this is where distribution fixes (Phase 1) have the most immediate revenue protection value.
2. **Grow territories second** (6 territories, incl. Kolkata, Chennai) — the highest-ROI incremental investment, since potential is proven but capture is low.
3. **Build territories selectively** — invest only where Phase 1-2 data validates the approach.
4. **Deprioritize territories last**, if at all, within the 12-month window modelled.

## 4. Distribution rollout

Stock availability should be brought toward the network median (80.6%) in Defend and Grow territories within Phase 1 (0-90 days), since this is the fastest-acting lever identified (~21% unit swing across stock bands). Priority territories, ranked by current sales at risk from under-stocking: Pune, Delhi South, Indore, Kanpur-Agra.

## 5. Messaging framework

| Audience | Core message | Avoid |
|---|---|---|
| Pre-recall prescribing pediatricians | Formulation/quality reassurance + easy re-trial support (samples, updated PI) | Overselling "new and improved" claims not in official Sanofi material |
| Health-conscious parents | Adherence/consistency ("one pack, one month") | Discount-led messaging — undermines premium positioning |
| Low-awareness parents | Basic Vitamin D deficiency education, IAP-aligned | Fear-based messaging about the recall itself |
| Price-sensitive parents | Not a near-term priority audience for this brand | Competing on price — undermines the premium tier |

## 6. What this GTM plan deliberately does not do

- **It does not propose a price cut.** DePURA sits in the premium cluster; competing down-market against Ultra D3 or the value tier would abandon the segment where the brand's advantage (doctor trust) actually matters.
- **It does not spend the Upside case's marketing budget uniformly.** The scenario model shows marketing spend scaling sub-linearly (diminishing returns); the model's implied allocation favours HCP, stock, and adherence execution over raw media spend.
- **It does not treat all HCPs as one call list.** The volume-recommendation confounder (`relaunch_strategy.md` §4) means a volume-sorted call list would waste field capacity on HCPs unlikely to convert.
