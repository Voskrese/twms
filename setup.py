#!/usr/bin/python2

import os
import platform
from glob import glob as abs_glob
from setuptools import setup, find_packages

__platform__ = platform.system()
is_windows = __platform__ in ['Windows']

__name__ = "twms"

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def glob(fname):
    return abs_glob(os.path.join(os.path.dirname(__file__), fname))

def man_path(fname):
    category = fname.rsplit('.', 1)[1]
    return os.path.join('share', 'man', 'man' + category), [fname]

def man_files(pattern):
    return map(man_path, glob(pattern))

def config_files():
    if not is_windows:
        return [(os.path.join('/etc', __name__), [os.path.join('twms', 'twms.conf')])]
    else:
        return []

# monkey patch setuptools to use distutils owner/group functionality
from setuptools.command import sdist
sdist_org = sdist.sdist
class sdist_new(sdist_org):
    def initialize_options(self):
        sdist_org.initialize_options(self)
        self.owner = self.group = 'root'
sdist.sdist = sdist_new

setup(
    name = __name__,
    version = "0.06y",
    author = 'Darafei Praliaskoiski',
    author_email = 'me@komzpa.net',
    url = 'https://github.com/komzpa/twms',
    description = 'tiny web map service',
    long_description = read('README.md'),
    license = 'Public Domain or ISC',
    packages = find_packages(),
    install_requires = ['Pillow', 'web.py'],
    extras_require = {
        'proj': ['pyproj'],
        'cairo': ['pycairo'],
    },
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    include_package_data = True,
    data_files = [
        (os.path.join('share', 'doc', __name__), ['COPYING']),
        (os.path.join('share', 'doc', __name__), glob('*.md')),
        (os.path.join('share', __name__), glob('*.jpg')),
        (os.path.join('share', __name__, 'tools'), glob(os.path.join('tools', '*.py')))
    ] + man_files('*.1') + config_files(),
    entry_points = {
        'console_scripts': [
            'twms = twms.daemon:main'
        ]
    }
)
