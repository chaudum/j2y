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
    description="Jinja2 Template CLI",
    long_description=long_description,
    platforms=["any"],
    license="Apache License 2.0",
    packages=["j2y"],
    entry_points={"console_scripts": ["j2y = j2y.cli:main"]},
    python_requires=">=3.6",
    install_requires=requirements,
    setup_requires=["setuptools_scm"],
    extras_require={
        "test": [
            "mypy",
            "black==18.6b2",
            "pytest>=3.5",
            "pytest-flake8",
            "pytest-black==0.1.7",
            "pytest-mypy",
        ],
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
