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
('S-004','P2','Thiết kế cam và truyền động servo','todo','R-09','cad/parts/','Đủ lực, giới hạn hành trình, có cảm biến'),
('S-005','P2','Chốt lò xo khóa khi mất điện','todo','R-05','cad/parts/','Không bung khi cắt điện có tải'),
('S-006','P3','Liên động hai tầng và thử FIFO','todo','R-03,R-04','simulation/validation/acceptance.md','50 chu kỳ chỉ nhả một tô'),
('S-007','P1','Tính lực cánh, khe guốc và ma sát theo dải μ','doing','R-10','design/friction_analysis.md','Script và bảng sensitivity khớp tham số'),
('S-008','P1','Vẽ sơ đồ lực và servo đúng kích thước','doing','R-10,R-11','exports/drawings/force_path_concept.svg','Sơ đồ khớp công thức và CAD'),
('S-009','P0','Đo μ, tải lệch tâm và torque MG996R thật','todo','R-11,R-12','simulation/validation/','Có dữ liệu coupon và biên độ tải thực');
INSERT OR IGNORE INTO bom_item VALUES
('B-001','MG996R continuous rotation',2,NULL,'user supplied','measure','Đo phiên bản thực, nguồn riêng'),
('B-002','Trụ kết cấu Ø8',4,'metal or validated polymer','TBD','candidate','Liên kết hai tầng'),
('B-003','Thanh dẫn Ø10',4,'PETG/PA-CF candidate','print','candidate','Điều chỉnh khe hở với tô'),
('B-004','Trụ/vít đồng M3',4,'brass','user reference','measure','Đo ren, chiều dài và lục giác'),
('B-005','Lò xo + chốt khóa',2,'metal','TBD','design','Khóa khi mất điện; hình học chưa có'),
('B-006','Cảm biến mở/đóng',4,NULL,'TBD','design','Ít nhất 2 tín hiệu/tầng');
UPDATE bom_item SET note='User variant: 40.7 x 19.7 x 42.9 mm, 55 g, 4.8-7.2 V; 9.4/11 kgf.cm stall at 4.8/6 V. Measure real continuous torque.' WHERE id='B-001';
