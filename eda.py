"""Simple diagnostics before and after cleaning; these are not research Q1–Q10."""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from IPython.display import display
from pipeline import ROOT, SOURCES


def inspect(name, frame):
    profile = pd.DataFrame({'type': frame.dtypes.astype(str), 'missing': frame.isna().sum(),
                            'missing_pct': frame.isna().mean().mul(100).round(2), 'distinct': frame.nunique()})
    print(name.upper(), frame.shape, '| Exact duplicate rows:', int(frame.duplicated().sum()))
    display(frame.head(3))
    display(profile)
    display(frame.describe(include='all').T)
    date = pd.to_datetime(frame[SOURCES[name]['date']], errors='coerce', format='mixed')
    print('Date range:', date.min(), 'to', date.max(), '| Unparseable:', int(date.isna().sum()))
    geo = 'borough' if name == 'housing' else 'boro'
    category = 'work_type' if name == 'housing' else 'reason'
    fig, axes = plt.subplots(1, 3, figsize=(16, 4))
    profile.missing_pct.sort_values().plot.barh(ax=axes[0], title='Missing values (%)')
    frame[geo].fillna('MISSING').value_counts().head(12).plot.bar(ax=axes[1], title='Raw geography values')
    frame[category].fillna('MISSING').value_counts().head(8).plot.barh(ax=axes[2], title='Most common categories')
    fig.suptitle(name.title() + ' — raw data checks')
    fig.tight_layout()
    fig.savefig(ROOT / f'reports/{name}_eda.png', dpi=120, bbox_inches='tight')
    plt.show()
    profile.to_csv(ROOT / f'reports/{name}_profile.csv')
    return profile


def after_cleaning(housing, transport):
    display(housing[['cost']].describe())
    display(transport[['delay_minutes', 'students']].describe())
    print('Delay values that remain missing:', int(transport.delay_minutes.isna().sum()))
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    # Limit the display only; the cleaned cost data keeps legitimate large values.
    cap = housing.cost.quantile(.99)
    sns.histplot(housing.loc[housing.cost <= cap, 'cost'].dropna(), bins=30, ax=axes[0])
    axes[0].set_title('Costs: display up to 99th percentile')
    sns.histplot(transport.delay_minutes.dropna(), bins=30, ax=axes[1])
    axes[1].set_title('Parsed delay minutes')
    sns.histplot(transport.students.dropna(), bins=25, ax=axes[2])
    axes[2].set_title('Valid student counts per report')
    fig.tight_layout()
    fig.savefig(ROOT / 'reports/clean_distributions.png', dpi=120, bbox_inches='tight')
    plt.show()
