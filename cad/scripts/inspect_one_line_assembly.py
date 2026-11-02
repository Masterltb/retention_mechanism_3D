"""Report significant interferences between major prototype assembly solids."""
import FreeCAD as App
import os
from pathlib import Path

root = Path(__file__).resolve().parents[2]
state = os.environ.get("PIVOT_STATE", "closed")
doc = App.openDocument(str(root / "cad" / "assembly" / ("one_line_pivot_prototype_%s.FCStd" % state)))
out = root / "exports" / "preview" / ("one_line_%s_interference_report.txt" % state)
objects = [o for o in doc.Objects if hasattr(o, "Shape") and not o.Shape.isNull()]
lines = ["objects=%d" % len(objects)]
for stage in (1, 2):
    prefixes = [
        "Stage%d_fixed_carrier" % stage,
        "Stage%d_geared_sync_ring" % stage,
        "Stage%d_servo_pinion" % stage,
        "Stage%d_servo_body_ENVELOPE" % stage,
        "Stage%d_servo_output_shaft_ENVELOPE" % stage,
        "Stage%d_limit_" % stage,
        "Stage%d_positive_latch_ENVELOPE" % stage,
        "Stage%d_hard_stop_" % stage,
        "Stage%d_reinforced_latch_bracket" % stage,
        "Stage%d_lock_pin_" % stage,
        "Stage%d_ring_lock_steel_bushing" % stage,
        "Stage%d_latch_M5_through_bolt_" % stage,
        "Stage%d_closed_positive_hard_stop" % stage,
        "Stage%d_open_positive_hard_stop" % stage,
        "Stage%d_guide_bridge_" % stage,
        "Stage%d_hinged_flap_" % stage,
        "Stage%d_hinge_pin_" % stage,
        "Stage%d_hinge_bearing_" % stage,
        "Stage%d_sync_link_" % stage,
        "Stage%d_flap_link_pin_" % stage,
        "L1_package_",
        "structure_post_",
        "guide_post_",
        "guide_column_",
        "guide_shoe_",
    ]
    group = [o for o in objects if any(o.Name.startswith(p) for p in prefixes)]
    lines.append("stage%d major_pair_interference_mm3:" % stage)
    for i, a in enumerate(group):
        for b in group[i+1:]:
            if a.Name.startswith("L1_package_") and b.Name.startswith("L1_package_"):
                continue
            if a.Name.startswith("Stage%d_" % (3-stage)) or b.Name.startswith("Stage%d_" % (3-stage)):
                continue
            pair={a.Name,b.Name}
            # Pinned joints intentionally share volume at the pin/eye interface.
            if any("_flap_link_pin_" in n for n in pair) and any("_hinged_flap_" in n or "_sync_link_" in n for n in pair):
                continue
            if any("_ring_link_pin_" in n for n in pair) and any("geared_sync_ring" in n or "_sync_link_" in n for n in pair):
                continue
            if any("_flap_link_pin_" in n for n in pair) and any("_hinged_flap_" in n or "_sync_link_" in n for n in pair):
                continue
            if any("ring_lock_steel_bushing" in n for n in pair) and any("geared_sync_ring" in n for n in pair):
                continue
            if any("lock_pin_6mm_steel_engaged" in n for n in pair) and any("geared_sync_ring" in n for n in pair):
                continue
            if any("positive_hard_stop" in n for n in pair) and any("geared_sync_ring" in n for n in pair):
                continue
            if any("guide_shoe_" in n for n in pair) and any("guide_post_" in n for n in pair):
                continue
            if any("guide_shoe_" in n for n in pair) and any("M3_clamp_screw" in n for n in pair):
                continue
            if any("latch_M5_through_bolt_" in n for n in pair) and any("fixed_carrier" in n or "reinforced_latch_bracket" in n for n in pair):
                continue
            if any("servo_pinion" in n for n in pair) and any("servo_output_shaft" in n for n in pair):
                continue
            if any("ENVELOPE" in n for n in pair) and any("hard_stop_" in n or "positive_latch" in n or "limit_" in n for n in pair):
                continue
            try:
                common = a.Shape.common(b.Shape)
                if common.Volume > 0.05:
                    lines.append("%s <> %s: %.4f" % (a.Name,b.Name,common.Volume))
            except Exception as e:
                lines.append("BOOLEAN_ERROR %s <> %s: %s" % (a.Name,b.Name,e))
out.write_text("\n".join(lines)+"\n", encoding="utf-8")
App.closeDocument(doc.Name)
