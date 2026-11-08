"""Names, questions and proposed responsibilities for the five-member team."""
TEAM = [
    ('Eyad Elsafty', '16003613', 'Q1–Q2', 'Missing-value and borough checks; header, labels and source links'),
    ('Jana Hazem', '14003384', 'Q3–Q4', 'Housing dates, identifiers and duplicate rules; borough/year filters'),
    ('Omar Hisham', '16008286', 'Q5–Q6', 'Bus versions, delay parsing and outliers; category filters'),
    ('Anas Mohamed', '13005403', 'Q7–Q8', 'Aggregation and post-join checks; Generate Report callback'),
    ('Yassin Ahmed', '16002450', 'Q9–Q10', 'Student-count checks and validation; search, Story and deployment'),
]
QUESTIONS = [
    ('Which boroughs have a larger share of bus incident reports than of permit activity?', 'Grouped percentage bars'),
    ('Do permit activity and bus incident reports rise and fall together across months?', 'Two indexed time-series lines'),
    ('Which seasons show unusually high incident reporting relative to permit activity?', 'Borough-by-calendar-month heatmap'),
    ('Within each borough, how closely do monthly permit and incident counts move together?', 'Spearman correlation bars'),
    ('Are reported delays longer in high-permit months than in low-permit months?', 'Box plot of monthly mean delay'),
    ('Do high-permit months have a higher share of reported delays of at least 30 minutes?', 'Scatter plot with borough colours'),
    ('Do year-over-year permit changes coincide with year-over-year incident changes?', 'Percentage-change scatter plot'),
    ('Does the association change when incidents are measured one to three months after permits?', 'Lag-correlation heatmap'),
    ('How often are both permit activity and incidents above their borough medians?', 'Co-occurrence bars with a reference benchmark'),
    ('Do high-permit months coincide with more students aboard the average reported incident?', 'Scatter plot of monthly mean students'),
]

def owner(index):
    name, student_id, _, _ = TEAM[index // 2]
    return f'{name} · {student_id}'
