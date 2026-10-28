# Open and refresh the report

## View the saved report

1. Download the repository ZIP and extract it, or clone the repository.
2. Open `report/Northstar_Healthcare_Operations.pbix` in a compatible version of Power BI Desktop on Windows.
3. View the saved report before refreshing. Its model already contains imported data.
4. Review all four tabs. The saved Patient Demand and Coverage page selects Northgate; clear that facility slicer for a network view.

The PBIX is unchanged from the uploaded file. It still references the author's original local CSV folder. This folder does not need to exist to inspect saved imported data, but refresh requires changing the source paths.

## Change paths before refreshing

The largest table is stored as `data/fact_shift_assignments.csv.zip` to keep downloads manageable. Before refreshing Power BI, extract this ZIP into the same `data` folder so `fact_shift_assignments.csv` sits alongside the other CSVs. The Python analysis reads the ZIP directly.


Use Power Query Editor to point each of the ten CSV queries to the matching file in this repository's `data` folder. Preserve the existing transformations and column types. If the data-source settings expose a Change Source option for each file, that is another route. Verify all ten paths, not just the coverage query.

For a reusable setup, create a **Text** parameter called `DataFolder` in Power Query with a value such as `C:\Projects\healthcare-operations-powerbi\data\` (including its final separator). Each corresponding `.pq` file in `model/` preserves the original query transformations and replaces the machine-specific file path with:

```powerquery
File.Contents(DataFolder & "fact_shift_coverage.csv")
```

Replace each existing query's Advanced Editor expression with the matching example, after creating the parameter. The examples are separate text files and are **not automatically applied to the PBIX**.

Then Close & Apply, refresh, and compare against `docs/verified_metrics.json`. Save a local copy after successful refresh. The first headline checks should be 109,650 department-shifts, 99.6% coverage, 42.2% undercoverage, and 8,153 incidents with full-period/all-facility filters.

## Things to check during the Desktop presentation rehearsal

- Use an explicit date/year filter when comparing years. The staffing page uses `month_number`, which groups January from both years together.
- Static finding text has its own stated scope and does not update with slicers.
- On the demand page, required and worked hours have matching fixed axis endpoints of 0–300,000. Check readability for your selected scope.
- Confirm the `dim_shift` times display correctly after refresh. Time values are exported to the nearest second to avoid floating-point truncation.
- Export or capture one clean screenshot of each page with the intended filters, and label those filters in the repository.
- Do not describe reconstructed previews as Power BI screenshots.

No Desktop refresh or UI interaction was performed during packaging.
