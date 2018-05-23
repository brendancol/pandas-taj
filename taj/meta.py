"""
TAJ metadata classes and functions
"""
from pandas import MultiIndex

DEFAULT_COLORS = {
    'bg': '#FFFFFF',
    'fg': '#000000'
}


def to_json(metaSection, indent=None):
    import json
    mt = {'meta': metaSection}
    return json.dumps(mt, indent=indent)


def metaSection(df):
    mt = {'tableType': get_tableType(df)}
    mt['colors'] = DEFAULT_COLORS.copy()
    mt['filterFields'] = None

    _mc = _metaColumns(df)
    _mi = _metaIndex(df)
    mt['columns'] = _mc
    mt['index'] = _mi

    return mt


def _metaColumns(df):
    mt = get_columnsMeta(df)
    mt.update({'bins': {}})
    return mt


def _metaIndex(df):
    mt = get_indexMeta(df)
    return mt


def get_tableType(df):
    if df is None:
        return ''
    _type = 'Simple'
    if isinstance(df.index, MultiIndex) or isinstance(df.columns, MultiIndex):
        _type = 'MultiIndex'
    return _type


def get_indexMeta(df):
    mt = {'type': None,
          'name': None}
    if df is None:
        return mt
    if isinstance(df.index, MultiIndex):
        _type = 'MultiIndex'
        _name = df.index.names
    else:
        _type = 'Simple'
        _name = df.index.name
    mt['type'] = _type
    mt['name'] = _name
    return mt


def get_columnsMeta(df):
    mt = {'type': None,
          'name': None}
    if df is None:
        return mt
    if isinstance(df.columns, MultiIndex):
        _type = 'MultiIndex'
        _name = df.columns.names
    else:
        _type = 'Simple'
        _name = df.columns.name
    mt['type'] = _type
    mt['name'] = _name
    return mt
