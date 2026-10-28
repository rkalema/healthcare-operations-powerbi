# Five-minute presentation

## Opening: 30 seconds

“This project asks where a healthcare operations team should focus its staffing review. I used a synthetic two-year case study of ten fictional facilities. The key result is that a healthy network average can hide recurring shortages: worked coverage is 99.6%, but 42.2% of department-shifts fall below their modeled requirement.”

## Staffing: 75 seconds

Show Staffing Coverage Review with full-period/all-facility scope. Explain the ratio of sums and the difference between shortage frequency and shortage magnitude. Northgate has 61.2% undercoverage frequency; Harborview has 54.2%. Drill into Northgate's departments and night shift. Night scheduled coverage is 93.9%, falling to 88.5% worked coverage. This motivates reviewing both scheduling and replacement coverage.

## Overtime: 45 seconds

Show Overtime and Staffing Pressure. Northgate and Harborview have overtime reliance around 5%, alongside persistent gaps. The recommendation is to inspect allocation and timing. This analysis does not prove that overtime spending is wasteful or that cutting it improves coverage.

## Demand: 45 seconds

Show Patient Demand and Coverage with Northgate selected. In January 2025 there are 11,224 patient-days and 90.7% worked coverage. Patient-days measure accumulated census, not unique people. Recommend earlier seasonal staffing planning and a review of Emergency and Intensive Care night coverage.

## Incidents: 45 seconds

Show Operational Incidents. Northgate and Harborview have the highest incident rates per 1,000 department-shifts. Review severity and reporting practices alongside staffing. The denominator is not patient volume or care intensity, and a facility-level association does not prove causation.

## Close: 60 seconds

“Start with Northgate and Harborview, examine the affected departments and shifts, and monitor uncovered hours and shortage frequency. I would validate these modeled requirements with operational leaders before proposing staffing changes. A next phase would examine shift-level incident timing, patient acuity, skill mix, replacement response, and the cost and effect of any intervention.”

## Questions to be ready for

| Question | Defensible answer |
|---|---|
| Why not average coverage percentages? | A ratio of sums weights each shift by required hours. An unweighted average gives small and large requirements equal influence. |
| Is 99.6% safe? | This project cannot determine safety. Requirements are modeled, and local shortages can be hidden by aggregate surpluses. |
| Did staffing gaps cause incidents? | No causal analysis was performed; synthetic assumptions and reporting differences can shape associations. |
| Why use department-shifts for incident rates? | It provides a consistent operational activity denominator. Patient exposure and acuity would support a different comparison. |
| What did you validate? | Unique keys, foreign keys, full coverage/demand grids, hour reconciliation, and selected report claims. Desktop refresh and UI behavior still require rehearsal. |
| Where did the data come from? | This package contains synthetic tables recovered from the uploaded PBIX's loaded model. The original generation code was not supplied. |
| What does the GitHub preview show? | Charts reconstructed from the same embedded data, clearly labeled separately from the original Power BI interface. |

Use these notes to rehearse in your own words. Explain the business reasoning before the technical details.
