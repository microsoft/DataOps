# Databricks notebook source

# COMMAND ----------

# Instrument for unit tests. This is only executed in local unit tests, not in Databricks.
if 'dbutils' not in locals():
    import databricks_test
    databricks_test.inject_variables()

# COMMAND ----------

display(spark.range(10))

# COMMAND ----------

displayHTML("<b>42</b>")

# COMMAND ----------

dbutils.fs.help()

# COMMAND ----------

assert len(sc.range(1, 7, 2).collect()) == 3

# COMMAND ----------

assert sqlContext.sql("SELECT 2").collect()[0][0] == 2

# COMMAND ----------

spark.range(3).write.mode("overwrite").saveAsTable("mytesttable")

# COMMAND ----------

assert table("mytesttable").collect()[2][0] == 2

# COMMAND ----------

assert sql("SELECT 7").collect()[0][0] == 7
