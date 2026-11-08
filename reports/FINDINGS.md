# Findings from the current processed snapshot

180 paired borough-months; 461,437 permit-work-type records and 241,862 incident reports. Delay parsing coverage: 94.2%. Incident share exceeds permit share in Bronx, Brooklyn, Queens, Staten Island. Manhattan has the largest absolute gap: incident share minus permit share = -19.6 percentage points. Within-borough Spearman correlations range from -0.09 to 0.20 across 5 eligible boroughs.

## Q1 — Eyad Elsafty · 16003613
Which boroughs have a larger share of bus incident reports than of permit activity?

Incident share exceeds permit share in Bronx, Brooklyn, Queens, Staten Island. Manhattan has the largest absolute gap: incident share minus permit share = -19.6 percentage points.

Limitation: Shares refer to the selected boroughs and months. They are not exposure-adjusted risk; a single selected borough has 100% of both totals.

## Q2 — Eyad Elsafty · 16003613
Do permit activity and bus incident reports rise and fall together across months?

The two series moved in the same direction in 24 of 35 consecutive monthly comparisons where both changed. By 2024-12, the permit index is 131.4 and the incident index 114.8 (starting month = 100).

Limitation: The first selected month is 100. School schedules and reporting changes can create common trends. Only complete selected-borough months are used.

## Q3 — Jana Hazem · 14003384
Which seasons show unusually high incident reporting relative to permit activity?

The largest absolute seasonal gap is +149.4 index points in STATEN ISLAND, October.

Limitation: Positive values mean incidents are further above their borough average than permits. Partial-year selections are not a full seasonal assessment.

## Q4 — Jana Hazem · 14003384
Within each borough, how closely do monthly permit and incident counts move together?

Within-borough Spearman correlations range from -0.09 to 0.20 across 5 eligible boroughs.

Limitation: Spearman correlation compares ranks, not causes. At least 12 paired months and variation in both counts are required; serial dependence remains.

## Q5 — Omar Hisham · 16008286
Are reported delays longer in high-permit months than in low-permit months?

Across the eligible borough-months, median monthly mean delay is 40.7 minutes in high-permit months and 36.6 in low/median months. The chart separates boroughs.

Limitation: High means above the borough median in the selected period. Each dot is a monthly mean with at least 10 parsed delays. School seasons can confound the comparison.

## Q6 — Omar Hisham · 16008286
Do high-permit months have a higher share of reported delays of at least 30 minutes?

The long-delay share was higher in above-median permit months in 5 of 5 comparable boroughs. Manhattan had the widest gap: 74.2% versus 57.4% in low/median months, among parsed delays.

Limitation: The denominator is parsed delays, not all incidents or journeys. A 30-minute midpoint is classified as long; changing the parser can change this percentage.

## Q7 — Anas Mohamed · 13005403
Do year-over-year permit changes coincide with year-over-year incident changes?

There are 120 year-over-year pairs. Their pooled rank correlation is 0.07.

Limitation: Each point compares a month with the same month one year earlier. Zero previous counts are excluded; reporting growth may influence both measures.

## Q8 — Anas Mohamed · 13005403
Does the association change when incidents are measured one to three months after permits?

The largest absolute exploratory lag correlation is -0.46 for MANHATTAN at lag 3 month(s), using 33 pairs. This is selected from multiple comparisons.

Limitation: A positive lag pairs permits in month t with incidents in t+lag. At least 12 calendar-aligned pairs are needed. A lagged association is not a prediction.

## Q9 — Yassin Ahmed · 16002450
How often are both permit activity and incidents above their borough medians?

BROOKLYN has the largest observed-minus-benchmark difference: +5.6 percentage points.

Limitation: The benchmark multiplies the two high-month proportions. It is descriptive, not a significance test; shared seasonality violates independence.

## Q10 — Yassin Ahmed · 16002450
Do high-permit months coincide with more students aboard the average reported incident?

Average students per reported incident was higher in above-median permit months in 2 of 5 comparable boroughs. The widest gap was in Queens: 2.7 students per valid report versus 2.1 in low/median months.

Limitation: Students are per reported incident, not unique students or total children affected. Each monthly mean requires at least 10 valid student-count reports.

## NYC use
DOB and school-transport planners can use these comparisons to nominate periods and boroughs for route-level investigation. They should check reporting coverage and school schedules before changing services. The results do not identify a construction-caused incident.