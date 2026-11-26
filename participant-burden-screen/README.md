# Participant-burden screen of registered studies (ClinicalTrials.gov)

What registered studies ask of participants whose energy is limited: steps done from home, exercise or walking tests, exclusions by physical function, and rest breaks or flexible rescheduling. Public data only (ClinicalTrials.gov API v2). Part of the "Energy-Aware Research Visits" entry; independent work by DBbun LLC, not funded or endorsed by NIH.

## Files
- `participant_burden_screen.py`: keyword screen of ME/CFS, Long COVID and Lyme studies (started 2020 or later, or open with no start date). Outputs in `out/`: `studies_flags.csv` (one row per study, each flag with the phrase that triggered it), `summary.csv`, `boston_area_sites_open.csv`, the two hand-check samples and their coded versions, `run_info.txt`.
- `HAND_CHECK_RESULTS.md`: how the keyword patterns were tuned on one random sample of 30 and tested on a second, fresh sample of 30, with the agreement for each flag and what 58 hand-read records show.
- `other_conditions_screen.py`: the same patterns, unchanged, for COPD, heart failure, dialysis, and cancer and multiple sclerosis studies that mention fatigue (9,950 studies). Outputs in `out_other/`.
- `dump_sample_other.py`: fetches the full public record of each study in the second-round sample for hand-reading.
- `OTHER_CONDITIONS_RESULTS.md`: results, and a blind hand-check of 30 random records with agreement per flag.

## Run
Python 3, standard library only:

```
python -I participant_burden_screen.py
python -I other_conditions_screen.py
python -I dump_sample_other.py
```

Results change as ClinicalTrials.gov is updated; each run writes its pull date to `run_info.txt`.

## Limits
- A keyword screen of registry records, not a reading of full protocols. Records can leave out options that a study offers.
- Use the hand-checked figures, not raw keyword percentages, where they differ (see the two results files). The "must attend" and functional-exclusion flags are not reliable enough to report as percentages.

## AI disclosure
Code, patterns and write-ups drafted with Claude (claude-opus-5-5, Anthropic) and reviewed by the author. The second hand-check was coded by a separate Claude (claude-opus-5-5) agent reading the full records without seeing the keyword flags.

License: CC BY 4.0 (text and data); code may also be reused under the same terms.
