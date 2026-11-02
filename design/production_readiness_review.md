# Review độ sẵn sàng production — cơ cấu giữ tô

Trạng thái: **chưa đủ dữ liệu để phát hành sản xuất**. CAD được nâng thành prototype PETG có cánh, bearing, chốt khóa và chặn cơ; chưa thử tải vật lý, chưa đo đủ 10 package và chưa hoàn thiện điều khiển khóa.

## 1. Đầu vào đã biết / chưa biết

- Theo người dùng: miệng tô Ø175,7 mm, đáy Ø90 mm, thân cao 70 mm; nắp cao thêm khoảng 5 mm và nhô 3 mm mỗi bên; tô khoảng 0,8 kg.
- Dùng tạm package Ø181,7 × 75 mm và tầng cách 75 mm. `requirements/packaged_bowl_measurements.csv` còn trống; đây chưa phải số đo 10 package.
- Bound tính toán hiện tại là 1 kg/package, 5 package, hệ số tải tĩnh `K=3`. Số 3 là hệ số screening, không thay thế tải động/va đập đo.
- PETG là vật liệu phần in. Allowable của chi tiết FDM tùy máy, sợi, hướng lớp, nhiệt độ, độ ẩm và creep; hiện chưa có giá trị cho phép hoặc hệ số an toàn cuối.

## 2. Tải cánh PETG

Với 5 × 0,8 kg, `W=39,24 N`, `W_d=K W=117,72 N`. Với bound 5 × 1 kg, `W=49,05 N`, `W_d=147,15 N`. Cánh prototype `b=26 mm`, `h=8 mm`, sải `L=18 mm`; `Z=bh²/6=277,3 mm³`.

Trường hợp bound 1 kg, giả định 3 cánh chia đều cho `F_j=49,05 N`; `M=F_jL=882,9 N·mm`, `σ_nom=3,18 MPa`. Nếu một cánh nhận toàn tải thiết kế, `M=2648,7 N·mm`, `σ_nom=9,55 MPa`. Dùng `K_t=2` sơ bộ tại chân cánh thì screening là khoảng `19,1 MPa`, không phải allowable. `SF=σ_allow/σ_max` **chưa xác định**; xem bảng tính trong [petg_reinforced_prototype.md](petg_reinforced_prototype.md).

## 3. Prototype cơ khí hiện tại

- Carrier PETG dày 8 mm; 6 cánh bản lề/tầng dày đứng 8 × rộng 26 mm.
- Mỗi cánh quay trên bearing 625-2RS (OD16/ID5/W5) đặt trong carrier; pin thép Ø5 mm. Liên kết đồng bộ dùng pin thép Ø4 mm.
- Vòng 72T/pinion 12T (6:1); hai chặn PETG cố định chạm tai vòng ở hai đầu hành trình.
- Khóa mỗi tầng: pin lò xo thép Ø6 mm vào bạc OD8/ID6,2 mm trên tai vòng; tháp PETG bắt hai M5 xuyên carrier, có long đền/ê-cu tự hãm. Hình học pin gài/rút được thể hiện ở hai trạng thái FCStd.
- Tải đứng đi qua tô → cánh → pin/bearing/carrier → bốn trụ kim loại Ø12 mm. Khung Ø320 mm; bốn trụ dẫn kim loại Ø12 mm trên PCD292 mm.
- Actuator rút pin đề xuất ở mức yêu cầu: solenoid kéo 12 V, hành trình 9 mm, tối thiểu 30 N tại cuối hành trình; đây chưa phải mã sản phẩm được chọn. Lực lò xo/drag, sensor pin gài/rút, chặn servo điện và liên động phải thử. MG996R 360° là biến thể user supplied; stall torque không phải torque liên tục. Không dựa vào servo để giữ tải.

## 4. Ma sát và truyền động

Sàng lọc dùng `F_f≈μW_d`, tay đòn ma sát `r_eff≈114−87,85=26,15 mm`, `T_ring≈F_f r_eff`, `T_servo≈T_ring/(6η_g)` với `η_g=0,75` giả định. Tại bound 147,15 N và `μ=0,2`, `T_servo≈0,171 N·m`; tại `μ=0,4`, khoảng `0,342 N·m`. Dải `μ=0,1…0,4` chưa đo; phép tính chưa gồm joint friction, kẹt, gia tốc, lực lò xo hoặc sai số lắp. Bảng đầy đủ sinh bởi `py tools/calculate_mechanics.py` trong `simulation/kinematics/force_friction_sensitivity.csv`.

## 5. Rủi ro và gate còn mở

| Rủi ro | Mức | Điều kiện đóng |
|---|---|---|
| Khoảng tầng/biên dạng sai, tô kẹt hoặc nghiêng | Cao | Đo 10 package hoàn chỉnh mỗi line, cập nhật CAD và thử lồng không nén |
| Nứt/creep PETG ở cánh, boss bearing hoặc chân tháp khóa | Cao | Coupon đúng hướng, proof-load, tải lệch, creep 72 h và chu kỳ |
| Pin khóa không gài/rút dưới phản lực hoặc mất điện | Cực cao | Chọn actuator/lò xo, đo lực pin, thêm sensor gài/rút, thử cut-power ở mọi trạng thái |
| Mất tải khi hai tầng chuyển trạng thái | Cực cao | Interlock phần cứng/phần mềm; không mở tầng nếu tầng đối diện chưa xác nhận khóa và nhận tải |
| MG996R hụt lực/nóng | Cao | Đo torque–tốc độ–nhiệt của đúng servo và tải thật; stall torque chỉ để tham khảo |
| Fit bearing OD16 vào PETG và tuột pin | Trung bình/Cao | In coupon lỗ Ø16,2, đo press fit; làm chặn dọc trục pin và kiểm tra mòn |

Gate trước production: điền dữ liệu package thật; hoàn thiện actuator/cảm biến/liên động; xác định allowable PETG từ coupon; chứng minh `SF` trên tiết diện thực; thử proof-load ít nhất 147 N/tầng, 72 giờ creep, tải lệch và 100 chu kỳ một tầng; hoàn thành 50 chu kỳ FIFO và thử mất điện. Chỉ sau review độc lập mới chuyển sang P4/release. Kiểm tra CAD không thay thế các phép thử này.
