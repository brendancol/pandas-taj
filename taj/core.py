import json


def df_to_json(df):
    content = json.loads(df.to_json(orient='table'))
    content['data'] = json.loads(df.to_json(orient='columns'))
    content['tableType'] = 'Simple'
    return json.dumps(content)


def multidf_to_json(df):
    content = json.loads(df.to_json(orient='split'))
    content['index_field'] = df.index.name
    content['tableType'] = 'MultiIndex'
    return json.dumps(content)
