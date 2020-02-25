# Databricks notebook source

# COMMAND ----------

# Instrument for unit tests. This is only executed in local unit tests, not in Databricks.
if 'dbutils' not in locals():
    import databricks_test
    databricks_test.inject_variables()

# COMMAND ----------

# Widgets for interactive development.
dbutils.widgets.text("input", "")
dbutils.widgets.text("output", "")

# COMMAND ----------

with open(dbutils.widgets.get('output'), "w") as output_file:
    output_file.write(dbutils.widgets.get('input'))
