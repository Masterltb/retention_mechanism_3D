"""Engineering harness: check, phase-gate, snapshot and controlled phase closure.

Only the `close-phase` command changes project status. Git commits/tags remain
explicit so a reviewer can inspect staged files before publishing.
"""
import argparse
import csv
import json
import sqlite3
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "BOM/history.sqlite"


def fail(message):
    raise SystemExit("FAIL: " + message)


def database():
    if not DB.is_file():
        fail("Missing BOM/history.sqlite; run py tools/harness.py init")
    cx = sqlite3.connect(DB)
    cx.execute("PRAGMA foreign_keys=ON")
    return cx


def check():
    p = json.loads((ROOT / "requirements/parameters.json").read_text(encoding="utf-8"))
    t, g, b, a = (p[k] for k in ("topology", "gates", "bowl", "analysis_assumptions_not_validated"))
    if not (t["column_count_in_this_model"] == 1 and t["holding_mechanisms_per_column"] == g["count"] == 2):
        fail("Topology must describe one column with two mechanisms")
    if not (g["open_clear_aperture_diameter"] > b["rim_outer_diameter"] > g["closed_clear_aperture_diameter"]):
        fail("Bowl rim must be between closed and open apertures")
    if abs(g["jaw_radial_travel"] - (g["open_clear_aperture_diameter"] - g["closed_clear_aperture_diameter"])/2) > 1e-6:
        fail("Jaw travel is inconsistent with apertures")
    if not all(0 < mu < 1 for mu in a["friction_sensitivity_mu"]):
        fail("Friction sensitivity values must be between zero and one")
    for name in ("overview_concept.svg", "force_path_concept.svg"):
        ET.parse(ROOT / "exports/drawings" / name)
    with (ROOT / "simulation/kinematics/force_friction_sensitivity.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 3 * len(a["friction_sensitivity_mu"]):
        fail("Sensitivity table is missing load/friction cases")
    with database() as cx:
        if cx.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            fail("SQLite integrity_check failed")
        if cx.execute("PRAGMA foreign_key_check").fetchone():
            fail("SQLite foreign_key_check failed")
        dump = ROOT / "BOM/history_dump.sql"
        if not dump.is_file() or dump.read_text(encoding="utf-8") != "\n".join(cx.iterdump()) + "\n":
            fail("SQL backup is stale; run py tools/engineering.py snapshot")
        for story, artifact in cx.execute("SELECT id, artifact FROM story WHERE artifact IS NOT NULL"):
            if not (ROOT / artifact).exists():
                fail("Missing artifact for " + story + ": " + artifact)
    for required in ("cad/assembly/layout.FCStd", "exports/STEP/layout_printed_concept.step",
                     "docs/MECHANICAL_PLAN.md", "design/friction_analysis.md"):
        if not (ROOT / required).is_file():
            fail("Missing deliverable: " + required)
    print("PASS: topology, geometry, CSV, SVG, SQLite, trace links and deliverables")


def phase_gate(phase_id):
    with database() as cx:
        row = cx.execute("SELECT status, acceptance FROM phase WHERE id=?", (phase_id,)).fetchone()
        if row is None:
            fail("Unknown phase " + phase_id)
        earlier = cx.execute("SELECT id FROM phase WHERE id<? AND status!='done' ORDER BY id", (phase_id,)).fetchall()
        if earlier:
            fail("Earlier phases remain open: " + ",".join(x[0] for x in earlier))
        if phase_id == "P0":
            p = json.loads((ROOT / "requirements/parameters.json").read_text(encoding="utf-8"))
            measured = (p["bowl"]["nested_rim_pitch"], p["bowl"]["rim_underside_profile"],
                        p["analysis_assumptions_not_validated"]["measured_static_mu"],
                        p["analysis_assumptions_not_validated"]["measured_kinetic_mu"],
                        p["analysis_assumptions_not_validated"]["measured_servo_running_torque_6v_Nm"],
                        p["analysis_assumptions_not_validated"]["print_design_allowable_bending_MPa"])
            if any(x is None for x in measured):
                fail("P0 physical measurements are incomplete")
        stories = cx.execute("SELECT id, status, artifact FROM story WHERE phase_id=?", (phase_id,)).fetchall()
        if not stories:
            fail("Phase has no stories: " + phase_id)
        for sid, status, artifact in stories:
            if status != "done":
                fail(sid + " is " + status)
            if not artifact or not (ROOT / artifact).exists():
                fail(sid + " lacks an existing artifact")
            evidences = cx.execute("SELECT evidence FROM implementation_event WHERE story_id=? AND kind='test' AND evidence IS NOT NULL", (sid,)).fetchall()
            if not evidences:
                fail(sid + " lacks a test event with evidence")
            if not any((ROOT / evidence).exists() for (evidence,) in evidences):
                fail(sid + " test evidence path does not exist")
        open_bugs = cx.execute("SELECT b.id FROM bug b JOIN story s ON s.id=b.story_id WHERE s.phase_id=? AND b.status='open' AND b.severity IN ('high','critical')", (phase_id,)).fetchall()
        if open_bugs:
            fail("Phase has open high/critical bugs: " + ",".join(str(x[0]) for x in open_bugs))
    print("PASS: phase gate", phase_id, "—", row[1])


def snapshot():
    with database() as cx:
        cx.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        lines = list(cx.iterdump())
    dump = ROOT / "BOM/history_dump.sql"
    dump.write_text("\n".join(lines) + "\n", encoding="utf-8")
    # Verify the SQL backup can reconstruct a database independently.
    with sqlite3.connect(":memory:") as restored:
        restored.executescript(dump.read_text(encoding="utf-8"))
        if restored.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            fail("SQL snapshot restore failed")
        if restored.execute("PRAGMA foreign_key_check").fetchone():
            fail("SQL snapshot foreign keys failed")
    print("PASS: SQL backup written and restore verified:", dump)


def close_phase(phase_id):
    check()
    phase_gate(phase_id)
    with database() as cx:
        cx.execute("UPDATE phase SET status='done' WHERE id=?", (phase_id,))
    snapshot()
    print("Closed", phase_id, "; review Git diff, commit and tag it")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="command", required=True)
    for name in ("check", "snapshot"):
        sub.add_parser(name)
    for name in ("phase-gate", "close-phase"):
        sub.add_parser(name).add_argument("phase_id")
    a = p.parse_args()
    {"check": check, "snapshot": snapshot,
     "phase-gate": lambda: phase_gate(a.phase_id),
     "close-phase": lambda: close_phase(a.phase_id)}[a.command]()


if __name__ == "__main__":
    main()
