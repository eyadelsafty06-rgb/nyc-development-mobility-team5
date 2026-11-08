"""Dash website: staged dropdowns, search, ten charts and a computed Story."""
from pathlib import Path
import re
import pandas as pd
from dash import Dash, dcc, html, Input, Output, State, ctx, no_update
from pipeline import ROOT, BOROUGHS, TRANSPORT_TOTALS, integrate
from team import TEAM, QUESTIONS, owner
from charts import blank, figure, tables, insight, story, CAVEATS


def load_data():
    h = pd.read_csv(ROOT / 'data/processed/housing_monthly.csv', parse_dates=['month'])
    t = pd.read_csv(ROOT / 'data/processed/transport_monthly.csv', parse_dates=['month'])
    if set(TRANSPORT_TOTALS) - set(t.columns):
        raise ValueError('Old processed data detected. Run the five-member notebook and export again.')
    return h, t


try:
    HOUSING, TRANSPORT = load_data()
    LOAD_ERROR = ''
except (OSError, ValueError) as exc:
    HOUSING, TRANSPORT = pd.DataFrame(), pd.DataFrame()
    LOAD_ERROR = str(exc)
YEARS = [2022, 2023, 2024]
HCATS = ['ALL'] + sorted(HOUSING.category.unique()) if not HOUSING.empty else ['ALL']
TCATS = ['ALL'] + sorted(TRANSPORT.category.unique()) if not TRANSPORT.empty else ['ALL']


def parse_search(query, boroughs, years, hcat, tcat):
    """Recognize boroughs, years and exact dropdown categories; reject unknown words."""
    remaining = re.sub(r'\s+', ' ', (query or '').upper()).strip()
    if not remaining:
        return boroughs, years, hcat, tcat
    found_b = []
    found_y = [int(y) for y in re.findall(r'\b20\d{2}\b', remaining)]
    if any(y not in YEARS for y in found_y):
        raise ValueError('Available years are 2022, 2023 and 2024.')
    for b in BOROUGHS:
        if re.search(r'\b' + re.escape(b) + r'\b', remaining):
            found_b.append(b)
            remaining = re.sub(r'\b' + re.escape(b) + r'\b', ' ', remaining)
    remaining = re.sub(r'\b20\d{2}\b', ' ', remaining)
    found_categories = []
    for options in [HCATS[1:], TCATS[1:]]:
        matches = []
        for category in sorted(options, key=len, reverse=True):
            pattern = r'(?<!\w)' + re.escape(category) + r'(?!\w)'
            if re.search(pattern, remaining):
                matches.append(category)
                remaining = re.sub(pattern, ' ', remaining)
        if len(matches) > 1:
            raise ValueError('Use one permit category and one incident reason per search.')
        found_categories.append(matches[0] if matches else 'ALL')
    if remaining.strip():
        raise ValueError('Unrecognized text: ' + remaining.strip() + '. Use boroughs, years and exact dropdown labels.')
    # Search starts from ALL for unspecified dimensions, making queries reproducible.
    return found_b or BOROUGHS, sorted(set(found_y)) or YEARS, *found_categories


def make_report(boroughs, years, hcat, tcat):
    panel = integrate(HOUSING, TRANSPORT, hcat, tcat)
    panel = panel[panel.borough.isin(boroughs or []) & panel.year.isin(years or [])]
    data = tables(panel)
    figures = [figure(i, panel, data[i]) for i in range(10)]
    notes = [insight(i, data[i]) for i in range(10)]
    coverage = f'{len(panel)} selected calendar rows; {(panel.coverage == "both").sum()} paired rows. Categories: {hcat} / {tcat}.'
    return figures + notes + [story(panel), coverage]


app = Dash(__name__, title='NYC Development & School Transport', assets_folder=str(ROOT / 'assets'))
server = app.server


def dropdown(identifier, label, options, value, multi=False):
    return html.Div([html.Label(label, htmlFor=identifier),
                     dcc.Dropdown(options=options, value=value, id=identifier, multi=multi,
                                  clearable=False)], className='filter')


app.layout = html.Main([
    html.Header([
        html.P('GIU · DATA ENGINEERING & VISUALIZATION · WINTER 2026', className='eyebrow'),
        html.H1('Building activity. School-bus disruption.'),
        html.P('Explore the relationship across five NYC boroughs, January 2022–December 2024.'),
        html.P('Five members · Two datasets · Ten research questions', className='subtitle'),
    ]),
    html.Section([
        html.H2('Choose your report'),
        html.Label('Search by borough, year or exact category'),
        html.Div([dcc.Input(id='search', type='text', placeholder='Brooklyn 2022 heavy traffic',
                           value='', debounce=False), html.Button('Apply Search', id='apply', n_clicks=0)], className='search'),
        html.Div([
            dropdown('borough', 'Borough', BOROUGHS, BOROUGHS, True),
            dropdown('year', 'Calendar year', YEARS, YEARS, True),
            dropdown('housing', 'Permit work type', HCATS, 'ALL'),
            dropdown('transport', 'Incident reason', TCATS, 'ALL'),
        ], className='filters'),
        html.Button('Generate Report', id='generate', n_clicks=0, className='primary'),
        html.P('Generate Report applies the dropdowns and any search text, then refreshes all ten charts.'),
        html.Div(id='status', role='status'),
        html.P('Data preparation error: ' + LOAD_ERROR, className='error') if LOAD_ERROR else html.Div(),
    ], className='card'),
    html.Section([
        html.H2('Our story'),
        html.P('Question: Do changes in development activity coincide with reported school-bus disruption?'),
        html.P('We count permit issuances and school-bus reports separately, then match totals for the same borough and month. A report with an unreadable delay still counts as an incident; it does not enter a delay average.'),
        html.Div('Choose filters and generate a report to see computed findings.', id='story'),
        html.P(id='coverage', className='muted'),
        html.H3('What the data cannot tell us'),
        html.P('Permits are not completed homes. School-bus reports are not all journeys. Borough size, school schedules and reporting changes can affect both series. Associations do not prove causation.'),
        html.H3('Why it matters to NYC'),
        html.P('DOB and school-transport planners can use these patterns to choose boroughs and periods for further investigation, then check routes, reporting coverage and school schedules before changing services.'),
    ], className='card'),
    dcc.Loading(html.Div([
        html.Article([
            html.P(f'Q{i+1} · {owner(i)}', className='eyebrow'), html.H2(q[0]),
            html.P(q[1], className='muted'), dcc.Graph(id=f'chart-{i}', figure=blank('Click Generate Report'),
                config={'displaylogo': False, 'responsive': True}),
            html.P(id=f'note-{i}', className='finding'), html.P(CAVEATS[i], className='caveat'),
        ], className='card') for i, q in enumerate(QUESTIONS)
    ], className='charts')),
    html.Section([
        html.H2('Team and sources'),
        html.Ul([html.Li(f'{name} · {student_id} · {qs}') for name, student_id, qs, _ in TEAM]),
        html.A('DOB NOW approved permits', href='https://data.cityofnewyork.us/d/rbx6-tga4', target='_blank'),
        html.Span(' · '), html.A('Bus Breakdown and Delays', href='https://data.cityofnewyork.us/d/ez4e-fazm', target='_blank'),
        html.P('Counts describe the downloaded snapshot. Filtered-out categories and missing source coverage are handled separately.'),
    ], className='card'),
], className='container')


outputs = ([Output(f'chart-{i}', 'figure') for i in range(10)] +
           [Output(f'note-{i}', 'children') for i in range(10)] +
           [Output('story', 'children'), Output('coverage', 'children'),
            Output('borough', 'value'), Output('year', 'value'), Output('housing', 'value'),
            Output('transport', 'value'), Output('search', 'value'), Output('status', 'children')])


@app.callback(outputs, Input('generate', 'n_clicks'), Input('apply', 'n_clicks'), Input('search', 'n_submit'),
              State('borough', 'value'), State('year', 'value'), State('housing', 'value'),
              State('transport', 'value'), State('search', 'value'), prevent_initial_call=True)
def update_report(_generate, _apply, _enter, boroughs, years, hcat, tcat, query):
    if LOAD_ERROR:
        return [no_update] * 27 + ['Upload the five-member processed data before generating a report.']
    try:
        boroughs, years, hcat, tcat = parse_search(query, boroughs, years, hcat, tcat)
    except ValueError as exc:
        return [no_update] * 27 + [str(exc)]
    selected = [boroughs, years, hcat, tcat, '']
    if ctx.triggered_id in ['apply', 'search']:
        return [no_update] * 22 + selected + ['Search applied. Click Generate Report.']
    return make_report(boroughs, years, hcat, tcat) + selected + ['Report updated.']


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8050)
