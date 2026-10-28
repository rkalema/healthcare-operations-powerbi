let
  Source = Csv.Document(File.Contents(DataFolder & "fact_shift_assignments.csv"), [Delimiter = ",", Columns = 17, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"assignment_id", type text}, {"date", type date}, {"facility_id", type text}, {"department_id", type text}, {"shift_id", type text}, {"employee_id", type text}, {"role_id", type text}, {"scheduled_hours", Int64.Type}, {"worked_hours", Int64.Type}, {"absence_hours", Int64.Type}, {"absence_reason", type text}, {"overtime_hours", Int64.Type}, {"hourly_rate_usd", type number}, {"regular_labor_cost_usd", type number}, {"overtime_labor_cost_usd", type number}, {"shift_status", type text}, {"is_agency_staff", Int64.Type}})
in
  #"Changed column type"