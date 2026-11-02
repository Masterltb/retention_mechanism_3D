"""Generate a dimensioned SVG overview from parameters (concept, not shop drawing)."""
import json
import math
from pathlib import Path

root = Path(__file__).resolve().parents[2]
p = json.loads((root / "requirements" / "parameters.json").read_text(encoding="utf-8"))
b, f, g = p["bowl"], p["frame"], p["gates"]
cx, cy = 150, 160
colors = {"frame": "#3158a8", "bowl": "#3a9db7", "shoe": "#d68b23"}
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="520" viewBox="0 0 1000 520">',
       '<rect width="1000" height="520" fill="white"/>',
       '<style>text{font:15px Arial,sans-serif;fill:#203048}.small{font-size:12px}.title{font-size:20px;font-weight:bold}</style>',
       '<text x="30" y="35" class="title">Bộ nhả tô FIFO — bản vẽ bố trí concept (mm)</text>',
       '<text x="30" y="59" class="small">Không dùng làm bản vẽ sản xuất hoặc chứng nhận chịu tải</text>']
for d, stroke, width, dash in [
    (f["outside_diameter"], colors["frame"], 4, ""),
    (f["ring_inside_diameter"], colors["frame"], 2, ""),
    (b["rim_outer_diameter"], colors["bowl"], 2, ' stroke-dasharray="6 4"'),
    (g["closed_clear_aperture_diameter"], colors["shoe"], 2, "")]:
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{d/2}" fill="none" stroke="{stroke}" stroke-width="{width}"{dash}/>')
for angle in range(0, 360, 60):
    a = math.radians(angle)
    x = cx + 89*math.cos(a)
    y = cy + 89*math.sin(a)
    svg.append(f'<rect x="{x-9}" y="{y-11}" width="18" height="22" fill="{colors["shoe"]}" opacity="0.6" transform="rotate({angle} {x} {y})"/>')
for angle in (0,90,180,270):
    a = math.radians(angle)
    x = cx + f["guide_post_pcd"]/2*math.cos(a)
    y = cy + f["guide_post_pcd"]/2*math.sin(a)
    svg.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#688d76"/>')
for angle in (45,135,225,315):
    a = math.radians(angle)
    x = cx + f["structural_post_pcd"]/2*math.cos(a)
    y = cy + f["structural_post_pcd"]/2*math.sin(a)
    svg.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#646a73"/>')
svg += [
    '<line x1="32" y1="310" x2="268" y2="310" stroke="#203048" marker-start="url(#arrow)" marker-end="url(#arrow)"/>',
    '<defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="3" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6 Z" fill="#203048"/></marker></defs>',
    f'<text x="80" y="303">Ø{f["outside_diameter"]} ngoài</text>',
    f'<text x="310" y="105">Lỗ đóng Ø{g["closed_clear_aperture_diameter"]} / mở Ø{g["open_clear_aperture_diameter"]}</text>',
    f'<text x="310" y="135">Miệng tô Ø{b["rim_outer_diameter"]}; đáy Ø{b["base_outer_diameter"]}; cao {b["height"]}</text>',
    f'<text x="310" y="165">4 trụ kết cấu Ø{f["structural_post_diameter"]} trên PCD {f["structural_post_pcd"]}</text>',
    f'<text x="310" y="195">4 thanh dẫn Ø{f["guide_post_diameter"]} trên PCD {f["guide_post_pcd"]}</text>',
    f'<text x="310" y="225">1 cột = 2 cơ chế giữ; cách tầng {g["gate_center_spacing"]} mm — phải đo bước lồng</text>',
    '<text x="310" y="255">6 guốc/tầng; truyền động cam và chốt khóa chưa được thiết kế</text>',
    '<text x="30" y="388">Màu xanh: khung; xanh nhạt nét đứt: miệng tô; cam: guốc đóng; xanh lá: thanh dẫn; xám: trụ kết cấu.</text>',
    '<text x="30" y="419">Tham số: requirements/parameters.json  |  Mô hình: cad/assembly/layout.FCStd  |  Kiểm chứng: simulation/validation/acceptance.md</text>',
    '</svg>']
out = root / "exports" / "drawings" / "overview_concept.svg"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("\n".join(svg), encoding="utf-8")
print(out)
