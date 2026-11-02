"""FreeCAD 1.1: dimensional layout only; placeholders are not manufacturing parts.

Run: freecadcmd.exe build_freecad.py
Output: cad/assembly/layout.FCStd, exports/STEP/layout.step, STL envelopes.
"""
import json
import math
from pathlib import Path

import FreeCAD as App
import Part
import Mesh


ROOT = Path(__file__).resolve().parents[2]
P = json.loads((ROOT / "requirements" / "parameters.json").read_text(encoding="utf-8"))
assert P["topology"]["column_count_in_this_model"] == 1
assert P["topology"]["holding_mechanisms_per_column"] == P["gates"]["count"] == 2
doc = App.newDocument("BowlDispenserConcept")
parts = []
envelopes = []


def feature(name, shape, group="part", color=(0.25, 0.38, 0.78)):
    if shape.isNull() or not shape.isValid():
        raise ValueError("Invalid FreeCAD shape: " + name)
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Shape = shape
    obj.addProperty("App::PropertyString", "Status", "Design")
    obj.Status = "Envelope - do not print" if group == "envelope" else "Concept geometry - verify before print"
    if App.GuiUp:
        obj.ViewObject.ShapeColor = color
    (envelopes if group == "envelope" else parts).append(obj)
    return obj


def annulus(ro, ri, height, z):
    outer = Part.makeCylinder(ro, height, App.Vector(0, 0, z))
    inner = Part.makeCylinder(ri, height + 2, App.Vector(0, 0, z - 1))
    return outer.cut(inner)


def cylinder_at_polar(radius, theta_deg, diameter, height, z):
    a = math.radians(theta_deg)
    return Part.makeCylinder(diameter / 2, height,
                             App.Vector(radius * math.cos(a), radius * math.sin(a), z))


def jaw(theta_deg, z, open_state=False):
    # Concept radial shoe with a forked roller mount under its outer half.
    inner = (P["gates"]["open_clear_aperture_diameter"] if open_state else
             P["gates"]["closed_clear_aperture_diameter"]) / 2
    g = P["gates"]
    length = g["jaw_radial_length"]
    width = g["jaw_tangential_width"]
    thickness = g["jaw_thickness"]
    shape = Part.makeBox(length, width, thickness,
                         App.Vector(inner, -width/2, z + 8))
    b = P["hardware"]["jaw_guide_bearing"]
    axle_x = inner + length * 0.65
    axle_z = z + 8 - b["outer_diameter"] / 2
    # Two cheeks hold a 625 bearing between them; the axle is tangential,
    # allowing the outer race to roll on a radial track beneath the shoe.
    cheek_t = 2.5
    cheek_radial = max(8.0, b["axle_clearance_hole_diameter"] + 2 * P["print"]["minimum_wall"])
    cheek_bottom = axle_z - b["outer_diameter"] / 2 - 1.0
    cheek_top = z + 8 + 4.0
    cheek_h = cheek_top - cheek_bottom
    holes = []
    for y0 in (-b["width"] / 2 - cheek_t, b["width"] / 2):
        cheek = Part.makeBox(cheek_radial, cheek_t, cheek_h,
                             App.Vector(axle_x - cheek_radial/2, y0, cheek_bottom))
        shape = shape.fuse(cheek)
        holes.append(Part.makeCylinder(b["axle_clearance_hole_diameter"] / 2,
                                       cheek_t + 0.4,
                                       App.Vector(axle_x, y0 - 0.2, axle_z),
                                       App.Vector(0, 1, 0)))
    for bore in holes:
        shape = shape.cut(bore)
    shape = shape.removeSplitter()
    shape.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), theta_deg)
    return shape


def jaw_bearing(theta_deg, z, index):
    g, b = P["gates"], P["hardware"]["jaw_guide_bearing"]
    inner = g["closed_clear_aperture_diameter"] / 2
    axle_x = inner + g["jaw_radial_length"] * 0.65
    axle_z = z + 8 - b["outer_diameter"] / 2
    outer = Part.makeCylinder(b["outer_diameter"] / 2, b["width"],
                              App.Vector(axle_x, -b["width"] / 2, axle_z),
                              App.Vector(0, 1, 0))
    bore = Part.makeCylinder(b["bore_diameter"] / 2, b["width"] + 0.4,
                             App.Vector(axle_x, -b["width"] / 2 - 0.2, axle_z),
                             App.Vector(0, 1, 0))
    roller = outer.cut(bore)
    roller.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), theta_deg)
    return roller


frame = P["frame"]
gates = P["gates"]
gap = gates["gate_center_spacing"]
ring_z = [0, gap]
for index, z in enumerate(ring_z, 1):
    base = annulus(frame["outside_diameter"] / 2,
                   frame["ring_inside_diameter"] / 2,
                   frame["plate_thickness"], z)
    for post_angle in (45, 135, 225, 315):
        post_bore = cylinder_at_polar(frame["structural_post_pcd"] / 2,
                                       post_angle,
                                       P["hardware"]["printed_post_hole_diameter"],
                                       frame["plate_thickness"] + 2, z - 1)
        base = base.cut(post_bore)
    feature("T%d_fixed_ring" % index, base)
    # Show closed support shoes. Separate objects make the travel easy to inspect.
    for j in range(gates["jaw_count"]):
        feature("T%d_support_shoe_%02d" % (index, j + 1),
                jaw(j * 360 / gates["jaw_count"], z), color=(0.94, 0.64, 0.17))
        angle = j * 360 / gates["jaw_count"]
        feature("T%d_625_bearing_%02d_ENVELOPE" % (index, j + 1),
                jaw_bearing(angle, z, j + 1), "envelope", (0.68, 0.70, 0.74))
        rail = Part.makeBox(52, 10, 4, App.Vector(74, -5, z - 8 - 4))
        rail.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), angle)
        feature("T%d_radial_roller_rail_%02d_ENVELOPE" % (index, j + 1),
                rail, "envelope", (0.25, 0.55, 0.42))
    # Annular volume reserved for a cam ring; details of grooves/teeth are pending.
    feature("T%d_cam_ring_ENVELOPE" % index,
            annulus(115, 99, 5, z + 15), "envelope", (0.7, 0.25, 0.2))
    # Servo cradle: two cheeks and an end stop, deliberately with extra clearance.
    c = P["hardware"]["servo_mount_clearance_each_side"]
    body = P["hardware"]["servo_body_envelope"]
    sx, sy, sz = body
    x0 = frame["outside_diameter"] / 2 + 4
    y0 = -sy / 2 - c
    cradle = Part.makeBox(sx + 2*c + 8, sy + 2*c + 8, 5,
                          App.Vector(x0, y0 - 4, z))
    bridge = Part.makeBox(12, sy + 2*c + 8, 5,
                          App.Vector(x0 - 8, y0 - 4, z))
    cradle = cradle.fuse(bridge)
    for hx in (x0 + 5, x0 + sx + 4):
        for hy in (-sy/2 - 1, sy/2 + 1):
            bore = Part.makeCylinder(P["hardware"]["servo_mount_hole_nominal"] / 2,
                                     7, App.Vector(hx, hy, z - 1))
            cradle = cradle.cut(bore)
    feature("T%d_servo_cradle_bottom" % index, cradle,
            color=(0.35, 0.35, 0.38))
    feature("T%d_servo_body_ENVELOPE" % index,
            Part.makeBox(sx, sy, sz, App.Vector(x0 + 4, -sy/2, z + 5)),
            "envelope", (0.1, 0.1, 0.1))
    # Spring pawl and hard stop are *space reservations*, not a functional lock.
    feature("T%d_spring_pawl_ENVELOPE" % index,
            Part.makeBox(16, 8, 12, App.Vector(-124, -4, z + 12)),
            "envelope", (0.8, 0.2, 0.15))

for j, angle in enumerate((45, 135, 225, 315), 1):
    feature("structure_post_%d" % j,
            cylinder_at_polar(frame["structural_post_pcd"] / 2, angle,
                              frame["structural_post_diameter"], gap + 8, 0),
            color=(0.56, 0.58, 0.62))
for j, angle in enumerate((0, 90, 180, 270), 1):
    # Radial slot lets each guide post move inward/outward for bowl tolerance.
    bridge = Part.makeBox(17, 16, 8, App.Vector(88, -8, gap))
    bridge.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), angle)
    slot_r = P["hardware"]["printed_standoff_hole_pilot"] / 2
    slot_adjust = frame.get("guide_radial_adjustment_each_side", 3.0)
    slot_x = frame["guide_post_pcd"] / 2
    slot = Part.makeBox(2 * slot_adjust, 2 * slot_r, 10,
                        App.Vector(slot_x - slot_adjust, -slot_r, gap - 1))
    for x in (slot_x - slot_adjust, slot_x + slot_adjust):
        slot = slot.fuse(Part.makeCylinder(slot_r, 10,
                            App.Vector(x, 0, gap - 1)))
    slot.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), angle)
    feature("guide_bridge_%d" % j, bridge.cut(slot),
            color=(0.25, 0.38, 0.78))
    rod = cylinder_at_polar(frame["guide_post_pcd"] / 2, angle,
                            frame["guide_post_diameter"],
                            frame["guide_post_height"], gap + 8)
    pilot = cylinder_at_polar(frame["guide_post_pcd"] / 2, angle,
                              P["hardware"]["printed_standoff_hole_pilot"], 17, gap + 7)
    feature("guide_post_%d" % j,
            rod.cut(pilot),
            color=(0.55, 0.62, 0.65))
    # M3 brass standoff envelope at guide-post foot; verify real hex + screw length.
    feature("M3_standoff_%d_ENVELOPE" % j,
            cylinder_at_polar(frame["guide_post_pcd"] / 2, angle, 6, 15, gap + 3),
            "envelope", (0.83, 0.69, 0.28))

# Two lidded packages shown in the one-line transfer stack. The 75 mm
# package pitch and lid envelope are estimates until the complete packs are measured.
line1 = P["sales_lines"][0]
body_h = P["bowl"]["height"]
rim_r = P["bowl"]["rim_outer_diameter"] / 2
base_r = P["bowl"]["base_outer_diameter"] / 2
lid_r = line1["complete_package_max_diameter_estimate_mm"] / 2
lid_h = line1["lid_top_protrusion_estimate_mm"]
package_pitch = line1["estimated_package_stack_pitch_mm"]
lower_package_z = 16 - body_h
assert abs(package_pitch - P["gates"]["gate_center_spacing"]) < 1e-6, \
    "Gate spacing must equal the package-to-package support pitch"
lower_lid_top = lower_package_z + body_h + lid_h
upper_package_bottom = lower_package_z + package_pitch
assert abs(lower_lid_top - upper_package_bottom) < 1e-6, \
    "Estimated upper package bottom must touch the lower package lid"
for package_index, package_z in enumerate((lower_package_z, lower_package_z + package_pitch), 1):
    body = Part.makeCone(base_r, rim_r, body_h, App.Vector(0, 0, package_z))
    feature("L1_package_%d_body_ENVELOPE" % package_index,
            body, "envelope", (0.68, 0.85, 0.95))
    lid = Part.makeCylinder(lid_r, lid_h,
                            App.Vector(0, 0, package_z + body_h))
    feature("L1_package_%d_lid_ENVELOPE" % package_index,
            lid, "envelope", (0.75, 0.9, 1.0))

doc.recompute()
assembly = ROOT / "cad" / "assembly" / "layout.FCStd"
assembly.parent.mkdir(parents=True, exist_ok=True)
doc.saveAs(str(assembly))
step_dir = ROOT / "exports" / "STEP"
stl_dir = ROOT / "exports" / "STL"
step_dir.mkdir(parents=True, exist_ok=True)
stl_dir.mkdir(parents=True, exist_ok=True)
Part.export(parts, str(step_dir / "layout_printed_concept.step"))
for obj in parts:
    Mesh.export([obj], str(stl_dir / (obj.Name + ".stl")))
print("Generated concept:", assembly)
print("STEP and %d STL concept components" % len(parts))
