# Databricks notebook source

# Instrument for unit tests. This is only executed in local unit tests, not in Databricks.
if 'dbutils' not in locals():
    import databricks_test
    databricks_test.inject_variables()

# COMMAND ----------

res = dbutils.notebook.help()

res = dbutils.notebook.run("value", 0, {"arg": "value"})
assert isinstance(res, str) and res == ""

res = dbutils.notebook.exit("value")
assert False, "should not be executed"
