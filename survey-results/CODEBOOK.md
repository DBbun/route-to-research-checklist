# Codebook: Trip Experience Survey 2026 summary counts

File: `survey_summary_counts.csv` (UTF-8, comma-separated). All questions were optional.

## Columns

| Column | Meaning |
|---|---|
| `question_id` | Question number in this codebook (Q1–Q12) |
| `section` | About you / Checklist ratings / Experience |
| `question` | Question text, shortened. For Q5, the checklist item being rated is part of the text |
| `answer` | Answer option as shown on the form |
| `count` | Number of people who chose this answer. `<5` means 1 to 4 (shown this way only in "About you" questions) |
| `denominator` | Number of people who answered this question (chose at least one option) |
| `note` | Changes to the question during the survey, or how answers were grouped |

For questions where people could choose more than one answer, counts add up to more than the denominator.

## Questions

| ID | Question | Type | Counted in this dataset |
|---|---|---|---|
| Q1 | Which of these describe you? | Choose any | Yes (small-cell rule) |
| Q2 | When you travel to appointments, do you use or bring any of these? (mobility aids, a helper, a service animal, a stroller) | Choose any | Yes (small-cell rule) |
| Q3 | If you have a disability, which types? | Choose any | Yes (small-cell rule) |
| Q4 | Do any of these also make getting to appointments harder for you? (no car, cost, caring for others, distance from transit, age, language) | Choose any | Yes (small-cell rule) |
| Q5 | How important is each checklist item to you? 14 items; Essential / Helpful / Not needed / Not sure | Grid | Yes, from respondents 5 onward |
| Q6 | What is missing from the checklist? | Written | **No** (written answers aren't published) |
| Q7 | Have you ever missed, cancelled or turned down a medical appointment or a research study because getting there was too hard? | Choose one | Yes |
| Q8 | If yes, what made it too hard? | Choose any | Yes. Denominator = people who chose at least one reason |
| Q9 | What one change would help you most when getting to an appointment? | Written | **No** (written answers aren't published) |
| Q10 | If a research site used a route checklist like this and fixed the problems it found, would you be more likely to take part in a study there? | Choose one | Yes |
| Q11 | Which state (or country, if outside the US) do you live in? | Typed | Grouped: Massachusetts / outside Massachusetts / not answered (small-cell rule) |
| Q12 | How did you hear about this form? | Choose one | Yes, from respondents 5 onward (small-cell rule) |
| — | Permission to use short anonymous quotes in the challenge entry | Choose one | **No** (about consent, not about the trip) |

## Notes for reuse

- Answer options are copied from the form. "Other" means the respondent chose "Other"; what they wrote isn't published.
- For Q11, typed answers ("MA", "Ma", "Massachusetts") were merged by hand into "Massachusetts".
- The first 4 respondents used an earlier form version (before 2026-11-01). See the README.
- The full survey, ready to reuse, is in `survey/Trip_Experience_Survey_Template_2026-11-03.md`. If you run it yourself and publish summary counts in the same format, the results can be compared.
