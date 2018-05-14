from os import path
from pandas import read_csv


here = path.abspath(path.dirname(__file__))
fixtures = path.join(here, 'fixtures')
iris = read_csv(path.join(fixtures, 'iris.csv'))


def test_meta_simple():
    from taj import meta

    global iris

    m = meta.metaSection(iris)
    assert m['tableType'] == 'Simple'
    assert m['index'].get('type') == 'Simple'
    assert m['columns'].get('type') == 'Simple'
