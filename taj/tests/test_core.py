from os import path
from json import loads
from pandas import read_csv

from taj import df_to_json
# from taj import multidf_to_json

here = path.abspath(path.dirname(__file__))
fixtures = path.join(here, 'fixtures')


iris = read_csv(path.join(fixtures, 'iris.csv'))


def assert_standard_props(result_json):
    assert 'index' in result_json.keys()
    assert 'columns' in result_json.keys()
    assert 'data' in result_json.keys()
    assert 'meta' in result_json.keys()

    meta = result_json['meta']
    assert 'tableType' in meta

    assert 'colors' in meta
    assert all(k in meta['colors'] for k in ['bg', 'fg'])

    assert 'index' in meta
    assert all(k in meta['index'] for k in ['type', 'name'])

    assert 'columns' in meta
    assert all(k in meta['columns'] for k in ['type', 'name', 'bins'])


def test_simple_df_to_json():
    global iris
    output_json = df_to_json(iris)

    assert output_json
    assert_standard_props(loads(output_json))


def test_multiindex_df_to_json():
    global iris
    grouped = iris.groupby('species')
    agg = grouped.agg(['min', 'max', 'mean'])

    output_json = df_to_json(agg)
    assert output_json
    assert_standard_props(loads(output_json))


def test_binning_simple():
    global iris

    bins = dict(sepal_length={'method': 'quantile',
                              'count': 4,
                              'palette': 'green'},
                petal_length={'method': 'interval',
                              'count': 4,
                              'palette': 'magma'}
                )

    output_json = df_to_json(iris, bins=bins)

    assert output_json
    assert_standard_props(loads(output_json))


def test_binning_multiindex():
    global iris
    grouped = iris.groupby('species')
    agg = grouped.agg(['min', 'max', 'mean'])

    bins = {('sepal_length','mean'): {'method': 'quantile',
                                      'count': 4,
                                      'palette': 'green'},
            ('petal_length','min'): {'method': 'interval',
                                     'count': 4,
                                     'palette': 'blue'},
            ('petal_length','max'): {'method': 'interval',
                                     'count': 4,
                                     'palette': 'red'}
            }

    output_json = df_to_json(agg, bins=bins)
    assert output_json

    dt = loads(output_json)
    assert_standard_props(dt)

    meta_cols = dt['meta'].get('columns')
    assert 'sepal_length|mean' in meta_cols['bins']
    assert 'petal_length|min' in meta_cols['bins']
    assert 'petal_length|max' in meta_cols['bins']


def test_filter_simple():
    global iris

    filterFields = ['sepal_length', 'petal_length']

    output_json = df_to_json(iris, filterFields=filterFields)

    assert output_json

    df = loads(output_json)
    m = df['meta']
    assert m['filterFields'] == filterFields


def test_filter_multiindex():
    global iris
    grouped = iris.groupby('species')
    agg = grouped.agg(['min', 'max', 'mean'])

    filterFields = [('sepal_length','mean'), ('petal_length','min')]

    output_json = df_to_json(agg, filterFields=filterFields)
    assert output_json

    df = loads(output_json)
    m = df['meta']
    print(m)
    fields_from_JSON = []
    for f in m['filterFields']:
        fields_from_JSON.append(tuple(f.split("|")) if "|" in f else f)
    assert fields_from_JSON == filterFields
