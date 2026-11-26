"""Same participation-burden keyword screen as participant_burden_screen.py, for other energy-limiting conditions.
Patterns are read unchanged from participant_burden_screen.py (v2, tested on ME/CFS, Long COVID and Lyme records only).
Writes to ./out_other/ and never touches ./out/ (the hand-checked ME/CFS, Long COVID and Lyme results).
Same rules: start 2020-01-01 or later, or open with no start date. Public ClinicalTrials.gov API v2.
Run: python -I other_conditions_screen.py
"""
import ast, csv, datetime, json, random, re, sys, time, urllib.parse, urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
OUT = HERE / "out_other"; OUT.mkdir(exist_ok=True)
API = "https://clinicaltrials.gov/api/v2/studies"
START_FROM = "2020-01-01"
OPEN = ("RECRUITING", "NOT_YET_RECRUITING", "ENROLLING_BY_INVITATION", "ACTIVE_NOT_RECRUITING")

src = (HERE / "participant_burden_screen.py").read_text(encoding="utf-8")
PATTERNS = next(ast.literal_eval(n.value) for n in ast.walk(ast.parse(src))
                if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "PATTERNS")
RX = {k: re.compile(v, re.I) for k, v in PATTERNS.items()}

# (condition query, optional extra term). Fatigue term for MS and cancer, so the set is about energy, not the whole field.
GROUPS = {
    "COPD": ('"chronic obstructive pulmonary disease" OR COPD', None),
    "Heart failure": ('"heart failure"', None),
    "Cancer-related fatigue": ('cancer OR neoplasm OR tumor', 'fatigue'),
    "MS fatigue": ('"multiple sclerosis"', 'fatigue'),
    "Dialysis": ('"end stage renal disease" OR "end-stage kidney disease" OR "kidney failure" OR hemodialysis', 'dialysis'),
}


def fetch(cond, term):
    out, token = [], None
    while True:
        p = {"query.cond": cond, "pageSize": 200, "format": "json"}
        if term: p["query.term"] = term
        if token: p["pageToken"] = token
        req = urllib.request.Request(API + "?" + urllib.parse.urlencode(p), headers={"User-Agent": "trial-access-audit/1.0"})
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=90) as r:
                    d = json.load(r); break
            except Exception:
                time.sleep(3)
        out += d.get("studies", [])
        token = d.get("nextPageToken")
        if not token: return out
        time.sleep(0.3)


def text_of(ps, *paths):
    parts = []
    for path in paths:
        node = ps
        for key in path.split("."):
            node = node.get(key, {}) if isinstance(node, dict) else {}
        if isinstance(node, str): parts.append(node)
        elif isinstance(node, list): parts.append(json.dumps(node, ensure_ascii=False))
    return "\n".join(parts)


def hit(rx, text):
    m = rx.search(text or "")
    if not m: return 0, ""
    return 1, " ".join(text[max(0, m.start() - 60): m.end() + 60].split())


rows, seen = [], {}
for group, (cond, term) in GROUPS.items():
    got = fetch(cond, term)
    kept = 0
    for s in got:
        ps = s["protocolSection"]
        nct = ps["identificationModule"]["nctId"]
        status = ps["statusModule"].get("overallStatus", "")
        start = ps["statusModule"].get("startDateStruct", {}).get("date", "")
        if start and start[:10] < START_FROM[: len(start[:10])]: continue
        if not start and status not in OPEN: continue
        if str(ps.get("eligibilityModule", {}).get("healthyVolunteers", "")) == "True" and group != "Dialysis":
            pass  # kept, as in the main screen; reported separately below
        if nct in seen:
            seen[nct]["group"] += f"; {group}"; continue
        all_text = text_of(ps, "descriptionModule.briefSummary", "descriptionModule.detailedDescription",
                           "armsInterventionsModule.armGroups", "armsInterventionsModule.interventions",
                           "outcomesModule.primaryOutcomes", "outcomesModule.secondaryOutcomes",
                           "designModule.designInfo", "identificationModule.officialTitle")
        elig = ps.get("eligibilityModule", {}).get("eligibilityCriteria", "")
        row = {"nct_id": nct, "group": group, "title": ps["identificationModule"].get("briefTitle", ""),
               "study_type": ps.get("designModule", {}).get("studyType", ""), "status": status, "start_date": start}
        for k in ("remote", "exertion_test", "flexibility", "mentions_pem"):
            row[k], row[k + "_evidence"] = hit(RX[k], all_text + "\n" + elig)
        row["exercise_intervention"], row["exercise_intervention_evidence"] = hit(
            RX["exercise_intervention"], text_of(ps, "armsInterventionsModule.armGroups", "armsInterventionsModule.interventions"))
        for k in ("must_attend", "excludes_bedbound"):
            row[k], row[k + "_evidence"] = hit(RX[k], elig)
        row["url"] = f"https://clinicaltrials.gov/study/{nct}"
        seen[nct] = row; rows.append(row); kept += 1
    print(f"{group}: {len(got)} records from the API, {kept} new rows kept")

with (OUT / "other_studies_flags.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

FLAGS = ("remote", "exertion_test", "exercise_intervention", "excludes_bedbound", "flexibility")
summary = []
for group in list(GROUPS) + ["All"]:
    for stype in ("INTERVENTIONAL", "OBSERVATIONAL", "All"):
        sub = [r for r in rows if (group == "All" or group in r["group"]) and (stype == "All" or r["study_type"] == stype)]
        if not sub: continue
        rec = {"group": group, "study_type": stype, "n": len(sub)}
        for k in FLAGS:
            rec[k + "_pct"] = round(100 * sum(r[k] for r in sub) / len(sub), 1)
        summary.append(rec)
with (OUT / "other_summary.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(summary[0].keys())); w.writeheader(); w.writerows(summary)
for rec in summary:
    if rec["study_type"] == "All":
        print(rec)

random.seed(20261126)
samp = random.sample(rows, 30)
with (OUT / "hand_check_sample_other.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["nct_id", "url", "group", "remote", "exertion_test", "excludes_bedbound"])
    for r in samp: w.writerow([r["nct_id"], r["url"], r["group"], r["remote"], r["exertion_test"], r["excludes_bedbound"]])
(OUT / "run_info.txt").write_text(f"Pulled {datetime.datetime.now():%Y-%m-%d %H:%M} from {API}\nRows kept: {len(rows)}\n"
                                  f"Queries: {json.dumps(GROUPS, indent=1)}\nPatterns: v2, unchanged from participant_burden_screen.py\n", encoding="utf-8")
