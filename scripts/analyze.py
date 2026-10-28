"""Recompute portfolio findings and validate model exports. Run from any directory."""
from pathlib import Path
import hashlib,json
import pandas as pd
R=Path(__file__).resolve().parents[1]
D={p.name.removesuffix('.zip').removesuffix('.csv'):pd.read_csv(p,low_memory=False) for p in sorted((R/'data').glob('*.csv*')) if not p.name.startswith('.') and (p.name.endswith('.csv') or p.name.endswith('.csv.zip'))}
c=D['fact_shift_coverage']; f=D['dim_facility']; i=D['fact_operational_incidents']; p=D['fact_patient_demand_daily']
keys=['date','facility_id','department_id','shift_id']
checks={}
for name,key in [('dim_date','date'),('dim_facility','facility_id'),('dim_department','department_id'),('dim_shift','shift_id'),('dim_role','role_id'),('dim_employee','employee_id'),('fact_shift_assignments','assignment_id'),('fact_operational_incidents','incident_id')]:
 checks[name+'_unique_key']=bool(D[name][key].notna().all() and D[name][key].is_unique)
checks['coverage_unique_grain']=not bool(c.duplicated(keys).any())
checks['demand_unique_grain']=not bool(p.duplicated(keys[:3]).any())
rels=pd.read_csv(R/'model/relationships.csv')
for rel in rels.itertuples():
 checks[f'{rel.FromTableName}.{rel.FromColumnName}_foreign_key']=bool(D[rel.FromTableName][rel.FromColumnName].isin(D[rel.ToTableName][rel.ToColumnName]).all())
checks['complete_coverage_grid']=len(c)==731*10*5*3
checks['complete_demand_grid']=len(p)==731*10*5
# Assignment totals reconcile with the model coverage fact, at its exact grain.
a=D['fact_shift_assignments']; ag=a.groupby(keys)[['worked_hours','scheduled_hours','overtime_hours','absence_hours']].sum().reset_index()
joined=c.merge(ag,on=keys,validate='one_to_one',suffixes=('','_assignment'))
for source,target in [('worked_hours','worked_staff_hours'),('scheduled_hours','scheduled_staff_hours'),('overtime_hours_assignment','overtime_hours'),('absence_hours_assignment','absence_hours')]:
 checks['assignment_reconciles_'+target]=bool((joined[source]-joined[target]).abs().max()<0.01)
c=c.assign(uncovered=(c.required_staff_hours-c.worked_staff_hours).clip(lower=0),under=c.worked_staff_hours<c.required_staff_hours)
s=c.groupby('facility_id').agg(required=('required_staff_hours','sum'),worked=('worked_staff_hours','sum'),scheduled=('scheduled_staff_hours','sum'),absence=('absence_hours','sum'),overtime=('overtime_hours','sum'),overtime_cost=('overtime_labor_cost_usd','sum'),uncovered=('uncovered','sum'),undercovered=('under','sum'),department_shifts=('under','size')).reset_index().merge(f[['facility_id','facility_name']],on='facility_id')
s['coverage_pct']=100*s.worked/s.required;s['undercoverage_pct']=100*s.undercovered/s.department_shifts;s['overtime_pct']=100*s.overtime/s.worked
s=s.merge(i.groupby('facility_id').size().rename('incidents'),on='facility_id');s['incidents_per_1000_shifts']=s.incidents/s.department_shifts*1000
s.to_csv(R/'docs/facility_metrics.csv',index=False)
ng=f.loc[f.facility_name.str.startswith('Northgate'),'facility_id'].iloc[0]
n=c[(c.facility_id==ng)&(c.shift_id=='NIGHT')];jan=c[(c.facility_id==ng)&c.date.str.startswith('2025-01')]
metrics={'period':[c.date.min(),c.date.max()],'rows':{k:len(v) for k,v in D.items()},'coverage_pct':100*c.worked_staff_hours.sum()/c.required_staff_hours.sum(),'undercoverage_pct':100*c.under.mean(),'uncovered_hours':c.uncovered.sum(),'overtime_pct':100*c.overtime_hours.sum()/c.worked_staff_hours.sum(),'overtime_labor_cost_usd':c.overtime_labor_cost_usd.sum(),'incident_count':len(i),'incidents_per_1000_shifts':len(i)/len(c)*1000,'northgate_night_scheduled_coverage_pct':100*n.scheduled_staff_hours.sum()/n.required_staff_hours.sum(),'northgate_night_worked_coverage_pct':100*n.worked_staff_hours.sum()/n.required_staff_hours.sum(),'northgate_jan2025_patient_days':int(p[(p.facility_id==ng)&p.date.str.startswith('2025-01')].patient_census.sum()),'northgate_jan2025_coverage_pct':100*jan.worked_staff_hours.sum()/jan.required_staff_hours.sum()}
(R/'docs/verified_metrics.json').write_text(json.dumps(metrics,indent=2,default=lambda v:v.item()))
checks['report_claim_network_coverage']=round(metrics['coverage_pct'],1)==99.6
checks['report_claim_undercoverage']=round(metrics['undercoverage_pct'],1)==42.2
checks['report_claim_northgate_january_patient_days']=metrics['northgate_jan2025_patient_days']==11224
(R/'docs/validation.json').write_text(json.dumps(checks,indent=2,default=lambda v:v.item()))
print(json.dumps(metrics,indent=2,default=lambda v:v.item()));print(s[['facility_name','coverage_pct','undercoverage_pct','overtime_pct','incidents_per_1000_shifts']].to_string(index=False));print('Checks:',sum(checks.values()),'/',len(checks))
if not all(checks.values()): raise SystemExit('Failed checks: '+str([k for k,v in checks.items() if not v]))
