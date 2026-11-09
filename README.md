# NYC Development and School-Bus Disruption
This project compares NYC building permit activity with reported school-bus breakdowns and delays from 2022 to 2024. We join monthly summaries by borough and use an interactive dashboard to explore the results.

- [Live dashboard](https://janahazem.pythonanywhere.com)
- [Analysis notebook](NYC_Team5_Colab_%281%29%20%282%29.ipynb)
- [Full setup guide](START_HERE.md)

## Setup

1. Download this repository as a ZIP and open the analysis notebook in Google Colab.
2. Run the setup and project-file cells, then upload the ZIP in the **Import the data snapshot** cell.
3. Keep `REFRESH = False` to use the supplied raw data. Run the remaining cells in order.

To run the dashboard locally, use Python 3.12, install the packages with `python -m pip install -r requirements.txt`, and run `python app.py`. Open http://localhost:8050.

## Deployment

1. Clone the repository into `~/nyc_team5` on PythonAnywhere. Create a Python 3.12 virtual environment and install `requirements.txt`.
2. Create a web app using **Manual configuration** and Python 3.12. Set its source and working directories to the cloned project and select the virtual environment.
3. Use `pythonanywhere_wsgi.py` as the WSGI template and update its project path to match your account.
4. Reload the web app. Open the hosted dashboard, select a borough and year, and click **Generate Report**.

See [START_HERE.md](START_HERE.md) for the full walkthrough.

## Team

| Name | Student ID | Questions | Assigned work |
|---|---|---|---|
| Eyad Elsafty | 16003613 | Q1–Q2 | missing value and borough checks; header, labels and source links |
| Jana Hazem | 14003384 | Q3–Q4 | housing dates, identifiers and duplicate rules; borough/year filters and deployment|
| Omar Hisham | 16008286 | Q5–Q6 | bus versions, delay parsing and outliers; category filters |
| Anas Mohamed | 13005403 | Q7–Q8 | Aggregation and post-join checks; Generate Report callback |
| Yassin Ahmed | 16002450 | Q9–Q10 | student count checks and validation; search, Story |

Website deployed the dashboard on PythonAnywhere and reran the notebook in Colab, where all eight tests passed. See [TEAM.md](TEAM.md) for the detailed contribution log.

## Two datasets

The course catalog lists these as H3 and T5. Both satisfy the nine-column rule.
The packaged source snapshots were retrieved on **15 October 2026**.
These are historical snapshot counts, not claims about today's live database.

| Dataset | ID | Source rows at retrieval | Source columns | Extract rows | Extract columns |
|---|---|---:|---:|---:|---:|
| DOB NOW: Build – Approved Permits | `rbx6-tga4` | 1,014,496 | 46 | 461,601 | 14 |
| Bus Breakdown and Delays | `ez4e-fazm` | 1,304,698 | 21 | 262,875 | 12 |


Housing links:
- Page: https://data.cityofnewyork.us/d/rbx6-tga4
- API: https://data.cityofnewyork.us/resource/rbx6-tga4.json
- Full CSV: https://data.cityofnewyork.us/api/views/rbx6-tga4/rows.csv?accessType=DOWNLOAD

Transportation links:
- Page: https://data.cityofnewyork.us/d/ez4e-fazm
- API: https://data.cityofnewyork.us/resource/ez4e-fazm.json
- Full CSV: https://data.cityofnewyork.us/api/views/ez4e-fazm/rows.csv?accessType=DOWNLOAD

The notebook displays the row/column counts and download times for the snapshot
actually used. `data/processed/provenance.json` records those values and cleaning
counts. The notebook regenerates `reports/DATASET_OVERVIEW.md` after a refresh.

### Why this pair and this period?

Housing `borough` and `issued_date` align with transport `boro` and `occurred_on`.
Monthly aggregation provides a meaningful time/geography bridge without linking
a particular permit to a particular incident. Daily counts are noisy; yearly
aggregation would hide school-calendar patterns. ZIP-level linkage is not used
because the selected transport fields do not offer a consistent ZIP key.

Three complete calendar years give repeated seasons, exact previous-year
comparisons and 0–3-month lags while keeping the extract practical in Colab.
The pipeline retrieves all API records in that window, not a first-page sample.
Records with missing source dates are excluded by the API time predicate and
cannot be assigned to the study window. Source metadata and pagination checks
help detect an incomplete or changing download.

Permits include several work types, renewals and non-residential activity. We
count **permit-work-type issuance records**, not completed homes or distinct
projects. DOB NOW also omits legacy BIS permits. Transport records are
vendor-reported school-bus breakdowns and delays, not all trips or general
public-transit reliability. Reported incident borough is not student residence.

## EDA and cleaning

The notebook shows raw examples, types, null patterns, distinct values,
duplicates, date coverage, category distributions and numeric summaries.
All raw columns initially load as text to preserve identifiers; the cleaning
step converts the fields that need dates or numbers.

| Issue | Decision and reason |
|---|---|
| Missing/invalid borough, event date or required ID | Exclude and count; guessing these could create a false join. |
| Missing category | Use UNKNOWN and retain the record. |
| Exact duplicates | Remove after trimming strings. |
| Repeated housing identifiers | Keep separate work types and issue dates; exclude unresolved composite-key conflicts. |
| Repeated bus IDs | Keep the latest update/creation version; exclude unresolved ties. |
| Approval after issue date | Flag and retain; approval can be revised and is not the join date. |
| Costs | Parse currency, null negative costs, flag IQR outliers and retain them. Legitimate projects may be costly; never sum costs across permits. |
| Delay descriptions | Parse numeric minutes/hours and bounded-range midpoints. Leave unsupported/open-ended text, reversed ranges and >240 minutes missing. Bare numbers mean minutes. |
| Student counts | Keep whole numbers from 0 to 100; null other values without dropping the incident. This is a conservative plausibility rule, not a verified bus-capacity limit. |
| ZIP/coordinates | Keep five-digit ZIP strings, remove valid ZIP+4 suffixes, and null invalid coordinates using a broad NYC bounding box. These fields do not drive the join. |

Numeric outcomes are not mean-imputed. Delay means and long-delay percentages
use valid parsed delays only, and their parsing coverage is reported. A zero
recorded delay is valid. Q6 classifies delays of at least 30 minutes as long.
The notebook compares the 240-minute rule with a 120-minute sensitivity rule,
and record-based permit counts with unique-permit counts.

## Integration and post-cleaning

1. Aggregate housing by borough, month and work type.
2. Aggregate transport by borough, month and reason using counts and sums.
3. Apply category filters independently, then sum to borough-month.
4. Outer-join the unique source keys and expand to the five-borough calendar.
5. Use zero for an absent selected category only within an observed source-month.
6. Keep missing-source counts unknown. Months missing in both sources are marked
   `neither`, not filled with invented events.
7. Compute weighted means from sums and valid counts. Zero denominators stay null.
8. Check unique keys, datetime/integer types, preserved totals and coverage.

All research charts use paired source-months. The prepared calendar has 180 rows;
the supplied snapshot has coverage in both sources for all 180. Category absence
means absence in this snapshot, not proof of zero real-world activity.

## Ten research questions

| Q | Question | Chart | Owner |
|---|---|---|---|
| 1 | Which boroughs have a larger share of bus incident reports than of permit activity? | Grouped percentage bars | Eyad Elsafty |
| 2 | Do permit activity and bus incident reports rise and fall together across months? | Two indexed time-series lines | Eyad Elsafty |
| 3 | Which seasons show unusually high incident reporting relative to permit activity? | Borough-by-calendar-month heatmap | Jana Hazem |
| 4 | Within each borough, how closely do monthly permit and incident counts move together? | Spearman correlation bars | Jana Hazem |
| 5 | Are reported delays longer in high-permit months than in low-permit months? | Box plot of monthly mean delay | Omar Hisham |
| 6 | Do high-permit months have a higher share of reported delays of at least 30 minutes? | Scatter plot with borough colours | Omar Hisham |
| 7 | Do year-over-year permit changes coincide with year-over-year incident changes? | Percentage-change scatter plot | Anas Mohamed |
| 8 | Does the association change when incidents are measured one to three months after permits? | Lag-correlation heatmap | Anas Mohamed |
| 9 | How often are both permit activity and incidents above their borough medians? | Co-occurrence bars with a reference benchmark | Yassin Ahmed |
| 10 | Do high-permit months coincide with more students aboard the average reported incident? | Scatter plot of monthly mean students | Yassin Ahmed |

Chart data is exported to `reports/Q01_chart_data.csv` through
`reports/Q10_chart_data.csv`. EDA diagnostics are additional quality checks,
not extra research questions. `reports/FINDINGS.md` contains computed findings
and a limitation for each question. Each notebook chart includes an observation,
evidence, limitation and practical implication.

## Dashboard

`app.py` provides four dropdowns (borough, year, work type, incident reason),
search, Generate Report, all ten figures and a Story section.

Example search: `Brooklyn 2022 heavy traffic`.
Search accepts borough names, years and exact category labels, not arbitrary
natural language. It reports unrecognized words and unavailable years.
Generate Report also applies any typed search; Apply Search stages filters.
Search text clears once consumed, so later dropdown edits are not overridden.

Empty selections and insufficient data produce explanatory chart messages.
A narrow selection may not support yearly or lag analyses. Hover, zoom and
image download are available through Plotly. No map is required because the
scatter charts already connect both domains.

## Findings and limits

Use `reports/FINDINGS.md` and the notebook for numerical findings from the
current processed snapshot. No prediction accuracy is claimed.

Borough size, school seasons, reporting changes, omitted legacy permits and
missing delay descriptions affect interpretation. No journey or population
denominator is available, so incidents are not incident rates. Correlations,
selected lag patterns and co-occurrence benchmarks are exploratory; there are
no significance tests or causal conclusions. Students may appear in multiple
reports and cannot be counted as unique children affected.

DOB and school-transport planners could investigate highlighted borough-months,
then obtain route-level and school-calendar evidence before changing services.


## Files

-  [Analysis notebook](NYC_Team5_Colab_%281%29%20%282%29.ipynb) — standalone notebook with embedded project source.
- `pipeline.py`, `eda.py`, `charts.py`, `team.py`: data and chart functions.
- `app.py`, `assets/style.css`: dashboard.
- `data/raw`: compressed source extracts, schemas and timestamped manifests.
- `data/processed`: compact aggregates, integrated panel and provenance.
- `reports`: findings, cleaning audit, chart tables and verification record.
- `TEAM.md`, `RESEARCH_QUESTIONS.md`, `PROMPTS.md`: responsibilities and prompt log.
- `START_HERE.md`: complete beginner instructions.
- `pythonanywhere_wsgi.py`: ready-to-copy hosting configuration.

## AI assistance

ChatGPT assisted with the code, notebook, and documentation. See [PROMPTS.md](PROMPTS.md) for the prompt log.


