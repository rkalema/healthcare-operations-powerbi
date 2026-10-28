let
  Source = Csv.Document(File.Contents(DataFolder & "fact_shift_coverage.csv"), [Delimiter = ",", Columns = 16, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"date", type date}, {"facility_id", type text}, {"department_id", type text}, {"shift_id", type text}, {"required_staff_hours", type number}, {"scheduled_staff_hours", Int64.Type}, {"worked_staff_hours", Int64.Type}, {"absence_hours", Int64.Type}, {"overtime_hours", Int64.Type}, {"regular_labor_cost_usd", type number}, {"overtime_labor_cost_usd", type number}, {"staffing_gap_hours", type number}, {"coverage_ratio", type number}, {"scheduled_headcount", Int64.Type}, {"present_headcount", Int64.Type}, {"agency_headcount", Int64.Type}})
in
  #"Changed column type"