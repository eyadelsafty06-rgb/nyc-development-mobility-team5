"""Download two NYC sources, clean records, then join borough-month summaries."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
import re
import numpy as np
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parent
START, END = '2022-01-01', '2025-01-01'
BOROUGHS = ['BRONX', 'BROOKLYN', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND']
SOURCES = {
    'housing': {'id': 'rbx6-tga4', 'date': 'issued_date', 'columns': [
        'job_filing_number', 'work_permit', 'sequence_number', 'borough',
        'issued_date', 'approved_date', 'work_type', 'permit_status', 'zip_code',
        'bin', 'estimated_job_costs', 'latitude', 'longitude', 'filing_reason']},
    'transport': {'id': 'ez4e-fazm', 'date': 'occurred_on', 'columns': [
        'busbreakdown_id', 'occurred_on', 'created_on', 'last_updated_on', 'boro',
        'reason', 'run_type', 'how_long_delayed', 'number_of_students_on_the_bus',
        'breakdown_or_running_late', 'school_year', 'route_number']},
}
TRANSPORT_TOTALS = ['incidents', 'delay_sum', 'delay_n', 'long_delay_n', 'student_sum', 'student_n']


def prepare_folders():
    for folder in ['data/raw', 'data/processed', 'reports']:
        (ROOT / folder).mkdir(parents=True, exist_ok=True)


def extract(name):
    """Paginate the whole date window; reject incomplete or changing downloads."""
    spec = SOURCES[name]
    api = f"https://data.cityofnewyork.us/resource/{spec['id']}.json"
    schema_url = f"https://data.cityofnewyork.us/api/views/{spec['id']}.json"
    client = requests.Session()
    retry = Retry(total=4, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    client.mount('https://', HTTPAdapter(max_retries=retry))
    if os.getenv('SOCRATA_APP_TOKEN'):
        client.headers['X-App-Token'] = os.environ['SOCRATA_APP_TOKEN']

    def get(url, params=None):
        response = client.get(url, params=params, timeout=120)
        response.raise_for_status()
        return response.json()

    metadata = get(schema_url)
    fields = [c['fieldName'] for c in metadata['columns'] if not c['fieldName'].startswith(':')]
    missing = set(spec['columns']) - set(fields)
    if missing or len(fields) < 9:
        raise ValueError(f'{name}: source schema changed; missing fields: {missing}')
    where = f"{spec['date']} >= '{START}T00:00:00' AND {spec['date']} < '{END}T00:00:00'"

    def count(predicate=None):
        params = {'$select': 'count(*) as n'}
        if predicate:
            params['$where'] = predicate
        return int(get(api, params)[0]['n'])

    full_count, expected = count(), count(where)
    pages, offset = [], 0
    while offset < expected:
        records = get(api, {'$select': ','.join(spec['columns']), '$where': where,
                            '$order': ':id', '$limit': 50000, '$offset': offset})
        if not records:
            break
        pages.append(pd.DataFrame(records))
        offset += len(records)
        print(f'{name}: {offset:,} / {expected:,} records', flush=True)
    if offset != expected or count(where) != expected:
        raise RuntimeError('Incomplete or changing download. Rerun this step; no partial data accepted.')
    if metadata.get('rowsUpdatedAt') != get(schema_url).get('rowsUpdatedAt'):
        raise RuntimeError('The source changed during download. Please rerun this step.')
    if not pages:
        raise ValueError('The API returned no data in the study window.')
    frame = pd.concat(pages, ignore_index=True).reindex(columns=spec['columns'])
    prepare_folders()
    path = ROOT / f'data/raw/{name}.csv.gz'
    frame.to_csv(path, index=False, compression='gzip')
    manifest = {
        'name': metadata['name'], 'dataset_id': spec['id'],
        'full_source_rows': full_count, 'source_columns': len(fields),
        'extracted_rows': len(frame), 'extracted_columns': len(frame.columns),
        'start': START, 'end_exclusive': END,
        'retrieved_utc': datetime.now(timezone.utc).isoformat(),
        'rows_updated_at': metadata.get('rowsUpdatedAt'), 'where': where,
        'fields': spec['columns'], 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'api': api, 'download': f"https://data.cityofnewyork.us/api/views/{spec['id']}/rows.csv?accessType=DOWNLOAD",
    }
    (ROOT / f'data/raw/{name}_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    (ROOT / f'data/raw/{name}_schema.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')


def load_raw(refresh=False):
    """Reuse a verified cache, or download automatically on first run."""
    prepare_folders()
    raw, manifests = {}, {}
    for name, spec in SOURCES.items():
        path = ROOT / f'data/raw/{name}.csv.gz'
        manifest_path = ROOT / f'data/raw/{name}_manifest.json'
        if refresh or not (path.exists() and manifest_path.exists()):
            extract(name)
        manifest = json.loads(manifest_path.read_text())
        if (manifest['start'], manifest['end_exclusive']) != (START, END):
            raise ValueError('Cached study window differs. Set REFRESH=True to replace it.')
        if hashlib.sha256(path.read_bytes()).hexdigest() != manifest['sha256']:
            raise ValueError(f'{name}: checksum mismatch. Restore raw data or refresh it.')
        frame = pd.read_csv(path, dtype='string')
        if len(frame) != manifest['extracted_rows'] or set(spec['columns']) - set(frame.columns):
            raise ValueError(f'{name}: cached row count or columns do not match the manifest.')
        raw[name], manifests[name] = frame, manifest
    return raw, manifests


def parse_delay(value):
    """Minutes, hours or closed ranges only. Bare numbers mean minutes."""
    if pd.isna(value):
        return np.nan
    match = re.fullmatch(r'(\d+(?:\.\d+)?)\s*(?:-\s*(\d+(?:\.\d+)?))?\s*(min(?:ute)?s?|hr?s?|hours?)?', str(value).strip().lower())
    if not match:
        return np.nan
    low = float(match[1])
    high = float(match[2]) if match[2] else low
    if high < low:
        return np.nan
    minutes = (low + high) / 2
    if match[3] and match[3].startswith('h'):
        minutes *= 60
    return minutes if 0 <= minutes <= 240 else np.nan


def clean(frame, name):
    data = frame.copy()
    audit = {'input_rows': len(data)}
    for col in data.select_dtypes(include=['object', 'string']).columns:
        data[col] = data[col].astype('string').str.strip().replace('', pd.NA)
    before = len(data)
    data = data.drop_duplicates()
    audit['exact_duplicates_removed'] = before - len(data)
    data['date'] = pd.to_datetime(data[SOURCES[name]['date']], format='mixed', errors='coerce')
    aliases = {'1': 'MANHATTAN', '2': 'BRONX', '3': 'BROOKLYN', '4': 'QUEENS',
               '5': 'STATEN ISLAND', 'RICHMOND': 'STATEN ISLAND', 'NEW YORK': 'MANHATTAN',
               'KINGS': 'BROOKLYN', 'THE BRONX': 'BRONX'}
    geo_col = 'borough' if name == 'housing' else 'boro'
    data['borough'] = data[geo_col].str.upper().replace(aliases)
    valid = data.borough.isin(BOROUGHS) & data.date.ge(START) & data.date.lt(END)
    audit['invalid_geography_or_date_removed'] = int((~valid).sum())
    data = data.loc[valid].copy()

    if name == 'housing':
        keys = ['job_filing_number', 'work_permit', 'sequence_number']
        before = len(data)
        data = data.dropna(subset=keys)
        audit['missing_identifier_removed'] = before - len(data)
        valid_id = data.job_filing_number.str.match(r'^[BMQSX][0-9]+-', na=False)
        audit['placeholder_identifiers_removed'] = int((~valid_id).sum())
        data = data.loc[valid_id].copy()
        data['category'] = data.work_type.fillna('UNKNOWN').str.upper()
        # A permit can cover several work types and can be renewed.
        keys = keys + ['date', 'category']
        conflicts = data.duplicated(keys, keep=False)
        audit['conflicting_key_rows_excluded'] = int(conflicts.sum())
        data = data.loc[~conflicts].copy()
        data['approved_date'] = pd.to_datetime(data.approved_date, format='mixed', errors='coerce')
        audit['approval_after_issue_flagged'] = int((data.approved_date > data.date).sum())
        # Preserve these issuances: approval can be revised; approval date is not our join key.
        data['zip_code'] = data.zip_code.str.extract(r'^(\d{5})(?:-\d{4})?$')[0]
        data['cost'] = pd.to_numeric(data.estimated_job_costs.str.replace(r'[$,]', '', regex=True), errors='coerce')
        audit['negative_costs_nulled'] = int((data.cost < 0).sum())
        data.loc[data.cost < 0, 'cost'] = np.nan
        q1, q3 = data.cost.quantile([0.25, 0.75])
        data['cost_iqr_outlier'] = (data.cost < q1 - 1.5 * (q3 - q1)) | (data.cost > q3 + 1.5 * (q3 - q1))
        audit['cost_outliers_flagged_retained'] = int(data.cost_iqr_outlier.sum())
        for col, low, high in [('latitude', 40.45, 40.95), ('longitude', -74.3, -73.65)]:
            data[col] = pd.to_numeric(data[col], errors='coerce')
            data.loc[~data[col].between(low, high), col] = np.nan
    else:
        before = len(data)
        data = data.dropna(subset=['busbreakdown_id'])
        audit['missing_identifier_removed'] = before - len(data)
        for col in ['last_updated_on', 'created_on']:
            data[col] = pd.to_datetime(data[col], format='mixed', errors='coerce')
        data = data.sort_values(['last_updated_on', 'created_on'], na_position='first', kind='stable')
        # Exclude unresolved ties at the latest timestamp instead of guessing a version.
        last = data.groupby('busbreakdown_id', sort=False).tail(1)
        time_keys = ['busbreakdown_id', 'last_updated_on', 'created_on']
        candidates = data.merge(last[time_keys], on=time_keys, how='inner', validate='many_to_one')
        conflicts = candidates.duplicated('busbreakdown_id', keep=False)
        audit['latest_version_conflicts_excluded'] = int(conflicts.sum())
        audit['older_versions_removed'] = len(data) - len(candidates)
        data = candidates.loc[~conflicts].copy()
        data['category'] = data.reason.fillna('UNKNOWN').str.upper()
        data['students'] = pd.to_numeric(data.number_of_students_on_the_bus, errors='coerce')
        bad = ~data.students.between(0, 100) | (data.students % 1 != 0)
        data.loc[bad, 'students'] = np.nan
        data['delay_minutes'] = data.how_long_delayed.map(parse_delay)
        audit['students_missing_or_invalid'] = int(data.students.isna().sum())
        audit['delay_missing_or_unparsed'] = int(data.delay_minutes.isna().sum())
    data['month'] = data.date.dt.to_period('M').dt.to_timestamp()
    audit['output_rows'] = len(data)
    return data, audit


def aggregate(housing, transport):
    keys = ['borough', 'month', 'category']
    h = housing.groupby(keys).size().rename('permits').reset_index()
    transport = transport.assign(long_delay=transport.delay_minutes.ge(30).astype(int))
    t = transport.groupby(keys).agg(
        incidents=('busbreakdown_id', 'size'), delay_sum=('delay_minutes', 'sum'),
        delay_n=('delay_minutes', 'count'), long_delay_n=('long_delay', 'sum'),
        student_sum=('students', 'sum'), student_n=('students', 'count')).reset_index()
    return h, t


def integrate(housing, transport, hcategory='ALL', tcategory='ALL'):
    """One calendar row per borough/month; missing sources stay unknown."""
    keys = ['borough', 'month']
    h = housing.copy()
    t = transport.copy()
    h['month'] = pd.to_datetime(h.month)
    t['month'] = pd.to_datetime(t.month)
    source_coverage = h[keys].drop_duplicates().merge(
        t[keys].drop_duplicates(), on=keys, how='outer', indicator='coverage', validate='one_to_one')
    months = pd.date_range(START, pd.Timestamp(END) - pd.Timedelta(days=1), freq='MS')
    calendar = pd.MultiIndex.from_product([BOROUGHS, months], names=keys).to_frame(index=False)
    panel = calendar.merge(source_coverage, on=keys, how='left', validate='one_to_one')
    panel['coverage'] = panel.coverage.astype('string').fillna('neither')
    if hcategory != 'ALL':
        h = h[h.category == hcategory]
    if tcategory != 'ALL':
        t = t[t.category == tcategory]
    h = h.groupby(keys).permits.sum().reset_index()
    t = t.groupby(keys)[TRANSPORT_TOTALS].sum().reset_index()
    panel = panel.merge(h, on=keys, how='left', validate='one_to_one')
    panel = panel.merge(t, on=keys, how='left', validate='one_to_one')
    h_seen = panel.coverage.isin(['left_only', 'both'])
    t_seen = panel.coverage.isin(['right_only', 'both'])
    panel.loc[h_seen, 'permits'] = panel.loc[h_seen, 'permits'].fillna(0)
    panel.loc[t_seen, TRANSPORT_TOTALS] = panel.loc[t_seen, TRANSPORT_TOTALS].fillna(0)
    panel['mean_delay'] = panel.delay_sum / panel.delay_n.replace(0, np.nan)
    panel['long_delay_pct'] = 100 * panel.long_delay_n / panel.delay_n.replace(0, np.nan)
    panel['mean_students'] = panel.student_sum / panel.student_n.replace(0, np.nan)
    panel['delay_coverage_pct'] = 100 * panel.delay_n / panel.incidents.replace(0, np.nan)
    panel['student_coverage_pct'] = 100 * panel.student_n / panel.incidents.replace(0, np.nan)
    panel['year'] = panel.month.dt.year.astype(int)
    panel['month_number'] = panel.month.dt.month
    return panel.sort_values(keys).reset_index(drop=True)


def validate_panel(panel, housing, transport):
    assert not panel.duplicated(['borough', 'month']).any(), 'Duplicate join keys'
    assert panel.permits.sum() == len(housing), 'Housing counts changed in join'
    assert panel.incidents.sum() == len(transport), 'Incident counts changed in join'
    assert (panel.long_delay_n.dropna() <= panel.delay_n.dropna()).all()
    assert (panel.delay_n.dropna() <= panel.incidents.dropna()).all()
    assert pd.api.types.is_datetime64_any_dtype(panel.month)
    assert pd.api.types.is_integer_dtype(panel.year)


def save_results(h, t, panel, manifests, audits):
    prepare_folders()
    for name, frame in [('housing_monthly', h), ('transport_monthly', t), ('integrated', panel)]:
        frame.to_csv(ROOT / f'data/processed/{name}.csv', index=False)
    provenance = {'sources': manifests, 'cleaning': audits, 'grain': 'borough-month',
                  'processed_utc': datetime.now(timezone.utc).isoformat()}
    (ROOT / 'data/processed/provenance.json').write_text(json.dumps(provenance, indent=2), encoding='utf-8')
    pd.DataFrame(audits).to_csv(ROOT / 'reports/cleaning_audit.csv')


def build(refresh=False):
    raw, manifests = load_raw(refresh)
    housing, ah = clean(raw['housing'], 'housing')
    transport, at = clean(raw['transport'], 'transport')
    h, t = aggregate(housing, transport)
    panel = integrate(h, t)
    validate_panel(panel, housing, transport)
    save_results(h, t, panel, manifests, {'housing': ah, 'transport': at})
    return raw, manifests, housing, transport, h, t, panel


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--refresh', action='store_true')
    args = parser.parse_args()
    result = build(args.refresh)
    print(f'Created {len(result[-1])} borough-month rows.')
