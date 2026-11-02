# Engineering harness — quy trình phát triển và lưu bản production

## 1. Nguồn sự thật và giới hạn release

`requirements/parameters.json` chứa tham số đo và giả định; `requirements/requirements.md` có ID R-xx. `BOM/history.sqlite` lưu phase/story/bug/event/BOM; `BOM/history_dump.sql` là backup dạng text có thể khôi phục. Lệnh `check` buộc dump khớp database hiện tại. Mỗi story trỏ tới ID yêu cầu, phase, artifact và tiêu chí nghiệm thu. Mỗi bằng chứng thử phải có đường dẫn lưu trong repo hoặc kho lưu trữ được ghi rõ. Bản vẽ và STEP/STL trong `exports/` là **concept** cho đến khi P4 được duyệt; không đổi tên file thành “production” trước khi P0–P3 đạt.

## 2. Chu kỳ làm việc cho từng story

1. `py tools/harness.py status`; chọn story, ghi rủi ro/giả định và cập nhật tham số.
2. Tính: `py tools/calculate_mechanics.py`; kiểm tra dải `μ`, tải bình thường và lỗi, điều kiện servo, vị trí chốt.
3. Vẽ: `py cad/scripts/draw_overview.py`, `py cad/scripts/draw_force_path.py`, rồi `freecadcmd cad/scripts/build_freecad.py` khi đổi CAD. So STEP/FCStd với công thức và biên dạng tô đo thật.
4. Thử: coupon → một tầng → hai tầng → FIFO. Lưu ảnh, CSV lực, nhật ký mất điện; ghi một event `test` có `--evidence` và kết luận đạt/không đạt. Bug phải có ID story, mức độ, bằng chứng, artifact sửa và test xác nhận.
5. `py tools/engineering.py check`; kiểm tra diff, tạo snapshot SQL, rồi commit milestone có ý nghĩa. Không ép story `done` khi chỉ có hình vẽ mà chưa qua tiêu chí của nó.

## 3. Gate của mỗi phase

| Phase | Đầu ra phải được review | Điều kiện đóng |
|---|---|---|
| P0 — dữ liệu vật thật | Bản đo 10 tô, bước lồng, mặt dưới gờ; coupon `μ_s/μ_k`; MG996R đúng chiếc | Dữ liệu nguồn và sai số được lưu; không còn tham số quyết định ở `null` |
| P1 — tính + bố trí | Công thức và CSV sensitivity; FreeCAD/STEP/SVG khớp số; danh sách giao thoa | Từng story có test + artifact; khe guốc và rủi ro vành tô được giải quyết hoặc ghi bug |
| P2 — cơ cấu vận hành | Cam, truyền động, ray/chốt chống lật, khóa khi mất điện, giới hạn/cảm biến | Torque đo dưới ngưỡng vận hành; 100 chu kỳ một tầng; cắt điện an toàn |
| P3 — hệ thống | Hai tầng và liên động FIFO; đo tải tĩnh/động/lệch tâm và creep | Checklist `simulation/validation/acceptance.md` có bằng chứng, 50 chu kỳ FIFO đạt |
| P4 — bàn giao | Bản vẽ dung sai, hướng in, BOM, STEP/STL cuối, hướng dẫn lắp/bảo trì | Review độc lập và phát hành tag release |

Lệnh `phase-gate` kiểm tra tự động: mọi story trong phase `done`, mỗi story có event `test` kèm bằng chứng, artifact tồn tại, không còn bug `high/critical` mở. **Review cơ khí và thử nghiệm thực tế vẫn phải được người chịu trách nhiệm ký nhận**; script không thay thế kiểm tra vật lý. `close-phase` chạy check + gate, đổi trạng thái phase và tạo backup SQL. Phase chưa đạt được để ở `doing`/`todo`.

## 4. Git: commit từng phase, backup và phục hồi

Branch mặc định `main` chứa mốc đã review. Làm việc trên branch `phase/P0-measurements`, `phase/P1-cad`, v.v. Commit nhỏ theo story: `P1/S-007: calculate load and friction envelope`. Mỗi commit chỉ gồm tham số, phép tính, bản vẽ và bằng chứng liên quan; tránh commit cache/log. Sau khi review phase:

```powershell
py tools/engineering.py check
py tools/engineering.py phase-gate P1
py tools/engineering.py close-phase P1
git status --short
git diff --check
git add requirements design cad simulation exports BOM docs tools README.md
git diff --cached --stat
git commit -m "P1: approve CAD and mechanics baseline"
git tag -a phase/P1-v1 -m "P1 accepted; see BOM/history_dump.sql and evidence"
git push origin main
git push origin phase/P1-v1
```

Chỉ tag `phase/Pn-vN` sau gate và review. Mốc giữa phase dùng `milestone/P1-analysis-v0.2`, **không ngụ ý nghiệm thu**. Tag là điểm backup bất biến; GitHub là bản sao ngoài máy. Không force-push tag/`main`. Nếu cần sửa, tạo commit và tag phiên bản mới. Nhánh làm việc push thường xuyên để backup, PR/review trước khi gộp vào `main` khi có người review.

Khôi phục một mốc mà không phá lịch sử: `git switch -c recovery/P1-v1 phase/P1-v1`; khôi phục SQL bằng `sqlite3 BOM/restored.sqlite < BOM/history_dump.sql` hoặc `py`/Python `sqlite3.executescript`. Kiểm tra `PRAGMA integrity_check` và `foreign_key_check`, rồi so bằng chứng. Nếu cần lùi một commit đã push lên `main`, dùng `git revert`, không `reset --hard`/force-push. Nếu STEP/STL vượt giới hạn GitHub về sau, chuyển sang Git LFS và ghi rõ trong README trước khi commit file lớn.

## 5. Lệnh kiểm tra nhanh

```powershell
py tools/engineering.py check
py tools/engineering.py snapshot
py tools/engineering.py phase-gate P1
py tools/harness.py status
```

Workflow `.github/workflows/engineering-check.yml` chạy check trên push/PR và kiểm gate cho tag `phase/*`. Workflow không chạy FreeCAD trên GitHub Actions; bản xuất CAD được sinh và kiểm hình học bằng FreeCAD tại máy thiết kế, còn CI kiểm liên kết, tham số, XML/CSV và SQLite. Ghi version FreeCAD và máy in vào event khi đóng phase.
