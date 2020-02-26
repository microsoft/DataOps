# Databricks notebook source
# This notebook processed the training dataset (imported by Data Factory)
# and computes a cleaned dataset with additional feature

# COMMAND ----------

# Instrument for unit tests. This is only executed in local unit tests, not in Databricks.
if 'dbutils' not in locals():
    import databricks_test
    databricks_test.inject_variables()

# COMMAND ----------

# Widgets for interactive development. Values are automatically passed when run in Azure ML.
# In interactive development, use Databricks CLI to provision the proper secrets.

# Data input: training data

dbutils.widgets.text("secretscope", "amlscope")
dbutils.widgets.text(
    "training", "wasbs://trainingdata@stmyappdataopstrstage.blob.core.windows.net/"
)
dbutils.widgets.text(
    "training_blob_config",
    "fs.azure.account.key.stmyappdataopstrstage.blob.core.windows.net",
)
dbutils.widgets.text(
    "training_blob_secretname", "trainingdata@stmyappdataopstrstage"
)

# Data output: feature engineered data

dbutils.widgets.text(
    "feature_engineered", "wasbs://feature_engineereddata@stmyappdataopstrstage.blob.core.windows.net/"
)
dbutils.widgets.text(
    "feature_engineered_blob_config",
    "fs.azure.account.key.MYACCOUNT.blob.core.windows.net"
)
dbutils.widgets.text(
    "feature_engineered_blob_secretname", "MYCONTAINER@MYACCOUNT"
)

# COMMAND ----------

# Connect to Azure ML
dbutils.library.installPyPI(
    "azureml-sdk",
    version="1.0.85",
    extras="databricks")
from azureml.core import Run
# In an Azure ML run, settings get imported from passed --AZUREML_* parameters
run = Run.get_context(allow_offline=True)

# COMMAND ----------

# Set up storage credentials

spark.conf.set(
    dbutils.widgets.get("training_blob_config"),
    dbutils.secrets.get(
        scope=dbutils.widgets.get("secretscope"),
        key=dbutils.widgets.get("training_blob_secretname")
    ),
)

spark.conf.set(
    dbutils.widgets.get("feature_engineered_blob_config"),
    dbutils.secrets.get(
        scope=dbutils.widgets.get("secretscope"),
        key=dbutils.widgets.get("feature_engineered_blob_secretname")
    ),
)

# COMMAND ----------

rawdata = (
    spark.read.format("csv")
    .options(header="true", mode="FAILFAST")
    .load(dbutils.widgets.get('training'))
)


# COMMAND ----------

# Write data to CSV

dest_path_csv = dbutils.widgets.get('feature_engineered')
enriched_data.toPandas().to_csv("/tmp/output.csv", index=False)
csv_file = "%s/engineered.csv" % (dest_path_csv)
assert dbutils.fs.cp("file:/tmp/output.csv", csv_file)
