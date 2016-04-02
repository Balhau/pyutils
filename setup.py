from distutils.core import setup
import os
import codecs
from setuptools import setup, find_packages


pname="butils"

#packages=[pname]+[pname+ "." + name
#	for name in os.listdir(os.path.join(pname)) if os.path.isdir(os.path.join(pname, name))]

packages=[pname]+[pname+ "." + name
	for name in os.listdir(os.path.join(pname)) if os.path.isdir(os.path.join(pname, name))]

current_dir=os.path.dirname(__file__)

with codecs.open(os.path.join(current_dir,'README.md'),'r','utf8') as readme_file:
		long_description=readme_file.read()

setup(
	name=pname,
	author='Balhau',
	author_email='balhau@balhau.net',
	platforms='any',
	version='1.0.13',
	url='https://git.balhau.net/',
	license='MIT License',
	scripts=['bin/blog2epub'],
	include_package_data = True ,
	description='A bunch of utility scripts with balhau hacks',
	long_description=__doc__,
	packages=packages,
	install_requires=[
		'ebooklib',
		'bs4'
	]
)
