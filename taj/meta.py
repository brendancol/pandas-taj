"""
TAJ metadata classes and functions
"""


def to_json(metaSection, indent=None):
    import json
    mt = {'meta': metaSection}
    return json.dumps(mt, indent=indent)


def _metaColumns():
    return dict(type='',
                bins={},
                colors={})


def _metaIndex():
    return dict(type='',
                name='')


def metaSection(tableType):
    mt = {'tableType': tableType}
    _mc = _metaColumns()
    _mi = _metaIndex()
    mt['columns'] = _mc
    mt['index'] = _mi
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
