let
  Source = Csv.Document(File.Contents(DataFolder & "dim_facility.csv"), [Delimiter = ",", Columns = 7, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"facility_id", type text}, {"facility_name", type text}, {"region", type text}, {"facility_type", type text}, {"capacity_index", type number}, {"demand_index", type number}, {"opened_date", type date}})
in
  #"Changed column type"