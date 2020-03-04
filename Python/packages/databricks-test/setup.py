import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='databricks_test',
    version='0.0.4',
    author="Alexandre Gattiker",
    author_email="algattik@microsoft.com",
    description="Unit testing and mocking for Databricks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/microsoft/DataOps",
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
