import pandas as pd
import numpy as np
from taj import df_to_json

from os import path

here = path.abspath(path.dirname(__file__))
fixtures = path.join(here, 'fixtures')


iris = pd.read_csv(path.join(fixtures, 'iris.csv'))

iris['location'] = np.random.choice(['north','south'])

df = iris.sample(20)
gdf_columns = df.groupby('species').agg(['min','max'])
gdf_columns_rows = df.groupby(['species','location']).agg(['min','max'])


def test_simple_noColouring():
    js = df_to_json(df)
    with open('simple_noColoring.json', 'w') as f:
        f.write(js)


def test_simple_yesColouring():
    bins = {'sepal_length':{'method':'interval','count':5,'palette':'Greens'}}
    js = df_to_json(df, bins=bins)
    with open('simple_yesColoring.json', 'w') as f:
        f.write(js)


def test_nestedColumns_noColouring():
    js = df_to_json(gdf_columns)
    with open('nestedColumns_noColoring.json','w') as f:
        f.write(js)


def test_nestedColumns_yesColouring():
    bins = {('sepal_length','min'):{'method':'interval','count':5,'palette':'Greens'}}
    js = df_to_json(gdf_columns, bins=bins)
    with open('nestedColumns_yesColoring.json','w') as f:
        f.write(js)


def test_nestedRowsColumns_noColouring():
    js = df_to_json(gdf_columns_rows)
    with open('nestedRowsColumns_noColoring.json','w') as f:
        f.write(js)


def test_nestedRowsColumns_yesColouring():
    bins = {('sepal_length','min'):{'method':'interval','count':5,'palette':'Greens'}}
    js = df_to_json(gdf_columns_rows, bins=bins)
    with open('nestedRowsColumns_yesColoring.json','w') as f:
        f.write(js)


def test_simple_filterFields():
    filterFields = ['sepal_length']
    js = df_to_json(df, filterFields=filterFields)
    with open('simple_filterFields.json', 'w') as f:
        f.write(js)


def test_nestedColumns_filterFields():
    filterFields = [('sepal_length','min')]
    js = df_to_json(gdf_columns, filterFields=filterFields)
    with open('nestedColumns_filterFields.json','w') as f:
        f.write(js)


def test_nestedRowsColumns_yesColouring_filterFields():
    bins = {('sepal_length','min'):{'method':'interval','count':5,'palette':'Greens'}}
    filterFields = [('sepal_length','min')]
    js = df_to_json(gdf_columns_rows, bins=bins, filterFields=filterFields)
    with open('nestedRowsColumns_yesColoring_filterFields.json','w') as f:
        f.write(js)
