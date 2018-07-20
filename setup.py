import os
import io
import re

from pathlib import Path
from setuptools import setup, find_packages


def read(path):
    path = Path(os.path.dirname(__file__)) / path
    with io.open(path, 'r', encoding='utf-8') as f:
        return f.read()


long_description = read('README.rst')
requirements = read('requirements.txt').split('\n')


setup(
    name='j2y',
    url='https://github.com/chaudum/j2y',
    author='Christian Haudum',
    author_email='christian@christianhaudum.at',
    description='Jinja2 Template CLI',
    long_description=long_description,
    platforms=['any'],
    license='Apache License 2.0',
    packages=find_packages('src'),
    entry_points={
        'console_scripts': [
            'j2y = j2y.cli:main',
        ]
    },
    python_requires='>=3.6',
    install_requires=requirements
)
