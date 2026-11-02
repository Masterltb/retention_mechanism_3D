# Tải cánh quay, ma sát và MG996R — screening PETG

Sinh bởi `py tools/calculate_mechanics.py`; đầu vào tại `requirements/parameters.json`, bảng tại `simulation/kinematics/force_friction_sensitivity.csv`. Servo đảo chiều qua PWM, bánh răng 72:12 và vòng liên kết cánh; **không dùng cam**. Các hệ số ma sát 0,1–0,4 chỉ là dải sensitivity, chưa đo.

## Đầu vào

Theo người dùng: tô khoảng 0,8 kg; bound tạm để thiết kế là 1,0 kg/package. Có 5 package/line, 6 cánh/tầng, chỉ giả định 3 cánh chia tải khi lệch tâm; hệ số tĩnh `K=3`. CAD L1 tạm dùng vành ngoài Ø175,7 mm, thân cao 70 mm, nắp Ø181,7 × 5 mm, bước tầng 75 mm. Các giá trị package, gờ và bước tầng cần thay theo 10 package đã cân/đo.

## Tải và uốn cánh

`W=mg`, `W_d=K W`, `F_j=W_d/3`. Cánh được sàng lọc như công-xôn: `M=F_j L`, `Z=b h²/6`, `σ_nom=M/Z`, với `L=18 mm`, `b=26 mm`, `h=8 mm`, `Z=277,3 mm³`.

| Trường hợp | Khối lượng trên một tầng | `W_d` | `F_j` khi 3 cánh chia tải | `σ_nom` 3 cánh | `σ_nom` một cánh nhận toàn tải |
|---|---:|---:|---:|---:|---:|
| Dưới giữ 1 package 0,8 kg | 0,8 kg | 23,54 N | 7,85 N | 0,51 MPa | 1,53 MPa |
| Trên giữ 4 package × 0,8 kg | 3,2 kg | 94,18 N | 31,39 N | 2,04 MPa | 6,11 MPa |
| 5 package × 0,8 kg dồn một tầng | 4,0 kg | 117,72 N | 39,24 N | 2,55 MPa | 7,64 MPa |
| Lỗi bound 5 package × 1,0 kg | 5,0 kg | 147,15 N | 49,05 N | 3,18 MPa | 9,55 MPa |

Chân cánh có lỗ, bo góc và liên kết lớp; `Kt=2` chỉ là giả định sàng lọc khiến trường hợp lỗi một cánh thành `σ≈19,1 MPa`. Không có allowable PETG FDM theo đúng máy/hướng/nhiệt/thời gian tải nên `SF=σ_allow/σ_max` **chưa xác định**. Creep 72 giờ, proof-load và tải chu kỳ còn phải thử. Bảng script còn có một case bound 4 kg upper/1 kg lower/5 kg lỗi theo tham số harness; bảng phân tích package 0,8 kg ở đây tính riêng bằng công thức để dễ đối chiếu.

## Mô-men ma sát quanh bản lề

Screening đơn giản dùng tổng lực ma sát `F_f=μ W_d` và cánh tay tiếp xúc `r_eff=R_pivot−R_rim=114−87,85=26,15 mm`. Mô-men vòng cánh `T_ring≈F_f r_eff`; servo pinion 12T dẫn vòng 72T, nên `i=6`. Mô-men yêu cầu servo `T_servo≈T_ring/(i η_g)`, tạm dùng `η_g=0,75`. Chưa cộng ma sát khớp, biến dạng, kẹt, tăng tốc hoặc lực pin khóa.

Ví dụ lỗi bound `W_d=147,15 N`, nếu `μ=0,2`: `F_f≈29,43 N`, `T_ring≈0,770 N·m`, `T_servo≈0,171 N·m`. Nếu `μ=0,4`, `T_servo≈0,342 N·m` — cao hơn ngưỡng screening `0,324 N·m` (30% stall 6V). Ở tải trên bình thường 3,2 kg tại `μ=0,2`: `T_servo≈0,110 N·m`. Đây không chứng minh MG996R đạt: torque stall không phải định mức liên tục; đúng biến thể 360° phải đo torque–tốc độ/nhiệt. Mô-men bản lề thật phụ thuộc điểm tiếp xúc và đường truyền lực, cần đo lực mở trên cụm thật sau khi in.

Tải đứng phải đi từ vành tô qua cánh, trục/bệ bản lề và carrier đến trụ kim loại; servo không được giữ tải. Liên động chỉ cho rút chốt/mở một tầng sau khi tầng đối diện đã khóa và được xác nhận. PWM servo quay liên tục điều khiển chiều/tốc độ, không phải phản hồi góc; cần công tắc hành trình độc lập, chặn cơ và cảm biến trạng thái pin.

## Đo ma sát và ngưỡng an toàn

In coupon PETG đúng hướng/lớp. Kéo bề mặt tiếp xúc bằng lực kế với lực pháp tuyến đã biết; `μ_s=(F_break−F_0)/N`, `μ_k=(F_run−F_0)/N`. Thử khô/ẩm, sau mài mòn và ở các mức tải; lưu min/max và ảnh coupon. Dùng giá trị lớn nhất có căn cứ trong mô-men. Ma sát nắp–cánh, cánh–trục và guide shoe–package là các cặp riêng.

MG996R theo nhà sản xuất có stall torque đến 11 kgf·cm tại 6V; mốc 30% chỉ là ngưỡng cảnh báo. [TowerPro MG996R](https://towerpro.com.tw/product/mg996R/). PETG printed allowable phải lấy từ coupon và thử creep; datasheet filament kéo không thay thế dữ liệu chi tiết in.
