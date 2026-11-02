"""Annotated SVG for the load/friction calculation; conceptual, not a shop drawing."""
import json
import math
from pathlib import Path

root = Path(__file__).resolve().parents[2]
p = json.loads((root / "requirements" / "parameters.json").read_text(encoding="utf-8"))
s = json.loads((root / "simulation/kinematics/calculation_summary.json").read_text(encoding="utf-8"))
g, a, h = p["gates"], p["analysis_assumptions_not_validated"], p["hardware"]
r = g["closed_clear_aperture_diameter"] / 2
cx, cy = 185, 235
items = ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="790" viewBox="0 0 1200 790">',
         '<rect width="1200" height="790" fill="#fff"/>',
         '<style>text{font:16px Arial,sans-serif;fill:#1d2d42}.small{font-size:13px}.title{font-size:23px;font-weight:bold}.head{font-size:18px;font-weight:bold}</style>',
         '<defs><marker id="arr" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10Z" fill="#be3838"/></marker></defs>',
         '<text class="title" x="30" y="35">Một line / hai tầng — sơ đồ lực và truyền động cánh PETG</text>',
         '<text class="small" x="30" y="60">Không dùng cam. Mô-men PETG/ma sát là screening; cần đo package và thử tải thật.</text>',
         '<text class="head" x="40" y="95">Mặt bằng một tầng ở trạng thái đóng</text>',
         f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#d18b20" stroke-width="2"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{p["bowl"]["rim_outer_diameter"]/2}" fill="none" stroke="#2895aa" stroke-width="2" stroke-dasharray="5 5"/>']
for j in range(g["jaw_count"]):
    angle = j*360/g["jaw_count"]
    items.append(f'<rect x="{cx+r}" y="{cy-g["jaw_tangential_width"]/2}" width="{g["jaw_radial_length"]}" height="{g["jaw_tangential_width"]}" fill="#e3a64b" stroke="#8b5a15" transform="rotate({angle} {cx} {cy})"/>')
items += [
    f'<text x="315" y="140">6 guốc × rộng {g["jaw_tangential_width"]} mm</text>',
    f'<text x="315" y="170">Cung trống giữa 2 guốc: {s["closed_free_arc_gap_mm"]:.1f} mm</text>',
    f'<text x="315" y="200">Phủ chu vi ở mép trong: {100*s["contact_arc_fraction_closed"]:.1f}%</text>',
    f'<text x="315" y="230">Độ gối hình học tối đa: {(p["bowl"]["rim_outer_diameter"]-g["closed_clear_aperture_diameter"])/2:.2f} mm</text>',
    '<text x="315" y="260">Nét xanh đứt: Ø miệng tô; cam nhạt: vùng cánh đỡ.</text>',
    '<text class="head" x="40" y="365">Mặt cắt một guốc chịu tải lệch tâm</text>',
    '<rect x="90" y="430" width="320" height="40" fill="#415a85"/>',
    '<text x="180" y="458" fill="white">khung / ray dưới</text>',
    '<rect x="120" y="400" width="210" height="30" fill="#e3a64b" stroke="#8b5a15"/>',
    f'<text x="150" y="421">cánh PETG dày {g["jaw_thickness"]} mm</text>',
    '<rect x="120" y="378" width="210" height="12" fill="#8296ae"/>',
    '<text x="375" y="392">ray trên cần thiết kế</text>',
    '<path d="M240 325 L240 394" stroke="#be3838" stroke-width="3" marker-end="url(#arr)"/>',
    '<text x="210" y="318">F_j ↓</text>',
    '<path d="M240 344 L300 344" stroke="#202d42" stroke-width="2"/>',
    f'<text x="255" y="338">e = {a["contact_eccentricity_from_guide_mm"]} mm (giả định)</text>',
    f'<text x="40" y="500">M_j = F_j · e;  R_t = M_j / h;  h = {a["anti_tilt_bearing_separation_mm"]} mm (giả định)</text>',
    '<text x="40" y="530">PETG allowable chưa biết; thử coupon và proof-load trước khi kết luận hệ số an toàn.</text>',
    '<text class="head" x="40" y="595">Đường truyền torque ứng viên</text>',
    f'<text x="40" y="630">MG996R {h["servo_body_envelope"][0]} × {h["servo_body_envelope"][1]} × {h["servo_body_envelope"][2]} mm</text>',
    f'<text x="40" y="660">servo → pinion 12T → vòng đồng bộ 72T ({a["candidate_gear_reduction"]:.0f}:1) → thanh nối → 6 cánh bản lề</text>',
    '<text x="40" y="690">F_f ≈ μ W_d;  T_ring ≈ F_f r_eff;  T_servo ≈ T_ring/(i η_gear)</text>',
    '<text class="small" x="40" y="740">Nguồn: requirements/parameters.json; design/friction_analysis.md; simulation/kinematics/force_friction_sensitivity.csv</text>',
    '</svg>']
target = root / "exports/drawings/force_path_concept.svg"
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text("\n".join(items), encoding="utf-8")
print(target)
