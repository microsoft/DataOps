# Databricks notebook source
from pyspark.sql.types import StructType, StructField
from pyspark.sql.types import DoubleType, IntegerType
from pyspark.sql.functions import col, pandas_udf, PandasUDFType

# COMMAND ----------

# Instrument for unit tests. This is only executed in local unit tests, not in Databricks.
if 'dbutils' not in locals():
    import databricks_test
    databricks_test.inject_variables()

# COMMAND ----------

# Widgets for interactive development.
dbutils.widgets.text("input", "")
dbutils.widgets.text("output", "")
dbutils.widgets.text("secretscope", "")
dbutils.widgets.text("secretname", "")
dbutils.widgets.text("keyname", "")

# COMMAND ----------

# Set up storage credentials

spark.conf.set(
    dbutils.widgets.get("keyname"),
    dbutils.secrets.get(
        scope=dbutils.widgets.get("secretscope"),
        key=dbutils.widgets.get("secretname")
    ),
)

# COMMAND ----------

# Import CSV files
schema = StructType(
    [
        StructField("aDouble", DoubleType(), nullable=False),
        StructField("anInteger", IntegerType(), nullable=False),
    ]
)

df = (
    spark.read.format("csv")
    .options(header="true", mode="FAILFAST")
    .schema(schema)
    .load(dbutils.widgets.get('input'))
)
display(df)

# COMMAND ----------

df.count()

# COMMAND ----------

# Inputs and output are pandas.Series of doubles
@pandas_udf('integer', PandasUDFType.SCALAR)
def square(x):
    return x * x


# COMMAND ----------

# Write out Parquet data
(df
    .withColumn("aSquaredInteger", square(col("anInteger")))
    .write
    .parquet(dbutils.widgets.get('output'))
 )
