#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


setup(
    name='eiapy',
    version='0.1.3',
    description='A simple wrapper for the EIA API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    py_modules=['eiapy'],
    python_requires='>=3',
    install_requires=['requests'],
    author='Chris Brown',
    author_email='cebrown999@gmail.com',
    keywords='EIA Data API Energy',
    url='https://github.com/systemcatch/eiapy',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
