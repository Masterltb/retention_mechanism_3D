# Harness dự án

Quy trình production, gate phase và Git backup: [ENGINEERING_HARNESS.md](ENGINEERING_HARNESS.md).

Nguồn sự thật về trạng thái là `BOM/history.sqlite`; `schema.sql` và `seed.sql` cho phép tạo lại bộ khung. Một story tham chiếu ID yêu cầu, phase và artifact; bug tham chiếu story; mỗi lần implement/test/decision ghi một event ngắn cùng đường dẫn bằng chứng. Không chép nguyên tài liệu vào event.

Chạy trong `mechanical-dispenser/`:

```powershell
py tools/harness.py init
py tools/harness.py status
py tools/harness.py set S-002 doing
py tools/harness.py event S-002 implement "Dựng vòng và 6 guốc mỗi tầng" --artifact cad/scripts/build_freecad.py
py tools/harness.py bug S-004 high "Pin khóa chưa kiểm chứng dưới tải" --evidence design/petg_reinforced_prototype.md
```

**Mỗi vòng làm việc:** xem `status` → chọn 1 story → sửa artifact → chạy kiểm tra liên quan → ghi `event` có kết quả → đổi trạng thái nếu đạt acceptance → cập nhật bug nếu phát hiện. Phase chuyển `done` chỉ khi mọi story trong phase đạt tiêu chí. Việc hiện tại: P0/P1. Việc tiếp theo: P2/P3/P4. Lịch sử event giữ tối đa một câu kết luận + đường dẫn, giúp đọc nhanh mà không tiêu tốn context.

SQL đọc lịch sử gọn:

```sql
SELECT at_utc, story_id, kind, summary, artifact FROM implementation_event ORDER BY id DESC LIMIT 20;
SELECT s.id, s.title, b.id, b.severity, b.status, b.title FROM bug b JOIN story s ON s.id=b.story_id WHERE b.status='open';
```
