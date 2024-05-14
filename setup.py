import os

import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    required = f.read().splitlines()

with open(os.path.join('explorateur', '_version.py')) as f:
    exec(f.read())

# python setup.py bdist_wheel
setuptools.setup(
    name="explorateur",
    description="State space search",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=__version__,
    author="xxx",
    url="https://github.com/skadio/explorateur",
    packages=setuptools.find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests", "notebooks"]),
    install_requires=required,
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Documentation": "https://xxx",
        "Source": "https://xxx"
    }
)
