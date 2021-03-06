import codecs
import os
import sys
import unittest

try:
    from setuptools import setup
except:
    from distutils.core import setup

def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('test', pattern='test_*.py')
    return test_suite

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


NAME = "sltlocaltools"


PACKAGES = ["sltlocaltools"]

DESCRIPTION = "a tool to help convert iOS localizable.strings and xls"

LONG_DESCRIPTION = read("README.txt")

KEYWORDS = "iOS localize strings"


AUTHOR = "ShulongLiu"

AUTHOR_EMAIL = "slliutyler@gmail.com"


URL = "https://github.com/LiuShulong/sltlocaltools"

VERSION = "1.0.2"

LICENSE = "MIT"


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'xlrd',
        'xlwt'
    ],
    test_suite='setup.my_test_suite'
)