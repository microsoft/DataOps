# Databricks notebook source

# COMMAND ----------

# Instrument for unit tests. This is only executed in local unit tests, not in Databricks.
if 'dbutils' not in locals():
    import databricks_test
    databricks_test.inject_variables()

# COMMAND ----------

assert dbutils.widgets.get("input") == "input_value"
