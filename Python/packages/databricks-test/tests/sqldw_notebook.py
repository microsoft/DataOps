# Databricks notebook source

# Instrument for unit tests. This is only executed in local unit tests, not in Databricks.
if 'dbutils' not in locals():
    import databricks_test
    databricks_test.inject_variables()

# COMMAND ----------

# Set up the Blob storage account access key in the notebook session conf.
spark.conf.set(
    "fs.azure.account.key.myaccount.blob.core.windows.net",
    dbutils.secrets.get("dwsecrets", "accountkey"))

# Get some data from a SQL DW table.
df = spark.read \
    .format("com.databricks.spark.sqldw") \
    .option('url', 'jdbc:sqlserver://myserver.database.windows.net:1433;database=mydb;user=myuser;password=secret;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30;')\
    .option("tempDir", "wasbs://mycontainer@myaccount.blob.core.windows.net/") \
    .option("forwardSparkAzureStorageCredentials", "true") \
    .option("dbTable", "mytable") \
    .load()

# Apply some transformations to the data, then use the
# Data Source API to write the data back to another table in SQL DW.

dfres = df.select("id", "age")

dfres.write \
    .format("com.databricks.spark.sqldw") \
    .option('url', 'jdbc:sqlserver://myserver.database.windows.net:1433;database=mydb;user=myuser;password=secret;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30;')\
    .option("forwardSparkAzureStorageCredentials", "true") \
    .option("dbTable", "my_table_in_dw_copy") \
    .option("tempDir", "wasbs://mycontainer@myaccount.blob.core.windows.net/") \
    .save()
