# Databricks notebook source

# Instrument for unit tests. This is only executed in local unit tests, not in Databricks.
if 'dbutils' not in locals():
    import databricks_test
    databricks_test.inject_variables()

# COMMAND ----------

dbutils.fs.help()

res = dbutils.library.install("path")
assert isinstance(res, bool) and res

res = dbutils.library.installPyPI("pypiPackage")
assert isinstance(res, bool) and res
res = dbutils.library.installPyPI(
    "pypiPackage", version="1", repo="repo", extras="extras")
assert isinstance(res, bool) and res

res = dbutils.library.list()
assert isinstance(res, list) and res == []

dbutils.library.restartPython()
