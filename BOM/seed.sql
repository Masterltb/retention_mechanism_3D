INSERT OR IGNORE INTO phase VALUES
('P0','Đo tô và linh kiện','doing','Bản đo 10 tô, servo, trụ đồng và máy in'),
('P1','CAD bố trí + nguyên lý khóa','doing','FCStd/STEP mở được; envelope không nhầm chi tiết sản xuất'),
('P2','Cam, truyền động, chốt khóa','todo','Một tầng chạy 100 chu kỳ, cắt điện mọi vị trí'),
('P3','Thử tải và FIFO','todo','Đạt checklist simulation/validation/acceptance.md'),
('P4','Bản vẽ sản xuất','todo','Dung sai, BOM, hướng in, torque vít được chốt');
INSERT OR IGNORE INTO story VALUES
('S-001','P0','Đo mặt dưới gờ và bước lồng tô','todo','R-01','requirements/parameters.json','Có mẫu đo 10 tô và bước lồng'),
('S-002','P1','Dựng layout hai tầng FreeCAD','doing','R-06','cad/assembly/layout.FCStd','FCStd/STEP/STL concept mở được'),
('S-003','P1','Bố trí 4 trụ kết cấu và 4 thanh dẫn','doing','R-08','cad/scripts/build_freecad.py','Không giao thoa với tô khi kiểm bằng tô thật'),
('S-004','P2','Thiết kế cánh xoay, đồng bộ và servo PWM không cam','todo','R-09','cad/assembly/one_line_pivot_prototype_closed.FCStd','Chốt cơ dương, chặn, cảm biến, torque và 100 chu kỳ đạt'),
('S-005','P2','Chốt lò xo khóa khi mất điện','todo','R-05','cad/parts/','Không bung khi cắt điện có tải'),
('S-006','P3','Liên động hai tầng và thử FIFO','todo','R-03,R-04','simulation/validation/acceptance.md','50 chu kỳ chỉ nhả một tô'),
('S-007','P1','Tính lực cánh, khe guốc và ma sát theo dải μ','doing','R-10','design/friction_analysis.md','Script và bảng sensitivity khớp tham số'),
('S-008','P1','Vẽ sơ đồ lực và servo đúng kích thước','doing','R-10,R-11','exports/drawings/force_path_concept.svg','Sơ đồ khớp công thức và CAD'),
('S-009','P0','Đo μ, tải lệch tâm và torque MG996R thật','todo','R-11,R-12','simulation/validation/','Có dữ liệu coupon và biên độ tải thực');
INSERT OR IGNORE INTO bom_item VALUES
('B-001','MG996R continuous rotation',2,NULL,'user supplied','measure','Đo phiên bản thực, nguồn riêng'),
('B-002','Trụ kết cấu Ø12',4,'aluminum or stainless steel','TBD','candidate','Liên kết hai tầng; through-fit carrier; verify buckling and connection'),
('B-003','Trụ dẫn Ø12',4,'stainless steel','TBD','candidate','PCD292; external to flap sweep; shoes in PETG; verify against measured package'),
('B-004','Trụ/vít đồng M3',4,'brass','user reference','measure','Đo ren, chiều dài và lục giác'),
('B-005','Chốt khóa lò xo Ø6 + bạc OD8/ID6.2',2,'stainless steel','TBD','prototype','Pin engages sync-ring bushing when closed; validate pin force and depth'),
('B-006','Cảm biến hành trình mở/đóng',4,NULL,'TBD','design','Hai trạng thái xác nhận/tầng; safety interlock required'),
('B-007','Bu-lông xuyên M5, vòng đệm, ê-cu tự hãm',4,'stainless steel','TBD','candidate','Hai bộ cho mỗi latch bracket'),
('B-008','Trục bản lề Ø5',12,'stainless steel','TBD','candidate','Six per stage; retain against axial escape'),
('B-009','Chốt link Ø4',24,'stainless steel','TBD','candidate','Pins at flap and synchronization ring ends'),
('B-010','Solenoid kéo pin khóa 12 V, hồi lò xo',2,'metal','TBD','candidate','Stroke 9 mm; target pull >=30 N at full stroke; verify side-load and voltage'),
('B-011','Bạc đạn bản lề 625-2RS',12,'steel','TBD','candidate','OD16/ID5/W5; counterbore in carrier; verify fit by coupon');
UPDATE bom_item SET note='User variant: 40.7 x 19.7 x 42.9 mm, 55 g, 4.8-7.2 V; 9.4/11 kgf.cm stall at 4.8/6 V. Measure real continuous torque.' WHERE id='B-001';

INSERT OR IGNORE INTO bom_item VALUES ('B-012','Bu-lông kẹp guốc dẫn M3 x 12',20,'stainless steel','TBD','prototype','Một vít inox cho mỗi guốc PETG; dùng long đen, siết nhẹ để không ép lún nhựa');
