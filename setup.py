import pathlib
from setuptools import setup, find_packages

# the directory containing this file
HERE = pathlib.Path(__file__).parent

setup(
    name="gridmaze",
    version="1.0.0",
    author="hy-kiera",
    url="https://github.com/ku-dmlab/gridmaze.git",
    packages=find_packages(exclude=["captures", "tests", "scripts"]),
    install_requires=[
        "gym==0.21.0",
        "numpy",
        "pygame==2.5.1"
    ],
    extras_require={"test": ["pytest"]},
)