PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS phase (
  id TEXT PRIMARY KEY, title TEXT NOT NULL, status TEXT NOT NULL
    CHECK(status IN ('todo','doing','done','blocked')), acceptance TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS story (
  id TEXT PRIMARY KEY, phase_id TEXT NOT NULL REFERENCES phase(id), title TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('todo','doing','done','blocked')),
  requirement_id TEXT NOT NULL, artifact TEXT, acceptance TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS bug (
  id INTEGER PRIMARY KEY AUTOINCREMENT, story_id TEXT REFERENCES story(id),
  title TEXT NOT NULL, severity TEXT NOT NULL CHECK(severity IN ('low','medium','high','critical')),
  status TEXT NOT NULL CHECK(status IN ('open','fixed','verified')) DEFAULT 'open',
  evidence TEXT, fix_artifact TEXT
);
CREATE TABLE IF NOT EXISTS implementation_event (
  id INTEGER PRIMARY KEY AUTOINCREMENT, at_utc TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
  story_id TEXT NOT NULL REFERENCES story(id), kind TEXT NOT NULL,
  summary TEXT NOT NULL, artifact TEXT, evidence TEXT
);
CREATE TABLE IF NOT EXISTS bom_item (
  id TEXT PRIMARY KEY, name TEXT NOT NULL, qty INTEGER NOT NULL,
  material TEXT, source TEXT, status TEXT NOT NULL DEFAULT 'candidate', note TEXT
);
