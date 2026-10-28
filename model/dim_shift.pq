let
  Source = Csv.Document(File.Contents(DataFolder & "dim_shift.csv"), [Delimiter = ",", Columns = 4, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"shift_id", type text}, {"start_time", type time}, {"end_time", type time}, {"scheduled_hours", Int64.Type}})
in
  #"Changed column type"