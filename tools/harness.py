"""Small SQLite harness: py tools/harness.py init|status|set|event|bug."""
import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "BOM" / "history.sqlite"
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def connect():
    cx = sqlite3.connect(DB)
    cx.execute("PRAGMA foreign_keys=ON")
    return cx


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    sub.add_parser("status")
    s = sub.add_parser("set")
    s.add_argument("story")
    s.add_argument("status", choices=["todo", "doing", "done", "blocked"])
    e = sub.add_parser("event")
    e.add_argument("story")
    e.add_argument("kind", choices=["implement", "test", "decision", "review"])
    e.add_argument("summary")
    e.add_argument("--artifact")
    e.add_argument("--evidence")
    b = sub.add_parser("bug")
    b.add_argument("story")
    b.add_argument("severity", choices=["low", "medium", "high", "critical"])
    b.add_argument("title")
    b.add_argument("--evidence")
    a = p.parse_args()
    with connect() as cx:
        if a.cmd == "init":
            cx.executescript((ROOT / "BOM" / "schema.sql").read_text(encoding="utf-8"))
            cx.executescript((ROOT / "BOM" / "seed.sql").read_text(encoding="utf-8"))
            print(DB)
        elif a.cmd == "status":
            for row in cx.execute("SELECT p.id,p.status,s.id,s.status,s.title FROM phase p LEFT JOIN story s ON s.phase_id=p.id ORDER BY p.id,s.id"):
                print(" | ".join(str(x or "") for x in row))
            print("Open bugs:", cx.execute("SELECT count(*) FROM bug WHERE status='open'").fetchone()[0])
        elif a.cmd == "set":
            cur = cx.execute("UPDATE story SET status=? WHERE id=?", (a.status, a.story))
            if not cur.rowcount:
                raise SystemExit("Unknown story: " + a.story)
        elif a.cmd == "event":
            cx.execute("INSERT INTO implementation_event(story_id,kind,summary,artifact,evidence) VALUES(?,?,?,?,?)",
                       (a.story, a.kind, a.summary, a.artifact, a.evidence))
        elif a.cmd == "bug":
            cx.execute("INSERT INTO bug(story_id,severity,title,evidence) VALUES(?,?,?,?)",
                       (a.story, a.severity, a.title, a.evidence))


if __name__ == "__main__":
    main()
