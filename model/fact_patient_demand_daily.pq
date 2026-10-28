let
  Source = Csv.Document(File.Contents(DataFolder & "fact_patient_demand_daily.csv"), [Delimiter = ",", Columns = 10, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"date", type date}, {"facility_id", type text}, {"department_id", type text}, {"patient_census", Int64.Type}, {"admissions", Int64.Type}, {"discharges", Int64.Type}, {"acuity_index", type number}, {"required_care_hours", type number}, {"target_staff_hours", type number}, {"demand_pressure_flag", Int64.Type}})
in
  #"Changed column type"