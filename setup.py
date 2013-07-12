#!/usr/bin/env python2.7
# encoding: UTF-8

import ast
import os.path
import shutil

from setuptools import setup


try:
    # For setup.py install
    from cybele import __version__ as version
except ImportError:
    # For pip installations
    version = str(ast.literal_eval(
                open(os.path.join(os.path.dirname(__file__),
                "cybele", "__init__.py"),
                'r').read().split("=")[-1].strip()))

README = os.path.join(os.path.dirname(__file__), "README.rst")
shutil.copyfile(README, README[:-3] + "txt")

__doc__ = open(README, 'r').read()

setup(
    name="cybele",
    version=version,
    description="A log monitor and web console",
    author="Atalanta Systems",
    author_email="dave@atalanta-systems.com",
    url="http://atalanta-systems.com",
    long_description=__doc__,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Other/Proprietary License",
        "Operating System :: Microsoft :: Windows :: Windows NT/2000",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Topic :: System :: Monitoring"
    ],
    packages=["cybele", "cybele.test"],
    package_data={"cybele": [
                    "templates/*.html",
                    "templates/*.j2",
                    "static/*.css",
                    ]},
    tests_require=[
        "Jinja2>=2.7",
        ],
    install_requires=[
        "Flask>=0.10.1",
        ],
    entry_points={
        "console_scripts": [
        "cybele-monitor = cybele.monitor:run",
        "cybele-viewer = cybele.viewer:run"
        ],
    },
    zip_safe=False
)

