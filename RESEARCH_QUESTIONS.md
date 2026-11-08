# Ten questions for five members

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

## Q1
Which boroughs have a larger share of bus incident reports than of permit activity?

Shares refer to the selected boroughs and months. They are not exposure-adjusted risk; a single selected borough has 100% of both totals.

## Q2
Do permit activity and bus incident reports rise and fall together across months?

The first selected month is 100. School schedules and reporting changes can create common trends. Only complete selected-borough months are used.

## Q3
Which seasons show unusually high incident reporting relative to permit activity?

Positive values mean incidents are further above their borough average than permits. Partial-year selections are not a full seasonal assessment.

## Q4
Within each borough, how closely do monthly permit and incident counts move together?

Spearman correlation compares ranks, not causes. At least 12 paired months and variation in both counts are required; serial dependence remains.

## Q5
Are reported delays longer in high-permit months than in low-permit months?

High means above the borough median in the selected period. Each dot is a monthly mean with at least 10 parsed delays. School seasons can confound the comparison.

## Q6
Do high-permit months have a higher share of reported delays of at least 30 minutes?

The denominator is parsed delays, not all incidents or journeys. A 30-minute midpoint is classified as long; changing the parser can change this percentage.

## Q7
Do year-over-year permit changes coincide with year-over-year incident changes?

Each point compares a month with the same month one year earlier. Zero previous counts are excluded; reporting growth may influence both measures.

## Q8
Does the association change when incidents are measured one to three months after permits?

A positive lag pairs permits in month t with incidents in t+lag. At least 12 calendar-aligned pairs are needed. A lagged association is not a prediction.

## Q9
How often are both permit activity and incidents above their borough medians?

The benchmark multiplies the two high-month proportions. It is descriptive, not a significance test; shared seasonality violates independence.

## Q10
Do high-permit months coincide with more students aboard the average reported incident?

Students are per reported incident, not unique students or total children affected. Each monthly mean requires at least 10 valid student-count reports.