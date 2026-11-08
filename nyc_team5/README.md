# NYC Development and School-Bus Disruption

GIU · Data Engineering and Visualization · Winter 2026 · Milestone 1

This project asks whether changes in development activity coincide with
reported school-bus disruption across New York City's five boroughs.
We study January 2022 to December 2024, clean each source separately,
and combine monthly summaries. This is descriptive analysis, not a causal model.

## Start here

Open `NYC_Team5_Colab.ipynb` in Google Colab. Save a copy to Drive and run
cells in order. It creates the project files automatically. It downloads raw
records if a verified cache is not already present. A CPU runtime is enough.

The delivered ZIP includes the raw snapshot and prepared data used for testing.
The notebook includes an optional ZIP-import cell if you want to reproduce that
snapshot without downloading from NYC again. Refreshing can change counts.

The full click-by-click instructions are in `START_HERE.md`.
Eyad's two charts and basic checks are explained in `EYAD_QUICK_GUIDE.md`.
No local Python installation, credit card or Render subscription is needed
for the documented Colab + GitHub + PythonAnywhere workflow.

## Team

| Name | Student ID | Questions | Assigned work |
|---|---|---|---|
| Eyad Elsafty | 16003613 | Q1–Q2 | Missing-value and borough checks; header, labels and source links |
| Jana Hazem | 14003384 | Q3–Q4 | Housing dates, identifiers and duplicate rules; borough/year filters |
| Omar Hisham | 16008286 | Q5–Q6 | Bus versions, delay parsing and outliers; category filters |
| Anas Mohamed | 13005403 | Q7–Q8 | Aggregation and post-join checks; Generate Report callback |
| Yassin Ahmed | 16002450 | Q9–Q10 | Student-count checks and validation; search, Story and deployment |

See `TEAM.md` for the work log. Names are filled in; members still need to
record actual review, tests and changes before submission.

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

## Run locally (optional)

With Python 3.12 installed, open a terminal in the project folder:

```bash
python -m pip install -r requirements-analysis.txt
python app.py
```

Open http://127.0.0.1:8050 . The prepared data is included.
Rebuild from a verified cache: `python pipeline.py`.
Download fresh official records: `python pipeline.py --refresh`.
Run checks: `python -m pytest -q`.

## PythonAnywhere deployment (free Beginner account)

The chosen deployment path is PythonAnywhere, not Render. Keep source code on
GitHub. The PDF names hosting examples rather than requiring a specific provider.
Use the existing `eyadelsafty` account. Its expected website address is
https://eyadelsafty.pythonanywhere.com — this is a target, not a verified live URL.

In a Bash console, after uploading this version to the suggested new GitHub repo:

```bash
cd ~
git clone --depth 1 https://github.com/eyadelsafty06-rgb/nyc-development-mobility-team5.git nyc_team5
cd ~/nyc_team5
python3.12 -m venv --system-site-packages ~/nyc-team5-env
source ~/nyc-team5-env/bin/activate
python -m pip install --no-cache-dir -r requirements.txt
python -c "from app import LOAD_ERROR; assert not LOAD_ERROR, LOAD_ERROR; print('Dashboard ready')"
```

If the clone destination already exists, inspect it rather than deleting it.
The `requirements.txt` file installs only website dependencies. Full EDA runs
in Colab, avoiding an unnecessary analysis installation on the free host.

In Web → Add a new web app choose Manual configuration → Python 3.12.
If the free account already has a website, configure that existing app instead.
Set source/working directory to `/home/eyadelsafty/nyc_team5` and virtualenv to
`/home/eyadelsafty/nyc-team5-env`.
Copy the complete contents of `pythonanywhere_wsgi.py` into the WSGI editor.
Save, reload and test the website. Do not run `app.run()` or Gunicorn there.

The free plan currently lists one web app, 512 MiB storage and one-month expiry.
Check the Web tab for the renewal/extension control and keep it active through
grading. Do not upgrade or enter card details for this workflow.

Official setup references (checked 5 November 2026):
- https://www.pythonanywhere.com/registration/register/beginner/
- https://help.pythonanywhere.com/pages/FreeAccountsFeatures/
- https://help.pythonanywhere.com/pages/Flask/
- https://help.pythonanywhere.com/pages/DashWSGIConfig
- https://dash.plotly.com/dash-in-jupyter

## Files

- `NYC_Team5_Colab.ipynb`: standalone notebook with embedded project source.
- `pipeline.py`, `eda.py`, `charts.py`, `team.py`: data and chart functions.
- `app.py`, `assets/style.css`: dashboard.
- `data/raw`: compressed source extracts, schemas and timestamped manifests.
- `data/processed`: compact aggregates, integrated panel and provenance.
- `reports`: findings, cleaning audit, chart tables and verification record.
- `TEAM.md`, `RESEARCH_QUESTIONS.md`, `PROMPTS.md`: responsibilities and prompt log.
- `START_HERE.md`: complete beginner instructions.
- `pythonanywhere_wsgi.py`: ready-to-copy hosting configuration.

## Submission status

- Suggested new repository: `nyc-development-mobility-team5` (create it first).
- Actual final GitHub URL: pending team upload.
- Verified live website URL: pending deployment and live tests.
- Hosted test date: pending.
- Member work log: pending member review.

Local tests are documented in `reports/VALIDATION.md`. They do not establish
that the hosted website works. Replace pending entries with actual results.

The supplied PDF gives a deadline of **9 November 2026**. It instructs one team
email to **ICS503Data@gmail.com** containing all five student IDs, the GitHub
URL, the deployed website URL and both dataset links. Include all project files
in GitHub before that deadline; later changes are not considered.

## AI assistance

ChatGPT helped prepare the code, notebook, documentation and setup guidance.
`PROMPTS.md` records the initial request and relevant follow-up prompts.
Each member must understand and verify their assigned work. The assignment
requires the prompts to be recorded; the log does not claim independent authorship.
