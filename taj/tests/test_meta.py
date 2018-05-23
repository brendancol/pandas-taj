from os import path
from pandas import read_csv


here = path.abspath(path.dirname(__file__))
fixtures = path.join(here, 'fixtures')
iris = read_csv(path.join(fixtures, 'iris.csv'))


def test_meta_null():
    from taj import meta
    m = meta.metaSection(None)
    assert 'tableType' in m
    assert m['tableType'] == ''
    assert 'colors' in m
    assert m['colors'] == meta.DEFAULT_COLORS
    assert 'filterFields' in m
    assert m['filterFields'] is None

    assert 'index' in m
    mi = m['index']
    assert mi.get('type') is None
    assert mi.get('name') is None

    assert 'columns' in m
    mc = m['columns']
    assert mc.get('type') is None
    assert mc.get('name') is None
    assert mc.get('bins') == {}


def test_meta_simple():
    from taj import meta

    global iris

    m = meta.metaSection(iris)
    assert m['tableType'] == 'Simple'
    assert m['colors'] == meta.DEFAULT_COLORS
    assert m['filterFields'] is None
    assert m['index'].get('type') == 'Simple'
    assert m['columns'].get('type') == 'Simple'
    assert m['columns'].get('bins') == {}


def test_meta_multiColumns():
    from taj import meta

    global iris
    grouped = iris.groupby('species')
    agg = grouped.agg(['min', 'max'])

    m = meta.metaSection(agg)
    assert m['tableType'] == 'MultiIndex'
    assert m['colors'] == meta.DEFAULT_COLORS
    assert m['filterFields'] is None

    assert m['index'].get('type') == 'Simple'
    assert m['index'].get('name') == 'species'

    assert m['columns'].get('type') == 'MultiIndex'
    assert m['columns'].get('bins') == {}
