from os import path
from json import loads
from pandas import read_csv

from taj import df_to_json
# from taj import multidf_to_json

here = path.abspath(path.dirname(__file__))
fixtures = path.join(here, 'fixtures')


iris = read_csv(path.join(fixtures, 'iris.csv'))

# Getting iris dataset straight from sklearn:
#
# import numpy as np
# import pandas as pd
# from sklearn.datasets import load_iris
# data = load_iris()
# feat = data.data
# spec = data.target_names[data.target]
# df = pd.DataFrame(np.column_stack((feat, spec)),
#      columns = ['_'.join(s.split()[:2]) for s in data.feature_names]+['species'])
# iris = df


def assert_standard_props(result_json):
    assert 'data' in result_json.keys()
    assert 'meta' in result_json.keys()
    meta = result_json['meta']
    assert 'tableType' in meta
    # assert 'schema' in result_json.keys()


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
    assert ('sepal_length','mean') in meta_cols['bins']
    assert ('petal_length','min') in meta_cols['bins']
    assert ('petal_length','max') in meta_cols['bins']
