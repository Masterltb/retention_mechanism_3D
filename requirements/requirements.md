# Yêu cầu hệ nhả tô FIFO

## Đầu vào đã biết

Máy có **2 line bán 2 loại tô khác nhau**. Mỗi line được nạp các tô đã đóng gói hoàn chỉnh bên ngoài, gồm cả nắp; máy không đóng nắp. Mỗi line cần một module FIFO riêng gồm hai cơ chế giữ đồng trục. CAD hiện là module một line để tái sử dụng; chưa bố trí khoảng cách giữa hai line vì kích thước gói L2 còn thiếu.

Line L1: thân tô cao **70 mm không gồm phần nắp nhô**, đường kính miệng danh nghĩa **175,7 mm**, đáy **90 mm**. Mỗi line tối đa **5 gói**. Người dùng ước tính mỗi tô khoảng **0,8 kg**; khối lượng package gồm nắp/seal chưa cân. Tạm giữ **1,0 kg/gói** làm giới hạn thiết kế screening cho tới khi cân package đầy đủ. Cần đo đường bao **gói hoàn chỉnh có nắp**, bước chồng gói, khối lượng gói và bề mặt chịu lực. Không dùng chiều cao tô trần hoặc bước lồng tô trần để đặt tầng. L2 có hình dạng/kích thước khác và chưa đo. Ảnh là tham khảo hình dáng, không cho phép suy ra dung sai.

Mỗi line có 2 cơ chế giữ: trên giữ các gói còn lại, dưới nhả gói cuối. Mỗi module hiện dự kiến dùng hai servo, tổng cộng bốn servo cho hai line. Bốn cột dẫn của module phải đặt theo đường bao gói lớn nhất và có chỉnh tâm/khe hở.

## Yêu cầu truy vết

| ID | Yêu cầu | Kiểm chứng |
|---|---|---|
| R-01 | Nhả đúng 1 tô ở đáy theo FIFO | 50 chu kỳ với tô thật, quay video |
| R-02 | Tầng trên giữ 4 tô khi tầng dưới mở | Thử tải tĩnh và lệch tâm |
| R-03 | Tầng dưới chỉ mở khi tầng trên đã đóng và khóa | Công tắc xác nhận + thử ngắt điện |
| R-04 | Hai tầng không đồng thời mở | Liên động điện và cơ, thử lỗi cảm biến |
| R-05 | Tự giữ khi mất điện, không tải ngược lên trục servo | Pin khóa lò xo vào tai vòng đồng bộ có bạc kim loại; xác nhận pin, thử mất điện có tải |
| R-06 | Đường kính thông thủy mục tiêu khi đóng ≈160 mm; khi mở ≥200 mm | Đo trên mẫu in |
| R-07 | Dẫn hướng tô không kẹt; khe guốc chỉnh theo package đo, không ép biến dạng | Đo 10 package và kiểm tra ở hai đầu chỉnh |
| R-08 | 4 thanh dẫn giữ cột tô không kẹt | Thử rơi 4 tô, có lệch tâm có kiểm soát |
| R-09 | Lắp được MG996R và vít/trụ đồng M3 | Đo servo, vít, trụ thật trước khi in |
| R-10 | Tính khoảng trống giữa guốc, tải cánh, lực lật và ma sát theo từng trạng thái | Chạy `tools/calculate_mechanics.py`, kiểm tra bằng lực kế/coupon |
| R-11 | Phân biệt torque stall và torque vận hành của MG996R 360° | Đo torque–tốc độ thực ở 6 V; không thiết kế theo stall |
| R-12 | Chứng minh ray/chốt chống lật chịu tải và guốc không creep | Thử tải lệch tâm, 72 giờ và cắt điện |

## Dữ liệu còn phải đo trên vật thật

1. Với mỗi line, đo 10 **gói hoàn chỉnh có nắp**: đường kính/kích thước lớn nhất tại nhiều cao độ, chiều cao tổng, khối lượng và độ méo. Xếp 10 gói không nén; đo bước tiếp xúc thực và độ nghiêng. Khoảng cách 2 tầng phải dựa trên gói, **không dùng mặc định 30 mm để chế tạo**.
2. Với L1/L2, ghi riêng biên dạng vùng chịu lực của package. Chỉ dùng mặt dưới vành tô làm mặt đỡ nếu gói/nắp không che vùng đó và phép thử tải chứng minh vùng này chịu được lực.
3. Kích thước MG996R đang sở hữu: thân, tai, lỗ bắt vít, trục, khoảng xoay và dạng 360° thật (quay liên tục hay có phản hồi góc).
4. Kích thước trụ đồng: ren M3, chiều dài, phần lục giác, cách khóa ren. Lỗ in được hiệu chuẩn bằng mẫu coupon.
5. Kích thước bao của hai line, khoảng cách giữa line, bề rộng buồng máy và khoảng không bên dưới để gói rơi; số 80/60 trong ảnh chưa đủ thông tin.
6. Hệ số ma sát tĩnh/động đúng vật liệu và bề mặt in; lực kéo của guốc ở các tải khác nhau. Đến khi đo, `μ=0,1…0,4` chỉ là dải khảo sát.

## Điều kiện chưa được nghiệm thu

Prototype một line trong `cad/assembly/` hiện có cánh bản lề, bánh răng 72:12, pin khóa lò xo Ø6 mm, bạc lót và chặn cơ PETG. Biên dạng răng là xấp xỉ; actuator rút pin, công tắc, liên động, vật liệu in và chịu tải chưa được kiểm chứng. Bước hai tầng 75 mm và profile gói vẫn là giả định. Không chạy máy bán hàng hoặc đặt người dưới tải trước khi qua checklist trong `simulation/validation/acceptance.md`.
