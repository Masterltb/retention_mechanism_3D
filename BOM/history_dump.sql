BEGIN TRANSACTION;
CREATE TABLE bom_item (
  id TEXT PRIMARY KEY, name TEXT NOT NULL, qty INTEGER NOT NULL,
  material TEXT, source TEXT, status TEXT NOT NULL DEFAULT 'candidate', note TEXT
);
INSERT INTO "bom_item" VALUES('B-001','MG996R continuous rotation',2,NULL,'user supplied','measure','User variant: 40.7 x 19.7 x 42.9 mm, 55 g, 4.8-7.2 V; 9.4/11 kgf.cm stall at 4.8/6 V. Measure real continuous torque.');
INSERT INTO "bom_item" VALUES('B-002','Trụ kết cấu Ø12',4,'aluminum or stainless steel','TBD','candidate','Liên kết hai tầng; through-fit carrier; verify buckling and connection');
INSERT INTO "bom_item" VALUES('B-003','Trụ dẫn Ø12',4,'stainless steel','print','candidate','PCD292; external to flap sweep; PETG shoes; verify measured package');
INSERT INTO "bom_item" VALUES('B-004','Trụ/vít đồng M3',4,'brass','user reference','measure','Đo ren, chiều dài và lục giác');
INSERT INTO "bom_item" VALUES('B-005','Chốt khóa lò xo Ø6 + bạc OD8/ID6.2',2,'stainless steel','TBD','prototype','Pin engages sync-ring bushing when closed; validate pin force and depth');
INSERT INTO "bom_item" VALUES('B-006','Cảm biến hành trình mở/đóng',4,NULL,'TBD','design','Two confirmation signals per stage; interlock required');
INSERT INTO "bom_item" VALUES('B-007','Bu-lông xuyên M5, vòng đệm, ê-cu tự hãm',4,'stainless steel','TBD','candidate','Hai bộ cho mỗi latch bracket');
INSERT INTO "bom_item" VALUES('B-008','Trục bản lề Ø5',12,'stainless steel','TBD','candidate','Six per stage; retain against axial escape');
INSERT INTO "bom_item" VALUES('B-009','Chốt link Ø4',24,'stainless steel','TBD','candidate','Pins at flap and synchronization ring ends');
INSERT INTO "bom_item" VALUES('B-010','Solenoid kéo pin khóa 12 V, hồi lò xo',2,'metal','TBD','candidate','Stroke 9 mm; target pull >=30 N at full stroke; verify side-load and voltage');
INSERT INTO "bom_item" VALUES('B-011','Bạc đạn bản lề 625-2RS',12,'steel','TBD','candidate','OD16/ID5/W5; counterbore in carrier; verify fit by coupon');
INSERT INTO "bom_item" VALUES('B-012','Bu-lông kẹp guốc dẫn M3 x 12',20,'stainless steel','TBD','prototype','Một vít inox cho mỗi guốc PETG; dùng long đen, siết nhẹ để không ép lún nhựa');
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
INSERT INTO "implementation_event" VALUES(8,'2026-11-02T15:58:31Z','S-002','test','FreeCAD 1.1.4: 12 cụm guốc/bạc đạn/ray có shape hợp lệ, mỗi chi tiết là một solid','cad/assembly/layout.FCStd','simulation/validation/bearing_fit.md');
INSERT INTO "implementation_event" VALUES(9,'2026-11-02T16:01:01Z','S-007','decision','Lập baseline tải và production risk review; mô hình còn ở screening do thiếu dữ liệu tô, vật liệu, torque làm việc và cam/khóa','design/production_readiness_review.md','simulation/kinematics/force_friction_sensitivity.csv');
INSERT INTO "implementation_event" VALUES(10,'2026-11-02T16:04:21Z','S-004','decision','Theo yêu cầu người dùng: PWM đảo chiều, không dùng cam; cần bản lề/liên kết, limit switch hoặc encoder vì servo liên tục không điều khiển vị trí','design/production_readiness_review.md','design/production_readiness_review.md');
INSERT INTO "implementation_event" VALUES(11,'2026-11-02T16:07:39Z','S-004','implement','Đề xuất prototype một cột 2 tầng, 6 cánh quay/tầng, vòng đồng bộ và liên động tuần tự; screening torque theo stall/4','design/pivot_flap_prototype.md','design/production_readiness_review.md');
INSERT INTO "implementation_event" VALUES(12,'2026-11-02T16:11:12Z','S-001','implement','Tạo quy trình và phiếu đo 10 tô: kích thước vành, gờ dưới, khối lượng và bước lồng','requirements/bowl_measurement_protocol.md','requirements/nested_stack_measurements.csv');
INSERT INTO "implementation_event" VALUES(13,'2026-11-02T16:21:25Z','S-003','implement','Đặt 4 cột dẫn tại PCD 188,7 mm cho khe danh nghĩa 1,5 mm với tô Ø175,7 và cột Ø10; thêm rãnh chỉnh hướng kính ±3 mm','cad/scripts/build_freecad.py','design/bowl_geometry_estimate.md');
INSERT INTO "implementation_event" VALUES(14,'2026-11-02T16:23:59Z','S-001','decision','Máy có hai line sản phẩm; mỗi line nạp package kín có nắp. Chiều cao 70 mm của L1 là tô trần; đo bao bì hoàn chỉnh và pitch xếp package riêng cho L1/L2','requirements/packaged_bowl_measurements.csv','requirements/bowl_measurement_protocol.md');
INSERT INTO "implementation_event" VALUES(15,'2026-11-02T16:26:59Z','S-001','decision','Người dùng ước tính 5 package/line, khoảng 0,8 kg/tô; giữ 1,0 kg/package làm bound screening tới khi cân cả nắp/seal','requirements/parameters.json','design/production_readiness_review.md');
INSERT INTO "implementation_event" VALUES(16,'2026-11-02T16:30:03Z','S-002','implement','Dựng lại module 1 line hai tầng liền trụ; thêm package envelope L1 có nắp và chỉnh guide PCD theo Ø181,7 mm ước lượng','cad/assembly/layout.FCStd','design/bowl_geometry_estimate.md');
INSERT INTO "implementation_event" VALUES(17,'2026-11-02T16:30:03Z','S-002','test','FreeCAD 1.1.4 sinh FCStd, STEP và 28 STL concept thành công; engineering check đạt','cad/assembly/layout.FCStd','design/bowl_geometry_estimate.md');
INSERT INTO "implementation_event" VALUES(18,'2026-11-02T16:34:07Z','S-002','decision','Gate spacing derived from same relative wing contact point on adjacent packages: Hbody 70 + lid rise 5 = provisional stack pitch 75 mm; CAD asserts upper package base touches lower lid','cad/scripts/build_freecad.py','design/bowl_geometry_estimate.md');
INSERT INTO "implementation_event" VALUES(19,'2026-11-02T16:53:57Z','S-004','implement','Tạo assembly pivot flap một line gồm hai tầng, 12 cánh bản lề, gói có nắp, 4 cột dẫn và trụ liên kết','cad/assembly/one_line_pivot_prototype.FCStd','simulation/validation/pivot_prototype_check.md');
INSERT INTO "implementation_event" VALUES(20,'2026-11-02T16:53:57Z','S-004','test','FreeCAD 1.1.4: 76 shape hợp lệ, 12 cánh không giao thể tích với package, khoảng cách carrier 75 mm','cad/assembly/one_line_pivot_prototype.FCStd','simulation/validation/pivot_prototype_check.md');
INSERT INTO "implementation_event" VALUES(21,'2026-11-02T17:02:22Z','S-004','implement','Hoàn thiện prototype hình học: hinge tabs, 6 thanh nối, vòng đồng bộ răng 72:12, pinion, 4 cột dẫn qua hai tầng và file đóng/mở riêng','cad/scripts/build_line_pivot_prototype.py','design/pivot_flap_prototype.md');
INSERT INTO "implementation_event" VALUES(22,'2026-11-02T17:02:22Z','S-004','test','FreeCAD 1.1.4: hai trạng thái có 80 shape hợp lệ; gear và cánh/package không giao thể tích; aperture 166,68/204 mm','cad/assembly/one_line_pivot_prototype_closed.FCStd','simulation/validation/pivot_prototype_check.md');
INSERT INTO "implementation_event" VALUES(23,'2026-11-02T17:05:22Z','S-004','implement','Grouped complete one-line assembly with five package envelopes and open/closed compound STEP exports','cad/assembly/one_line_pivot_prototype_closed.FCStd','simulation/validation/pivot_prototype_check.md');
INSERT INTO "implementation_event" VALUES(24,'2026-11-02T17:05:22Z','S-004','test','FreeCAD 1.1.4 regenerated closed/open FCStd and STEP; 87 document objects, 86 grouped assembly members, 70 component STLs; geometry limitations documented','exports/STEP/one_line_complete_assembly_closed.step','simulation/validation/pivot_prototype_check.md');
INSERT INTO "implementation_event" VALUES(25,'2026-11-02T17:08:54Z','S-004','implement','Saved FreeCAD GUI visibility and fit-to-view state for closed/open assembly; generated PNG previews','cad/scripts/prepare_assembly_views.FCMacro','simulation/validation/pivot_prototype_check.md');
INSERT INTO "implementation_event" VALUES(26,'2026-11-02T17:08:54Z','S-004','test','FreeCAD GUI reopened and saved both assembly states; 93 shape objects per file, all valid; closed/open PNG previews generated','exports/preview/one_line_closed.png','exports/preview/one_line_closed_validation.txt');
INSERT INTO "implementation_event" VALUES(27,'2026-11-02T17:38:19Z','S-004','implement','Rebuilt one-line assembly: 3 mm hinge pins, bored-eye links with separate pins, servo carrier relief, trapezoidal gear teeth, outer guide columns with five profile-matched shoes per column, hidden envelope subgroups','cad/scripts/build_line_pivot_prototype.py','simulation/validation/pivot_prototype_check.md');
INSERT INTO "implementation_event" VALUES(28,'2026-11-02T17:38:19Z','S-004','test','FreeCAD 1.1.4 BRep validity: 107/107 shapes valid; pairwise common-volume check: no major-pair interference over 0.05 mm3 in closed or open state; guide-shoe/package clearance geometry checked','exports/preview/one_line_closed_interference_report.txt','exports/preview/one_line_open_interference_report.txt');
INSERT INTO "implementation_event" VALUES(29,'2026-11-02T17:39:11Z','S-004','implement','Integrated four Ø10 guide columns with five bowl-profile shoes each, radial arms and 3.5 mm nominal/0.5 mm full-inward gap; expanded frame to Ø290 mm and saved clean subgroup visibility','cad/scripts/build_line_pivot_prototype.py','design/bowl_geometry_estimate.md');
INSERT INTO "implementation_event" VALUES(30,'2026-11-02T17:39:11Z','S-004','test','FreeCAD 1.1.4: 107/107 shape objects valid; no major-pair common volume above 0.05 mm3 in closed or open state; guide shoes checked against all five bowl envelopes','exports/preview/one_line_closed_interference_report.txt','exports/preview/one_line_open_interference_report.txt');
INSERT INTO "implementation_event" VALUES(31,'2026-11-02T18:39:11Z','S-004','implement','Gia cường prototype PETG: carrier 8 mm, cánh 8x26 mm, chốt/bạc khóa kim loại, M5 xuyên carrier, trụ kim loại Ø12 mm; bước 75 mm vẫn provisional','design/petg_reinforced_prototype.md','cad/assembly/one_line_pivot_prototype_closed.FCStd');
INSERT INTO "implementation_event" VALUES(32,'2026-11-02T18:39:11Z','S-004','test','FreeCAD 1.1.4 closed/open BRep generation and major-pair interference check: no unplanned common volume >0.05 mm3; physical strength/latch tests not performed','cad/scripts/inspect_one_line_assembly.py','exports/preview/one_line_closed_interference_report.txt');
INSERT INTO "implementation_event" VALUES(33,'2026-11-02T18:46:37Z','S-003','implement','Gia cường guide/structure rods lên Ø12 mm, đưa guide PCD292 và frame Ø320 để clear quỹ đạo cánh; package fit vẫn chờ 10 mẫu','requirements/parameters.json','exports/preview/one_line_open_interference_report.txt');
INSERT INTO "implementation_event" VALUES(34,'2026-11-02T18:46:37Z','S-003','test','FreeCAD closed/open CAD major-pair check báo không có giao thể tích ngoài joint/contact đã định nghĩa; kích thước thực tô chưa được kiểm chứng','cad/scripts/inspect_one_line_assembly.py','exports/preview/one_line_closed_interference_report.txt');
INSERT INTO "implementation_event" VALUES(35,'2026-11-02T18:46:37Z','S-004','implement','Cánh PETG 8x26, 625-2RS, truyền động 72:12, 2 hard stops và pin khóa/bạc kim loại; đã xuất FCStd, STEP, STL đóng/mở','cad/scripts/build_line_pivot_prototype.py','cad/assembly/one_line_pivot_prototype_closed.FCStd');
INSERT INTO "implementation_event" VALUES(36,'2026-11-02T18:46:37Z','S-004','test','FreeCAD 1.1.4: closed/open shape generation and CAD interference checks no unplanned common volume >0.05 mm3; không phải thử tải vật lý','cad/scripts/inspect_one_line_assembly.py','exports/preview/one_line_open_interference_report.txt');
INSERT INTO "implementation_event" VALUES(37,'2026-11-02T18:46:37Z','S-005','implement','Tạo hình học chốt lò xo Ø6, bushing ID6.2, bracket PETG 2xM5, pin trạng thái đóng/mở và 2 chặn cơ mỗi tầng; actuator/spring spec còn mở','design/petg_reinforced_prototype.md','cad/assembly/one_line_pivot_prototype_closed.FCStd');
INSERT INTO "implementation_event" VALUES(38,'2026-11-02T18:46:37Z','S-005','test','CAD kiểm tra đóng/mở không giao thể tích ngoài joint; pin/latch lực thực, spring, actuator và mất điện chưa thử','cad/scripts/inspect_one_line_assembly.py','exports/preview/one_line_closed_interference_report.txt');
INSERT INTO "implementation_event" VALUES(39,'2026-11-02T18:47:51Z','S-004','implement','Thêm 12 bearing 625-2RS vào carrier, chốt pin Ø5 và relief boss; các chi tiết xuất vào assembly/STL','requirements/parameters.json','exports/STL/pivot_Stage1_hinge_bearing_01_625_2RS.stl');
INSERT INTO "implementation_event" VALUES(40,'2026-11-02T18:47:51Z','S-005','implement','Chốt yêu cầu actuator pull-solenoid 12V, stroke 9 mm, lực kéo tối thiểu 30 N cuối hành trình theo screening phản lực pin; cần verify catalog và side-load','requirements/parameters.json','design/petg_reinforced_prototype.md');
INSERT INTO "implementation_event" VALUES(41,'2026-11-02T18:51:22Z','S-003','implement','Tách bốn ty dẫn kim loại và 20 guốc PETG điều chỉnh theo từng cao độ; thêm kẹp M3','cad/scripts/build_line_pivot_prototype.py','exports/preview/one_line_closed_interference_report.txt');
INSERT INTO "implementation_event" VALUES(42,'2026-11-02T18:51:22Z','S-004','implement','Gia cường prototype 2 tầng: carrier 8 mm, cánh 8 mm, ổ 625-2RS, khóa pin thép và STL PETG-only','design/petg_reinforced_prototype.md','exports/preview/one_line_open_interference_report.txt');
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
INSERT INTO "story" VALUES('S-001','P0','Đo mặt dưới gờ và bước lồng tô','doing','R-01','requirements/parameters.json','Có mẫu đo 10 tô và bước lồng');
INSERT INTO "story" VALUES('S-002','P1','Dựng layout hai tầng FreeCAD','done','R-06','cad/assembly/layout.FCStd','FCStd/STEP/STL concept mở được');
INSERT INTO "story" VALUES('S-003','P1','Bố trí 4 trụ kết cấu và 4 thanh dẫn','doing','R-08','cad/scripts/build_freecad.py','Không giao thoa với tô khi kiểm bằng tô thật');
INSERT INTO "story" VALUES('S-004','P2','Thiết kế cánh xoay, đồng bộ và servo PWM không cam','doing','R-09','cad/assembly/one_line_pivot_prototype_closed.FCStd','Chốt cơ dương, chặn, cảm biến, torque và 100 chu kỳ đạt');
INSERT INTO "story" VALUES('S-005','P2','Chốt lò xo khóa khi mất điện','doing','R-05','cad/parts/','Không bung khi cắt điện có tải');
INSERT INTO "story" VALUES('S-006','P3','Liên động hai tầng và thử FIFO','todo','R-03,R-04','simulation/validation/acceptance.md','50 chu kỳ chỉ nhả một tô');
INSERT INTO "story" VALUES('S-007','P1','Tính lực cánh, khe guốc và ma sát theo dải μ','doing','R-10','design/friction_analysis.md','Script và bảng sensitivity khớp tham số');
INSERT INTO "story" VALUES('S-008','P1','Vẽ sơ đồ lực và servo đúng kích thước','done','R-10,R-11','exports/drawings/force_path_concept.svg','Sơ đồ khớp công thức và CAD');
INSERT INTO "story" VALUES('S-009','P0','Đo μ, tải lệch tâm và torque MG996R thật','todo','R-11,R-12','simulation/validation/','Có dữ liệu coupon và biên độ tải thực');
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('implementation_event',42);
COMMIT;
