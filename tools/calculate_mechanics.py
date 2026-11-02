"""Screening calculations only. No guessed friction value is treated as measured."""
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = json.loads((ROOT / "requirements" / "parameters.json").read_text(encoding="utf-8"))
G, B, S, A, H = (P[k] for k in ("gates", "bowl", "safety", "analysis_assumptions_not_validated", "hardware"))
out = ROOT / "simulation" / "kinematics"
out.mkdir(parents=True, exist_ok=True)
gravity = 9.81
count = G["jaw_count"]
width = G["jaw_tangential_width"]
thick = G["jaw_thickness"]
ecc = A["contact_eccentricity_from_guide_mm"]
bearing_sep = A["anti_tilt_bearing_separation_mm"]
stroke_m = G["jaw_radial_travel"] / 1000
cam_radians = math.radians(A["cam_motion_angle_deg"])
cam_lead = stroke_m / cam_radians
reduction = A["candidate_gear_reduction"]
gear_eff = A["candidate_gear_efficiency"]
cam_eff = A["cam_efficiency"]
torque_6v = H["servo_stall_torque_kgf_cm"]["6V"] * gravity / 100
screen_torque = torque_6v * A["continuous_torque_fraction_of_stall_for_screening"]


def free_gap(radius):
    half_angle = math.atan(width / (2 * radius))
    return radius * (2 * math.pi / count - 2 * half_angle)


rows = []
for label, mass in (("lower_normal", S["lower_design_mass_kg"]),
                    ("upper_normal", S["upper_design_mass_kg"]),
                    ("single_gate_fault", S["fault_mass_on_one_mechanism_kg"])):
    design_load = mass * gravity * S["static_load_factor"]
    per_loaded_jaw = design_load / S["minimum_engaged_jaws_off_center"]
    bending_moment_nmm = per_loaded_jaw * ecc
    # Rectangular cantilever. b=width, t=thickness, section modulus b*t²/6.
    section_modulus = width * thick * thick / 6
    bending_stress_mpa = bending_moment_nmm / section_modulus
    anti_tilt_force_per_jaw = bending_moment_nmm / bearing_sep
    normal_sum_loaded = design_load * (1 + 2*ecc/bearing_sep)
    for mu in A["friction_sensitivity_mu"]:
        slide_force = mu * normal_sum_loaded
        cam_torque = slide_force * cam_lead / cam_eff
        servo_torque = cam_torque / (reduction * gear_eff)
        rows.append({
            "case": label, "mass_kg": mass, "design_load_N": round(design_load, 3),
            "loaded_jaws": S["minimum_engaged_jaws_off_center"],
            "load_per_loaded_jaw_N": round(per_loaded_jaw, 3),
            "max_rim_overlap_mm": round((B["rim_outer_diameter"] - G["closed_clear_aperture_diameter"])/2, 3),
            "closed_free_arc_gap_mm": round(free_gap(G["closed_clear_aperture_diameter"]/2), 3),
            "open_free_arc_gap_mm": round(free_gap(G["open_clear_aperture_diameter"]/2), 3),
            "bending_moment_Nmm_per_jaw": round(bending_moment_nmm, 3),
            "required_anti_tilt_reaction_N_per_jaw": round(anti_tilt_force_per_jaw, 3),
            "bending_stress_MPa": round(bending_stress_mpa, 3),
            "mu_assumed_not_measured": mu,
            "slide_force_total_N": round(slide_force, 3),
            "cam_torque_Nm": round(cam_torque, 3),
            "servo_torque_with_candidate_gear_Nm": round(servo_torque, 3),
            "ratio_to_screen_continuous_torque": round(servo_torque/screen_torque, 3),
        })

with (out / "force_friction_sensitivity.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)

summary = {
    "closed_free_arc_gap_mm": free_gap(G["closed_clear_aperture_diameter"]/2),
    "open_free_arc_gap_mm": free_gap(G["open_clear_aperture_diameter"]/2),
    "contact_arc_fraction_closed": 1 - free_gap(G["closed_clear_aperture_diameter"]/2)/(2*math.pi*(G["closed_clear_aperture_diameter"]/2)/count),
    "servo_stall_torque_6v_Nm": torque_6v,
    "servo_screen_continuous_torque_6v_Nm": screen_torque,
    "cam_lead_mm_per_rad": cam_lead*1000,
    "no_load_servo_motion_time_s_at_6v_candidate_gear": A["cam_motion_angle_deg"]*reduction/60*H["servo_no_load_seconds_per_60deg"]["6V"],
    "status": "screening only; friction, anti-tilt support, cam and continuous torque must be measured",
}
(out / "calculation_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print("closed/open free gap (mm):", round(summary["closed_free_arc_gap_mm"], 2), round(summary["open_free_arc_gap_mm"], 2))
print("6V stall/screen continuous (Nm):", round(torque_6v, 3), round(screen_torque, 3))
print("wrote", len(rows), "sensitivity rows")
