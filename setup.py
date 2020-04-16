import io
from setuptools import setup, find_packages


setup(name='savify',
      version='2020.04.01',
      description='Convert Spotify songs to Mp3 along with all metadata including cover art.',
      keywords='savify',
      author='Laurence Rawlings',
      author_email='rawlingslaurence@gmail.com',
      url='https://github.com/LaurenceRawlings/savify',
      license='3-clause BSD',
      long_description=io.open(
          './docs/README.rst', 'r', encoding='utf-8').read(),
      platforms='any',
      zip_safe=False,
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Development Status :: 1 - Planning',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   ],
      packages=find_packages(exclude=('tests', 'tests.*')),
      include_package_data=True,
      install_requires=[],
      entry_points={
          'console_scripts': [
              'savify = savify.__main__:main',
          ]
      },
      )
