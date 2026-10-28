let
  Source = Csv.Document(File.Contents(DataFolder & "dim_department.csv"), [Delimiter = ",", Columns = 3, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"department_id", type text}, {"department_name", type text}, {"acuity_multiplier", type number}})
in
  #"Changed column type"