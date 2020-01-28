# Databricks notebook source

# Instrument for unit tests. This is only executed in local unit tests, not in Databricks.
if 'dbutils' not in locals():
    import databricks_test
    databricks_test.inject_variables()

# COMMAND ----------

res = dbutils.secrets.help()

res = dbutils.secrets.get("scope", "key")
assert isinstance(res, str) and res == ""

res = dbutils.secrets.getBytes("scope", "key")
assert isinstance(res, bytearray) and res == bytearray()

res = dbutils.secrets.list("scope")
assert isinstance(res, list) and res == []

res = dbutils.secrets.listScopes()
assert isinstance(res, list) and res == []
