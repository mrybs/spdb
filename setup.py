from setuptools import setup

setup(name='spdb',
	  version='2.1.2',
	  description='SPDB - Sassy Python DB',
	  packages=['spdb'],
	  author_email='mrybs2@gmail.com',
	  zip_safe=False,
	  install_requires=[
	  	'qrcode',
	  	'pyotp'
	  ])