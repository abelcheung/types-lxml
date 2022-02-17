import re

from setuptools import setup

with open("README.md") as fh:
    long_description = re.sub(
        "<!-- start-no-pypi -->.*<!-- end-no-pypi -->\n",
        "",
        fh.read(),
        flags=re.M | re.S,
    )

setup(
    name="lxml-stubs",
    version="0.3.1",
    description="Type annotations for the lxml package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={"lxml-stubs": ["*.pyi", "*/*.pyi"]},
    packages=["lxml-stubs"],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
    ],
    zip_safe=False
)
