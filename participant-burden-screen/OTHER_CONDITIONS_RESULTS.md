# Same screen, other energy-limiting conditions (run 2026-11-26)

Script `other_conditions_screen.py` (outputs in `out_other/`). Same v2 keyword patterns and date rule as the ME/CFS, Long COVID and Lyme screen (start 2020 or later, or open with no start date). ClinicalTrials.gov API v2, public records. Keyword screen, then a **blind hand-check of 30 random records** (2026-11-26; see the section below).

Queries: COPD; heart failure; cancer studies whose record mentions fatigue; multiple sclerosis studies that mention fatigue; kidney failure or hemodialysis studies that mention dialysis. A study matching two groups is counted once overall.

| Group | Studies | Mentions any remote or home step | Exercise or walking test | Exercise as the treatment | Excludes people who can't walk or are bedbound | Mentions rescheduling or breaks |
|---|---|---|---|---|---|---|
| COPD | 1,960 | 22% | 29% | 14% | 1.9% | 0.5% |
| Heart failure | 3,148 | 23% | 24% | 6% | 2.8% | 0.2% |
| Cancer (fatigue mentioned) | 2,793 | 33% | 15% | 15% | 2.2% | 0.3% |
| Multiple sclerosis (fatigue mentioned) | 621 | 39% | 36% | 25% | 6.1% | 1.8% |
| Dialysis | 1,589 | 14% | 6% | 6% | 0.9% | 0.3% |
| **All five (unique studies)** | **9,950** | **25%** | **20%** | **11%** | **2.4%** | **0.4%** |
| For comparison: ME/CFS, Long COVID, Lyme | 831 | 34% | 28% | 11% | 3.2% | 0.0% |

## How to read it
- "Mentions any remote step" means at least one step without travel (one online survey is enough). In the hand-check of the original screen, records with a remote mention were mostly still in person for the main visits; about 1 in 10 was fully remote.
- The same pattern holds across conditions: by keyword, **about 1 in 5 studies uses an exercise or walking test** (most often the 6-minute walk in COPD and heart failure; the hand-check puts it nearer 3 in 10), **about two-thirds have no step done from home** (hand-check; the keyword 3 in 4 overstates this), and **almost none mention rescheduling or rest breaks**.
- The cancer and MS groups are "studies whose record mentions fatigue", not "studies of fatigue"; fatigue may appear only as a side effect or outcome.
- "Mentions rescheduling" was 0 of 831 in the original screen and the hand-check confirmed none; here a few records mention it, mostly as visit windows.

## Hand-check (2026-11-26)
30 random records (seed 20261126), full public records fetched with `dump_sample_other.py` (`out_other/records/`), read in full and coded **blind to the keyword flags** by a separate Claude agent (claude-opus-5-5), with the same definitions as the ME/CFS, Long COVID and Lyme hand-check; one addition stated in advance: an ECOG performance-status cutoff counts as a functional exclusion. Codes: `out_other/hand_check_other_CODED.csv`. 28 of 30 enroll participants (2 use records or claims only).

| Measure | Keyword vs hand (28 relevant) | Hand count (of 28) | Use |
|---|---|---|---|
| Exercise or walking test | 26/28 agree; 0 false positives, 2 missed (chair-stand tests) | **8 (29%)** | Keyword 20% is a floor; use the hand count |
| Any step done from home | 20/28 agree; 2 false positives, 6 missed (daily diaries, activity trackers) | **10 (36%)**; fully remote 3 (11%); **no step from home 18 (64%)** | Keyword overstates "no remote step" (75%); use the hand count |
| Functional exclusion | 19/28 agree; 0 false positives, 9 missed | **11 (39%)** including ECOG cutoffs; **6 (21%)** without ECOG | **Keyword not usable** here (2.4%); cancer trials use ECOG, MS trials a disability-scale cutoff, which the patterns don't catch |
| Rest breaks or flexible rescheduling | text search of all 30 records | **0** | Same as the ME/CFS, Long COVID and Lyme hand-check |

Unsure calls listed by the coder: daily diaries counted as a home step (2 records); chair-stand tests counted as exertion tests (2); NYHA class treated as medical severity, not function; one inpatient chart-review study kept as relevant.

## Line in Entry 2 (field 2.4, 2026-11-26)
"The same screen on 9,950 studies of COPD, heart failure, dialysis, and cancer and MS studies that mention fatigue found the same pattern; of 28 hand-read records, 8 used an exercise or walking test, 18 had no step done from home, and none described rest breaks or rescheduling."