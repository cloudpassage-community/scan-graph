import os
import re
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_version():
    raw_init_file = read("scangraph/__init__.py")
    rx_compiled = re.compile(r"\s*__version__\s*=\s*\"(\S+)\"")
    ver = rx_compiled.search(raw_init_file).group(1)
    return ver


def get_long_description(fnames):
    retval = ""
    for fname in fnames:
        retval = retval + (read(fname)) + "\n\n"
    return retval


setup(
    name="scangraph",
    version=get_version(),
    author="CloudPassage",
    author_email="toolbox@cloudpassage.com",
    description="Turn CloudPassage Halo scan results into directed graphs",
    license="BSD",
    keywords="cloudpassage halo api scan graph",
    url="http://github.com/cloudpassage-community/scan-graph",
    packages=["scangraph"],
    install_requires=["cloudpassage >= 1.0",
                      "networkx >= 1.11",
                      "pygraphviz >= 1.3.1"],
    long_description=get_long_description(["README.rst", "CHANGELOG.rst"]),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Topic :: Security",
        "License :: OSI Approved :: BSD License"
        ],
    )
