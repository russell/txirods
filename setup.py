from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='txIRODS',
      version=version,
      description="a native interface to iRODS",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Russell Sim',
      author_email='russell@vpac.org',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'setuptools',
          'twisted',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      txirods = txirods.client:main
      """,
      )
