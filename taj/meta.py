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
    _type = 'Simple'
    if isinstance(df.index, MultiIndex) or isinstance(df.columns, MultiIndex):
        _type = 'MultiIndex'
    return _type


def get_indexMeta(df):
    mt = {}
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
    mt = {}
    if isinstance(df.columns, MultiIndex):
        _type = 'MultiIndex'
        _name = df.columns.names
    else:
        _type = 'Simple'
        _name = df.columns.name
    mt['type'] = _type
    mt['name'] = _name
    return mt

# class Meta(defaultdict):
#     def __init__(self, tableType=''):
#         super().__init__()
#         self['tableType'] = tableType
#         self['columns'] = self._columns()
#         self['index'] = self._index()
#
#     def _index(self):
#         if self['tableType'] == 'Simple':
#             return MetaIndexSimple
#         return MetaIndexMulti
#
#     def index_insert(self, **kwargs):
#         assert isinstance(self['index'], defaultdict)
#
#     def _columns(self):
#         return MetaColumns
#
#     def columns_insert(self, **kwargs):
#         assert isinstance(self['columns'], defaultdict)
#
#     def to_json(self, indent=None):
#         mt = dict(meta=self)
#         print(mt)
#         return json.dumps(mt, indent=indent)
#
#
# class MetaColumns(defaultdict):
#     def __init__(self):
#         super().__init__()
#         self['type'] = ''
#         self['bins'] = {}
#         self['colors'] = {}
#
#
# class _MetaIndex(defaultdict):
#     def __init__(self):
#         super().__init__()
#         self['type'] = ''
#
#
# class MetaIndexSimple(_MetaIndex):
#     def __init__(self):
#         super().__init__()
#         self['name'] = ''
#
#
# class MetaIndexMulti(_MetaIndex):
#     def __init__(self):
#         super().__init__()
#         self['names'] = ''
