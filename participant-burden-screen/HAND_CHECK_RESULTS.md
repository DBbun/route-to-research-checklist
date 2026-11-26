# Hand-check of the keyword screen (2026-11-12)

Source: ClinicalTrials.gov API v2, public records, pulled 2026-11-12. 831 studies on ME/CFS, Long COVID or Lyme, started 2020 or later (or open with no start date). Every check below was done by reading the full public record (summary, detailed description, arms, outcomes, eligibility). Coded files: `out/hand_check_sample_CODED.csv` (sample 1) and `out/hand_check_sample_2_CODED.csv` (sample 2).

## Method
1. **Sample 1** (30 random studies, seed 20261112) was checked against the first keyword patterns (v1). The patterns had no false positives but missed a lot. I widened them (v2) using what sample 1 missed.
2. Because sample 1 was used to tune the patterns, it cannot also test them. **Sample 2** (30 new random studies, seed 20261113, none from sample 1) was the test of the v2 patterns. The patterns were **not changed** after sample 2.
3. Definitions used when reading each record:
   - **Remote or home element:** the record describes at least one step done without travel (online survey, telephone or video visit, app or wearable at home, mailed kit, home sessions). One step is enough; it doesn't mean the whole study is remote.
   - **Exertion or orthostatic test:** a test of exercise capacity or standing tolerance used as a study procedure (CPET, 6- or 2-minute walk, sit-to-stand, cycle ergometer, NASA lean or tilt test). Gait-speed tests (10-meter walk) and grip strength don't count. Exercise mentioned only as background doesn't count.
   - **Must attend:** eligibility requires attending in-person visits or sessions, or excludes people who live too far.
   - **Functional exclusion:** eligibility excludes people by physical function ("able to walk", Barthel index cutoff, can't do the exercise test).

## Agreement on sample 2 (v2 patterns, the honest test)
| Flag | Agreed | False positives | Missed | Use in the entry? |
|---|---|---|---|---|
| Remote or home element | 25/30 | 2 | 3 | Yes, as an approximate figure |
| Exertion or orthostatic test | 28/30 | 2 | 0 | Yes |
| Functional exclusion | 30/30 | 0 | 0 | Yes, but only 2 cases in the sample, so the count is small |
| Must attend | 27/30 | 1 | 2 | **No.** Found 1 of 3 true cases. Eligibility rarely uses fixed wording. Quote individual examples only. |
| Flexibility (reschedule, breaks) | 0 matches in 831 | — | — | Don't report as a percentage. Report as "not described in the sampled records" from the hand-check. |

Sample 1 against the v1 patterns, for the record: remote 19/28 (9 missed), exertion 26/28, must attend 25/28, functional exclusion 26/28. Two sample-1 records were dropped as not relevant: one on tick-borne relapsing fever (not Lyme), one using insurance claims only (no participants to visit).

## What the 58 hand-read studies show (both samples, relevant studies only)
| How people take part | Studies | Share |
|---|---|---|
| Every step in person (no remote or home step described) | 31 | 53% |
| Mix of in-person and remote or home steps | 17 | 29% |
| Fully remote, clearly stated ("no in-person visits", "everything online") | 6 | 10% |
| Probably fully remote (app, online program) but not stated | 4 | 7% |

- **Exertion or orthostatic tests:** 15 of 58 (26%). One ME/CFS study gives a maximal exercise test on two days in a row to study post-exertional malaise. That is a real research question, so the point is the **recovery support** people need around it, not that the test is wrong.
- **Functional exclusions:** 4 of 58. Examples: "able to walk independently", "to be able to walk", Barthel index above 80, excludes people whose conditions prevent the exercise test.
- **Attendance and distance:** explicit wording in 8 of 58, e.g. "must be able to attend all study visits located at [one address]", "place of living does not allow... the planned study visits".
- **Good practice found:** fully home-based studies with no in-person visits (an ME/CFS biofeedback study); remote visits allowed to replace two in-person visits (a Long COVID drug trial); a 6-month home activity-monitoring study that **includes people with severe ME/CFS**.

## Full-dataset keyword figures (v2), interventional studies
| Group | Studies | Remote or home element | Exertion or orthostatic test | Exercise as the treatment | Mentions PEM |
|---|---|---|---|---|---|
| ME/CFS | 84 | 43% | 33% | 8 studies | 37% |
| Long COVID | 492 | 37% | 35% | 80 studies | 18% |
| Lyme, patients only | 18 | 44% | 2 studies | 0 | 1 study |
| All | 578 | 37% | 33% | 84 studies | 18% |

- **Lyme:** 61 studies in total; 26 accept healthy volunteers (mostly vaccine and tick-bite studies). The table shows patient studies only. With 18 interventional patient studies, give counts, not percentages.
- **Exercise as the treatment, ME/CFS:** 8 studies tagged ME/CFS include an exercise-based treatment. One names graded exercise therapy outright (NCT05534997, post-COVID fatigue, 2022). Two describe activity that increases step by step (NCT06978582, NCT05967052). One is about lymphoma survivors with chronic fatigue, not ME/CFS. NICE NG206 (rec 1.11.14) says not to offer graded exercise therapy for ME/CFS. **Read each of these records before quoting.**
- These are keyword figures. Use them as "about", next to the hand-check figures, and never as "X% of trials don't offer...".

## Wording for the entry (draft)
"In a keyword screen of 831 registered ME/CFS, Long COVID and Lyme studies, checked by hand on 58 randomly chosen records, about half required every step in person, and about 1 in 10 clearly allowed full participation from home. About a quarter included an exercise or standing test, and a few excluded people who cannot walk. None of the hand-read records described flexible rescheduling or rest breaks."

Limits to state: registry records are short and may leave out remote options that the full protocol includes; one reader coded both samples (no second reader); the samples are small (58 studies).
