# Tóm tắt tính toán prototype cánh quay

Tính lại bằng `py tools/calculate_mechanics.py`; CSV sinh tự động ở `simulation/kinematics/force_friction_sensitivity.csv`. Công thức và giả định chi tiết: [friction_analysis.md](friction_analysis.md).

- Tổng tải 5 × 0,8 kg: `W=39,24 N`; nhân `K=3` cho screening `117,72 N`.
- Bound tạm 1 kg/package: tải 5 tô `W=49,05 N`; với `K=3`, `W_d=147,15 N`.
- Cánh 26 × 8 mm: `Z=bh²/6=277,3 mm³`; sải công-xôn 18 mm. Với toàn bộ `147,15 N` dồn lên một cánh: `M=2648,7 N·mm`, `σ_nom=9,55 MPa`; hệ số chân cánh `Kt=2` giả định → khoảng `19,1 MPa`. PETG allowable/hệ số an toàn vẫn chưa xác định.
- Tâm trục cánh R=114 mm, bán kính miệng tô 87,85 mm → tay đòn ma sát sơ bộ 26,15 mm.
- Servo pinion 12T và vòng 72T cho giảm tốc 6:1. Tại tải bound `W_d=147,15 N`, `μ=0,2`, `η_g=0,75`, mô-men servo sàng lọc khoảng `0,171 N·m`; tại `μ=0,4` khoảng `0,342 N·m`. `μ` và mô-men làm việc chưa đo; 30% stall không phải định mức liên tục.
- Khe cung giữa sáu cánh được sinh theo đường tròn aperture, không chứng minh mép tô không võng qua khoảng trống.

Không dùng mô hình để phát hành production trước khi đo 10 package, thử coupon/tải/creep, khóa mất điện và chu kỳ FIFO.
