# Trip Experience Survey 2026: summary counts

**Version 1.0 (November 24, 2026): built from the export of November 17, 2026 (31 respondents). A later version may add responses received after that date; earlier versions stay available under the same DOI.**

Summary counts from an anonymous online survey about getting to medical appointments and research visits, with a focus on people with disabilities. The survey was run as part of the Route to Research pilot (Boston, Cambridge and Somerville, Massachusetts, October–December 2026).

This is real survey data in summary form. It is **not synthetic**.

## Credit

Please cite:

> Kartoun U. *Trip Experience Survey 2026: summary counts* (version 1.0). DBbun LLC; 2026. https://github.com/DBbun/route-to-research-checklist. DOI: https://doi.org/10.5281/zenodo.24514955 (all versions; version 1.0: https://doi.org/10.5281/zenodo.24514956)

License: [CC BY 4.0](../LICENSE). You may reuse, share and adapt the data, including for commercial use, as long as you credit the source as above and say if you changed anything. A machine-readable citation is in [`CITATION.cff`](../CITATION.cff).

## What's in this folder

| File | Contents |
|---|---|
| `survey_summary_counts.csv` | One row per answer option: question, answer, count, number of people who answered, notes |
| `CODEBOOK.md` | Every question, how it was asked, and how the counts were made |
| `README.md` | This file |

The full questions, ready to copy into any form tool, are in [`survey/`](../survey/).

## Why only summary counts

Respondents were told: "Your answers are anonymous and will only be reported in summary form." To keep that promise:

- No individual responses, dates or times of response, or written answers are published.
- Each question is counted on its own. There are no tables that combine two questions, because combinations can point to one person in a small group.
- In the "About you" questions (who you are, mobility aids, disability types, other factors, where you live, how you heard), any count from 1 to 4 is shown as `<5`.
- Answers about experiences (reasons a trip was too hard, ratings of checklist items, likelihood of taking part) are shown in full.
- Short quotes that respondents allowed are used only in the challenge entry, as they agreed, and are not part of this dataset.

## Who answered (and who didn't)

- 31 people, October 27 to November 17, 2026. Most found the survey through disability-related Facebook groups and neighborhood email lists; most live in Massachusetts.
- 18 of 23 described themselves as having a disability. Others were caregivers, family members, or people working in healthcare or research.
- **This is a small, self-selected group, not a random sample.** The counts show what this group reported. They are not estimates for all people with disabilities. Use them to generate questions and design larger studies, not as a measure of how common something is.
- People who are too sick or tired to fill in an online form, people without internet access, and people who need another language or format are likely under-represented. One screen-reader user reported that the form showed a blank screen inside the Facebook app.
- A separate easy-read version of the survey had 1 response at the time of this release. It is not included, because a single response can't be summarized without identifying it.

## Changes during the survey

The form was updated on 2026-11-01. The first 4 respondents saw an earlier version:
- They rated an earlier list of 9 checklist items. Those ratings are not included; item ratings come from respondents 5 onward.
- "How did you hear about this form?" was added in the update, so they weren't asked it.
- Denominators in the CSV show exactly how many people answered each question.

## How it was made

The survey ran on Google Forms. The response export stays on the author's computer. A Python script (`build_open_data.py`) reads the export locally and writes only the counts in this folder. The survey collected no names or contact details. The AI assistant (see below) ran the script on the author's computer and saw parts of the anonymous export while checking the counts; the export itself is not published anywhere.

## About this project

Independent project by Uri Kartoun, PhD, DBbun LLC (Cambridge, Massachusetts), entered in the NIH *Advancing the Inclusion of People with Disabilities in Clinical Research Challenge*. Not funded or endorsed by NIH or any other federal source.

**AI disclosure:** the script, this README and the codebook were drafted with AI assistance from Claude (Anthropic), model `claude-opus-5-5`. The author reviewed the counts against the export.

**Contact:** uri.kartoun@dbbun.com · https://dbbun.com · ORCID [0000-0003-0988-8037](https://orcid.org/0000-0003-0988-8037)
