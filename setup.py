#!/usr/bin/env python

from setuptools import setup

setup(
    name="bucketeer_cli",
    version="0.1.0",
    py_modules=["bucketeer_cli"],
    install_requires=["beautifulsoup4", "click", "requests"],
    entry_points="""
        [console_scripts]
        bucketeer_cli=bucketeer_cli:cli
    """,
)
