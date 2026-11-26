"""Fetch the full public record of each study in out_other/hand_check_sample_other.csv and write a plain-text dump
(summary, description, design, arms, interventions, outcomes, eligibility) for hand-reading. Output: out_other/records/NCT*.txt
Run: python -I dump_sample_other.py
"""
import csv, json, time, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out_other" / "records"; OUT.mkdir(parents=True, exist_ok=True)
ids = [r["nct_id"] for r in csv.DictReader((HERE / "out_other" / "hand_check_sample_other.csv").open(encoding="utf-8"))]


def g(d, path):
    for k in path.split("."):
        d = d.get(k, {}) if isinstance(d, dict) else {}
    return d


for nct in ids:
    f = OUT / f"{nct}.txt"
    if f.exists():
        continue
    req = urllib.request.Request(f"https://clinicaltrials.gov/api/v2/studies/{nct}?format=json", headers={"User-Agent": "trial-access-audit/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        ps = json.load(r)["protocolSection"]
    parts = [f"{nct} | {g(ps,'identificationModule.briefTitle')}", f"Type: {g(ps,'designModule.studyType')} | Status: {g(ps,'statusModule.overallStatus')}"]
    for lab, path in [("SUMMARY", "descriptionModule.briefSummary"), ("DESCRIPTION", "descriptionModule.detailedDescription")]:
        v = g(ps, path)
        if isinstance(v, str) and v: parts.append(f"## {lab}\n{v}")
    for a in g(ps, "armsInterventionsModule.armGroups") or []:
        parts.append(f"## ARM {a.get('label','')}: {a.get('description','')}")
    for i in g(ps, "armsInterventionsModule.interventions") or []:
        parts.append(f"## INTERVENTION {i.get('type','')} {i.get('name','')}: {i.get('description','')}")
    for kind in ("primaryOutcomes", "secondaryOutcomes"):
        for o in g(ps, f"outcomesModule.{kind}") or []:
            parts.append(f"## {kind[:3].upper()} OUTCOME {o.get('measure','')} | {o.get('description','')} | {o.get('timeFrame','')}")
    parts.append("## ELIGIBILITY\n" + (g(ps, "eligibilityModule.eligibilityCriteria") or ""))
    f.write_text("\n".join(parts), encoding="utf-8")
    time.sleep(0.3)
print(len(ids), "records in", OUT)
