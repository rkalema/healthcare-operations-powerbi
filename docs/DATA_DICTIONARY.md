# Data dictionary

Recovered from the loaded PBIX model. Types are extraction types; see the matching `.pq` query for Power Query source types. Field names and units are retained from the model. Source generation formulas and code were not supplied.

## dim_date

| Column | Loaded type |
|---|---|
| `date` | datetime64[ns] |
| `year` | Int64 |
| `quarter` | string |
| `month_number` | Int64 |
| `month_name` | string |
| `week_number` | Int64 |
| `day_of_week` | string |
| `is_weekend` | Int64 |
| `Month Start` | datetime64[ns] |

## dim_department

| Column | Loaded type |
|---|---|
| `department_id` | string |
| `department_name` | string |
| `acuity_multiplier` | Float64 |

## dim_employee

| Column | Loaded type |
|---|---|
| `employee_id` | string |
| `facility_id` | string |
| `home_department_id` | string |
| `role_id` | string |
| `hire_date` | datetime64[ns] |
| `termination_date` | datetime64[ns] |
| `employment_type` | string |
| `fte` | Float64 |
| `base_hourly_rate_usd` | Float64 |
| `shift_preference` | string |

## dim_facility

| Column | Loaded type |
|---|---|
| `facility_id` | string |
| `facility_name` | string |
| `region` | string |
| `facility_type` | string |
| `capacity_index` | Float64 |
| `demand_index` | Float64 |
| `opened_date` | datetime64[ns] |

## dim_role

| Column | Loaded type |
|---|---|
| `role_id` | string |
| `role_name` | string |
| `base_hourly_rate_usd` | Int64 |

## dim_shift

| Column | Loaded type |
|---|---|
| `shift_id` | string |
| `start_time` | datetime64[ns] |
| `end_time` | datetime64[ns] |
| `scheduled_hours` | Int64 |

## fact_operational_incidents

| Column | Loaded type |
|---|---|
| `incident_id` | string |
| `date` | datetime64[ns] |
| `facility_id` | string |
| `department_id` | string |
| `shift_id` | string |
| `incident_type` | string |
| `severity` | string |
| `impact_minutes` | Int64 |
| `linked_to_staffing_pressure` | Int64 |
| `reporting_delay_days` | Int64 |

## fact_patient_demand_daily

| Column | Loaded type |
|---|---|
| `date` | datetime64[ns] |
| `facility_id` | string |
| `department_id` | string |
| `patient_census` | Int64 |
| `admissions` | Int64 |
| `discharges` | Int64 |
| `acuity_index` | Float64 |
| `required_care_hours` | Float64 |
| `target_staff_hours` | Float64 |
| `demand_pressure_flag` | Int64 |

## fact_shift_assignments

| Column | Loaded type |
|---|---|
| `assignment_id` | string |
| `date` | datetime64[ns] |
| `facility_id` | string |
| `department_id` | string |
| `shift_id` | string |
| `employee_id` | string |
| `role_id` | string |
| `scheduled_hours` | Int64 |
| `worked_hours` | Int64 |
| `absence_hours` | Int64 |
| `absence_reason` | string |
| `overtime_hours` | Int64 |
| `hourly_rate_usd` | Float64 |
| `regular_labor_cost_usd` | Float64 |
| `overtime_labor_cost_usd` | Float64 |
| `shift_status` | string |
| `is_agency_staff` | Int64 |

## fact_shift_coverage

| Column | Loaded type |
|---|---|
| `date` | datetime64[ns] |
| `facility_id` | string |
| `department_id` | string |
| `shift_id` | string |
| `required_staff_hours` | Float64 |
| `scheduled_staff_hours` | Int64 |
| `worked_staff_hours` | Int64 |
| `absence_hours` | Int64 |
| `overtime_hours` | Int64 |
| `regular_labor_cost_usd` | Float64 |
| `overtime_labor_cost_usd` | Float64 |
| `staffing_gap_hours` | Float64 |
| `coverage_ratio` | Float64 |
| `scheduled_headcount` | Int64 |
| `present_headcount` | Int64 |
| `agency_headcount` | Int64 |

## Interpretation notes

- `capacity_index`, `demand_index`, `acuity_multiplier`, and `acuity_index` are synthetic modeling inputs, not externally validated clinical scores.
- `required_care_hours`, `target_staff_hours`, and `required_staff_hours` have different model field names; do not assume they are interchangeable without the generator definitions.
- `staffing_gap_hours` and `coverage_ratio` are stored values. The report DAX recomputes uncovered hours and weighted coverage from required/worked hours.
- Monetary columns ending `_usd` are in US dollars. `_hours`, `_minutes`, and `_days` indicate the recorded unit.
- `linked_to_staffing_pressure`, `demand_pressure_flag`, `is_agency_staff`, and `is_weekend` are stored indicators, not evidence of causal effects.
- `start_time` and `end_time` are exported as times, despite the generic datetime type reported by the extraction schema.
- `Month Start` is a DAX calculated column and is deliberately absent from the date source CSV.
