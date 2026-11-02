# Yêu cầu hệ nhả tô FIFO

## Đầu vào đã biết

Tô: đường kính miệng **175,7 mm**, đáy **90 mm**, cao **70 mm**. **Mỗi cột tô có 2 cơ chế giữ xếp chồng đồng trục**: cơ chế trên giữ các tô còn lại, cơ chế dưới nhả từng tô. Một cột tối đa 5 tô, giả thiết tải lớn nhất **1 kg/tô**. Hai cơ chế của cùng một cột nối bằng 4 trụ chịu lực. Mỗi cơ chế dùng một MG996R 360°, tức **2 servo/cột**. Bốn thanh dẫn phía trên bắt bằng vít/trụ đồng. Mô hình CAD hiện có **1 cột**; nếu máy có nhiều cột thì mỗi cột lặp lại cụm hai cơ chế này. Ảnh tham chiếu là ý tưởng hình học, không phải bản vẽ có kích thước kiểm chứng. Hình cuối có số 80/60 nhưng không rõ đơn vị và vị trí liên quan, nên không dùng làm kích thước cơ cấu.

## Yêu cầu truy vết

| ID | Yêu cầu | Kiểm chứng |
|---|---|---|
| R-01 | Nhả đúng 1 tô ở đáy theo FIFO | 50 chu kỳ với tô thật, quay video |
| R-02 | Tầng trên giữ 4 tô khi tầng dưới mở | Thử tải tĩnh và lệch tâm |
| R-03 | Tầng dưới chỉ mở khi tầng trên đã đóng và khóa | Công tắc xác nhận + thử ngắt điện |
| R-04 | Hai tầng không đồng thời mở | Liên động điện và cơ, thử lỗi cảm biến |
| R-05 | Tự giữ khi mất điện, không tải ngược lên trục servo | Chốt lò xo vào vành cam, thử mất điện có tải |
| R-06 | Đường kính thông thủy mục tiêu khi đóng ≈160 mm; khi mở ≥200 mm | Đo trên mẫu in |
| R-07 | Kẹp hờ mục tiêu 0,1 mm chỉ sau hiệu chuẩn | Đo dung sai thực của tô và mẫu in |
| R-08 | 4 thanh dẫn giữ cột tô không kẹt | Thử rơi 4 tô, có lệch tâm có kiểm soát |
| R-09 | Lắp được MG996R và vít/trụ đồng M3 | Đo servo, vít, trụ thật trước khi in |
| R-10 | Tính khoảng trống giữa guốc, tải cánh, lực lật và ma sát theo từng trạng thái | Chạy `tools/calculate_mechanics.py`, kiểm tra bằng lực kế/coupon |
| R-11 | Phân biệt torque stall và torque vận hành của MG996R 360° | Đo torque–tốc độ thực ở 6 V; không thiết kế theo stall |
| R-12 | Chứng minh ray/chốt chống lật chịu tải và guốc không creep | Thử tải lệch tâm, 72 giờ và cắt điện |

## Dữ liệu còn phải đo trên vật thật

1. Bước lồng tô: khoảng cách hai mép miệng liên tiếp trong cột 5 tô. Thay `nested_rim_pitch: null` trong JSON; khoảng cách 2 tầng phải chỉnh theo giá trị này, **không được dùng mặc định 30 mm để chế tạo**.
2. Mặt cắt gờ miệng, độ dày, bán kính góc dưới gờ và độ biến thiên đường kính của ít nhất 10 tô. Xác định mặt thực sự đặt lên 6 gờ đỡ.
3. Kích thước MG996R đang sở hữu: thân, tai, lỗ bắt vít, trục, khoảng xoay và dạng 360° thật (quay liên tục hay có phản hồi góc).
4. Kích thước trụ đồng: ren M3, chiều dài, phần lục giác, cách khóa ren. Lỗ in được hiệu chuẩn bằng mẫu coupon.
5. Kích thước buồng máy và khoảng không phía dưới để tô rơi; số 80/60 trong ảnh chưa đủ thông tin.
6. Hệ số ma sát tĩnh/động đúng vật liệu và bề mặt in; lực kéo của guốc ở các tải khác nhau. Đến khi đo, `μ=0,1…0,4` chỉ là dải khảo sát.

## Điều kiện chưa được nghiệm thu

Mẫu CAD là bố trí không gian và nguyên lý tải. Chưa có biên dạng cam, bánh răng, hình học khóa và liên động đã được kiểm chứng để vận hành 5 kg. Không chạy máy bán hàng với thực phẩm hoặc với người đứng dưới cơ cấu trước khi qua checklist trong `simulation/validation/acceptance.md`.
