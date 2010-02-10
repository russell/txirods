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
          'construct',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      txrodsServer = txirods.clients.txrodsServer:main
      iinit = txirods.clients.iinit:main
      ipwd = txirods.clients.ipwd:main
      ils = txirods.clients.ils:main
      icd = txirods.clients.icd:main
      iput = txirods.clients.iput:main
      iget = txirods.clients.iget:main
      imkdir = txirods.clients.imkdir:main
      irmdir = txirods.clients.irmdir:main
      irm = txirods.clients.irm:main
      imiscsrvinfo = txirods.clients.imiscsrvinfo:main
      """,
      )
