# Gia cường prototype PETG giữ tối đa 5 tô — L1

Trạng thái: **bản prototype hình học đã cập nhật; chưa phát hành sản xuất hoặc chứng nhận tải**. Dùng cho kiểm tra lắp, in thử và thử nghiệm có giám sát. Các số đo của 10 package chưa được điền vào CSV; vì vậy bước lồng 75 mm và hình dạng nón vẫn là giả định.

## Đầu vào và hình học hiện tại

- Theo người dùng: miệng tô Ø175,7 mm, đáy Ø90 mm, thân cao 70 mm; nắp nhô cao khoảng 5 mm, nhô bán kính khoảng 3 mm mỗi bên; khối lượng tô khoảng 0,8 kg.
- Envelope tạm của package: Ø181,7 × 75 mm. Bước hai cơ chế đang để 75 mm cho đến khi đo bước tiếp xúc của package đã đóng nắp.
- Một line, hai tầng giữ, sáu cánh/tầng, bốn cột dẫn với năm guốc định hướng mỗi cột, chứa tối đa năm package.
- Khung carrier PETG dày 8 mm; cánh PETG dày đứng 8 mm, rộng tiếp tuyến 26 mm; mỗi bản lề có bạc đạn 625-2RS (OD16/ID5/W5) trong counterbore Ø16,2 sâu 5 mm; trục bản lề thép không gỉ Ø5 mm; chốt thanh nối Ø4 mm; vòng đồng bộ dày 6 mm; tâm chốt vòng đồng bộ R=103 mm để tạo khe với nắp.
- Bốn trụ kết cấu kim loại Ø12 mm trên PCD276 mm; bốn trụ dẫn kim loại Ø12 mm trên PCD292 mm; khung ngoài Ø320 mm. Trụ dẫn được đưa ra ngoài quỹ đạo quét cánh. Mỗi trụ có năm guốc kẹp PETG tháo rời theo cao độ package, mỗi guốc có tai kẹp và một bu-lông M3; bridge có rãnh chỉnh hướng kính ±3 mm để cân vị trí cột.
- Khóa mỗi tầng: chốt lò xo thép Ø6 mm, bạc lót thép OD8/ID6,2 mm trên tai vòng; tháp đỡ PETG bắt bằng hai bu-lông M5 xuyên carrier, vòng đệm và ê-cu tự hãm. Pin ở trạng thái đóng đi vào bạc lót; muốn mở phải rút pin, xác nhận công tắc rồi mới chạy servo đảo chiều. Khi đóng, pin tự gài và công tắc xác nhận độc lập.

Khóa pin giữ **vị trí góc của vòng**, không thay thế cánh đỡ tải đứng. Tải tô phải đi từ mép tô → cánh → trục/bệ bản lề → carrier → trụ Ø12 mm. Hai tầng phải liên động sao cho tầng còn lại đã đóng và có xác nhận khóa trước khi rút pin/mở tầng đang giữ tải. Mất điện khi một tầng mở chỉ an toàn khi tầng kia đã khóa và nhận tải.

### Sàng lọc lực pin khóa và solenoid

Vòng khóa tại bán kính `R_lock=R_pitch+14=129,9 mm`. Dùng servo screen 30% stall ở 6 V `T_servo=0,324 N·m`, tỷ số 6:1 và `η=0,75`: `T_ring≈1,46 N·m`; phản lực tiếp tuyến pin `F_side=T_ring/R_lock≈11,2 N`. Nếu pin Ø6 mm chịu cắt đơn, `A=πd²/4=28,3 mm²`, ứng suất cắt danh nghĩa khoảng `0,40 MPa`. Tại stall vendor (không phải chế độ làm việc), screen cực đại thành `T_ring≈4,86 N·m`, `F_side≈37,4 N`, `τ≈1,32 MPa`. Chốt không nên hoạt động khi servo còn ép vào hard stop.

Ước lượng lực kéo pin: `F_pull ≥ SF_lock(μ_pin F_side + F_spring + F_drag)`. Với giả định bảo thủ `μ_pin=0,2`, lò xo hồi/drag tổng 4 N và `SF_lock=2`, yêu cầu khoảng 12,5 N ở torque screen hoặc 23,0 N ở vendor stall. Vì vậy đề xuất actuator sơ bộ là solenoid kéo 12 V, hành trình 9 mm, **ít nhất 30 N tại cuối hành trình**; giá trị 30 N cho `SF≈2,6` so với phép sàng lọc stall ở trên. Đây là yêu cầu chọn actuator, không phải thông số của sản phẩm đã chọn. Cần kiểm tra datasheet lực tại hành trình 9 mm và điện áp thấp nhất, thử rút pin khi có side-load, và xác nhận hai sensor riêng cho “pin rút”/“pin gài”. Hỏng actuator thì giữ chốt gài; không cho phép servo quay khi sensor chưa xác nhận rút pin.

## Tải và kiểm tra sơ bộ cánh

`W=mg`, `W_d=K W`, với `K=3` là hệ số thiết kế sơ bộ. Cánh xem như công-xôn chữ nhật; `Z=b h²/6`, `M=F l`, `σ_nom=M/Z`. Dùng `b=26 mm`, `h=8 mm`, `l=18 mm`; chưa gồm tập trung ứng suất, lỗ, lớp in, creep, lệch tâm hoặc va đập.

| Trường hợp | Khối lượng gói trên tầng | Tải thiết kế `W_d` | `F` nếu 3 cánh chia đều | `σ_nom` tại 3 cánh | `σ_nom` nếu 1 cánh nhận toàn tải |
|---|---:|---:|---:|---:|---:|
| Tầng trên bình thường, theo 0,8 kg/gói | 3,2 kg | 94,18 N | 31,39 N | 2,04 MPa | 6,11 MPa |
| Cả chồng 5 gói, theo 0,8 kg/gói | 4,0 kg | 117,72 N | 39,24 N | 2,55 MPa | 7,64 MPa |
| Lỗi thiết kế, 5 gói × 1 kg/gói | 5,0 kg | 147,15 N | 49,05 N | 3,18 MPa | 9,55 MPa |

`Z=277,3 mm³`. Nếu sàng lọc tại chân cánh với `K_t=2` (giả định sơ bộ), trường hợp lỗi 1 cánh cho `σ≈19,1 MPa`. Đây **không phải hệ số an toàn PETG**: `SF=σ_allow/σ_max` chưa xác định vì chưa có coupon đúng loại PETG, máy, hướng in, nhiệt độ và thời gian tải. Dùng tải 1 kg/package làm bound cho prototype; cân package thật và thử tải trước khi chốt.

Tải đứng tổng với 5 × 0,8 kg là `39,24 N`; với bound 1 kg/package là `49,05 N`. Hệ số K=3 đưa tải thiết kế tương ứng lên 117,72 N và 147,15 N. Tính trên không chứng minh carrier, tai bản lề, khóa, bulông, cột hoặc tô đạt bền; không vận hành trên người/vật dễ hỏng.

## Chỉ dẫn in và phần cứng

STL chỉ dành cho nhựa nằm trong `exports/STL/PETG_prototype/`. Không in/không dùng STL cũ ở thư mục `exports/STL/` để chế tạo phần kim loại; ty Ø12, bearing, pin, vít và solenoid cần mua theo BOM.

- Vật liệu in: PETG khô, đúng hồ sơ nhiệt của nhà sản xuất sợi. Bắt đầu coupon ở layer 0,20 mm, tối thiểu 6 perimeter, infill gyroid 50%; quanh tai/chân cánh và tháp khóa dùng vùng đặc/100% modifier. Đây là cấu hình thử, không phải allowable.
- Carrier in phẳng trên bàn. Cánh đặt sao cho chiều dài từ bản lề tới mũi cánh nằm trong mặt phẳng XY, đường chạy perimeter liên tục dọc cánh; in coupon uốn cùng hướng trước. Không đặt seam tại chân cánh/lỗ pin.
- Tháp khóa in nằm cạnh để lỗ bulông không bị xé theo lớp; ream lỗ sau in. Có vòng đệm rộng ở cả hai mặt, ê-cu tự hãm; siết vừa đủ, không ép lún PETG. Không taro ren chịu lực trực tiếp vào PETG.
- Trụ kết cấu/dẫn Ø12, 12 bạc đạn bản lề 625-2RS, pin bản lề Ø5, chốt link Ø4, chốt khóa Ø6, bạc khóa OD8/ID6,2 và 20 bu-lông M3 kẹp guốc đều là kim loại. Pin bản lề phải được giữ dọc trục bằng đầu chặn/circlip; thử lắp bearing trên coupon carrier trước khi in cả carrier.
- Không dùng chi tiết PETG làm bề mặt trượt tải cao nếu có thể thay bằng bạc/roller hoặc đệm UHMW-PE. Bước lồng, lực ma sát và ma sát gờ phải đo trên package thật.

## Điều kiện trước khi dùng trong máy

1. Điền đủ 10 mẫu L1 vào `requirements/packaged_bowl_measurements.csv`; cập nhật bước tầng, profile gờ và khe guốc từ min/max đo.
2. Kiểm riêng chốt khóa: lực/mô-men phản lực vòng, độ sâu ăn pin, lực lò xo, lực rút actuator, trạng thái limit switch, chặn cơ và mất điện.
3. In coupon kéo/uốn; thử từng cánh, bản lề, carrier và chốt với proof-load tối thiểu `147 N` mỗi tầng theo đường tải đã phân tích. Đo biến dạng; thử creep 72 giờ, tải lệch và tối thiểu 100 chu kỳ một tầng.
4. Thử mất điện tại mọi bước FIFO. Trước khi nhả tầng, xác nhận tầng đối diện chịu tải và khóa cơ đã gài. Bất kỳ cảm biến/motor timeout nào phải dừng chuyển động.
5. Chỉ cập nhật allowables/hệ số an toàn khi có dữ liệu thử; làm review độc lập trước khi phát hành sản xuất.
