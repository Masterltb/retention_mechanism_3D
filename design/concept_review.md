# Đánh giá concept hiện tại — một line, hai tầng

## Cấu hình đang phát triển

Mỗi line có hai vòng carrier đồng trục; mỗi tầng có sáu cánh bản lề do servo MG996R quay đảo chiều bằng PWM điều khiển qua pinion 12T/vòng đồng bộ 72T và thanh nối. **Không dùng cam.** Mỗi trục cánh chạy trên bearing 625-2RS. Tải đứng đi qua cánh, bearing/trục bản lề, carrier và bốn trụ kim loại Ø12 mm; servo chỉ tạo chuyển động. Hai chặn cơ giới hạn đầu hành trình; chốt thép lò xo Ø6 mm khóa tai vòng có bạc OD8/ID6,2 mm khi đóng.

Tháp khóa PETG được bắt hai bu-lông xuyên M5; actuator rút pin và công tắc xác nhận vẫn cần lựa chọn/thiết kế chi tiết. Tầng đối diện phải đóng, chịu tải và xác nhận pin trước khi mở tầng còn lại. Servo liên tục không xác định được góc chỉ bằng PWM; cần limit switch độc lập, timeout và liên động.

CAD hiện tại là [prototype PETG gia cường](petg_reinforced_prototype.md), không phải bản vẽ sản xuất. Carrier dày 8 mm, cánh dày 8 × 26 mm, trụ dẫn kim loại Ø12 mm trên PCD292, khung Ø320 mm. Bao tô đầu vào L1 là 175,7/90/70 mm theo người dùng; package Ø181,7 × 75 mm vẫn là ước lượng. CSV đo 10 package còn trống.

## Chu kỳ FIFO đề xuất

1. Xác nhận trên và dưới đóng, pin khóa gài.
2. Giữ chồng tô bằng tầng trên; chỉ rút khóa dưới rồi mở tầng dưới để nhả một tô.
3. Xác nhận tô đã qua; đóng tầng dưới, nhả lệnh actuator để pin gài và xác nhận pin.
4. Chỉ khi tầng dưới báo khóa và nhận tải, tầng trên mới được phép chuyển trạng thái theo logic điều khiển.
5. Mọi timeout, mất cảm biến hoặc chuyển động bất thường đều dừng servo và không mở tầng kia.

## Rủi ro còn mở

| Rủi ro | Cách kiểm chứng |
|---|---|
| Bước 75 mm/biên dạng gờ sai so với tô thật | Đo 10 package, cập nhật STEP và thử chồng không nén |
| PETG creep/nứt chân cánh hoặc tháp khóa | Coupon, proof-load theo tải 147 N/tầng, 72 h và chu kỳ |
| Chốt khóa không rút/gài khi có lực phản lực | Đo lực rút pin, độ ăn khớp, spring return, sensor confirm, power-loss test |
| MG996R hụt lực/nóng | Đo torque–tốc độ và nhiệt trên servo thật; stall torque không phải torque liên tục |
| Tải lệch/tô nghiêng làm dồn lực vào 1–2 cánh | Cảm biến lực tại điểm đỡ và proof-load lệch tâm |

Xem [bảng tải PETG](petg_reinforced_prototype.md), [review production](production_readiness_review.md), [bản kiểm tra FreeCAD](../simulation/validation/pivot_prototype_check.md), và `simulation/validation/acceptance.md`.
