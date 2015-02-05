__author__ = "walter"
try:
    import logging
    import multiprocessing
except:
    pass

import sys
py_version = sys.version_info[:2]

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

dependency_links = []

install_requires=[
    "scriptine",
    "paramiko",
    ]

setup(
    name='claire',
    version='0.1',
    description='Tool to manage multiple servers via SSH',
    author='Walter Danilo Galante',
    author_email='walter.galante@proxtome.com',
    packages=find_packages(),
    dependency_links=dependency_links,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'claire = claire.claire:main',
        ]
    },
    zip_safe=True
)

