"""Render data-derived previews, not screenshots of Power BI."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter,FuncFormatter
R=Path(__file__).resolve().parents[1]; C='#177e89'; N='#142d4e'; O='#e38a39'; RED='#b84b54'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':N,'text.color':N,'axes.titleweight':'bold','axes.titlesize':14,'axes.titlepad':18,'axes.edgecolor':'#cdd6df','grid.alpha':.2})
c=pd.read_csv(R/'data/fact_shift_coverage.csv');p=pd.read_csv(R/'data/fact_patient_demand_daily.csv');f=pd.read_csv(R/'data/dim_facility.csv');i=pd.read_csv(R/'data/fact_operational_incidents.csv');s=pd.read_csv(R/'docs/facility_metrics.csv')
short=lambda x:x.replace(' General Hospital','').replace(' Community Hospital','').replace(' Medical Center','').replace(' Regional Hospital','').replace(' Health Center','').replace(' Memorial Hospital','').replace(' Specialty Hospital','')
def canvas(title,sub):
 fig=plt.figure(figsize=(18,10),facecolor='#f3f6fa');fig.text(.045,.94,'NORTHSTAR  /  HEALTHCARE OPERATIONS',fontsize=12,color=C,weight='bold');fig.text(.045,.89,title,fontsize=27,weight='bold');fig.text(.045,.848,sub,fontsize=12)
 fig.text(.045,.035,'Synthetic data • Jan 2024–Dec 2025 • Reconstructed from embedded model; not a Power BI screenshot',fontsize=10,color='#5a6a7a')
 return fig

def save(fig,name):fig.savefig(R/'assets'/name,dpi=110,facecolor=fig.get_facecolor());plt.close(fig)
fig=canvas('Near-full coverage hides recurring shortages','Network coverage: 99.6%  |  Undercovered department-shifts: 42.2%  |  109,650 department-shifts')
a=fig.add_axes([.16,.17,.35,.58]);b=fig.add_axes([.64,.17,.30,.58]);z=s.sort_values('undercoverage_pct'); colors=[RED if ('Northgate' in n or 'Harborview' in n) else C for n in z.facility_name]
a.barh(z.facility_name.map(short),z.undercoverage_pct,color=colors);a.set_title('Undercoverage frequency by facility');a.xaxis.set_major_formatter(PercentFormatter());a.set_xlim(0,75);a.grid(axis='x');
for k,v in enumerate(z.undercoverage_pct):a.text(v+.6,k,f'{v:.1f}%',va='center',fontsize=10)
b.bar(['Scheduled','Worked'],[93.9,88.5],color=[C,RED],width=.5);b.axhline(100,color=N,linestyle='--');b.set_ylim(0,110);b.yaxis.set_major_formatter(PercentFormatter());b.set_title('Northgate night coverage');b.text(.03,-.17,'Review scheduling and absence replacement.\nAggregate surpluses do not fill a different shift’s gap.',transform=b.transAxes,fontsize=11);save(fig,'01-staffing.png')
fig=canvas('Overtime coexists with staffing gaps','Review where overtime is allocated before proposing broad spending cuts.')
a=fig.add_axes([.07,.20,.42,.54]);b=fig.add_axes([.59,.20,.35,.54]);c['month']=pd.to_datetime(c.date).dt.to_period('M').dt.to_timestamp();m=c.groupby('month').sum(numeric_only=True)
a.plot(m.index,100*m.overtime_hours/m.worked_staff_hours,label='Overtime / worked',color=C,lw=2.5);a.plot(m.index,100*m.absence_hours/m.scheduled_staff_hours,label='Absence / scheduled',color=O,lw=2.5);a.set_title('Monthly overtime and absence rates');a.yaxis.set_major_formatter(PercentFormatter());a.legend(frameon=False);a.grid(axis='y')
b.scatter(s.undercoverage_pct,s.overtime_pct,s=100,color=C)
for row in s.itertuples():
 if 'Northgate' in row.facility_name or 'Harborview' in row.facility_name: b.annotate(short(row.facility_name),(row.undercoverage_pct,row.overtime_pct),xytext=(4,6),textcoords='offset points',fontsize=10)
b.set_title('Overtime reliance vs undercoverage');b.set_xlabel('Undercovered department-shifts (%)');b.set_ylabel('Overtime / worked hours (%)');b.margins(.25);b.grid();save(fig,'02-overtime.png')
ng=f.loc[f.facility_name.str.startswith('Northgate'),'facility_id'].iloc[0];nc=c[c.facility_id==ng];mc=nc.groupby('month').sum(numeric_only=True);p['month']=pd.to_datetime(p.date).dt.to_period('M').dt.to_timestamp();np=p[p.facility_id==ng].groupby('month').agg(patient_days=('patient_census','sum'),days=('date','nunique'))
fig=canvas('Winter demand calls for earlier coverage planning','Northgate • January 2025: 11,224 patient-days and 90.7% worked coverage of modeled requirements')
a=fig.add_axes([.07,.2,.42,.54]);b=fig.add_axes([.59,.2,.35,.54]);a.stackplot(mc.index,mc.worked_staff_hours-mc.overtime_hours,mc.overtime_hours,labels=['Regular worked hours','Overtime hours'],colors=[C,O]);a.plot(mc.index,mc.required_staff_hours,color=N,lw=2,label='Required hours');a.set_title('Northgate worked vs required staff hours');a.legend(frameon=False,loc='lower left');a.grid(axis='y')
b.plot(np.index,np.patient_days/np.days,color=C,lw=2.5);b.set_title('Northgate average daily census');b.set_ylabel('Patient-days / calendar days');b.grid(axis='y');save(fig,'03-demand.png')
fig=canvas('Prioritize incident reviews using activity-adjusted rates','Reported incidents are descriptive. Facility patterns do not establish a causal staffing effect.')
a=fig.add_axes([.07,.2,.31,.54]);b=fig.add_axes([.56,.2,.38,.54]);v=i.severity.value_counts();a.bar(v.index,v.values,color=[C,O,RED,N][:len(v)]);a.set_title('Reported incidents by severity');a.set_ylabel('Incident count');a.grid(axis='y');z=s.sort_values('incidents_per_1000_shifts');b.barh(z.facility_name.map(short),z.incidents_per_1000_shifts,color=[RED if ('Northgate' in n or 'Harborview' in n) else C for n in z.facility_name]);b.set_title('Reported incidents per 1,000 department-shifts');b.grid(axis='x');save(fig,'04-incidents.png')
