let
  Source = Csv.Document(File.Contents(DataFolder & "dim_role.csv"), [Delimiter = ",", Columns = 3, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"role_id", type text}, {"role_name", type text}, {"base_hourly_rate_usd", Int64.Type}})
in
  #"Changed column type"