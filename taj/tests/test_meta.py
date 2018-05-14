
def test_index_sections():
    from taj import meta

    m = meta.MetaIndexSimple()
    assert 'type' in m
    assert 'name' in m

    m = meta.MetaIndexMulti()
    assert 'type' in m
    assert 'names' in m


def test_columns_sections():
    from taj import meta

    m = meta.MetaColumns()
    assert 'type' in m
    assert 'bins' in m
    assert 'colors' in m
    assert 'method' in m


def test_sections():
    from taj import meta

    m = meta.Meta()
    assert m['tableType'] == ''
    assert 'index' in m
    assert 'columns' in m


def test_meta_simple():
    from taj import meta

    m = meta.Meta('Simple')
    assert m['tableType'] == 'Simple'
    assert m['index'].get('type') == 'Simple'
    assert m['columns'].get('type') == 'Simple'
