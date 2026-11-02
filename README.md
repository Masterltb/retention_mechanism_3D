# Mechanical dispenser — bộ giữ/nhả tô FIFO

Thiết kế là concept cho máy bán **2 line sản phẩm**, mỗi line dùng một loại tô/package có nắp khác nhau. CAD hiện dựng một module line để tái sử dụng; mỗi module có 2 cơ chế giữ xếp chồng (trên/dưới), 6 guốc concept mỗi tầng và 2 servo. Máy dự kiến có tổng 4 cơ chế và 4 servo. Line L1 có tô trần miệng Ø175,7 mm, đáy Ø90 mm, thân cao 70 mm; số đo chưa gồm phần nắp nhô. Kích thước package hoàn chỉnh và L2 còn phải đo. **CAD chưa phải thiết kế sản xuất; cơ cấu cánh, đồng bộ, khóa và liên động chưa được kiểm chứng dưới tải.**

## Mở và sinh CAD

1. Đo tô và sửa `requirements/parameters.json`, đặc biệt `nested_rim_pitch` và `gate_center_spacing`.
2. Chạy `freecadcmd.exe cad/scripts/build_freecad.py` (hoặc mở script trong FreeCAD Python console).
3. Mở `cad/assembly/layout.FCStd`; STEP tại `exports/STEP/`, STL concept tại `exports/STL/PETG_prototype/` (chỉ chi tiết in PETG; phần cứng kim loại mua riêng), bản vẽ tổng quan tại `exports/drawings/overview_concept.svg`. Chỉ in coupon và mẫu thử không tải trước khi hoàn tất P2/P3.

## Bản đồ thư mục

| Thư mục | Nội dung |
|---|---|
| `requirements/` | R-01…R-12, tham số JSON và phiếu đo package L1/L2 |
| `design/` | concept, tính tải và quyết định còn mở |
| `cad/scripts/` | script sinh FreeCAD |
| `cad/parts/`, `cad/assembly/` | bản vẽ chi tiết tương lai, assembly concept |
| `simulation/` | trạng thái FIFO, mô hình chuyển động, nghiệm thu |
| `exports/` | STEP, STL, drawings, renders |
| `BOM/` | BOM và lịch sử SQLite |
| `docs/HARNESS.md` | quy trình phase/story/bug/event |

Điểm nghẽn còn lại là đo bước lồng/gờ trên 10 package và thử tải prototype cánh bản lề PETG, pin khóa, chặn cơ. Cơ cấu dùng servo PWM đảo chiều và bánh răng đồng bộ, không dùng cam. Đọc `design/petg_reinforced_prototype.md`, `design/production_readiness_review.md` và `simulation/validation/acceptance.md` trước khi lắp thực tế.

Tính toán tải–ma sát và MG996R: `design/friction_analysis.md`; kế hoạch tính/vẽ/thử theo phase: `docs/MECHANICAL_PLAN.md`. Chạy `py tools/calculate_mechanics.py` mỗi khi đổi tham số để cập nhật CSV độ nhạy.

Quy trình engineering production, kiểm gate, commit/tag/backup: `docs/ENGINEERING_HARNESS.md`. Chạy `py tools/engineering.py check` và `py tools/engineering.py snapshot`; SQL backup có thể khôi phục nằm ở `BOM/history_dump.sql`.
