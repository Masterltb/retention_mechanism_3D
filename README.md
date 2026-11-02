# Mechanical dispenser — bộ giữ/nhả tô FIFO

Thiết kế concept FreeCAD cho **1 cột tô Ø175,7 mm với 2 cơ chế giữ xếp chồng**: tầng trên và tầng dưới. Mỗi cơ chế có 6 guốc đỡ và 1 servo MG996R 360°, tổng cộng 2 servo/cột. Hai cơ chế của cùng một cột nối bởi 4 trụ kết cấu; 4 thanh dẫn phía trên bắt bằng trụ/vít đồng M3. Đường chịu lực dự kiến: gờ tô → guốc → khung → trụ. Khóa lò xo giữ vành cam lúc mất điện. **CAD hiện là bố trí không gian; cam, truyền động và khóa còn là placeholder, chưa phải bộ in có thể vận hành dưới tải 5 tô.**

## Mở và sinh CAD

1. Đo tô và sửa `requirements/parameters.json`, đặc biệt `nested_rim_pitch` và `gate_center_spacing`.
2. Chạy `freecadcmd.exe cad/scripts/build_freecad.py` (hoặc mở script trong FreeCAD Python console).
3. Mở `cad/assembly/layout.FCStd`; STEP tại `exports/STEP/`, STL concept tại `exports/STL/`, bản vẽ tổng quan tại `exports/drawings/overview_concept.svg`. Chỉ in coupon và mẫu thử không tải trước khi hoàn tất P2/P3.

## Bản đồ thư mục

| Thư mục | Nội dung |
|---|---|
| `requirements/` | R-01…R-09, tham số JSON |
| `design/` | concept, tính tải và quyết định còn mở |
| `cad/scripts/` | script sinh FreeCAD |
| `cad/parts/`, `cad/assembly/` | bản vẽ chi tiết tương lai, assembly concept |
| `simulation/` | trạng thái FIFO, mô hình chuyển động, nghiệm thu |
| `exports/` | STEP, STL, drawings, renders |
| `BOM/` | BOM và lịch sử SQLite |
| `docs/HARNESS.md` | quy trình phase/story/bug/event |

Điểm nghẽn quan trọng nhất là đo bước lồng và gờ miệng tô, sau đó thiết kế cam/chốt có thử tải. Đọc `design/concept_review.md` và `simulation/validation/acceptance.md` trước khi lắp thực tế.

Tính toán tải–ma sát và MG996R: `design/friction_analysis.md`; kế hoạch tính/vẽ/thử theo phase: `docs/MECHANICAL_PLAN.md`. Chạy `py tools/calculate_mechanics.py` mỗi khi đổi tham số để cập nhật CSV độ nhạy.

Quy trình engineering production, kiểm gate, commit/tag/backup: `docs/ENGINEERING_HARNESS.md`. Chạy `py tools/engineering.py check` và `py tools/engineering.py snapshot`; SQL backup có thể khôi phục nằm ở `BOM/history_dump.sql`.
