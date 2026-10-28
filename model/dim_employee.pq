let
  Source = Csv.Document(File.Contents(DataFolder & "dim_employee.csv"), [Delimiter = ",", Columns = 10, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"employee_id", type text}, {"facility_id", type text}, {"home_department_id", type text}, {"role_id", type text}, {"hire_date", type date}, {"termination_date", type date}, {"employment_type", type text}, {"fte", type number}, {"base_hourly_rate_usd", type number}, {"shift_preference", type text}})
in
  #"Changed column type"