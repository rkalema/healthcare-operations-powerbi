let
  Source = Csv.Document(File.Contents(DataFolder & "dim_date.csv"), [Delimiter = ",", Columns = 8, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"date", type date}, {"year", Int64.Type}, {"quarter", type text}, {"month_number", Int64.Type}, {"month_name", type text}, {"week_number", Int64.Type}, {"day_of_week", type text}, {"is_weekend", Int64.Type}})
in
  #"Changed column type"