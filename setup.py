import os
import io

from pathlib import Path
from setuptools import setup


def read(path):
    path = Path(os.path.dirname(__file__)) / path
    with io.open(path, "r", encoding="utf-8") as f:
        return f.read()


long_description = read("README.rst")
requirements = read("requirements.txt").split("\n")


setup(
    name="j2y",
    url="https://github.com/chaudum/j2y",
    author="Christian Haudum",
    author_email="christian@christianhaudum.at",
    description="A command line interface for rendering Jinja2 templates.",
    long_description=long_description,
    platforms=["any"],
    license="Apache License 2.0",
    packages=["j2cli"],
    entry_points={
        "console_scripts": ["j2y = j2cli.cli:main_deprecated", "j2cli = j2cli.cli:main"]
    },
    python_requires=">=3.6",
    install_requires=requirements,
    setup_requires=["setuptools_scm"],
    extras_require={
        "test": ["pytest>=3.5", "pytest-flake8", "pytest-black", "pytest-mypy"],
        "docs": ["Sphinx>=1.8,<1.9"],
    },
    use_scm_version=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
