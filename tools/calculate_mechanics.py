"""Screening calculations for the pivot-flap drive; no guessed mu is measured data."""
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = json.loads((ROOT / "requirements" / "parameters.json").read_text(encoding="utf-8"))
G, B, S, A, H, K, F = (P[k] for k in (
    "gates", "bowl", "safety", "analysis_assumptions_not_validated",
    "hardware", "pivot_flap_prototype", "frame"))
out = ROOT / "simulation" / "kinematics"
out.mkdir(parents=True, exist_ok=True)
gravity = 9.81
count = G["jaw_count"]
width = G["jaw_tangential_width"]
thick = G["jaw_thickness"]
ecc = A["contact_eccentricity_from_guide_mm"]
bearing_sep = A["anti_tilt_bearing_separation_mm"]
cantilever_mm = G["jaw_radial_length"]
contact_arm_mm = K["flap_pivot_radius_mm"] - B["rim_outer_diameter"] / 2
reduction = K["sync_ring_teeth"] / K["servo_pinion_teeth"]
gear_eff = A["candidate_gear_efficiency"]
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
    bending_moment = per_loaded_jaw * cantilever_mm
    section_modulus = width * thick * thick / 6
    bending_stress = bending_moment / section_modulus
    anti_tilt_moment = per_loaded_jaw * ecc
    anti_tilt_reaction = anti_tilt_moment / bearing_sep
    for mu in A["friction_sensitivity_mu"]:
        friction_force = mu * design_load
        pivot_torque = friction_force * contact_arm_mm / 1000
        servo_torque = pivot_torque / (reduction * gear_eff)
        rows.append({
            "case": label,
            "mass_kg": mass,
            "design_load_N_K3": round(design_load, 3),
            "assumed_loaded_flaps": S["minimum_engaged_jaws_off_center"],
            "load_per_flap_N": round(per_loaded_jaw, 3),
            "flap_width_mm": width,
            "flap_bending_thickness_mm": thick,
            "cantilever_mm": cantilever_mm,
            "section_modulus_mm3": round(section_modulus, 3),
            "bending_moment_Nmm_per_flap": round(bending_moment, 3),
            "bending_stress_MPa_nominal": round(bending_stress, 3),
            "anti_tilt_eccentricity_mm_assumed": ecc,
            "anti_tilt_reaction_N_assumed": round(anti_tilt_reaction, 3),
            "mu_assumed_not_measured": mu,
            "friction_force_N": round(friction_force, 3),
            "pivot_contact_arm_mm_estimated": round(contact_arm_mm, 3),
            "pivot_friction_torque_Nm": round(pivot_torque, 4),
            "ring_pinion_reduction": round(reduction, 3),
            "gear_efficiency_assumed": gear_eff,
            "servo_torque_required_Nm_screen": round(servo_torque, 4),
            "ratio_to_30pct_stall_screen": round(servo_torque / screen_torque, 3),
        })

with (out / "force_friction_sensitivity.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)

summary = {
    "closed_free_arc_gap_mm": free_gap(G["closed_clear_aperture_diameter"] / 2),
    "open_free_arc_gap_mm": free_gap(G["open_clear_aperture_diameter"] / 2),
    "contact_arc_fraction_closed": 1 - free_gap(G["closed_clear_aperture_diameter"] / 2) /
        (2 * math.pi * (G["closed_clear_aperture_diameter"] / 2) / count),
    "flap_section_modulus_mm3": width * thick * thick / 6,
    "flap_bending_span_mm": cantilever_mm,
    "flap_contact_arm_mm_estimated": contact_arm_mm,
    "ring_pinion_reduction": reduction,
    "gear_efficiency_assumed": gear_eff,
    "servo_stall_torque_6v_Nm_vendor": torque_6v,
    "servo_screen_torque_6v_Nm_30pct_stall_not_continuous_rating": screen_torque,
    "static_design_factor_K": S["static_load_factor"],
    "status": "pivot-flap screening only; mu, contact lever, joint torque, torque-speed, PETG allowable and dynamic loads are not validated",
}
(out / "calculation_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print("closed/open free gap (mm):", round(summary["closed_free_arc_gap_mm"], 2), round(summary["open_free_arc_gap_mm"], 2))
print("pivot ring/pinion ratio:", round(reduction, 2), "; estimated lever mm:", round(contact_arm_mm, 2))
print("6V stall/screen torque (Nm):", round(torque_6v, 3), round(screen_torque, 3))
print("wrote", len(rows), "pivot friction sensitivity rows")
