from setuptools import setup

setup(name='spdb',
	  version='1.1.0',
	  description='Sassy Python Databases utils',
	  packages=['spdb'],
	  author_email='mrybs2@gmail.com',
	  zip_safe=False,
	  install_requires=[
	  	'qrcode',
	  	'pyotp'
	  ])