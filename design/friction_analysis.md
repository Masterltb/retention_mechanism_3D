# Tính lực, khe cánh, ma sát và MG996R — screening v0.2

Các trị số tính bằng `py tools/calculate_mechanics.py` từ `requirements/parameters.json`; bảng đầy đủ ở `simulation/kinematics/force_friction_sensitivity.csv`. **Đây là kiểm tra sơ bộ trên guốc trượt 6 cánh hiện có, chưa phải chứng nhận chịu tải hoặc thiết kế cam.** Ký hiệu `μ` là hệ số ma sát nhựa–nhựa *chưa đo*. Các giá trị 0,1–0,4 chỉ là dải khảo sát, không phải thông số PETG/PA-CF đã xác nhận.

## 1. Hình học và khoảng cách cánh

Tô: `D_rim = 175,7 mm`, bán kính `R_rim = 87,85 mm`. Đóng: lỗ thông thủy `D_c = 160 mm`, bán kính trong cánh `R_c = 80 mm`. Mở: `D_o = 200 mm`, `R_o = 100 mm`. Hành trình hướng tâm `s = (D_o − D_c)/2 = 20 mm`. Độ gối tối đa theo hình chiếu `R_rim − R_c = 7,85 mm`; độ tiếp xúc thực phụ thuộc mặt dưới vành tô. Khe hướng tâm khi mở là `(D_o − D_rim)/2 = 12,15 mm` mỗi bên nếu đồng tâm.

Với `n = 6` guốc, rộng tiếp tuyến `b = 22 mm`, tại bán kính trong `r`:

`Δθ_trống = 2π/n − 2 atan[b/(2r)]` và `g_cung = r Δθ_trống`.

Kết quả: **61,91 mm cung trống khi đóng** ở `r = 80 mm` và **82,81 mm khi mở** ở `r = 100 mm`. Khi đóng, các guốc chỉ phủ khoảng **26,1% chu vi** tại mép trong. Ø160 mm là đường tròn lọt lớn nhất chạm cả sáu mép trong, **không phải lỗ tròn liên tục** vì tồn tại các khoảng trống này. Đây là khoảng trống *giữa* các guốc, khác hoàn toàn mục tiêu khe kẹp hờ **0,1 mm** giữa tô và mặt định tâm. Các guốc là gờ đỡ rời, không phải iris chồng cánh liên tục như ảnh mẫu. Phải thử độ võng vành tô giữa các điểm đỡ; nếu không đạt, tăng số guốc/độ rộng hoặc chuyển sang cánh iris chồng mép và tính lại từ đầu.

## 2. Tải cột và lực trên cánh

Tổng cột 5 tô × 1 kg = `5 kg`, `W = 49,05 N`. FIFO bình thường: trên giữ **4 kg → 39,24 N**, dưới giữ **1 kg → 9,81 N**. Lỗi dồn toàn bộ lên một tầng: **5 kg → 49,05 N**. Dùng hệ số tải tĩnh sơ bộ `K = 3` để sàng lọc, tải tính toán tương ứng **117,72 / 29,43 / 147,15 N**. Va đập lúc chuyển tầng chưa được bao gồm.

Nếu chỉ `n_eff = 3` trong 6 guốc thực sự tiếp xúc khi lệch tâm: `F_j = K W/n_eff`. Mỗi guốc chịu **39,24 N** ở tầng trên, **9,81 N** ở tầng dưới, hoặc **49,05 N** khi 5 tô dồn một tầng. Lực phân bố thực phải đo bằng cảm biến/coupon; 3 guốc là giả định kiểm tra, chưa phải kết quả đo.

## 3. Cong và lật guốc ("hệ số bền")

Mô hình bảo thủ: tâm lực lệch `e = 10 mm` từ vùng dẫn hướng; khoảng cách hai mặt chịu phản lực chống lật `h = 8 mm`. Đây là **kích thước giả định**, vì ray giữ và chốt chống lật chưa được hoàn thiện trong CAD. Mômen `M_j = F_j e`; phản lực cần cho **một** mặt của cặp chống lật `R_t = M_j/h`. Kết quả trên/dưới/lỗi 5 tô: `M_j = 392,4 / 98,1 / 490,5 N·mm`, `R_t = 49,05 / 12,26 / 61,31 N` trên mỗi guốc chịu tải. Nếu muốn biên chống lật `SF_t = 2`, cặp ray/chốt phải chứng minh khả năng chịu ít nhất `2R_t` tại cùng cánh, ngoài lực đứng.

Với tiết diện chữ nhật guốc `b = 22 mm`, dày `t = 6 mm`, `Z = bt²/6 = 132 mm³`. Ứng suất uốn danh nghĩa `σ_b = M_j/Z` lần lượt **2,97 / 0,74 / 3,72 MPa**. Hệ số bền vật liệu chỉ tính được sau khi đo/đặt ứng suất cho phép theo hướng lớp in và nhiệt độ: `SF_b = σ_allow / σ_b`. **Chưa có `σ_allow`, nên chưa được ghi một hệ số bền số học hoặc kết luận guốc đạt.** Mô hình này cũng chưa tính tập trung ứng suất, creep, lỗ chốt và tải động.

## 4. Ma sát nhựa–nhựa và torque cam

Không thể suy ra `μ` chỉ từ khối lượng tô và kích thước; cần thử chính cặp vật liệu/bề mặt in. Với guốc bị tải lệch và kẹp giữa hai mặt ray, ước lượng trên của tổng pháp tuyến các guốc chịu tải là `N_Σ ≈ KW(1 + 2e/h)`. Công thức này giả định cặp phản lực lật làm tăng tổng pháp tuyến và **không** gồm lực tiền ép, cọ mặt bên, lực chốt khóa hay biến dạng. Lực ma sát trượt guốc–ray `F_f ≈ μ N_Σ`; ma sát tĩnh dùng `μ_s` khi bắt đầu chuyển động, động dùng `μ_k` khi đang chạy. Ma sát vành tô–guốc và chốt cam–vành cam là **hai cặp tiếp xúc khác**; phải đo riêng hoặc đưa vào hiệu suất thực, chưa được cộng vào bảng dưới.

Nếu cam làm guốc đi `s = 20 mm` trong `θ = 60° = 1,047 rad`, độ dốc `q = s/θ = 19,10 mm/rad`. Với hiệu suất cam giả định `η_c = 0,65`: `T_cam ≈ F_f q/η_c`. Truyền giảm tốc ứng viên `i = 4:1`, hiệu suất giả định `η_g = 0,75`: `T_servo ≈ T_cam/(i η_g)`. Bảng tại `μ = 0,2`:

| Tình huống | `F_f` | `T_cam` | `T_servo` với 4:1 |
|---|---:|---:|---:|
| Dưới, 1 tô | 20,60 N | 0,605 N·m | 0,202 N·m |
| Trên, 4 tô | 82,40 N | 2,421 N·m | 0,807 N·m |
| Lỗi, 5 tô/một tầng | 103,00 N | 3,027 N·m | 1,009 N·m |

Ở dưới 1 tô, nếu `μ = 0,4`, `T_servo ≈ 0,404 N·m`. Nếu trên vẫn bị tải 4 tô lúc mở, ngay cả `μ = 0,1` cũng cần `0,404 N·m` với ứng viên 4:1. **Do đó tầng trên chỉ được mở sau khi tầng dưới thực sự đã nhận tải**, điều này phải xác nhận bằng cảm biến hoặc thử lực. Torque thực có thể lớn hơn vì tiền ép, bánh răng, chốt và kẹt.

## 5. MG996R 360° do người dùng cung cấp

Thân `40,7 × 19,7 × 42,9 mm`, nặng khoảng `55 g`, điện áp `4,8–7,2 V`, nhiệt độ `0–55 °C`, bánh răng kim loại, hộp số mô tả "bán kim loại". `9,4 kgf·cm` tại 4,8 V = **0,922 N·m**; `11 kgf·cm` tại 6 V = **1,079 N·m**. Đây là **stall torque**, không được dùng làm torque liên tục. Vì không có đường cong torque–tốc độ/nhiệt cho đúng chiếc servo, tạm lấy `0,30 × stall(6 V) = 0,324 N·m` chỉ làm **ngưỡng sàng lọc giả định**, không phải định mức nhà sản xuất. Với `μ = 0,2`, ứng viên 4:1 vượt ngưỡng này khi mở tầng trên còn tải; trường hợp dưới 1 tô dưới ngưỡng nhưng phải đo thực tế.

Tốc độ công bố `0,17 s/60°` tại 4,8 V, `0,14 s/60°` tại 6 V là tốc độ không tải. Để cam quay 60° qua giảm tốc 4:1, servo quay 240°: thời gian tối thiểu lý tưởng ở 6 V là **0,56 s**, thực tế chậm hơn. Servo 360° quay liên tục cần công tắc/cảm biến vị trí mở, đóng và khóa; không suy ra vị trí từ thời gian chạy.

## 6. Cách đo `μ` và các số còn thiếu

In coupon đúng vật liệu, hướng lớp, chiều cao lớp, bề mặt và độ ẩm sẽ dùng. Ép coupon guốc lên coupon vành/khung bằng lực pháp tuyến `N` đã biết; kéo song song mặt trượt bằng lực kế ở tốc độ giống vận hành. Đo đỉnh lực trước khi trượt `F_break` và lực ổn định `F_run`. Trừ lực nền của đồ gá `F_0`: `μ_s = (F_break−F_0)/N`, `μ_k = (F_run−F_0)/N`. Lặp ở nhiều `N`, ba hướng in, khô/ẩm và sau mài mòn; dùng **giá trị lớn nhất có căn cứ** để tính motor. Cách phân biệt ma sát tĩnh/động tham chiếu [ASTM D1894-24](https://store.astm.org/standards/d1894), vốn dành cho màng/tấm nhựa; đồ gá này là thử nghiệm riêng cho chi tiết FDM, không tự nhận là thử theo ASTM.

Phải đo thêm biên dạng vành tô, bước lồng, điểm đặt tải `e`, khoảng ray `h`, lực chốt, hiệu suất cam/bánh răng, sức bền coupon theo hướng in và biến dạng dài hạn. Chốt cơ khí dương vẫn bắt buộc; không dựa vào ma sát hoặc khả năng tự hãm của servo để giữ tải lúc mất điện. Thông số MG996R chuẩn [TowerPro](https://towerpro.com.tw/product/mg996R/) hỗ trợ mốc torque, nhưng phiên bản 360° đang dùng cần được đo riêng.
