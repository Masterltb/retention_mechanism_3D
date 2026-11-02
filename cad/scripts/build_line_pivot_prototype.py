"""Conceptual one-line, two-stage hinged-flap retention module.

Generates a FreeCAD assembly and STEP for the closed state. Open-state flap
envelopes are saved in the FCStd document as hidden reference geometry.
All actuator/link geometry is conceptual pending measured package and servo data.
"""
import json
import math
from pathlib import Path

import FreeCAD as App
import Part
import Mesh

ROOT = Path(__file__).resolve().parents[2]
P = json.loads((ROOT / "requirements" / "parameters.json").read_text(encoding="utf-8"))
L = P["sales_lines"][0]
G, F, H = P["gates"], P["frame"], P["hardware"]
K = P["pivot_flap_prototype"]
gap = P["gates"]["gate_center_spacing"]
pitch = L["estimated_package_stack_pitch_mm"]
body_h = P["bowl"]["height"]
lid_h = L["lid_top_protrusion_estimate_mm"]
package_z0 = 16.0 - body_h
base_r = P["bowl"]["base_outer_diameter"]/2
rim_r = P["bowl"]["rim_outer_diameter"]/2
lid_r = L["complete_package_max_diameter_estimate_mm"]/2
assert abs(gap-pitch) < 1e-6
assert abs(package_z0+body_h+lid_h-(package_z0+pitch)) < 1e-6
PIVOT_R = K["flap_pivot_radius_mm"]
CRANK_DX, CRANK_DY = K["flap_crank_radial_offset_mm"], K["flap_crank_tangential_offset_mm"]
LINK_R, LINK_PHASE = K["sync_ring_pin_radius_mm"], K["sync_ring_pin_phase_deg"]
FLAP_OPEN_DEG = K["flap_open_angle_deg"]
GEAR_MODULE, RING_TEETH, PINION_TEETH = K["gear_module_mm"], K["sync_ring_teeth"], K["servo_pinion_teeth"]
RING_PITCH_R = GEAR_MODULE * RING_TEETH / 2
PINION_PITCH_R = GEAR_MODULE * PINION_TEETH / 2
PINION_CENTER_R = RING_PITCH_R + PINION_PITCH_R + K["gear_center_backlash_mm"]
LOCK_RADIUS = RING_PITCH_R + 14.0

def rotate_xy(x, y, deg):
    a = math.radians(deg)
    return (x*math.cos(a)-y*math.sin(a), x*math.sin(a)+y*math.cos(a))

q0 = (PIVOT_R+CRANK_DX, CRANK_DY)
ring_b0 = rotate_xy(LINK_R, 0, LINK_PHASE)
link_length = math.dist(q0, ring_b0)
q1 = (PIVOT_R-CRANK_DY, CRANK_DX)
q1_angle = math.atan2(q1[1],q1[0])
q1_radius = math.hypot(*q1)
cos_arg = (q1_radius*q1_radius+LINK_R*LINK_R-link_length*link_length)/(2*q1_radius*LINK_R)
assert -1 <= cos_arg <= 1
RING_OPEN_ROT_DEG = math.degrees(q1_angle+math.acos(cos_arg))-LINK_PHASE
doc = App.newDocument("OneLinePivotFlapPrototype")
physical, envelopes, open_refs = [], [], []


def add(name, shape, group="physical", color=(0.25, 0.4, 0.75)):
    if shape.isNull() or not shape.isValid():
        raise ValueError("Invalid shape: " + name)
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Shape = shape
    obj.addProperty("App::PropertyString", "Status", "Design")
    obj.Status = "Concept - verify dimensions, strength and motion before printing"
    if App.GuiUp:
        obj.ViewObject.ShapeColor = color
    if group == "physical":
        physical.append(obj)
    elif group == "open":
        if App.GuiUp:
            obj.ViewObject.Visibility = False
        open_refs.append(obj)
    else:
        if App.GuiUp:
            obj.ViewObject.Transparency = 78
        envelopes.append(obj)
    return obj


def annulus(ro, ri, h, z):
    return Part.makeCylinder(ro, h, App.Vector(0, 0, z)).cut(
        Part.makeCylinder(ri, h + 2, App.Vector(0, 0, z - 1)))


def polar(r, angle):
    a = math.radians(angle)
    return App.Vector(r * math.cos(a), r * math.sin(a), 0)


def flap(angle, z, opened=False):
    pivot_r = PIVOT_R
    arm_w = 26.0
    pivot = polar(pivot_r, angle)
    # Match the inner face to the estimated tapered bowl side over the 6 mm
    # flap height. This is a zero-clearance contact prototype, not a clamp fit.
    pkg_bottom = z + package_z0
    def side_r(z_abs):
        local_z = max(0.0, min(body_h, z_abs - pkg_bottom))
        return base_r + (rim_r - base_r) * local_z / body_h
    r_low, r_high = side_r(z + 8), side_r(z + 16)
    points = [App.Vector(r_low,-arm_w/2,z+8),
              App.Vector(pivot_r,-arm_w/2,z+8),
              App.Vector(pivot_r,-arm_w/2,z+16),
              App.Vector(r_high,-arm_w/2,z+16),
              App.Vector(r_low,-arm_w/2,z+8)]
    face = Part.Face(Part.makePolygon(points))
    shape = face.extrude(App.Vector(0,arm_w,0))
    boss = Part.makeCylinder(9.5, 8, App.Vector(pivot_r,0,z+8))
    crank = Part.makeBox(12,10,8,App.Vector(pivot_r-12,4,z+8))
    shape = shape.fuse(boss).fuse(crank)
    bearing_relief=Part.makeCylinder(8.25,5,App.Vector(pivot_r,0,z+8))
    bearing_relief=bearing_relief.cut(Part.makeCylinder(4.5,5.2,App.Vector(pivot_r,0,z+7.9)))
    shape=shape.cut(bearing_relief)
    shape = shape.cut(Part.makeCylinder(2.65,10,App.Vector(pivot_r,0,z+7)))
    shape = shape.cut(Part.makeCylinder(2.15,10,
                        App.Vector(pivot_r+CRANK_DX,CRANK_DY,z+7))).removeSplitter()
    shape.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), angle)
    if opened:
        shape.rotate(pivot, App.Vector(0, 0, 1), FLAP_OPEN_DEG)
    return shape


def link_points(angle, opened, z):
    if opened:
        q_local = (PIVOT_R-CRANK_DY, CRANK_DX)
        b_angle = LINK_PHASE + RING_OPEN_ROT_DEG
    else:
        q_local = (PIVOT_R+CRANK_DX, CRANK_DY)
        b_angle = LINK_PHASE
    qx,qy = rotate_xy(q_local[0],q_local[1],angle)
    bx,by = rotate_xy(LINK_R*math.cos(math.radians(b_angle)),
                      LINK_R*math.sin(math.radians(b_angle)),angle)
    return App.Vector(qx,qy,z+20),App.Vector(bx,by,z+20)


def drive_ring(z, opened=False):
    # One-piece conceptual rotary spider with external gear teeth and six link pins.
    ring_angle = RING_OPEN_ROT_DEG if opened else 0.0
    root_r = RING_PITCH_R - GEAR_MODULE/2
    parts = [annulus(root_r,root_r-5,6,z+20)]
    root_width = 1.7*GEAR_MODULE
    tip_width = 1.05*GEAR_MODULE
    for k in range(RING_TEETH):
        a = k*360/RING_TEETH
        r0 = RING_PITCH_R-GEAR_MODULE/2
        r1 = RING_PITCH_R+GEAR_MODULE/2
        wire = Part.makePolygon([
            App.Vector(r0,-root_width/2,z+20), App.Vector(r1,-tip_width/2,z+20),
            App.Vector(r1,tip_width/2,z+20), App.Vector(r0,root_width/2,z+20),
            App.Vector(r0,-root_width/2,z+20)])
        tooth = Part.Face(wire).extrude(App.Vector(0,0,6))
        tooth.rotate(App.Vector(0,0,0),App.Vector(0,0,1),a)
        parts.append(tooth)
    for j in range(6):
        a = j*60
        spoke = Part.makeBox(root_r-LINK_R,6,6,
                             App.Vector(LINK_R,-3,z+20))
        spoke.rotate(App.Vector(0,0,0),App.Vector(0,0,1),a+LINK_PHASE)
        parts.append(spoke)
        x,y=rotate_xy(LINK_R*math.cos(math.radians(LINK_PHASE)),
                      LINK_R*math.sin(math.radians(LINK_PHASE)),a)
        anchor=Part.makeCylinder(4.5,6,App.Vector(x,y,z+20))
        anchor=anchor.cut(Part.makeCylinder(2.15,6,App.Vector(x,y,z+20)))
        parts.append(anchor)
    # Reinforced lock lug: a spring-loaded 6 mm steel pin drops into this
    # bushing seat only at the closed stop. It is released before ring motion.
    lug=Part.makeBox(12,16,6,App.Vector(-LOCK_RADIUS-6,-8,z+20))
    lug=lug.cut(Part.makeCylinder(4.05,8,
                    App.Vector(-LOCK_RADIUS,0,z+19)))
    parts.append(lug)
    shape=Part.makeCompound(parts)
    if opened:
        shape.rotate(App.Vector(0,0,0),App.Vector(0,0,1),ring_angle)
    return shape


def pinion(z):
    # Approximate 12-tooth spur pinion at the module-matched center distance.
    r=PINION_PITCH_R
    cx=PINION_CENTER_R
    parts=[Part.makeCylinder(r-GEAR_MODULE/2,6,App.Vector(cx,0,z+20))]
    root_width = 1.7*GEAR_MODULE
    tip_width = 1.05*GEAR_MODULE
    for k in range(PINION_TEETH):
        # Half-tooth phase puts a pinion gap opposite the ring tooth at +X.
        a=k*360/PINION_TEETH + 180/PINION_TEETH
        r0 = r-GEAR_MODULE/2
        r1 = r+GEAR_MODULE/2
        wire = Part.makePolygon([
            App.Vector(cx+r0,-root_width/2,z+20), App.Vector(cx+r1,-tip_width/2,z+20),
            App.Vector(cx+r1,tip_width/2,z+20), App.Vector(cx+r0,root_width/2,z+20),
            App.Vector(cx+r0,-root_width/2,z+20)])
        tooth=Part.Face(wire).extrude(App.Vector(0,0,6))
        tooth.rotate(App.Vector(cx,0,0),App.Vector(0,0,1),a)
        parts.append(tooth)
    return Part.makeCompound(parts)


def connecting_link(p1, p2, z):
    """Flat link with bored eyelets at both pivot centers; no solid rod through pins."""
    dx, dy = p2.x-p1.x, p2.y-p1.y
    length = math.hypot(dx,dy)
    angle = math.degrees(math.atan2(dy,dx))
    link_z = z+16
    bar = Part.makeBox(length,7.0,3.0,App.Vector(0,-3.5,link_z))
    bar.rotate(App.Vector(0,0,link_z),App.Vector(0,0,1),angle)
    bar.translate(App.Vector(p1.x,p1.y,0))
    for p in (p1,p2):
        eye = Part.makeCylinder(5.5,3.0,App.Vector(p.x,p.y,link_z))
        bar = bar.fuse(eye)
    for p in (p1,p2):
        bore = Part.makeCylinder(2.15,3.2,App.Vector(p.x,p.y,link_z-0.1))
        bar = bar.cut(bore)
    return bar.removeSplitter()


assert abs(gap - pitch) < 1e-6
assert abs((package_z0 + body_h + lid_h) - (package_z0 + pitch)) < 1e-6

# Two fixed support rings, each with six hinged flaps and an actuator ring.
for stage, z in enumerate((0.0, gap), 1):
    carrier = annulus(F["outside_diameter"]/2, F["ring_inside_diameter"]/2,
                      F["plate_thickness"], z)
    for j in range(6):
        carrier = carrier.cut(Part.makeCylinder(2.75, F["plate_thickness"]+2,
                           polar(PIVOT_R,j*60)+App.Vector(0,0,z-1)))
        carrier = carrier.cut(Part.makeCylinder(8.1,5.2,
                           polar(PIVOT_R,j*60)+App.Vector(0,0,z+2.9)))
    for a in (45, 135, 225, 315):
        carrier = carrier.cut(Part.makeCylinder(F["structural_post_diameter"]/2+0.4, F["plate_thickness"] + 2,
                           polar(F["structural_post_pcd"]/2, a) + App.Vector(0,0,z-1)))
    for hx in (-152,):
        for hy in (-10,10):
            carrier=carrier.cut(Part.makeCylinder(2.7,F["plate_thickness"]+2,
                           App.Vector(hx,hy,z-1)))
    # Radial edge relief lets the vertical servo output shaft reach the pinion
    # without passing through the fixed carrier plate.
    carrier = carrier.cut(Part.makeCylinder(3.5,F["plate_thickness"]+2,
                       App.Vector(PINION_CENTER_R,0,z-1)))
    add("Stage%d_fixed_carrier" % stage, carrier)

    for j in range(6):
        a = j * 60
        closed = flap(a, z)
        opened = flap(a, z, True)
        add("Stage%d_hinged_flap_%02d" % (stage, j+1), closed,
            color=(0.93, 0.62, 0.18))
        add("Stage%d_flap_open_ref_%02d" % (stage, j+1), opened, "open",
            color=(0.96, 0.82, 0.35))
        # Vertical hinge pin and a support boss on the carrier.
        p = polar(PIVOT_R, a)
        bearing=Part.makeCylinder(8.0,5.0,p+App.Vector(0,0,z+3))
        bearing=bearing.cut(Part.makeCylinder(2.5,5.2,p+App.Vector(0,0,z+2.9)))
        add("Stage%d_hinge_bearing_%02d_625_2RS" % (stage,j+1),
            bearing,color=(0.48,0.51,0.55))
        add("Stage%d_hinge_pin_%02d_STEEL_5mm" % (stage, j+1),
            Part.makeCylinder(2.5, 15, p + App.Vector(0,0,z+3)),
            color=(0.68,0.7,0.74))

    # Reversible geared ring drives all six flaps through pinned equal-length links.
    closed_ring = drive_ring(z, False)
    open_ring = drive_ring(z, True)
    add("Stage%d_geared_sync_ring" % stage, closed_ring, color=(0.25,0.65,0.42))
    add("Stage%d_geared_sync_ring_open_ref" % stage, open_ring, "open", (0.3,0.72,0.46))
    add("Stage%d_servo_pinion" % stage, pinion(z), color=(0.72,0.32,0.2))
    open_pinion=pinion(z)
    open_pinion.rotate(App.Vector(PINION_CENTER_R,0,0),App.Vector(0,0,1),
                       -RING_OPEN_ROT_DEG*RING_TEETH/PINION_TEETH)
    add("Stage%d_servo_pinion_open_ref" % stage,open_pinion,"open",(0.76,0.36,0.22))
    for j in range(6):
        a = j * 60
        for opened, suffix, group in ((False,"closed","physical"),(True,"open_ref","open")):
            p1,p2=link_points(a,opened,z)
            link=connecting_link(p1,p2,z)
            add("Stage%d_sync_link_%02d_%s" % (stage,j+1,suffix),link,group,
                (0.35,0.55,0.38))
            add("Stage%d_flap_link_pin_%02d_%s" % (stage,j+1,suffix),
                Part.makeCylinder(2.0,8,App.Vector(p1.x,p1.y,z+11)),group,
                (0.68,0.7,0.74))
            add("Stage%d_ring_link_pin_%02d_%s" % (stage,j+1,suffix),
                Part.makeCylinder(2.0,12,App.Vector(p2.x,p2.y,z+14)),group,
                (0.68,0.7,0.74))

    # Servo body envelope. The pinion axis meets the 72:12 gear pair;
    # endpoint switches and hard stops are required for this continuous servo.
    sx, sy, sz = H["servo_body_envelope"]
    sx0 = PINION_CENTER_R - sx/2
    add("Stage%d_servo_body_ENVELOPE" % stage,
        Part.makeBox(sx, sy, sz, App.Vector(sx0, -sy/2, z-sz)),
        "envelope", (0.22,0.22,0.24))
    add("Stage%d_servo_output_shaft_ENVELOPE" % stage,
        Part.makeCylinder(3.0,24,App.Vector(PINION_CENTER_R,0,z)),
        "envelope", (0.55,0.55,0.58))
    for side,y in (("closed",-16),("open",12)):
        add("Stage%d_limit_%s_ENVELOPE" % (stage, side),
            Part.makeBox(6,4,8,App.Vector(-RING_PITCH_R-14,y,z+14)),
            "envelope", (0.85,0.25,0.18))
    add("Stage%d_positive_latch_ENVELOPE" % stage,
        Part.makeBox(8,8,10,App.Vector(-RING_PITCH_R-32,-46,z+13)),
        "envelope", (0.8,0.25,0.16))
    # Fixed reinforced latch tower and steel spring pin. In the closed state
    # the pin enters the ring lug; in the open state it is shown retracted.
    latch_leg=Part.makeBox(12,32,20,App.Vector(-158,-16,z+8))
    latch_cap=Part.makeBox(48,32,8,App.Vector(-158,-16,z+28))
    latch_bracket=latch_leg.fuse(latch_cap)
    latch_center_x=-LOCK_RADIUS
    latch_bracket=latch_bracket.cut(Part.makeCylinder(3.3,10,
                  App.Vector(latch_center_x,0,z+27)))
    # Four M5 clearance holes attach the printed bracket to the reinforced frame.
    for hx in (-152,):
        for hy in (-10,10):
            latch_bracket=latch_bracket.cut(Part.makeCylinder(2.7,40,
                   App.Vector(hx,hy,z-1)))
    add("Stage%d_reinforced_latch_bracket_PETG" % stage,
        latch_bracket.removeSplitter(),color=(0.83,0.48,0.2))
    for bolt_no,(hx,hy) in enumerate(((-152,-10),(-152,10)),1):
        bolt=Part.makeCylinder(2.5,38,App.Vector(hx,hy,z-1))
        washer=Part.makeCylinder(5.0,1.5,App.Vector(hx,hy,z-1))
        washer=washer.cut(Part.makeCylinder(2.7,1.7,App.Vector(hx,hy,z-1.1)))
        nut=Part.makeCylinder(4.2,4,App.Vector(hx,hy,z+36))
        nut=nut.cut(Part.makeCylinder(2.5,4.2,App.Vector(hx,hy,z+35.9)))
        add("Stage%d_latch_M5_through_bolt_%02d_STEEL" % (stage,bolt_no),
            Part.makeCompound([bolt,washer,nut]),color=(0.68,0.7,0.74))
    bushing=Part.makeCylinder(4.0,6,App.Vector(latch_center_x,0,z+20))
    bushing=bushing.cut(Part.makeCylinder(3.1,6.2,App.Vector(latch_center_x,0,z+19.9)))
    add("Stage%d_ring_lock_steel_bushing_8x6_ID6_2" % stage,
        bushing,color=(0.68,0.7,0.74))
    # Two fixed PETG stop shoes meet opposite tangential faces of the ring lug.
    # They define closed/open travel mechanically; contact is intentional.
    for stop_side,sy in (("closed",-12),("open",18.65)):
        support=Part.makeBox(4,4,12,App.Vector(-144,sy,z+8))
        shoe=Part.makeBox(20,4,6,App.Vector(-144,sy,z+20))
        add("Stage%d_%s_positive_hard_stop_PETG" % (stage,stop_side),
            support.fuse(shoe).removeSplitter(),color=(0.86,0.31,0.18))
    add("Stage%d_lock_pin_6mm_steel_engaged" % stage,
        Part.makeCylinder(3.0,17,App.Vector(latch_center_x,0,z+19)),
        color=(0.68,0.7,0.74))
    add("Stage%d_lock_pin_open_reference_retracted" % stage,
        Part.makeCylinder(3.0,17,App.Vector(latch_center_x,0,z+28)),
        "open",(0.72,0.74,0.78))
    add("Stage%d_lock_actuator_ENVELOPE" % stage,
        Part.makeBox(18,18,24,App.Vector(latch_center_x-9,-9,z+34)),
        "envelope",(0.22,0.22,0.24))
    for side,x,y in (("closed",-RING_PITCH_R-14,26),("open",-RING_PITCH_R-28,-4)):
        add("Stage%d_hard_stop_%s_ENVELOPE" % (stage,side),
            Part.makeBox(5,5,10,App.Vector(x,y,z+13)),
            "envelope", (0.72,0.24,0.16))

# Four load posts join the stages; four adjustable guide posts constrain the packs.
for j, a in enumerate((45,135,225,315), 1):
    add("structure_post_%d" % j,
        Part.makeCylinder(F["structural_post_diameter"]/2, gap+8,
                          polar(F["structural_post_pcd"]/2,a)),
        color=(0.55,0.57,0.6))
for j, a in enumerate((30,105,195,285), 1):
    x=F["guide_post_pcd"]/2
    # Guide rods pass through clearance windows and clamp into adjustable
    # bridge blocks at both retention stages.
    adj = F.get("guide_radial_adjustment_each_side",3.0)
    sr=H["printed_standoff_hole_pilot"]/2
    for stage,z in enumerate((0.0,gap),1):
        window=Part.makeBox(12,12,F["plate_thickness"]+2,App.Vector(x-6,-6,z-1))
        window.rotate(App.Vector(0,0,0),App.Vector(0,0,1),a)
        carrier=doc.getObject("Stage%d_fixed_carrier" % stage)
        carrier.Shape=carrier.Shape.cut(window)
        # Keep the bridge outside the full flap sweep while preserving room for
        # the radial adjustment slots and their fastener heads.
        # The external guide-post collar sits above the complete flap/ring
        # motion plane so it cannot cross the moving linkage.
        bridge=Part.makeBox(28,18,8,App.Vector(x-14,-9,z+28))
        bridge=bridge.cut(Part.makeCylinder(F["guide_post_diameter"]/2+0.4,10,
                                           App.Vector(x,0,z+27)))
        for xx in (x-7.5,x+7.5):
            for yy in (-6.5,6.5):
                slot=Part.makeBox(2*adj,2*sr,10,App.Vector(xx-adj,yy-sr,z+27))
                for sx in (xx-adj,xx+adj):
                    slot=slot.fuse(Part.makeCylinder(sr,10,App.Vector(sx,yy,z+27)))
                bridge=bridge.cut(slot)
        bridge.rotate(App.Vector(0,0,0),App.Vector(0,0,1),a)
        add("Stage%d_guide_bridge_%d" % (stage,j),bridge,color=(0.3,0.4,0.7))
    guide_center=polar(x,a)
    add("guide_post_%d_METAL_D12" % j,
        Part.makeCylinder(F["guide_post_diameter"]/2,F["guide_post_height"]+36,
                          guide_center+App.Vector(0,0,-28)),
        color=(0.68,0.7,0.74))
    # Five replaceable PETG shoe clamps ride on each metal guide post.
    adj = F.get("guide_radial_adjustment_each_side",3.0)
    for package_index in range(P["bowl"]["stack_count"]):
        package_bottom=package_z0+package_index*pitch
        contact_z=package_bottom+34.0
        body_r=base_r+(rim_r-base_r)*34.0/body_h
        shoe_inner_r=body_r+3.5
        shoe_center_r=shoe_inner_r+3.0
        arm_start=shoe_center_r+2.5
        arm=Part.makeBox(x+1-arm_start,6,6,
                         App.Vector(arm_start,-3,contact_z-3))
        shoe=Part.makeBox(6,14,8,
                          App.Vector(shoe_center_r-3,-7,contact_z-4))
        collar=Part.makeCylinder(9.5,8,App.Vector(x,0,contact_z-4))
        collar=collar.cut(Part.makeCylinder(F["guide_post_diameter"]/2+0.2,8.2,
                                           App.Vector(x,0,contact_z-4.1)))
        split=Part.makeBox(1.5,10,10,App.Vector(x-0.75,0,contact_z-5))
        collar=collar.cut(split)
        left_ear=Part.makeBox(5.25,4,8,App.Vector(x-6,6,contact_z-4))
        right_ear=Part.makeBox(5.25,4,8,App.Vector(x+0.75,6,contact_z-4))
        clamp=collar.fuse(left_ear).fuse(right_ear)
        clamp=clamp.cut(Part.makeCylinder(1.7,12,App.Vector(x-6,8,contact_z),
                                         App.Vector(1,0,0)))
        support=Part.makeCompound([clamp,arm,shoe])
        support.rotate(App.Vector(0,0,0),App.Vector(0,0,1),a)
        add("guide_shoe_%d_%02d_PETG_clamp" % (j,package_index+1),
            support,color=(0.45,0.58,0.67))
        screw=Part.makeCylinder(1.5,11,App.Vector(x-5.5,8,contact_z),
                                App.Vector(1,0,0))
        screw.rotate(App.Vector(0,0,0),App.Vector(0,0,1),a)
        add("guide_shoe_%d_%02d_M3_clamp_screw_STEEL" % (j,package_index+1),
            screw,color=(0.68,0.7,0.74))

# Five touching, lidded package envelopes show the full line capacity.
for i in range(P["bowl"]["stack_count"]):
    z=package_z0+i*pitch
    package_no=i+1
    add("L1_package_%d_body_ENVELOPE" % package_no,
        Part.makeCone(base_r,rim_r,body_h,App.Vector(0,0,z)),
        "envelope",(0.68,0.84,0.94))
    add("L1_package_%d_lid_ENVELOPE" % package_no,
        Part.makeCylinder(lid_r,lid_h,App.Vector(0,0,z+body_h)),
        "envelope",(0.76,0.9,1.0))

doc.recompute()
assembly = ROOT / "cad" / "assembly" / "one_line_pivot_prototype_closed.FCStd"
assembly.parent.mkdir(parents=True,exist_ok=True)
step_dir = ROOT / "exports" / "STEP"
step_dir.mkdir(parents=True,exist_ok=True)
Part.export(physical,str(step_dir / "one_line_pivot_prototype_closed.step"))
stl_dir = ROOT / "exports" / "STL" / "PETG_prototype"
stl_dir.mkdir(parents=True,exist_ok=True)
petg_prefixes = (
    "Stage1_fixed_carrier", "Stage2_fixed_carrier",
    "Stage1_hinged_flap_", "Stage2_hinged_flap_",
    "Stage1_geared_sync_ring", "Stage2_geared_sync_ring",
    "Stage1_servo_pinion", "Stage2_servo_pinion",
    "Stage1_sync_link_", "Stage2_sync_link_",
    "Stage1_reinforced_latch_bracket", "Stage2_reinforced_latch_bracket",
    "Stage1_closed_positive_hard_stop", "Stage2_closed_positive_hard_stop",
    "Stage1_open_positive_hard_stop", "Stage2_open_positive_hard_stop",
    "Stage1_guide_bridge_", "Stage2_guide_bridge_", "guide_shoe_",
)
for obj in physical:
    if obj.Name.startswith(petg_prefixes) and "_STEEL" not in obj.Name:
        Mesh.export([obj],str(stl_dir / ("pivot_"+obj.Name+".stl")))

# Save a separate open-state file so the closed and open positions are never
# overlaid accidentally in a GUI or manufacturing export.
open_map = {}
for obj in open_refs:
    n=obj.Name
    if "flap_open_ref_" in n:
        target=n.replace("_flap_open_ref_","_hinged_flap_")
    elif n.endswith("_geared_sync_ring_open_ref"):
        target=n.replace("_geared_sync_ring_open_ref","_geared_sync_ring")
    elif n.endswith("_servo_pinion_open_ref"):
        target=n.replace("_servo_pinion_open_ref","_servo_pinion")
    elif "_sync_link_" in n:
        target=n.replace("_open_ref","_closed")
    elif "_flap_link_pin_" in n or "_ring_link_pin_" in n:
        target=n.replace("_open_ref","_closed")
    elif "lock_pin_open_reference_retracted" in n:
        target=n.replace("_lock_pin_open_reference_retracted","_lock_pin_6mm_steel_engaged")
    else:
        continue
    open_map[target]=obj.Shape.copy()
    doc.removeObject(n)
doc.recompute()
assembly_group=doc.addObject("App::DocumentObjectGroup","OneLineCompleteAssembly")
assembly_group.Label="One line - fully assembled prototype"
package_group=doc.addObject("App::DocumentObjectGroup","PackageEnvelopes")
package_group.Label="Package fit envelopes (toggle visibility)"
control_group=doc.addObject("App::DocumentObjectGroup","ControlEnvelopes")
control_group.Label="Unvalidated control envelopes (toggle visibility)"
for obj in list(doc.Objects):
    if obj in (assembly_group,package_group,control_group):
        continue
    if obj.Name.startswith("L1_package_"):
        package_group.addObject(obj)
    elif "ENVELOPE" in obj.Name and not (
        "servo_body_ENVELOPE" in obj.Name or "servo_output_shaft_ENVELOPE" in obj.Name
    ):
        control_group.addObject(obj)
    else:
        assembly_group.addObject(obj)
assembly_group.addObject(package_group)
assembly_group.addObject(control_group)
doc.saveAs(str(assembly))

def export_compound(path):
    shapes=[obj.Shape.copy() for obj in doc.Objects
            if hasattr(obj,"Shape") and not obj.Shape.isNull()]
    tmp=App.newDocument("AssemblyExport")
    unit=tmp.addObject("Part::Feature","OneLineAssembledUnit")
    unit.Shape=Part.makeCompound(shapes)
    tmp.recompute()
    Part.export([unit],str(path))
    App.closeDocument(tmp.Name)

export_compound(step_dir/"one_line_complete_assembly_closed.step")
for target,shape in open_map.items():
    doc.getObject(target).Shape=shape
doc.recompute()
open_assembly=ROOT/"cad"/"assembly"/"one_line_pivot_prototype_open.FCStd"
doc.saveAs(str(open_assembly))
Part.export(physical,str(step_dir/"one_line_pivot_prototype_open.step"))
export_compound(step_dir/"one_line_complete_assembly_open.step")
print("Generated closed/open one-line assemblies:",assembly,open_assembly)
print("Full assembly compounds plus",sum(1 for obj in physical if obj.Name.startswith(petg_prefixes) and "_STEEL" not in obj.Name),"PETG-only prototype STLs generated in",stl_dir)
