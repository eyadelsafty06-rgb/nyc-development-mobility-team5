"""Tests for decisions that can change the reported results."""
import json
import numpy as np
import pandas as pd
from pipeline import parse_delay, integrate, clean, ROOT
from charts import tables, figure, insight


def small_aggregates():
    h = pd.DataFrame([['BROOKLYN', '2022-01-01', 'A', 10], ['QUEENS', '2022-01-01', 'A', 5]],
                     columns=['borough', 'month', 'category', 'permits'])
    t = pd.DataFrame([
        ['BROOKLYN', '2022-01-01', 'X', 2, 20, 2, 0, 10, 2],
        ['BROOKLYN', '2022-01-01', 'Y', 8, 320, 8, 8, 40, 8],
        ['BRONX', '2022-01-01', 'X', 1, 0, 0, 0, 0, 0]],
        columns=['borough', 'month', 'category', 'incidents', 'delay_sum', 'delay_n',
                 'long_delay_n', 'student_sum', 'student_n'])
    return h, t


def test_delay_rules():
    assert parse_delay('10-20 mins') == 15
    assert parse_delay('1.5 hours') == 90
    assert parse_delay('0') == 0
    assert np.isnan(parse_delay('30+ minutes'))
    assert np.isnan(parse_delay('20-10 min'))
    assert np.isnan(parse_delay('5 hours'))


def test_weighted_mean_and_counts_no_multiplication():
    h, t = small_aggregates()
    p = integrate(h, t)
    row = p[(p.borough == 'BROOKLYN') & (p.month == '2022-01-01')].iloc[0]
    assert row.permits == 10 and row.incidents == 10
    assert row.mean_delay == 34  # weighted mean, not (10 + 40) / 2
    assert row.long_delay_pct == 80


def test_zero_category_and_unknown_source_are_different():
    h, t = small_aggregates()
    p = integrate(h, t, 'NO SUCH CATEGORY', 'X')
    jan = p[p.month == '2022-01-01'].set_index('borough')
    assert jan.loc['BROOKLYN', 'permits'] == 0
    assert pd.isna(jan.loc['BRONX', 'permits'])
    assert pd.isna(jan.loc['QUEENS', 'incidents'])
    assert jan.loc['MANHATTAN', 'coverage'] == 'neither'
    assert pd.isna(jan.loc['BRONX', 'mean_delay'])


def test_housing_preserves_different_work_types():
    raw = pd.read_csv(ROOT / 'data/raw/housing.csv.gz', dtype='string', nrows=1)
    raw.loc[0, 'work_type'] = 'A'
    other = raw.copy()
    other.loc[0, 'work_type'] = 'B'
    cleaned, audit = clean(pd.concat([raw, raw, other], ignore_index=True), 'housing')
    assert len(cleaned) == 2
    assert audit['exact_duplicates_removed'] == 1


def test_calendar_comparisons_do_not_bridge_wrong_dates():
    h, t = small_aggregates()
    p = integrate(h, t)
    data = tables(p)
    assert data[6].empty  # no previous-year match
    assert data[7].correlation.isna().all()  # too few pairs


def test_all_charts_full_empty_and_sparse():
    from app import HOUSING, TRANSPORT
    full = integrate(HOUSING, TRANSPORT)
    selections = [full, full.iloc[0:0], full[full.borough == 'BROOKLYN'].head(1),
                  integrate(HOUSING, TRANSPORT, 'NOT PRESENT', 'NOT PRESENT')]
    for panel in selections:
        data = tables(panel)
        assert len(data) == 10
        for i in range(10):
            json.loads(figure(i, panel, data[i]).to_json())
            assert insight(i, data[i]).strip()


def test_search_is_explicit_and_rejects_unknown_words():
    from app import parse_search
    result = parse_search('Brooklyn 2022', [], [], 'ALL', 'ALL')
    assert result[:2] == (['BROOKLYN'], [2022])
    import pytest
    with pytest.raises(ValueError):
        parse_search('Brooklyn 2026', [], [], 'ALL', 'ALL')
    with pytest.raises(ValueError):
        parse_search('random text', [], [], 'ALL', 'ALL')


def test_real_dash_callback_endpoint():
    from app import server, app, BOROUGHS, YEARS, outputs
    client = server.test_client()
    assert client.get('/').status_code == 200
    assert client.get('/assets/style.css').status_code == 200
    key = next(iter(app.callback_map))
    payload = {
        'output': key,
        'outputs': [{'id': o.component_id, 'property': o.component_property} for o in outputs],
        'changedPropIds': ['generate.n_clicks'],
        'inputs': [{'id': 'generate', 'property': 'n_clicks', 'value': 1},
                   {'id': 'apply', 'property': 'n_clicks', 'value': 0},
                   {'id': 'search', 'property': 'n_submit', 'value': 0}],
        'state': [{'id': 'borough', 'property': 'value', 'value': BOROUGHS},
                  {'id': 'year', 'property': 'value', 'value': YEARS},
                  {'id': 'housing', 'property': 'value', 'value': 'ALL'},
                  {'id': 'transport', 'property': 'value', 'value': 'ALL'},
                  {'id': 'search', 'property': 'value', 'value': 'Brooklyn 2022 heavy traffic'}],
    }
    response = client.post('/_dash-update-component', json=payload)
    assert response.status_code == 200
    body = response.get_json()['response']
    assert all(f'chart-{i}' in body for i in range(10))
    assert body['borough']['value'] == ['BROOKLYN']
    assert body['year']['value'] == [2022]
    assert body['transport']['value'] == 'HEAVY TRAFFIC'
    assert body['search']['value'] == ''
    assert '12 paired borough-months' in body['story']['children']
