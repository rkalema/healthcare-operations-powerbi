# Metric definitions

These definitions follow the actual extracted DAX, available in `model/measures.dax`.

| Metric | Definition | Interpretation |
|---|---|---|
| Required Staff Hours | Sum of `required_staff_hours` | Modeled requirement, not a clinical standard |
| Worked Staff Hours | Sum of `worked_staff_hours` | Includes overtime |
| Coverage % | Worked / required | Weighted ratio; may exceed 100% |
| Scheduled Coverage % | Scheduled / required | Separates scheduling from realized work |
| Uncovered Staff Hours | Sum of max(0, required − worked), per coverage row | Gross gaps; never netted against other shifts' surpluses |
| Department Shifts | Count of coverage rows | One date/facility/department/shift combination |
| Undercovered Department Shifts | Count where worked < required | Any positive shortfall counts |
| Undercovered Shifts % | Undercovered / all department-shifts | Frequency, not shortfall magnitude |
| Overtime Hours | Sum of `overtime_hours` | Already included in worked hours |
| Overtime % | Overtime / worked | Not overtime / scheduled |
| Overtime Labor Cost | Sum of `overtime_labor_cost_usd` | Full recorded overtime cost, not only the premium |
| Absence % | Absence / scheduled hours | Different denominator from overtime |
| Regular Worked Hours | Worked − overtime | Avoid adding overtime twice |
| Patient Days | Sum of daily `patient_census` | Not unique people |
| Average Daily Census | Patient-days / distinct dates in `dim_date` | Date filter context defines denominator; multiple departments/facilities sum together |
| Incident Count | Count of incident rows | Reported events |
| Incidents per 1,000 Department Shifts | Incidents / department-shifts × 1,000 | Adjusts for department-shift activity only |

DAX uses `DIVIDE`, returning blank on a zero denominator by default. Do not substitute an average of row percentages for the ratios above.

## Filter compatibility

Demand is daily, not shift-level. `dim_shift` filters the coverage and incident facts but has no relationship to demand. Role and employee filter assignments only. Do not imply that demand or coverage metrics respond to an employee/role selection unless you deliberately add suitable model logic. Compare measures at compatible grains.

## Why 99.6% coverage can coexist with frequent shortages

A shift requiring 100 hours and receiving 80 has a 20-hour gap. Another requiring 100 and receiving 120 has a 20-hour surplus. Aggregate coverage is 100%, yet half the shifts are undercovered and gross uncovered hours remain 20. Staff hours at a different time or location do not automatically cover the first shift.
