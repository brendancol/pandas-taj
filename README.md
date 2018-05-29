# Tables As JSON

* supports python2.7 and python3.6+


TAJ return a JSON string from Pandas' DataFrame table.
It implements a function `df_to_json` where the purpose is to return a custom JSON
string to further present the data in a custom interface.
The function has some parameters (see below in examples), but the primary one is
the `bins` argument where we may define a binning method and color aspects of the
data.

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



# Run Tests
```bash
pytest -sv
```


# Examples

Load data:
```python
>>> iris = pandas.read_csv('iris.csv')
```

Use `TAJ` to get a JSON. We will bin columns `sepal_length` in its quartiles and
define them to use the `Magma` palette:
```python
>>> import taj
>>> bins = {'sepal_length':{'method':'quantile', 'count':4, 'palette':'Magma'}}
>>> js = taj.df_to_json(df.head(20), bins)
>>>
>>> import json
>>> print(json.dumps(json.loads(jss), indent=4))
{
    "columns": [
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
        "species",
        "location"
    ],
    "index": [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19
    ],
    "data": [
        [
            5.1,
            3.5,
            1.4,
            0.2,
            "setosa",
            "south"
        ],
        [
            4.9,
            3.0,
            1.4,
            0.2,
            "setosa",
            "south"
        ],
        [
            4.7,
            3.2,
            1.3,
            0.2,
            "setosa",
            "north"
        ],
        [
            4.6,
            3.1,
            1.5,
            0.2,
            "setosa",
            "north"
        ],
        [
            5.0,
            3.6,
            1.4,
            0.2,
            "setosa",
            "north"
        ],
        [
            5.4,
            3.9,
            1.7,
            0.4,
            "setosa",
            "north"
        ],
        [
            4.6,
            3.4,
            1.4,
            0.3,
            "setosa",
            "south"
        ],
        [
            5.0,
            3.4,
            1.5,
            0.2,
            "setosa",
            "south"
        ],
        [
            4.4,
            2.9,
            1.4,
            0.2,
            "setosa",
            "north"
        ],
        [
            4.9,
            3.1,
            1.5,
            0.1,
            "setosa",
            "north"
        ],
        [
            5.4,
            3.7,
            1.5,
            0.2,
            "setosa",
            "south"
        ],
        [
            4.8,
            3.4,
            1.6,
            0.2,
            "setosa",
            "north"
        ],
        [
            4.8,
            3.0,
            1.4,
            0.1,
            "setosa",
            "north"
        ],
        [
            4.3,
            3.0,
            1.1,
            0.1,
            "setosa",
            "south"
        ],
        [
            5.8,
            4.0,
            1.2,
            0.2,
            "setosa",
            "north"
        ],
        [
            5.7,
            4.4,
            1.5,
            0.4,
            "setosa",
            "south"
        ],
        [
            5.4,
            3.9,
            1.3,
            0.4,
            "setosa",
            "south"
        ],
        [
            5.1,
            3.5,
            1.4,
            0.3,
            "setosa",
            "north"
        ],
        [
            5.7,
            3.8,
            1.7,
            0.3,
            "setosa",
            "north"
        ],
        [
            5.1,
            3.8,
            1.5,
            0.3,
            "setosa",
            "south"
        ]
    ],
    "meta": {
        "tableType": "Simple",
        "index": {
            "type": "Simple",
            "name": null
        },
        "columns": {
            "sepal_length": {
                "colors": [
                    "#000003",
                    "#711F81",
                    "#F0605D",
                    "#FBFCBF"
                ],
                "bins": [
                    4.2989999999999995,
                    4.775,
                    5.0,
                    5.4,
                    5.8
                ]
            }
        }
    }
}
```
