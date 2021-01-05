#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='LinkFinder',
    packages=find_packages(),
    version='1.0',
    description="A python script that finds endpoints in JavaScript files.",
    long_description=open('README.md').read(),
    author='Gerben Javado',
    url='https://github.com/GerbenJavado/LinkFinder',
    py_modules=['linkfinder'],
    install_requires=['jsbeautifier'],
)
