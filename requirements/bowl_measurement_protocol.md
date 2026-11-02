# Quy trình đo 10 gói tô để chốt cơ cấu giữ

Máy nhận gói đã đóng nắp. Vì vậy **kích thước dùng để thiết kế dẫn hướng và khoảng cách tầng là kích thước gói hoàn chỉnh**, không phải chiều cao tô trần. Đo riêng L1 và L2 bằng phiếu `packaged_bowl_measurements.csv`. Mục đo tô trần ở dưới chỉ dùng khi cần thiết kế điểm đỡ trực tiếp vào vành tô và có xác nhận nắp/bao bì không nằm trong đường tải.

## Dụng cụ

- Thước cặp điện tử 0,01 mm (hoặc tốt nhất có thể); kiểm tra về 0 trước khi đo.
- Cân điện tử độ chia 1 g; thước cao hoặc thước cặp có thanh đo sâu.
- Thước thẳng cứng, giấy kẻ ô hoặc giấy can, bút đánh dấu, điện thoại chụp ảnh.
- Nếu có: dưỡng đo biên dạng (profile gauge). Không cắt tô để đo.

Đánh số tô 01–10. Lau sạch, đo khi khô và ở cùng nhiệt độ phòng. Không bóp méo miệng tô bằng lực thước cặp; chỉ chạm nhẹ hai mỏ đo.

## A. Đo từng tô

Với mỗi tô ghi vào `bowl_measurements.csv`:

1. **Khối lượng:** cân riêng tô khô, ghi g.
2. **Đường kính vành ngoài `D_outer`:** đo ngang miệng theo 0°–180°, 45°–225°, 90°–270°, 135°–315°. Ghi cả bốn số. `D_max` và `D_min` là cực trị; chênh lệch là ovality.
3. **Đường kính vành trong `D_inner`:** đo tương tự nếu thước cặp chạm được mặt trong mà không làm biến dạng vành.
4. **Chiều cao tổng:** đặt tô ngửa trên mặt phẳng cứng; đo từ mặt phẳng đỡ đến mặt trên vành ở bốn vị trí. Ghi min/max.
5. **Tiết diện gờ:** chọn bốn góc quanh miệng. Ở mỗi góc, ghi chiều dày đứng từ mặt trên vành đến mặt dưới gờ; bề rộng phẳng ở mặt dưới; vị trí bo/vát trong và ngoài. Dùng profile gauge để lấy đường bao mặt cắt, hoặc chụp chính diện sát mặt cắt với thước mm trong cùng mặt phẳng. Lưu ảnh tên `bowl_01_rim_0deg.jpg`…
6. Ghi vết nứt, ba via, méo hoặc chỗ gờ không liên tục.

Mặt dưới cần xác định chính xác là mặt cánh sẽ đỡ. Đánh dấu vùng tiếp xúc dự kiến lên bản vẽ mặt cắt; không lấy tổng chiều dày vành thay cho chiều cao/bề rộng gờ đỡ.

## B. Đo bước lồng `nested_rim_pitch`

1. Với bước lồng tô trần, dùng 10 tô khô cùng chiều. Với máy nhận package đã đóng nắp, thực hiện phép xếp chồng chính trên 10 package mỗi line như mục D. Đặt từng món xuống bằng trọng lượng bản thân; **không ấn/nén** để ép khít.
2. Xoay nhẹ mỗi tô trong lúc lồng để tìm vị trí tựa ổn định tự nhiên. Nếu tô bị kẹt hoặc cần lực để xuống, ghi “kẹt”, không ép tiếp.
3. Đo cao độ của cùng một mốc trên vành tô số 1 và số 10 so với mặt bàn. Dùng thước cao/thước thẳng + đo sâu; đo tại bốn hướng quanh vành để phát hiện nghiêng.
4. Tính bước trung bình `p_avg=(z_10-z_1)/9`. Ghi riêng chênh cao giữa từng cặp liên tiếp `p_i=z_(i+1)-z_i` nếu đo được. Lặp lại cả phép xếp chồng 3 lần, tháo ra xếp lại từ đầu.
5. Ghi `p_min`, `p_max`, `p_avg` của từng lần. Thiết kế khoảng cách tầng từ khoảng đo và sai số, không dùng riêng trung bình nếu có biến thiên lớn.

## C. Kiểm tra độ nghiêng và lồng tự do

- Xếp lần lượt 2, 5, rồi 10 package. Đo độ cao chồng ở bốn hướng và ghi chênh lệch lớn nhất.
- Kiểm tra tô trên cùng có thể xoay nhẹ và nhấc lên bằng tay mà không mắc; không dùng lực ép xuống.
- Chụp ảnh chồng 10 tô từ cạnh, có thước đứng cạnh và số tô nhìn rõ.

## D. Đo package đã đóng nắp theo từng line

1. Chọn 10 package L1 và 10 package L2 đúng quy cách sẽ nạp máy. Không tháo nắp, seal hoặc màng co.
2. Cân từng package; đo kích thước bao lớn nhất (qua gân, mép seal và nắp) theo hai hướng vuông góc. Đo tại vùng đáy, thân giữa, vành/nắp và mọi chỗ nhô.
3. Đo chiều cao package từ mặt đáy chịu kê đến điểm cao nhất của nắp. Ghi riêng `lid_protrusion` so với miệng tô nếu có thể đo được mà không mở seal.
4. Xếp 10 package đúng chiều nạp, chỉ dùng trọng lượng bản thân. Nếu package không được thiết kế để chồng trực tiếp lên nắp gói dưới, ghi lại bề mặt đang đỡ (nắp, vai tô, đáy package) và không giả định chồng an toàn.
5. Đo khe tiếp xúc từng package trong chồng và tổng chiều cao; lặp lại ba lần. Giá trị pitch dùng trong cơ cấu là khoảng cách giữa các mặt package thực sự tiếp xúc khi xếp, không phải chiều cao tổng của một package.
6. Ghi biến dạng nắp/seal, trượt ngang, nghiêng hoặc móp. Không thử tải vượt cách xếp do nhà cung cấp package cho phép.

## E. Cách chuyển kết quả vào CAD

- Dùng `D_outer_max` để kiểm tra va chạm và cửa mở; dùng `D_outer_min` cùng `D_inner_min` để tính phần gờ cánh có thể đỡ.
- Dùng tiết diện gờ nhỏ nhất trong 10 tô làm trường hợp xấu cho độ chồng mép cánh và khoảng hở.
- Dùng `p_min/p_max` để chốt khoảng cách tầng và hành trình chuyển tải. Thêm dung sai đo và biến thiên tô; không đặt hai tầng bằng `p_avg` một cách máy móc.
- Dùng khối lượng lớn nhất đo được để thay 1 kg/tô nếu lớn hơn; giữ thêm tải thiết kế lỗi theo yêu cầu an toàn.
- Cập nhật `requirements/parameters.json` và ảnh đo; chạy lại tính lực, CAD và kiểm giao thoa. Giữ nguyên dữ liệu gốc trong CSV.

## Phiếu ghi

Ghi dữ liệu package vào `requirements/packaged_bowl_measurements.csv`; dữ liệu tô trần (nếu đo) vào `requirements/bowl_measurements.csv`. Điền ngày, người đo, model thước/cân và sai số dụng cụ trước khi bắt đầu.
