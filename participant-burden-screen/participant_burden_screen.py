"""Participation-burden audit of ME/CFS, Long COVID and Lyme studies on ClinicalTrials.gov (public API v2).

For each study that started in 2020 or later (or has no start date and is still open), it records:
  - remote or home options mentioned anywhere in the record (video, telehealth, home visits, at-home kits, decentralized)
  - exertion tests (exercise tests, CPET, treadmill, walk tests, tilt table)
  - eligibility wording that requires travel or attendance, or excludes people who are bedbound or housebound
  - for Lyme: eligibility that requires positive blood tests or a documented rash
  - flexibility wording (reschedule, visit window, flare)
It saves the phrase that triggered each flag, so every flag can be checked by hand.

This is a KEYWORD SCREEN, not a reading of every protocol. Before publishing any percentage, hand-check a random
sample (see make_check_sample in the outputs) and report the agreement.

Run: python -I participant_burden_screen.py   (writes to ./out/)
"""
import csv
import datetime
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path(__file__).resolve().parent / "out"
OUT.mkdir(exist_ok=True)
API = "https://clinicaltrials.gov/api/v2/studies"
START_FROM = "2020-01-01"

GROUPS = {
    "ME/CFS": '"myalgic encephalomyelitis" OR "chronic fatigue syndrome" OR "ME/CFS"',
    "Long COVID": '"long COVID" OR "post-acute COVID-19 syndrome" OR "post-COVID condition" OR PASC OR "post-COVID-19 condition"',
    "Lyme": '"Lyme disease" OR "post-treatment Lyme disease syndrome" OR "Lyme borreliosis" OR "Lyme neuroborreliosis"',
}

PATTERNS = {
    # v2 (2026-11-12): widened after the first hand-check (30 studies), which found no false positives but many misses.
    "remote": r"\b(remote\w*|virtual\w*|(?<!published )online|web-?based|internet-?based|tele-?health|tele-?medicine|tele-?rehabilitation|video (visit|call|conferenc)\w*|zoom|smart-?phone|mobile app|phone app|by (tele)?phone|phone calls?|home[- ]based|home visit\w*|in[- ]home|at[- ]home (test|testing|sample|collection|kit|assessment|visit|measurement)\w*|no in[- ]person visits?|decentrali[sz]ed|mailed|by mail|webinar)\b",
    "exertion_test": r"\b(cardiopulmonary exercise test\w*|CPET|exercise (test|challenge|tolerance test)\w*|treadmill|cycle ergometer\w*|bicycle ergometer\w*|ergometr\w*|(6|six)[- ]?min(ute)?[- ]walk\w*|6MWT|walk test|tilt[- ]table|NASA (10[- ]minute )?lean test|lean test|active stand(ing)? test|orthostatic (challenge|test)|sit[- ]to[- ]stand|step test|maximal exercise|graded exercise)\b",
    "must_attend": r"\b((able|willing) (and (able|willing) )?to (attend|travel|come|return|visit|comply with (all )?(study )?visits|adhere to)|abilit(y|ies) to (attend|participate in|come to) (all )?(scheduled |the )?(study )?visits?|(live|reside)s? within \d+|within \d+ (miles|km|kilometers) of|comply with (all )?(scheduled |study )?visits|attend all (scheduled |study )?visits|return to the (\w+'?s? )?site)\b",
    "excludes_bedbound": r"\b(bed-?bound|house-?bound|home-?bound|bedridden|non-?ambulatory|wheelchair[- ]bound|unable to walk|must be ambulatory|unable to (attend|travel to) (the )?(study )?(visits?|site|clinic)|barthel|(unable|inability) to (perform|complete|undergo) (the )?(exercise|CPET|walk|tests?)|preventing the (CPET|exercise|test)|able to (walk|perform (the )?(exercise|CPET|walk)))\b",
    "flexibility": r"\b(reschedul\w*|visit window\w*|flexible (scheduling|visit|timing)\w*|split (the |into )?(visit|session)\w*|rest (period|break)s? (between|during)|breaks? (between|during) (assessments|tests|sessions))\b",
    # Exercise as the TREATMENT (searched in arms and interventions only), kept apart from exercise tests used as measures.
    "exercise_intervention": r"\b(graded exercise( therapy)?|(?-i:GET)|exercise (therapy|training|program\w*|rehabilitation|intervention)|aerobic (exercise|training)|endurance training|resistance training|strength training|physical training|physiotherapy|physical therapy|pulmonary rehabilitation|cardiac rehabilitation|exercise-based|telerehabilitation)\b",
    "mentions_pem": r"\b(post-?exertional (malaise|symptom exacerbation)|PEM|PESE)\b",
    "lyme_serology_or_rash": r"\b(seropositiv\w*|positive (ELISA|EIA|western blot|immunoblot|two-tier|serolog\w*|IgG|IgM|antibod\w*)|two-tier\w*|erythema migrans|EM rash|physician-documented (EM|erythema))\b",
}
RX = {k: re.compile(v, re.I) for k, v in PATTERNS.items()}


def fetch(query):
    studies, token = [], None
    while True:
        params = {"query.cond": query, "pageSize": 200, "format": "json"}
        if token:
            params["pageToken"] = token
        url = API + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"User-Agent": "trial-access-audit/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.load(r)
        studies += d.get("studies", [])
        token = d.get("nextPageToken")
        if not token:
            return studies
        time.sleep(0.3)


def text_of(ps, *paths):
    parts = []
    for path in paths:
        node = ps
        for key in path.split("."):
            node = node.get(key, {}) if isinstance(node, dict) else {}
        if isinstance(node, str):
            parts.append(node)
        elif isinstance(node, list):
            parts.append(json.dumps(node, ensure_ascii=False))
    return "\n".join(parts)


def hit(rx, text):
    m = rx.search(text or "")
    if not m:
        return 0, ""
    a, b = max(0, m.start() - 60), min(len(text), m.end() + 60)
    return 1, " ".join(text[a:b].split())


rows, seen = [], {}
for group, q in GROUPS.items():
    got = fetch(q)
    print(f"{group}: {len(got)} records from the API")
    for s in got:
        ps = s["protocolSection"]
        nct = ps["identificationModule"]["nctId"]
        status = ps["statusModule"].get("overallStatus", "")
        start = ps["statusModule"].get("startDateStruct", {}).get("date", "")
        if start and start[:10] < START_FROM[: len(start[:10])]:
            continue
        if not start and status not in ("RECRUITING", "NOT_YET_RECRUITING", "ENROLLING_BY_INVITATION", "ACTIVE_NOT_RECRUITING"):
            continue
        if nct in seen:  # a study can match two groups; keep one row, list both groups
            seen[nct]["group"] += f"; {group}"
            continue
        all_text = text_of(ps, "descriptionModule.briefSummary", "descriptionModule.detailedDescription",
                           "armsInterventionsModule.armGroups", "armsInterventionsModule.interventions",
                           "outcomesModule.primaryOutcomes", "outcomesModule.secondaryOutcomes",
                           "designModule.designInfo", "identificationModule.officialTitle")
        elig = ps.get("eligibilityModule", {}).get("eligibilityCriteria", "")
        locs = ps.get("contactsLocationsModule", {}).get("locations", [])
        row = {
            "nct_id": nct,
            "group": group,
            "title": ps["identificationModule"].get("briefTitle", ""),
            "study_type": ps.get("designModule", {}).get("studyType", ""),
            "phases": ";".join(ps.get("designModule", {}).get("phases", [])),
            "status": status,
            "start_date": start,
            "healthy_volunteers": ps.get("eligibilityModule", {}).get("healthyVolunteers", ""),
            "enrollment": ps.get("designModule", {}).get("enrollmentInfo", {}).get("count", ""),
            "lead_sponsor": ps.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}).get("name", ""),
            "n_sites": len(locs),
            "countries": ";".join(sorted({l.get("country", "") for l in locs if l.get("country")})),
            "boston_area_sites": ";".join(sorted({f"{l.get('facility','')} ({l.get('city','')})" for l in locs
                                                   if l.get("state") == "Massachusetts" and l.get("city") in
                                                   ("Boston", "Cambridge", "Somerville", "Brookline", "Charlestown", "Chestnut Hill", "Newton", "Waltham")})),
        }
        for k in ("remote", "exertion_test", "flexibility", "mentions_pem"):
            row[k], row[k + "_evidence"] = hit(RX[k], all_text + "\n" + elig)
        arms_text = text_of(ps, "armsInterventionsModule.armGroups", "armsInterventionsModule.interventions")
        row["exercise_intervention"], row["exercise_intervention_evidence"] = hit(RX["exercise_intervention"], arms_text)
        for k in ("must_attend", "excludes_bedbound", "lyme_serology_or_rash"):
            row[k], row[k + "_evidence"] = hit(RX[k], elig)
        if "Lyme" not in group:
            row["lyme_serology_or_rash"], row["lyme_serology_or_rash_evidence"] = "", ""
        row["url"] = f"https://clinicaltrials.gov/study/{nct}"
        seen[nct] = row
        rows.append(row)

cols = list(rows[0].keys())
with (OUT / "studies_flags.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)

# Summary: counts and percentages by group and study type
summary = []
def in_group(r, group):
    if group == "Lyme (patients only)":
        return "Lyme" in r["group"] and str(r["healthy_volunteers"]) != "True"
    return group == "All" or group in r["group"]


for group in list(GROUPS) + ["Lyme (patients only)", "All"]:
    for stype in ("INTERVENTIONAL", "OBSERVATIONAL", "All"):
        sub = [r for r in rows if in_group(r, group) and (stype == "All" or r["study_type"] == stype)]
        if not sub:
            continue
        rec = {"group": group, "study_type": stype, "n_studies": len(sub)}
        for k in ("remote", "exertion_test", "must_attend", "excludes_bedbound", "flexibility", "mentions_pem", "exercise_intervention", "lyme_serology_or_rash"):
            vals = [r[k] for r in sub if r[k] != ""]
            rec[k + "_n"] = sum(vals) if vals else ""
            rec[k + "_pct"] = round(100 * sum(vals) / len(vals), 1) if vals else ""
        rec["no_remote_mention_n"] = sum(1 for r in sub if r["remote"] == 0)
        summary.append(rec)
with (OUT / "summary.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
    w.writeheader()
    w.writerows(summary)

# Boston-area sites (for the energy-cost walks): open studies only
open_status = {"RECRUITING", "NOT_YET_RECRUITING", "ENROLLING_BY_INVITATION", "ACTIVE_NOT_RECRUITING"}
sites = {}
for r in rows:
    if r["boston_area_sites"] and r["status"] in open_status:
        for site in r["boston_area_sites"].split(";"):
            sites.setdefault(site, []).append(f"{r['nct_id']} ({r['group']}, {r['status']})")
with (OUT / "boston_area_sites_open.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["site", "n_open_studies", "studies"])
    for site, st in sorted(sites.items(), key=lambda x: -len(x[1])):
        w.writerow([site, len(st), " | ".join(st)])

# Random sample for hand-checking the keyword flags
import random
# Sample 1 (seed 20261112) was used to tune the v2 patterns, so it is kept as is.
# Sample 2 (seed 20261113, excluding sample 1) is the fresh validation sample for the v2 patterns.
first = set()
p1 = OUT / "hand_check_sample.csv"
if p1.exists():
    first = {r["nct_id"] for r in csv.DictReader(p1.open(encoding="utf-8"))}
random.seed(20261113)
sample = random.sample([r for r in rows if r["nct_id"] not in first], 30)
with (OUT / "hand_check_sample_2.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["nct_id", "url", "group", "remote_flag", "remote_correct?", "exertion_flag", "exertion_correct?",
                "must_attend_flag", "must_attend_correct?", "excludes_bedbound_flag", "excludes_bedbound_correct?"])
    for r in sample:
        w.writerow([r["nct_id"], r["url"], r["group"], r["remote"], "", r["exertion_test"], "",
                    r["must_attend"], "", r["excludes_bedbound"], ""])

(OUT / "run_info.txt").write_text(
    f"Pulled {datetime.datetime.now():%Y-%m-%d %H:%M} from {API}\nStudies kept: {len(rows)} (start {START_FROM} or later, "
    f"or open with no start date)\nQueries: {json.dumps(GROUPS, indent=1)}\n", encoding="utf-8")
print(f"kept {len(rows)} studies; outputs in {OUT}")
