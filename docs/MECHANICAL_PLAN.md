# Plan cơ khí: tính → vẽ → thử, theo từng phase

**P0 — đang làm, dữ liệu vật thật.** Tính khoảng cách tầng từ bước lồng đo trên 10 tô; đo gờ dưới miệng và đường kính cực trị. Vẽ mặt cắt tô thật rồi thay envelope. In coupon cùng hướng/vật liệu dự kiến, đo `μ_s`, `μ_k`, độ bền uốn, độ đảo và độ cong khi giữ 72 giờ. Đo torque–tốc độ MG996R 360° và vị trí tai bắt vít của đúng phiên bản; ghi vào `parameters.json`. Story S-001/S-009.

**P1 — đang làm, screening + bố trí.** Mỗi khi đổi tham số, chạy `calculate_mechanics.py`, so sánh khe guốc, `F_j`, `M_j`, `R_t`, `σ_b`, `T_cam`, `T_servo`; sau đó chạy `build_freecad.py` và `draw_overview.py`/`draw_force_path.py`. Vẽ mặt cắt đường tải, khe cánh và chỗ lắp servo. Kết quả hiện tại ở `design/friction_analysis.md`; guốc 6 cánh có cung trống lớn, cần thử vành tô. Story S-002/S-003/S-007/S-008.

**P2 — sẽ triển khai, cơ cấu thật.** Dựa trên `μ_s` lớn nhất đã đo và torque làm việc thật, thiết kế profile cam `r(θ)` + truyền giảm tốc, tính lực chốt và góc nhả. Vẽ ray/chốt chống lật với cặp phản lực, bệ servo đúng tai bắt vít, vòng khóa lò xo dương và công tắc vị trí. Chỉ xuất STL sản xuất sau khi CAD có đủ bề mặt dẫn hướng/khóa và kiểm tra giao thoa trạng thái mở/đóng. Story S-004/S-005. Biên không đạt → đổi độ dốc cam, tỉ số truyền, vật liệu hoặc actuator.

**P3 — sẽ triển khai, thử nghiệm.** Một tầng không tải 100 chu kỳ; thử tải 1/4/5 kg, 3 guốc tiếp xúc, cắt điện ở mọi vị trí, lực nhả và thời gian. Sau đó lắp cả hai tầng, chạy 50 chu kỳ FIFO có tô thật, đo va đập và kẹt. Ghi event và bug có đường dẫn dữ liệu. Story S-006.

**P4 — sẽ triển khai, bản vẽ sản xuất.** Chốt dung sai sau coupon, vật liệu và hướng in, bắt vít, BOM, STEP/STL cuối, bản vẽ lắp và quy trình bảo trì. Chỉ đóng phase khi checklist nghiệm thu có bằng chứng.

Trình tự trong từng story: **tính → sửa tham số → vẽ → kiểm hình học → thử/đo → tính lại → ghi SQLite**. Dải `μ` và tỉ số 4:1 trong P1 là ứng viên khảo sát, không phải cấu hình đã chốt.
