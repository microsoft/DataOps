# Package maintainer documentation

## Testing and releasing

To install tox:
`pip install tox`

Use tox to run unit tests and release the package to PyPI:
`tox`

Unit tests are run within a Docker container containing Spark.
