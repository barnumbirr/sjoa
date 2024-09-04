#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as fi:
    required = fi.read().splitlines()

setup(
    name='sjoa',
    version='1.3.1',
    author='Martin Simon',
    author_email='martin@simon.tf',
    description='Command-line tool to read metadata from torrent files or magnet URLs.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/barnumbirr/sjoa',
    download_url='https://github.com/barnumbirr/sjoa/archive/refs/heads/master.zip',
    install_requires=required,
    packages=find_packages(),
    entry_points='''
    [console_scripts]
    sjoa=sjoa:main
    ''',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ]
)
