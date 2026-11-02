# Ước lượng tô và bố trí 4 cột dẫn

## Kích thước đầu vào người dùng

- Đường kính miệng ngoài danh nghĩa: 175,7 mm.
- Đường kính đáy: 90 mm.
- Chiều cao: 70 mm.
- Ảnh cho thấy tô nhựa trong, thành gân dọc, thân loe từ đáy lên vành; miệng có vành ngang nhô ra. Không thể lấy dung sai, bước lồng, hoặc mặt cắt gờ chính xác từ ảnh phối cảnh.
- Theo ước lượng mới của người dùng, nắp nhô cao khoảng 5 mm và nhô bán kính khoảng 3 mm mỗi bên. Bao gói sơ bộ: Ø181,7 mm × cao 75 mm. Đây là envelope ước lượng, chưa đo bằng thước.

## Bố trí cột và guốc dẫn prototype hiện tại

CAD gia cường hiện dùng 4 cột dẫn kim loại Ø12 mm trên PCD292 mm; khung ngoài Ø320 mm để đưa cột khỏi quỹ đạo cánh mở. Mỗi cột mang năm tay đỡ hướng kính và guốc đặt theo thân côn ước lượng tại cao độ 34 mm tính từ đáy mỗi tô. Bán kính thân tại cao độ đó là:

`r(34)=45+(87,85-45)*34/70=65,8 mm`.

Mặt guốc danh nghĩa cách bao hình thân 3,5 mm; dịch cột vào trong 3 mm còn 0,5 mm. Cấu hình giữ chừa khe, chưa ép cứng tô. Biên dạng guốc hiện theo nón cụt lý tưởng, nên có thể không khớp gân, chân, hoặc chỗ phình thật. CSV 10 package còn trống; các giá trị PCD và cao độ guốc chưa được chốt sản xuất.

Khi có 10 package, đo biên dạng/thân theo từng cao độ và đặt khoảng hở nhỏ nhất từ sai số lớn nhất:

`PCD_final=D_package,max+D_post,actual+2*c_target`.

`PCD_final` trên đây chỉ áp dụng cho một vòng/cữ dẫn tròn ở vành; guốc nhiều cao độ phải tính riêng theo đường kính thân ở từng cao độ. Rãnh cầu hiện cho ±3 mm chỉnh cột, nhưng dạng khóa và độ cứng cột chưa được tính bền. Nếu muốn tiếp xúc êm khi tô nghiêng, thay guốc cứng bằng roller/đệm UHMW-PE có lò xo nhẹ sau khi đo lực.

## Ước lượng thân côn

Chỉ để bố trí ban đầu, xấp xỉ thân tô trần là nón cụt thẳng giữa đáy Ø90 và miệng Ø175,7 trong chiều cao 70 mm:

`D(z)=90+(175,7-90)z/70`, với `z` tính từ đáy.

Ví dụ tại z=34 mm, `D≈131,6 mm`. Guốc được đặt theo thân tô tại cao độ này. Gân, vai, đáy chân và bước xếp package làm bao hình thật khác nón cụt; không dùng công thức này làm kích thước chốt chế tạo.

## Thông số lấy từ bản đo để chốt

1. `D_package,max/min` và ovality của 10 package đã đóng nắp mỗi line.
2. Chiều dày/bề rộng gờ dưới và bán kính bo; vị trí mặt cánh thực sự tựa.
3. Bước lồng min/avg/max khi xếp 10 tô tự do.
4. Đường kính thân tại các cao độ lắp dẫn hướng và vị trí đoạn gân/nhô lớn nhất.
5. Khoảng cách chỉnh thực tế và chỗ bắt chắc bốn cầu/rãnh vào khung.

## Khoảng cách hai cơ chế

Giả sử package dưới có mặt nắp cao 5 mm trên miệng, thân tô cao 70 mm, và đáy package phía trên chạm trực tiếp đỉnh nắp package dưới (không có hõm/chân làm lệch mặt chạm):

`P_stack = H_body + h_lid = 70 + 5 = 75 mm`.

Hai cơ chế giữ cùng một vị trí tương đối trên hai package kế tiếp, nên khoảng cách giữa hai mặt làm việc của cánh bằng bước package: `S_gate=P_stack=75 mm`. Cánh được đặt ở cùng cao độ tương đối quanh từng tô; envelope CAD kiểm tra đáy package trên chạm nắp package dưới. Nếu đáy tô có chân/hõm, nắp cong hoặc package còn khe hở, phải thay bằng pitch đo trên chồng package; không cộng riêng chiều cao package hai lần.

Ghi số liệu gốc ở `requirements/packaged_bowl_measurements.csv`. Ảnh hiện tại chỉ định hướng hình dạng; kích thước đã nhập từ lời người dùng là danh nghĩa, chưa phải giá trị min/max. Chiều cao/package pitch 75 mm vẫn là estimate cho tới stack test.
