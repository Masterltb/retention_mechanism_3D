# Đánh giá concept v0.1

## Cấu hình

Một cột tô đi qua hai cơ chế giữ đồng trục. Mỗi cơ chế gồm vòng khung cố định, 6 guốc trượt hướng tâm có gờ đỡ dưới miệng tô, và vành cam xoay. Bốn trụ đường kính 8 mm liên kết hai cơ chế của cùng một cột để truyền tải; 4 thanh dẫn đường kính 10 mm ở phía trên định tâm cột tô. Mỗi cơ chế có một servo gắn ở hông vào khung, điều khiển vành cam qua truyền động cần thiết kế chi tiết. Chốt lò xo khóa vành cam khi đóng; vấu chặn cơ giới hạn hành trình. Tải đứng đi qua guốc → khung → 4 trụ, không đi qua servo.

CAD `cad/scripts/build_freecad.py` dựng bố trí 3D có kích thước thật cho vòng, guốc, trụ, thanh dẫn, bệ servo và khối bao servo. Lỗ trụ Ø8,4, lỗ pilot M3 Ø3,4 và lỗ bệ servo Ø3,2 là kích thước khởi điểm để in coupon, chưa phải dung sai đã kiểm chứng. **Vành cam, rãnh cam, liên kết truyền động servo và chốt lò xo mới là envelope/placeholder**, chưa phải chi tiết sản xuất. Chúng được hiển thị để kiểm tra không gian, không xuất STL sản xuất.

## Chu kỳ dự kiến

1. Ban đầu: trên đóng + xác nhận khóa, dưới đóng + xác nhận khóa.
2. Trên giữ 4 tô. Dưới mở, nhả 1 tô; cảm biến xác nhận tô đã qua vùng nhả.
3. Dưới đóng và khóa, cảm biến xác nhận; chỉ khi đó trên mở.
4. Bốn tô hạ xuống một bước lồng tô; tầng dưới đỡ tô kế tiếp, thanh dẫn giới hạn lệch tâm.
5. Trên đóng để giữ 3 tô còn lại và khóa; sẵn sàng chu kỳ sau.

Nếu cơ chế trên nhả cả 4 tô từ độ cao không kiểm soát, va đập sẽ lớn. Bước lồng thực phải khớp khoảng cách giữa tầng; cần cảm biến tới vị trí, giới hạn hành trình và thử vận tốc rơi. Khi mất điện ở lúc chuyển trạng thái, khóa phải về trạng thái chịu tải hoặc hệ phải có phương án thu hồi an toàn.

## Điểm quyết định trước bản vẽ sản xuất

| Vấn đề | Cách đóng quyết định |
|---|---|
| Biên dạng gờ miệng | Đo 10 tô, chọn guốc có mặt tỳ đủ rộng và không nghiền mép |
| Vành cam và truyền động | Tính lực/rãnh, góc quay, răng hoặc dây đai, in và thử một tầng |
| Chốt khóa | Thiết kế chốt kim loại/lò xo, kiểm chứng khi mất điện ở mọi góc |
| Tải động | Thử thả 4 tô nặng giả, đo lực/biến dạng |
| Vật liệu | Coupon PETG hoặc PA-CF; kiểm tra creep 72 giờ và điều kiện nhiệt |

Liên kết: yêu cầu `R-01…R-09` ở `requirements/requirements.md`; phép tính ở `design/calculations.md`; trạng thái ở `simulation/motion_states.csv`; công việc ở SQLite `BOM/history.sqlite`.
Phần tính ma sát/tải và các giới hạn của 6 guốc hiện có ở `design/friction_analysis.md`; sơ đồ lực tại `exports/drawings/force_path_concept.svg`. Yêu cầu mới `R-10…R-12` ở cùng file requirements.
