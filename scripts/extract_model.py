"""Extract model-loaded synthetic tables and metadata from the supplied PBIX."""
from pathlib import Path
import re, sys
import pandas as pd
from pbixray import PBIXRay
root=Path(__file__).resolve().parents[1]
m=PBIXRay(str(Path(sys.argv[1]) if len(sys.argv)>1 else root/'report/Northstar_Healthcare_Operations.pbix'))
for table in m.tables:
 if not table.startswith(('dim_','fact_')): continue
 df=m.get_table(table)
 # Export source columns only; Month Start is a DAX calculated column.
 if table=='dim_date': df=df.drop(columns=['Month Start'],errors='ignore')
 for col in df.select_dtypes(include=['datetime','datetimetz']).columns:
  df[col]=df[col].dt.round('s').dt.strftime('%H:%M:%S' if table=='dim_shift' else '%Y-%m-%d')
 if table=='fact_shift_assignments':
  df.to_csv(root/'data'/f'{table}.csv.zip',index=False,compression={'method':'zip','archive_name':f'{table}.csv'})
 else: df.to_csv(root/'data'/f'{table}.csv',index=False)
 print(table,len(df),len(df.columns))
m.schema[m.schema.TableName.str.startswith(('dim_','fact_'))].to_csv(root/'model/schema.csv',index=False)
m.relationships.to_csv(root/'model/relationships.csv',index=False)
with open(root/'model/measures.dax','w') as f:
 for r in m.dax_measures.itertuples(): f.write(f'-- Table: {r.TableName}\n[{r.Name}] =\n{r.Expression.strip()}\n\n')
with open(root/'model/calculated_columns.dax','w') as f:
 for r in m.dax_columns.itertuples():
  if r.TableName.startswith(('dim_','fact_')): f.write(f'-- Table: {r.TableName}\n[{r.ColumnName}] =\n{r.Expression.strip()}\n\n')
for r in m.power_query.itertuples():
 exp=re.sub(r'File.Contents\("[^"]+"\)',lambda _:f'File.Contents(DataFolder & "{r.TableName}.csv")',r.Expression)
 (root/'model'/f'{r.TableName}.pq').write_text(exp)
