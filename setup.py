from setuptools import setup, find_packages

version = '0.1'

setup(name='iptree',
      version=version,
      description="IP tree",
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[],
      keywords="",
      author="Jasper Spaans",
      author_email="j@jasper.es",
      url="",
      license="",
      package_dir={'': 'iptree'},
      packages=find_packages('iptree'),
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'BTrees',
                        ],
      entry_points={
            'console_scripts': [
            ],
      },
      extras_require={
          'test' : ["pytest",
                  "pytest-cov",
                  "pytest-capturelog",
       	         ],
      }
      )
