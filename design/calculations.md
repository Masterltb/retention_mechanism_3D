# Tính nhanh để định cỡ thử nghiệm

Bản tính chi tiết mới: [friction_analysis.md](friction_analysis.md); dữ liệu sinh tự động: `simulation/kinematics/force_friction_sensitivity.csv`.

Với g = 9,81 m/s², tầng trên chịu 4 × 1 × 9,81 = **39,24 N**, tầng dưới **9,81 N**. Ở hệ số tải tĩnh 3: tầng trên **117,72 N**, tầng dưới **29,43 N**. Nếu chỉ 3/6 gờ tầng trên cùng tiếp xúc khi lệch tâm, mỗi gờ cần chịu ít nhất **39,24 N** ở tải tính toán. Đây chưa tính va đập lúc 4 tô rơi, nên tải động phải đo và thử riêng.

Miệng tô bán kính 87,85 mm. Lỗ đóng 160 mm có bán kính 80 mm, cho độ chồng hình học tối đa **7,85 mm** tại vành ngoài. Đó **không phải** chiều dài tiếp xúc thật: phải đo mặt dưới gờ. Mở 200 mm cho khe hở đường kính so với 175,7 mm là **24,3 mm**, tức 12,15 mm mỗi phía nếu đồng tâm.

Bốn thanh dẫn đường kính 10 mm trên vòng tâm đường kính 188,7 mm cho khe hở danh nghĩa với miệng tô: (188,7 − 10 − 175,7)/2 = **1,5 mm**. Thử cột tô lệch tâm và độ đảo thực trước khi chốt kích thước.

0,1 mm là mục tiêu sau chỉnh cơ khí, nhỏ hơn nhiều biến thiên FDM thường gặp. Thiết kế dùng vít chặn điều chỉnh và lá đệm; in thử coupon, đo và đặt chặn theo đường kính tô lớn nhất. Không dựa vào 0,1 mm danh nghĩa trong STL.

MG996R quay liên tục nhận lệnh tốc độ/chiều, không nhận vị trí góc trực tiếp. Mỗi tầng cần hai tín hiệu vị trí độc lập (mở, đóng/khóa) và timeout. Chốt lò xo chịu lực vào rãnh chặn trên vành cam; servo chỉ làm việc lúc chuyển trạng thái. Phải thử khả năng tự mở chốt bằng cam khi có tải và tình huống mất điện giữa hành trình.
