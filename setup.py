from setuptools import find_packages, setup

import versioneer

setup(name='pandas-taj',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='Tables As JSON',
      packages=['taj'],
      install_requires=['pandas'],
      tests_require=['pytest'],
      zip_safe=False,
      include_package_data=True)
