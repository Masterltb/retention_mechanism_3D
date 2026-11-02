# Engineering harness — quy trình phát triển và lưu bản production

## 1. Nguồn sự thật và giới hạn release

`requirements/parameters.json` chứa tham số đo và giả định; `requirements/requirements.md` có ID R-xx. `BOM/history.sqlite` lưu phase/story/bug/event/BOM; `BOM/history_dump.sql` là backup dạng text có thể khôi phục. Lệnh `check` buộc dump khớp database hiện tại. Mỗi story trỏ tới ID yêu cầu, phase, artifact và tiêu chí nghiệm thu. Mỗi bằng chứng thử phải có đường dẫn lưu trong repo hoặc kho lưu trữ được ghi rõ. Bản vẽ và STEP/STL trong `exports/` là **concept** cho đến khi P4 được duyệt; không đổi tên file thành “production” trước khi P0–P3 đạt.

Máy có hai line sản phẩm với package tô/nắp khác nhau. CAD một line là module mẫu; mỗi thay đổi kích thước phải lấy từ package hoàn chỉnh đúng line. Chiều cao tô trần không thay thế package stack pitch; không nhân đôi module thành máy hai line cho tới khi có kích thước L2 và khoảng hở máy.

## 2. Chu kỳ làm việc cho từng story

1. `py tools/harness.py status`; chọn story, ghi rủi ro/giả định và cập nhật tham số.
2. Tính: `py tools/calculate_mechanics.py`; kiểm tra dải `μ`, tải bình thường và lỗi, điều kiện servo, vị trí chốt.
3. Vẽ: `py cad/scripts/draw_overview.py`, `py cad/scripts/draw_force_path.py`, rồi `freecadcmd cad/scripts/build_line_pivot_prototype.py` và `freecadcmd cad/scripts/inspect_one_line_assembly.py` khi đổi prototype cánh. So STEP/FCStd với công thức và biên dạng package đo thật.
4. Thử: coupon → một tầng → hai tầng → FIFO. Lưu ảnh, CSV lực, nhật ký mất điện; ghi một event `test` có `--evidence` và kết luận đạt/không đạt. Bug phải có ID story, mức độ, bằng chứng, artifact sửa và test xác nhận.
5. Tạo snapshot bằng `py tools/engineering.py snapshot`, chạy `py tools/engineering.py check`, kiểm tra diff rồi commit milestone có ý nghĩa. `check` đối chiếu dump với database nên snapshot phải chạy trước. Không ép story `done` khi chỉ có hình vẽ mà chưa qua tiêu chí của nó.

## 3. Gate của mỗi phase

| Phase | Đầu ra phải được review | Điều kiện đóng |
|---|---|---|
| P0 — dữ liệu vật thật | Bản đo 10 tô, bước lồng, mặt dưới gờ; coupon `μ_s/μ_k`; MG996R đúng chiếc | Dữ liệu nguồn và sai số được lưu; không còn tham số quyết định ở `null` |
| P1 — tính + bố trí | Công thức và CSV sensitivity; FreeCAD/STEP/SVG khớp số; danh sách giao thoa | Từng story có test + artifact; khe guốc và rủi ro vành tô được giải quyết hoặc ghi bug |
| P2 — cơ cấu vận hành | Cánh bản lề và đồng bộ servo PWM không cam; ray/chốt chống lật; khóa lò xo khi mất điện; chặn cơ và cảm biến | Torque đo dưới ngưỡng vận hành; pin khóa xác nhận; 100 chu kỳ một tầng; cắt điện an toàn |
| P3 — hệ thống | Hai tầng và liên động FIFO; đo tải tĩnh/động/lệch tâm và creep | Checklist `simulation/validation/acceptance.md` có bằng chứng, 50 chu kỳ FIFO đạt |
| P4 — bàn giao | Bản vẽ dung sai, hướng in, BOM, STEP/STL cuối, hướng dẫn lắp/bảo trì | Review độc lập và phát hành tag release |

Lệnh `phase-gate` kiểm tra tự động: mọi story trong phase `done`, mỗi story có event `test` kèm bằng chứng, artifact tồn tại, không còn bug `high/critical` mở. **Review cơ khí và thử nghiệm thực tế vẫn phải được người chịu trách nhiệm ký nhận**; script không thay thế kiểm tra vật lý. `close-phase` chạy check + gate, đổi trạng thái phase và tạo backup SQL. Phase chưa đạt được để ở `doing`/`todo`.

## 4. Git: commit từng phase, backup và phục hồi

### Đồng bộ SQLite giữa các thiết bị và thành viên

`BOM/history.sqlite` là database nhị phân, Git không thể gộp an toàn hai bản cùng được sửa. `BOM/history_dump.sql` là snapshot để review/khôi phục, không phải cơ chế đồng bộ nhiều người đồng thời. Không đặt file database đang được mở trong OneDrive/Dropbox/Google Drive, thư mục đồng bộ, hoặc ổ mạng để nhiều máy cùng ghi. Khi dùng quy trình hiện tại, mỗi lần chỉ một người/thiết bị cập nhật SQLite; các thành viên khác cập nhật tài liệu/CAD trên nhánh riêng và phối hợp để tránh sửa đồng thời database.

Trên thiết bị bắt đầu một phiên làm việc, lấy thay đổi mới nhất trước khi mở hoặc sửa database:

```powershell
git switch main
git pull --ff-only origin main
py tools/harness.py status
```

Sau khi cập nhật trạng thái/story/event/BOM, tạo dump rồi kiểm tra, sau đó commit và push cả hai file SQLite:

```powershell
py tools/engineering.py snapshot
py tools/engineering.py check
git diff --check
git add BOM/history.sqlite BOM/history_dump.sql
git diff --cached --stat
git commit -m "Update engineering harness history"
git push origin main
```

Nếu `git pull` báo diverged hoặc `git push` bị từ chối, dừng việc ghi thêm vào database. Giữ bản database và dump đang có làm bản sao riêng, cập nhật nhánh từ remote, rồi đối chiếu các thao tác đã làm và ghi lại chúng lên bản mới nhất bằng `tools/harness.py`. Không giải quyết xung đột `history.sqlite` bằng cách chọn “ours”/“theirs” hoặc ghi đè file. Chạy snapshot và check trước khi commit lại. Không chạy `py tools/harness.py init` trên database đang có dữ liệu để đồng bộ; lệnh này chỉ dành cho khởi tạo database mới.

Nếu nhóm cần nhiều người ghi cùng lúc hoặc cần đồng bộ offline tự động, chuyển phần dữ liệu cộng tác sang dịch vụ database/API trung tâm; mỗi client có thể giữ SQLite cục bộ làm cache. SQLite phù hợp khi các tiến trình cùng dùng file cục bộ, nhưng WAL không hỗ trợ client ở các máy khác nhau truy cập qua network filesystem. Tham khảo [SQLite WAL](https://www.sqlite.org/wal.html) và [SQLite over a network](https://www.sqlite.org/useovernet.html).

Branch mặc định `main` chứa mốc đã review. Làm việc trên branch `phase/P0-measurements`, `phase/P1-cad`, v.v. Commit nhỏ theo story: `P1/S-007: calculate load and friction envelope`. Mỗi commit chỉ gồm tham số, phép tính, bản vẽ và bằng chứng liên quan; tránh commit cache/log. Sau khi review phase:

```powershell
py tools/engineering.py phase-gate P1
py tools/engineering.py close-phase P1
py tools/engineering.py check
git status --short
git diff --check
git add requirements design cad simulation exports BOM docs tools README.md
git diff --cached --stat
git commit -m "P1: approve CAD and mechanics baseline"
git tag -a phase/P1 -m "P1 accepted; see BOM/history_dump.sql and evidence"
git push origin main
git push origin phase/P1
```

Tag dạng `phase/Pn` phải dùng đúng ID phase trong database vì workflow truyền phần sau `phase/` trực tiếp cho `phase-gate`. Chỉ tạo tag phase sau gate và review. Mốc giữa phase dùng `milestone/P1-analysis-v0.2`, **không ngụ ý nghiệm thu**. Tag là điểm backup bất biến; GitHub là bản sao ngoài máy. Không force-push tag/`main`. Nếu cần sửa, tạo commit và tag phiên bản mới. Nhánh làm việc push thường xuyên để backup, PR/review trước khi gộp vào `main` khi có người review.

Khôi phục một mốc mà không phá lịch sử: `git switch -c recovery/P1-v1 phase/P1-v1`; khôi phục SQL bằng `sqlite3 BOM/restored.sqlite < BOM/history_dump.sql` hoặc `py`/Python `sqlite3.executescript`. Kiểm tra `PRAGMA integrity_check` và `foreign_key_check`, rồi so bằng chứng. Nếu cần lùi một commit đã push lên `main`, dùng `git revert`, không `reset --hard`/force-push. Nếu STEP/STL vượt giới hạn GitHub về sau, chuyển sang Git LFS và ghi rõ trong README trước khi commit file lớn.

## 5. Lệnh kiểm tra nhanh

```powershell
py tools/engineering.py snapshot
py tools/engineering.py check
py tools/engineering.py phase-gate P1
py tools/harness.py status
```

Workflow `.github/workflows/engineering-check.yml` chạy check trên push/PR và kiểm gate cho tag `phase/*`. Workflow không chạy FreeCAD trên GitHub Actions; bản xuất CAD được sinh và kiểm hình học bằng FreeCAD tại máy thiết kế, còn CI kiểm liên kết, tham số, XML/CSV và SQLite. Ghi version FreeCAD và máy in vào event khi đóng phase.
