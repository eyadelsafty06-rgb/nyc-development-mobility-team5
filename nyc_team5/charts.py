"""Ten research charts. Each table is also exported so results can be checked."""
import calendar
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from team import QUESTIONS, owner

COLORS = ['#2563eb', '#f97316', '#0d9488', '#a855f7', '#dc2626']
LABELS = {'permits': 'Permit-work-type records', 'incidents': 'Incident reports',
          'mean_delay': 'Monthly mean parsed delay (minutes)',
          'mean_students': 'Monthly mean reported students', 'borough': 'Borough',
          'long_delay_pct': 'Parsed delays ≥30 min (%)'}


def blank(message):
    fig = go.Figure()
    fig.add_annotation(text=message, x=.5, y=.5, xref='paper', yref='paper', showarrow=False)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return finish(fig)


def finish(fig):
    fig.update_layout(template='plotly_white', font={'family': 'Arial', 'size': 13},
                      margin={'l': 55, 'r': 25, 't': 35, 'b': 125},
                      paper_bgcolor='white', height=480, legend_title_text='',
                      legend={'orientation': 'h', 'x': 0, 'y': -.27})
    return fig


def rho(x, y, minimum=12):
    data = pd.DataFrame({'x': x, 'y': y}).dropna()
    if len(data) < minimum or data.x.nunique() < 2 or data.y.nunique() < 2:
        return np.nan
    return data.x.rank().corr(data.y.rank())


def tables(panel):
    """All comparisons use months observed in both domains, after filters."""
    paired = panel[panel.coverage == 'both'].copy()
    if paired.empty:
        return [pd.DataFrame() for _ in range(10)]
    paired['month_label'] = paired.month.dt.strftime('%Y-%m')
    paired['permit_group'] = np.where(
        paired.permits > paired.groupby('borough').permits.transform('median'),
        'High permits', 'Low / median permits')

    # Q1: shares use the same observed borough-month cohort for both measures.
    shares = paired.groupby('borough')[['permits', 'incidents']].sum()
    shares = 100 * shares.div(shares.sum().replace(0, np.nan), axis=1)
    shares['gap_pp'] = shares.incidents - shares.permits
    shares = shares.reset_index()

    # Q2: only compare totals when every selected borough has paired coverage.
    n_boroughs = panel.borough.nunique()
    counts = paired.groupby('month').borough.nunique()
    monthly = paired[paired.month.isin(counts[counts == n_boroughs].index)].groupby('month')[['permits', 'incidents']].sum()
    indexed = monthly.copy()
    if len(monthly):
        indexed = 100 * monthly.div(monthly.iloc[0].replace(0, np.nan))
        indexed = indexed.reindex(pd.date_range(monthly.index.min(), monthly.index.max(), freq='MS'))
    indexed.index.name = 'month'
    indexed = indexed.reset_index()

    # Q3: relative to each borough's own selected-period average (100 = average).
    seasonal = paired.copy()
    for col in ['permits', 'incidents']:
        seasonal[col] = 100 * seasonal[col] / seasonal.groupby('borough')[col].transform('mean').replace(0, np.nan)
    seasonal['gap'] = seasonal.incidents - seasonal.permits
    seasonal = seasonal.groupby(['borough', 'month_number']).gap.mean().reset_index()

    correlations = pd.DataFrame([{'borough': b, 'correlation': rho(g.permits, g.incidents),
                                  'months': len(g)} for b, g in paired.groupby('borough')])
    delay_groups = paired[paired.delay_n >= 10].copy()
    both_groups = delay_groups.groupby('borough').permit_group.nunique()
    delay_groups = delay_groups[delay_groups.borough.isin(both_groups[both_groups == 2].index)]
    long_delays = paired[paired.delay_n >= 10].copy()

    # Q7: exact previous-year dates; never use a 12-row shift across gaps.
    earlier = paired[['borough', 'month', 'permits', 'incidents']].copy()
    earlier['month'] = earlier.month + pd.DateOffset(years=1)
    annual = paired.merge(earlier, on=['borough', 'month'], suffixes=('', '_previous'), validate='one_to_one')
    for col in ['permits', 'incidents']:
        annual[col + '_change'] = 100 * (annual[col] / annual[col + '_previous'].replace(0, np.nan) - 1)
    annual = annual.dropna(subset=['permits_change', 'incidents_change'])

    lag_rows = []
    for b, group in paired.groupby('borough'):
        for lag in range(4):
            earlier = group[['month', 'permits']].copy()
            earlier['month'] = earlier.month + pd.DateOffset(months=lag)
            aligned = earlier.merge(group[['month', 'incidents']], on='month', validate='one_to_one')
            lag_rows.append({'borough': b, 'lag': lag, 'correlation': rho(aligned.permits, aligned.incidents), 'pairs': len(aligned)})
    lags = pd.DataFrame(lag_rows)

    co_rows = []
    for b, group in paired.groupby('borough'):
        if len(group) < 12 or group.permits.nunique() < 2 or group.incidents.nunique() < 2:
            continue
        high_h = group.permits > group.permits.median()
        high_t = group.incidents > group.incidents.median()
        co_rows.append({'borough': b, 'Observed both high': 100 * (high_h & high_t).mean(),
                        'Independence benchmark': 100 * high_h.mean() * high_t.mean(),
                        'months': len(group)})
    cooccurrence = pd.DataFrame(co_rows)
    students = paired[paired.student_n >= 10].copy()
    return [shares, indexed, seasonal, correlations, delay_groups, long_delays,
            annual, lags, cooccurrence, students]


CAVEATS = [
    'Shares refer to the selected boroughs and months. They are not exposure-adjusted risk; a single selected borough has 100% of both totals.',
    'The first selected month is 100. School schedules and reporting changes can create common trends. Only complete selected-borough months are used.',
    'Positive values mean incidents are further above their borough average than permits. Partial-year selections are not a full seasonal assessment.',
    'Spearman correlation compares ranks, not causes. At least 12 paired months and variation in both counts are required; serial dependence remains.',
    'High means above the borough median in the selected period. Each dot is a monthly mean with at least 10 parsed delays. School seasons can confound the comparison.',
    'The denominator is parsed delays, not all incidents or journeys. A 30-minute midpoint is classified as long; changing the parser can change this percentage.',
    'Each point compares a month with the same month one year earlier. Zero previous counts are excluded; reporting growth may influence both measures.',
    'A positive lag pairs permits in month t with incidents in t+lag. At least 12 calendar-aligned pairs are needed. A lagged association is not a prediction.',
    'The benchmark multiplies the two high-month proportions. It is descriptive, not a significance test; shared seasonality violates independence.',
    'Students are per reported incident, not unique students or total children affected. Each monthly mean requires at least 10 valid student-count reports.',
]


def compare_permit_groups(data, numerator, denominator, scale=1):
    """Compare high and low/median months within the same borough, using valid reports."""
    totals = data.groupby(['borough', 'permit_group'])[[numerator, denominator]].sum()
    pooled = scale * totals[numerator] / totals[denominator].replace(0, np.nan)
    return pooled.unstack().reindex(columns=['High permits', 'Low / median permits']).dropna()


def insight(index, data):
    if data.empty:
        return 'There are not enough usable observations for this selection.'
    if index == 0:
        valid = data.dropna(subset=['gap_pp'])
        if valid.empty:
            return 'At least one domain has no selected records, so shares cannot be compared.'
        if len(valid) == 1:
            return 'The one selected borough accounts for 100% of both totals. Select several boroughs to compare their shares.'
        row = valid.loc[valid.gap_pp.abs().idxmax()]
        larger = ', '.join(valid.loc[valid.gap_pp > 0.000001, 'borough'].str.title())
        comparison = f'Incident share exceeds permit share in {larger}. ' if larger else 'No borough has a higher incident share than permit share. '
        return comparison + f"{row.borough.title()} has the largest absolute gap: incident share minus permit share = {row.gap_pp:+.1f} percentage points."
    if index == 1:
        valid = data.dropna(subset=['permits', 'incidents'])
        if valid.empty:
            return 'The baseline is zero or complete source coverage is unavailable.'
        last = valid.iloc[-1]
        # Re-indexed calendar gaps remain missing, so only consecutive months count.
        changes = data[['permits', 'incidents']].diff().dropna()
        moving = changes[(changes.permits != 0) & (changes.incidents != 0)]
        same_way = int(((moving.permits > 0) == (moving.incidents > 0)).sum())
        direction = (f'The two series moved in the same direction in {same_way} of {len(moving)} consecutive monthly comparisons where both changed. '
                     if len(moving) else 'There is no consecutive monthly comparison where both series changed. ')
        return direction + f"By {last['month']:%Y-%m}, the permit index is {last.permits:.1f} and the incident index {last.incidents:.1f} (starting month = 100)."
    if index == 2:
        valid = data.dropna(subset=['gap'])
        if valid.empty:
            return 'No positive baseline counts are available.'
        row = valid.loc[valid.gap.abs().idxmax()]
        return f"The largest absolute seasonal gap is {row.gap:+.1f} index points in {row.borough}, {calendar.month_name[int(row.month_number)]}."
    if index == 3:
        valid = data.dropna(subset=['correlation'])
        if valid.empty:
            return 'No borough has at least 12 varying paired months.'
        return f"Within-borough Spearman correlations range from {valid.correlation.min():.2f} to {valid.correlation.max():.2f} across {len(valid)} eligible boroughs."
    if index == 4:
        med = data.groupby('permit_group').mean_delay.median()
        return f"Across the eligible borough-months, median monthly mean delay is {med.get('High permits', np.nan):.1f} minutes in high-permit months and {med.get('Low / median permits', np.nan):.1f} in low/median months. The chart separates boroughs."
    if index == 5:
        comparison = compare_permit_groups(data, 'long_delay_n', 'delay_n', scale=100)
        if comparison.empty:
            return 'No borough has enough parsed delays in both high- and low/median-permit months to compare their long-delay shares.'
        high, low = comparison.iloc[:, 0], comparison.iloc[:, 1]
        b = (high - low).abs().idxmax()
        return (f'The long-delay share was higher in above-median permit months in {int((high > low).sum())} of {len(comparison)} comparable boroughs. '
                f'{b.title()} had the widest gap: {high[b]:.1f}% versus {low[b]:.1f}% in low/median months, among parsed delays.')
    if index == 6:
        r = rho(data.permits_change, data.incidents_change)
        return f"There are {len(data)} year-over-year pairs. Their pooled rank correlation is {r:.2f}." if pd.notna(r) else f"There are {len(data)} year-over-year pairs, but too few or too little variation for a correlation."
    if index == 7:
        valid = data.dropna(subset=['correlation'])
        if valid.empty:
            return 'No lag has enough varying calendar-aligned observations.'
        row = valid.loc[valid.correlation.abs().idxmax()]
        return f"The largest absolute exploratory lag correlation is {row.correlation:+.2f} for {row.borough} at lag {int(row.lag)} month(s), using {int(row.pairs)} pairs. This is selected from multiple comparisons."
    if index == 8:
        gap = data['Observed both high'] - data['Independence benchmark']
        i = gap.abs().idxmax()
        return f"{data.loc[i, 'borough']} has the largest observed-minus-benchmark difference: {gap.loc[i]:+.1f} percentage points."
    comparison = compare_permit_groups(data, 'student_sum', 'student_n')
    if comparison.empty:
        return 'No borough has enough valid student counts in both high- and low/median-permit months for this comparison.'
    high, low = comparison.iloc[:, 0], comparison.iloc[:, 1]
    b = (high - low).abs().idxmax()
    return (f'Average students per reported incident was higher in above-median permit months in {int((high > low).sum())} of {len(comparison)} comparable boroughs. '
            f'The widest gap was in {b.title()}: {high[b]:.1f} students per valid report versus {low[b]:.1f} in low/median months.')


def figure(index, panel, data=None):
    data = tables(panel)[index] if data is None else data
    if data.empty:
        return blank('Not enough usable observations for these filters.')
    if index == 0:
        long = data.melt(id_vars=['borough', 'gap_pp'], value_vars=['permits', 'incidents'], var_name='Measure', value_name='Share (%)')
        fig = px.bar(long, x='borough', y='Share (%)', color='Measure', barmode='group', color_discrete_sequence=COLORS)
    elif index == 1:
        long = data.melt(id_vars='month', var_name='Measure', value_name='Index (first month = 100)')
        fig = px.line(long, x='month', y='Index (first month = 100)', color='Measure', markers=True, color_discrete_sequence=COLORS)
        fig.update_traces(connectgaps=False)
    elif index == 2:
        matrix = data.pivot(index='borough', columns='month_number', values='gap').reindex(columns=range(1, 13))
        matrix.columns = list(calendar.month_abbr)[1:]
        fig = px.imshow(matrix, color_continuous_scale='RdBu_r', color_continuous_midpoint=0,
                        aspect='auto', labels={'color': 'Index-point gap'})
    elif index == 3:
        if data.correlation.notna().sum() == 0:
            return blank('Select at least 12 months with variation in both counts.')
        fig = px.bar(data, x='borough', y='correlation', hover_data=['months'], color_discrete_sequence=COLORS)
        fig.update_yaxes(range=[-1, 1], title='Spearman correlation')
        fig.add_hline(y=0, line_color='#64748b')
    elif index == 4:
        fig = px.box(data, x='borough', y='mean_delay', color='permit_group', points='all',
                     hover_data=['month_label', 'delay_n', 'delay_coverage_pct'], labels=LABELS,
                     color_discrete_map={'High permits': '#f97316', 'Low / median permits': '#2563eb'})
    elif index == 5:
        fig = px.scatter(data, x='permits', y='long_delay_pct', color='borough',
                         hover_data=['month_label', 'delay_n', 'delay_coverage_pct'], labels=LABELS, color_discrete_sequence=COLORS)
    elif index == 6:
        fig = px.scatter(data, x='permits_change', y='incidents_change', color='borough',
                         hover_data=['month_label'], labels={'permits_change': 'Permit change vs previous year (%)',
                         'incidents_change': 'Incident change vs previous year (%)'}, color_discrete_sequence=COLORS)
        fig.add_hline(y=0, line_dash='dot')
        fig.add_vline(x=0, line_dash='dot')
    elif index == 7:
        if data.correlation.notna().sum() == 0:
            return blank('Not enough calendar-aligned pairs for lag correlations.')
        matrix = data.pivot(index='borough', columns='lag', values='correlation')
        fig = px.imshow(matrix, zmin=-1, zmax=1, aspect='auto', color_continuous_scale='RdBu_r',
                        labels={'x': 'Months after permits', 'color': 'Spearman r'}, text_auto='.2f')
    elif index == 8:
        long = data.melt(id_vars=['borough', 'months'], var_name='Measure', value_name='Months (%)')
        fig = px.bar(long, x='borough', y='Months (%)', color='Measure', barmode='group',
                     hover_data=['months'], color_discrete_sequence=COLORS)
    else:
        fig = px.scatter(data, x='permits', y='mean_students', color='borough',
                         hover_data=['month_label', 'student_n', 'student_coverage_pct'], labels=LABELS, color_discrete_sequence=COLORS)
    return finish(fig)


def figures(panel):
    data = tables(panel)
    return [figure(i, panel, data[i]) for i in range(10)]


def story(panel):
    paired = panel[panel.coverage == 'both']
    if paired.empty:
        return 'No matched borough-months for this selection. Try broader filters.'
    data = tables(panel)
    delay_n = paired.delay_n.sum()
    incidents = paired.incidents.sum()
    parsed = 100 * delay_n / incidents if incidents else 0
    return (f'{len(paired)} paired borough-months; {paired.permits.sum():,.0f} permit-work-type records and '
            f'{incidents:,.0f} incident reports. Delay parsing coverage: {parsed:.1f}%. '
            + insight(0, data[0]) + ' ' + insight(3, data[3]))


def write_findings(panel, folder):
    data = tables(panel)
    lines = ['# Findings from the current processed snapshot', '', story(panel), '']
    for i, table in enumerate(data):
        table.to_csv(folder / f'Q{i+1:02d}_chart_data.csv', index=False)
        lines += [f'## Q{i+1} — {owner(i)}', QUESTIONS[i][0], '', insight(i, table), '',
                  'Limitation: ' + CAVEATS[i], '']
    lines += ['## NYC use', 'DOB and school-transport planners can use these comparisons to nominate periods and boroughs for route-level investigation. They should check reporting coverage and school schedules before changing services. The results do not identify a construction-caused incident.']
    (folder / 'FINDINGS.md').write_text('\n'.join(lines), encoding='utf-8')
