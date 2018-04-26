from setuptools import find_packages, setup

import versioneer

setup(name='pandas-taj',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='Tables As JSON',
      packages=find_packages(),
      install_requires=['pandas', 'pytest'],
      zip_safe=False,
      include_package_data=True)
