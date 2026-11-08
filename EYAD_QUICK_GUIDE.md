# Eyad's part — the simplest tasks

**Eyad Elsafty — 16003613 — Q1 and Q2**

Your part is to understand and review two simple charts, check basic data
quality, and check the website's headings and links. Record what you actually
did in TEAM.md. You do not need to explain the other members' code in detail.

## 1. Understand the project

We compare building-permit activity with reported school-bus incidents in
New York City. We use the same borough and month to compare the two sources.
A permit is not a completed home, and an incident report is not a bus journey.

## 2. Explain Q1: borough shares

Open the notebook section titled **Q1 — Eyad Elsafty** and run its cell.
Use all five boroughs and all three years for your first explanation.

For each borough, the code calculates:

`permit share = borough permits / all selected permits × 100`

`incident share = borough incidents / all selected incidents × 100`

The two bars compare percentages. In the supplied snapshot, Manhattan has
about **38.0% of permit records** and **18.5% of incident reports**. Its incident
share is about **19.6 percentage points lower** than its permit share.
This does not mean Manhattan is safer: we do not know the number of journeys.
Check the values again if you refresh the data or change filters.

Read `reports/Q01_chart_data.csv`. Check that each percentage column totals
approximately 100. Selecting only one borough makes both its shares 100%,
so this chart is most informative with several boroughs selected.

## 3. Explain Q2: monthly trends

Run **Q2 — Eyad Elsafty**. The two sources have different count sizes, so the
chart puts both at 100 in the first selected month:

`index = this month's count / first month's count × 100`

An index of 120 means 20% above the first month. An index of 80 means 20%
below it. If both lines rise, both counts increased relative to their own
starting levels. They do not need to have the same number of records.

In the supplied all-borough results, February 2022 is about 103.5 for permits
and 90.0 for incidents. That is about 3.5% above and 10.0% below January,
respectively. Read `reports/Q02_chart_data.csv` to verify this.
School holidays and reporting changes can affect the lines. Matching trends
do not prove that building work caused bus incidents.

## 4. Complete your basic checks

1. Read the two raw missing-value tables in the EDA section. Identify one
   column with missing values and explain the team's documented decision.
2. Confirm the cleaned borough values are BRONX, BROOKLYN, MANHATTAN, QUEENS
   and STATEN ISLAND. Other locations cannot join this five-borough analysis.
3. In the website, check the project title and all five names and IDs.
4. Click both dataset links and confirm they open the expected source pages.
5. Generate the default report. Change the year, generate again, and confirm
   that Q1 and Q2 update. Restore all years when describing the examples above.
6. Add your actual review date and findings to TEAM.md. If you change wording,
   keep the notebook and website consistent.

Code to read: the Q1 and Q2 comments in `charts.py`, your two notebook cells,
and the header/source-link sections of `app.py`. Start with the formulas here;
you do not need to memorize the whole project.
