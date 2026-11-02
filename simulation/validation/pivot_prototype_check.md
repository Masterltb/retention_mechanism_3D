# One-line PETG reinforced prototype — CAD verification

Date: 2026-11-03. CAD: FreeCAD 1.1.4. Assembly remains **concept / prototype**, not a production or load-rated release.

## Current modeled geometry

- L1 input: rim Ø175.7 mm, base Ø90 mm, body height 70 mm; provisional lid package Ø181.7 × 75 mm and 0.8 kg/package; 1.0 kg/package retained as design screening bound. Stack pitch 75 mm remains unmeasured.
- One line, two stages spaced 75 mm, six flaps per stage. Flaps are 8 mm vertical thickness × 26 mm tangential width; two motion states exported separately.
- Carrier PETG thickness 8 mm; four Ø12 mm metal structural rods at PCD276 mm. Four Ø12 mm metal guides at PCD292 mm; frame outside Ø320 mm. Each guide has five estimated profile shoes.
- Twelve 625-2RS hinge bearings (OD16/ID5/W5) fit in modeled Ø16.2 × 5 mm carrier counterbores; Ø5 mm hinge pins pass through the inner races. Verify press/clearance fit on PETG coupon and add axial pin retention before use.
- Flap hinge pins are Ø5 mm metal; connecting pins Ø4 mm metal; sync ring thickness 6 mm. 72:12 simplified gear ratio is 6:1; ring pin radius R=103 mm.
- Closed-state latch geometry: PETG bracket attached through carrier by two M5 through-bolts with washers/locknuts; 6 mm spring pin enters the ring lug's 8 mm steel bushing (ID6.2 mm). Open-state export depicts pin retracted. The return spring, actuator, bracket clearances and limit sensing remain preliminary hardware choices.
- `requirements/packaged_bowl_measurements.csv` currently contains no measured rows. Lid and body profiles, guide shoe positions and the 75 mm pitch are still estimates.

## Calculations recorded

`design/petg_reinforced_prototype.md` records vertical loading at 0.8 kg/package and 1.0 kg/package, factor K=3, 3-support and single-flap screening, and nominal flap bending stress. The worst nominal case is about 9.55 MPa for one flap carrying the entire 5×1 kg design load; applying an assumed root concentration factor 2 gives 19.1 MPa. PETG printed allowable and resulting safety factor remain **unknown** pending coupons, orientation, temperature and creep tests.

## CAD checks completed

- FreeCAD regenerated closed/open FCStd and STEP assemblies plus component STLs. Builder rejects null/invalid BRep shapes as they are created.
- `cad/scripts/inspect_one_line_assembly.py` checks major carrier, flap, synchronization, guide, lock and package pairs. Closed-state and open-state reports show **no unplanned common volume above 0.05 mm³** after excluding intentional pin/eye, pin/bushing, and shaft/gear joints.
- Reports: `exports/preview/one_line_closed_interference_report.txt` and `exports/preview/one_line_open_interference_report.txt`.

These checks cover nominal CAD shape validity and modeled clearance only. They do not prove PETG strength, actual package fit, gear mesh, latch torque capacity, servo torque, switch stopping, print tolerances or physical operation. Keep P0/P2/P3 gates open until actual 10-package measurements, hardware selection, coupon and proof-load tests, power-loss/FIFO tests, and review are complete.
