# Kiểm tra hình học concept bạc đạn dẫn hướng

Ngày kiểm tra: 2026-11-02. Phần mềm: FreeCAD 1.1.4.

## Cấu hình

- Bạc đạn concept: 625-2RS, 5 × 16 × 5 mm.
- Lỗ trục trên tai guốc: Ø5,2 mm.
- Mỗi guốc có hai tai đỡ, khoảng hở giữa tai theo hướng trục bằng bề rộng bạc đạn.
- Mỗi bạc đạn lăn trên một ray hướng tâm dài 52 mm; ray và bạc đạn là envelope concept.
- Hai tầng, mỗi tầng sáu cụm guốc/bạc đạn/ray.

## Kết quả CAD

Chạy `C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe cad/scripts/build_freecad.py` để sinh lại assembly. Mở `cad/assembly/layout.FCStd`, kiểm tra 12 cụm: mọi guốc, bạc đạn và ray đều có shape hợp lệ và đúng một solid. Tai đỡ được làm rộng theo hướng kính để lỗ Ø5,2 mm không cắt ngang toàn bộ tai.

Hình học chỉ xác nhận tính hợp lệ và sự liên kết của solids trong trạng thái đóng. Ray và bạc đạn tiếp xúc danh nghĩa (không có khe chạy in bù); độ hở thực, lắp vít/trục, độ bền tai, tải, chuyển động toàn hành trình và tương thích với bạc đạn thật chưa được xác nhận. Không dùng STL này để vận hành hoặc chịu tải trước khi đo vòng bi thực, kiểm tra clearance, in coupon và thử tải.
