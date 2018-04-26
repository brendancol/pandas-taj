from os import path
from json import loads
from pandas import read_csv

from taj import df_to_json
from taj import multidf_to_json

here = path.abspath(path.dirname(__file__))
fixtures = path.join(here, 'fixtures')


iris = read_csv(path.join(fixtures, 'iris.csv'))


def assert_standard_props(result_json):
    assert 'data' in result_json.keys()
    assert 'tableType' in result_json.keys()
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

    output_json = multidf_to_json(agg)
    assert output_json
    assert_standard_props(loads(output_json))
