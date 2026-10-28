let
  Source = Csv.Document(File.Contents(DataFolder & "fact_operational_incidents.csv"), [Delimiter = ",", Columns = 10, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"incident_id", type text}, {"date", type date}, {"facility_id", type text}, {"department_id", type text}, {"shift_id", type text}, {"incident_type", type text}, {"severity", type text}, {"impact_minutes", Int64.Type}, {"linked_to_staffing_pressure", Int64.Type}, {"reporting_delay_days", Int64.Type}})
in
  #"Changed column type"