BEGIN TRANSACTION;
CREATE TABLE bom_item (
  id TEXT PRIMARY KEY, name TEXT NOT NULL, qty INTEGER NOT NULL,
  material TEXT, source TEXT, status TEXT NOT NULL DEFAULT 'candidate', note TEXT
);
INSERT INTO "bom_item" VALUES('B-001','MG996R continuous rotation',2,NULL,'user supplied','measure','User variant: 40.7 x 19.7 x 42.9 mm, 55 g, 4.8-7.2 V; 9.4/11 kgf.cm stall at 4.8/6 V. Measure real continuous torque.');
INSERT INTO "bom_item" VALUES('B-002','Trụ kết cấu Ø8',4,'metal or validated polymer','TBD','candidate','Liên kết hai tầng');
INSERT INTO "bom_item" VALUES('B-003','Thanh dẫn Ø10',4,'PETG/PA-CF candidate','print','candidate','Điều chỉnh khe hở với tô');
INSERT INTO "bom_item" VALUES('B-004','Trụ/vít đồng M3',4,'brass','user reference','measure','Đo ren, chiều dài và lục giác');
INSERT INTO "bom_item" VALUES('B-005','Lò xo + chốt khóa',2,'metal','TBD','design','Khóa khi mất điện; hình học chưa có');
INSERT INTO "bom_item" VALUES('B-006','Cảm biến mở/đóng',4,NULL,'TBD','design','Ít nhất 2 tín hiệu/tầng');
CREATE TABLE bug (
  id INTEGER PRIMARY KEY AUTOINCREMENT, story_id TEXT REFERENCES story(id),
  title TEXT NOT NULL, severity TEXT NOT NULL CHECK(severity IN ('low','medium','high','critical')),
  status TEXT NOT NULL CHECK(status IN ('open','fixed','verified')) DEFAULT 'open',
  evidence TEXT, fix_artifact TEXT
);
CREATE TABLE implementation_event (
  id INTEGER PRIMARY KEY AUTOINCREMENT, at_utc TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
  story_id TEXT NOT NULL REFERENCES story(id), kind TEXT NOT NULL,
  summary TEXT NOT NULL, artifact TEXT, evidence TEXT
);
INSERT INTO "implementation_event" VALUES(1,'2026-11-02T11:24:07Z','S-002','implement','FreeCAD concept: two rings, 12 shoes, 4 structural posts, 4 guide bridges and posts','cad/assembly/layout.FCStd','exports/STEP/layout_printed_concept.step');
INSERT INTO "implementation_event" VALUES(2,'2026-11-02T11:24:07Z','S-003','implement','Added M3 pilot bores in guide bridges and four guide bars','cad/scripts/build_freecad.py',NULL);
INSERT INTO "implementation_event" VALUES(3,'2026-11-02T11:25:04Z','S-002','test','FreeCADCmd generated valid shapes and 28 STL components','cad/assembly/layout.FCStd','exports/STEP/layout_printed_concept.step');
INSERT INTO "implementation_event" VALUES(4,'2026-11-02T11:31:20Z','S-002','decision','Topology clarified: one bowl column has two coaxial holding mechanisms and two servos','requirements/parameters.json','requirements/requirements.md');
INSERT INTO "implementation_event" VALUES(5,'2026-11-02T11:40:24Z','S-007','implement','Added friction/load sensitivity equations for 1, 4 and 5 bowl cases','design/friction_analysis.md','simulation/kinematics/force_friction_sensitivity.csv');
INSERT INTO "implementation_event" VALUES(6,'2026-11-02T11:40:24Z','S-007','test','12 sensitivity rows generated; lower 1 bowl at mu 0.2 needs 0.202 Nm with candidate 4:1','tools/calculate_mechanics.py','simulation/kinematics/calculation_summary.json');
INSERT INTO "implementation_event" VALUES(7,'2026-11-02T11:40:25Z','S-008','implement','Updated FreeCAD servo envelope and SVG force drawing','cad/assembly/layout.FCStd','exports/drawings/force_path_concept.svg');
CREATE TABLE phase (
  id TEXT PRIMARY KEY, title TEXT NOT NULL, status TEXT NOT NULL
    CHECK(status IN ('todo','doing','done','blocked')), acceptance TEXT NOT NULL
);
INSERT INTO "phase" VALUES('P0','Đo tô và linh kiện','doing','Bản đo 10 tô, servo, trụ đồng và máy in');
INSERT INTO "phase" VALUES('P1','CAD bố trí + nguyên lý khóa','doing','FCStd/STEP mở được; envelope không nhầm chi tiết sản xuất');
INSERT INTO "phase" VALUES('P2','Cam, truyền động, chốt khóa','todo','Một tầng chạy 100 chu kỳ, cắt điện mọi vị trí');
INSERT INTO "phase" VALUES('P3','Thử tải và FIFO','todo','Đạt checklist simulation/validation/acceptance.md');
INSERT INTO "phase" VALUES('P4','Bản vẽ sản xuất','todo','Dung sai, BOM, hướng in, torque vít được chốt');
CREATE TABLE story (
  id TEXT PRIMARY KEY, phase_id TEXT NOT NULL REFERENCES phase(id), title TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('todo','doing','done','blocked')),
  requirement_id TEXT NOT NULL, artifact TEXT, acceptance TEXT NOT NULL
);
INSERT INTO "story" VALUES('S-001','P0','Đo mặt dưới gờ và bước lồng tô','todo','R-01','requirements/parameters.json','Có mẫu đo 10 tô và bước lồng');
INSERT INTO "story" VALUES('S-002','P1','Dựng layout hai tầng FreeCAD','done','R-06','cad/assembly/layout.FCStd','FCStd/STEP/STL concept mở được');
INSERT INTO "story" VALUES('S-003','P1','Bố trí 4 trụ kết cấu và 4 thanh dẫn','doing','R-08','cad/scripts/build_freecad.py','Không giao thoa với tô khi kiểm bằng tô thật');
INSERT INTO "story" VALUES('S-004','P2','Thiết kế cam và truyền động servo','todo','R-09','cad/parts/','Đủ lực, giới hạn hành trình, có cảm biến');
INSERT INTO "story" VALUES('S-005','P2','Chốt lò xo khóa khi mất điện','todo','R-05','cad/parts/','Không bung khi cắt điện có tải');
INSERT INTO "story" VALUES('S-006','P3','Liên động hai tầng và thử FIFO','todo','R-03,R-04','simulation/validation/acceptance.md','50 chu kỳ chỉ nhả một tô');
INSERT INTO "story" VALUES('S-007','P1','Tính lực cánh, khe guốc và ma sát theo dải μ','done','R-10','design/friction_analysis.md','Script và bảng sensitivity khớp tham số');
INSERT INTO "story" VALUES('S-008','P1','Vẽ sơ đồ lực và servo đúng kích thước','done','R-10,R-11','exports/drawings/force_path_concept.svg','Sơ đồ khớp công thức và CAD');
INSERT INTO "story" VALUES('S-009','P0','Đo μ, tải lệch tâm và torque MG996R thật','todo','R-11,R-12','simulation/validation/','Có dữ liệu coupon và biên độ tải thực');
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('implementation_event',7);
COMMIT;
