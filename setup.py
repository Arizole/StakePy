import re
import os

from codecs import open
from setuptools import setup

root_dir = os.path.abspath(os.path.dirname(__file__))

def requirements():
    return [name.rstrip() for name in open(os.path.join(root_dir, "requirements.txt")).readlines()]

with open(os.path.join(root_dir, "stakepy\\__init__.py")) as file:
    init_text = file.read()
    license = re.search(r"__license__\s*=\s*[\'\"](.+?)[\'\"]", init_text).group(1)
    version = re.search(r"__version__\s*=\s*[\'\"](.+?)[\'\"]", init_text).group(1)
    author = re.search(r"__author__\s*=\s*[\'\"](.+?)[\'\"]", init_text).group(1)

assert license
assert version
assert author

setup(
    name="StakePy",
    packages=["StakePy"],
    version=version,
    license=license,
    requires=requirements(),
    author=author,
    description="非公式Stake.com APIライブラリ",
    keywords="stake, stake.com, stake casino, casino, unofficial, api, unofficial api",
    classifiers=[
        "Programming Language :: Python :: 3.9"
    ]
)