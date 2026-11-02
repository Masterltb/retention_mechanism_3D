# Plan cơ khí: tính → vẽ → thử, theo từng phase

**P0 — đang làm, dữ liệu vật thật.** Tính khoảng cách tầng từ bước lồng đo trên 10 tô; đo gờ dưới miệng và đường kính cực trị. Vẽ mặt cắt tô thật rồi thay envelope. In coupon cùng hướng/vật liệu dự kiến, đo `μ_s`, `μ_k`, độ bền uốn, độ đảo và độ cong khi giữ 72 giờ. Đo torque–tốc độ MG996R 360° và vị trí tai bắt vít của đúng phiên bản; ghi vào `parameters.json`. Story S-001/S-009.

**P1 — đang làm, screening + bố trí.** Mỗi khi đổi tham số, chạy `calculate_mechanics.py`, so sánh khe cánh, `F_j`, `M_j`, `R_t`, `σ_b` và mô-men bản lề/servo từ `μ` sensitivity; sau đó chạy `build_line_pivot_prototype.py`, `inspect_one_line_assembly.py` và `draw_overview.py`/`draw_force_path.py`. Vẽ mặt cắt đường tải, khe cánh và chỗ lắp servo. Kết quả ở `design/friction_analysis.md`; 6 cánh rời có cung trống lớn, cần thử độ võng vành tô thật. Story S-002/S-003/S-007/S-008.

**P2 — đang dựng prototype.** Theo cấu hình người dùng: servo quay đảo chiều bằng PWM, không dùng cam. Prototype hiện có sáu cánh bản lề, thanh nối, vòng răng 72:12, pin khóa lò xo và hai chặn cơ mỗi tầng; tháp khóa có actuator envelope nhưng actuator, lực lò xo và limit switch cần chốt phần cứng. Tính mô-men `T_pivot=Σ(F_i·r_perp,i)+T_joint+T_spring`; đo lực ma sát/torque làm việc thực. Chỉ phát hành STL sản xuất sau kiểm tra cơ cấu khóa, chống lật, tải PETG, mất điện và cycle test. Story S-004/S-005.

**P3 — sẽ triển khai, thử nghiệm.** Một tầng không tải 100 chu kỳ; thử tải 1/4/5 kg, 3 guốc tiếp xúc, cắt điện ở mọi vị trí, lực nhả và thời gian. Sau đó lắp cả hai tầng, chạy 50 chu kỳ FIFO có tô thật, đo va đập và kẹt. Ghi event và bug có đường dẫn dữ liệu. Story S-006.

**P4 — sẽ triển khai, bản vẽ sản xuất.** Chốt dung sai sau coupon, vật liệu và hướng in, bắt vít, BOM, STEP/STL cuối, bản vẽ lắp và quy trình bảo trì. Chỉ đóng phase khi checklist nghiệm thu có bằng chứng.

Trình tự trong từng story: **tính → sửa tham số → vẽ → kiểm hình học → thử/đo → tính lại → ghi SQLite**. Dải `μ` và tỉ số 4:1 trong P1 là ứng viên khảo sát, không phải cấu hình đã chốt.
