from __future__ import print_function, absolute_import

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from .core import df_to_json, multidf_to_json  # NOQA


def test():
    """Run the pandas-taj test suite."""
    import os
    try:
        import pytest
    except ImportError:
        import sys
        sys.stderr.write("You need to install py.test to run tests.\n\n")
        raise
    pytest.main(os.path.dirname(__file__))
