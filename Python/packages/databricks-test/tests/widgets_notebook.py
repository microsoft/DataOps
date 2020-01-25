# Databricks notebook source

# Instrument for unit tests. This is only executed in local unit tests, not in Databricks.
if 'dbutils' not in locals():
    import databricks_test
    databricks_test.inject_variables()

# COMMAND ----------

dbutils.widgets.help()

dbutils.widgets.combobox("name", "defaultValue", [
                         "choice1", "choice2"], "label")

dbutils.widgets.dropdown("name", "defaultValue", [
                         "choice1", "choice2"], "label")

res = dbutils.widgets.get("name")
assert isinstance(res, str) and res == ""

res = dbutils.widgets.getArgument("name")
assert isinstance(res, str) and res == ""
res = dbutils.widgets.getArgument("name", "optional")
assert isinstance(res, str) and res == ""

dbutils.widgets.multiselect("name", "defaultValue", [
                            "choice1", "choice2"], "label")

dbutils.widgets.remove("name")

dbutils.widgets.removeAll()

dbutils.widgets.text("name", "defaultValue", "label")
