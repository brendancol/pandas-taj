import pandas
from pandas import MultiIndex

from .palettes import palettes
from .meta import metaSection, to_json


def df_to_json(df, bins=None):
    """
    Return a JSON string from 'df' table

    Input:
     - df   : pandas.DataFrame
     - bins : dictionary (see `helper_funcs.bins`)

    Output:
     - jsons : string
        String containing json structure from df.to_json(orient='split')
        plus a "meta" section describing visualization properties to table.
    """
    # df := [my_col, my_col2, another_col]
    #
    # bins := {
    #   mycol={'method':'quantile', perc=[0.1,0.25,0.5,0.9], palette='viridis'},
    #   mycol2={'method':'equal-interval', count=7, palette='greens'}
    # }

    content = df.to_json(orient='split')

    meta = metaSection(get_tableType(df))

    _bins = do_bins(df, bins)
    # meta['columns'] = _bins
    meta['columns'].update({'bins': _bins})

    # meta['index'] = get_indexMeta(df)
    # meta['columns'] = get_columnsMeta(df)

    metajs = to_json(meta)
    return ','.join([content[:-1], metajs[1:]]).replace(' ', '')


def do_bins(df, bins=None):
    # Accepted methods:
    # - equal interval (input: number of intervals <int>)
    # - quantile (input: percentiles <list of floats>)
    # - breaks (input: values to cut <list of floats>)
    _cols = {}
    if not bins:
        return _cols

    for col, mt in bins.items():
        _col = {}
        method = mt['method']
        assert method in METHODS, ("Expected one of {}, got '{}' instead"
                                    .format(list(METHODS.keys()), method))
        slices = METHODS[method](df, col, mt['count'])
        _col['colors'] = get_colors(slices, mt['palette'])
        _col['edges'] = slices
        _cols[col] = _col
    return _cols


def get_tableType(df):
    # TODO: check column and row indexes (objects) to see whether Multi or Simple
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


def _interval(df, column, bins):
    include_lowest = True
    right = True
    retbins = True
    out,_bins = pandas.cut(df[column], bins=bins, retbins=retbins,
                           include_lowest=include_lowest, right=True)
    limits = list(out.cat.categories.left)
    limits.append(out.cat.categories.right[-1])
    return limits


def _quantile(df, column, bins):
    retbins = True
    out,_bins = pandas.qcut(df[column], q=bins, retbins=retbins)
    limits = list(out.cat.categories.left)
    limits.append(out.cat.categories.right[-1])
    return limits


METHODS = {'quantile': _quantile,
           'interval': _interval}


def get_colors(bins, palette):
    n = len(bins) - 1
    _all = palettes.all_palettes
    if palette not in _all:
        palette = 'Greens'
    palette = _all[palette]
    if n in palette:
        colors = palette[n]
    else:
        m = max(palette.keys())
        colors = palette[m]
        colors = palettes.linear_palette(colors, n)
    return colors
