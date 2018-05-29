import pandas
from pandas import MultiIndex

from .palettes import palettes
from .meta import metaSection, to_json


def df_to_json(df, bins=None, filterFields=None, extras={}):
    """
    Return a JSON string from 'df' table

    The 'bins' parameter is a dictionary indicating how a column or set of columns
    should be binned:
    ```
    bins = {'method': 'quantile' or 'interval',
            'count': number of intervals,
            'intervals': list of values to define bins ranges,
            'palette': name of a color palette from `taj.palettes`}
    ```

    The 'method' Methods the can be used are 'quantile' or
    'interval' to indicate sample amount defined bins or equaly spaced bins,
    respectively. After 'method' we have to define also the number of intervals
    with 'count' or, otherwise, the 'intervals' themselves that we want our data/column
    to be split. If both are indicated, 'count' has precedence over 'intervals'.

    Depending on the 'method' in use, values in 'intervals' will have different
    meaning: if 'method' == 'interval', 'intervals' should indicated the values
    to limit the bins; if 'method' == 'quantile', 'intervals' values are considered
    to be the size of the sample to consider when defining the bins; this will
    be done automatically by `taj`. Quantile 'intervals' range from `0` to `1`.

    The 'palette' associated value is the name of a color palette from
    `taj.palettes`; the method `taj.palettes.all_palettes` list all possibilities.

    Input:
     - df : pandas.DataFrame
     - bins : dictionary
        expected structure: {'method': 'quantile' or 'interval',
                             'count': integer,
                             'intervals': list of values,
                             'palette': string }
     - filterFields : list with column names
     - extras : args dict which are forwarded to pd.to_json

    Output:
     - json : string
        String containing json structure from df.to_json(orient='split')
        plus a "meta" section describing visualization properties to table.
    """
    # df := [my_col, my_col2, another_col]
    #
    # bins := {
    #   mycol={'method':'quantile', perc=[0.1,0.25,0.5,0.9], palette='viridis'},
    #   mycol2={'method':'equal-interval', count=7, palette='greens'}
    # }

    json_args = dict(orient='split')
    json_args.update(extras)
    content = df.to_json(**json_args)

    meta = metaSection(df)
    if filterFields:
        _filterFields = []
        for field in filterFields:
            if isinstance(field, (tuple, list)):
                _filterFields.append("|".join(field))
            else:
                _filterFields.append(field)
        meta['filterFields'] = _filterFields

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
        if 'count' in mt and int(mt['count']) > 0:
            _bins = int(mt['count'])
        elif 'intervals' in mt and len(mt['intervals']) > 0:
            _bins = [float(v) for v in mt['intervals']]
        else:
            assert 'intervals' in mt or 'count' in mt
        slices = METHODS[method](df, col, _bins)
        _col['colors'] = get_colors(slices, mt['palette'])
        _col['edges'] = slices
        if isinstance(col, (tuple, list)):
            col = "|".join(col)
        _cols[col] = _col
    return _cols


def _interval(df, column, bins):
    include_lowest = True
    right = True
    retbins = True
    out, _bins = pandas.cut(df[column], bins=bins, retbins=retbins,
                            include_lowest=include_lowest, right=right)
    limits = list(out.cat.categories.left)
    limits.append(out.cat.categories.right[-1])
    return limits


def _quantile(df, column, bins):
    retbins = True
    out, _bins = pandas.qcut(df[column], q=bins, retbins=retbins)
    limits = list(out.cat.categories.left)
    limits.append(out.cat.categories.right[-1])
    return limits


METHODS = {'quantile': _quantile,
           'interval': _interval}


def get_colors(bins, palette):
    colors = {}
    n = len(bins) - 1
    _all = palettes.all_palettes
    if palette not in _all:
        palette = 'Greens'
    palette = _all[palette]
    if n in palette:
        _bg = palette[n]
    else:
        m = max(palette.keys())
        _bg = palette[m]
        _bg = palettes.linear_palette(_bg, n)

    _fg = palettes.complements(_bg)

    colors['bg'] = _bg
    colors['fg'] = _fg
    return colors
