# databricks_test

## About

An experimental unit test framework for Databricks notebooks.

_This open-source project is not developed by nor affiliated with Databricks._

## Installing

```
pip install databricks_test
```

## Usage

Add a cell at the beginning of your Databricks notebook:

```python
# Instrument for unit tests. This is only executed in local unit tests, not in Databricks.
if 'dbutils' not in locals():
    import databricks_test
    databricks_test.inject_variables()
```

The `if` clause causes the inner code to be skipped when run in Databricks.
Therefore there is no need to install the `databricks_test` module on your Databricks environment.

Add your notebook into a code project, for example using [GitHub version control in Azure Databricks](https://docs.microsoft.com/en-us/azure/databricks/notebooks/azure-devops-services-version-control).

Set up pytest in your code project (outside of Databricks).

Create a test case with the following structure:

```python
import databricks_test

def test_method():
    with databricks_test.session() as dbrickstest:

        # Set up mocks on dbrickstest
        # ...

        # Run notebook
        dbrickstest.run_notebook("notebook_dir", "notebook_name_without_py_suffix")

        # Test assertions
        # ...
```

You can set up [mocks](https://docs.python.org/dev/library/unittest.mock.html) on `dbrickstest`, for example:

```python
dbrickstest.dbutils.widgets.get.return_value = "myvalue"
```

See samples below for more examples.

## Supported features

* Spark context injected into Databricks notebooks: `spark`, `table`, `sql` etc.
* PySpark with all Spark features including reading and writing to disk, UDFs and Pandas UDFs
* Databricks Utilities (`dbutils`, `display`) with user-configurable mocks
* Mocking connectors such as Azure Storage, S3 and SQL Data Warehouse

## Unsupported features

* Notebook formats other than `.py` (`.ipynb`, `.dbc`) are not supported
* Non-python cells such as `%scala` and `%sql` (those cells are skipped, as they are stored in `.py` notebooks as comments)
* Writing directly to `/dbfs` mount on local filesystem:
  write to a local temporary file instead and use dbutils.fs.cp() to copy to DBFS, which you can intercept with a mock
* Databricks extensions to Spark such as `spark.read.format("binaryFile")`

## Sample test

Sample test case for an ETL notebook reading CSV and writing Parquet.

```python
import pandas as pd
import databricks_test
from tempfile import TemporaryDirectory

from pandas.testing import assert_frame_equal

def test_etl():
    with databricks_test.session() as dbrickstest:
        with TemporaryDirectory() as tmp_dir:
            out_dir = f"{tmp_dir}/out"

            # Provide input and output location as widgets to notebook
            switch = {
                "input": "tests/etl_input.csv",
                "output": out_dir,
            }
            dbrickstest.dbutils.widgets.get.side_effect = lambda x: switch.get(
                x, "")

            # Run notebook
            dbrickstest.run_notebook(".", "etl_notebook")

            # Notebook produces a Parquet file (directory)
            resultDF = pd.read_parquet(out_dir)

        # Compare produced Parquet file and expected CSV file
        expectedDF = pd.read_csv("tests/etl_expected.csv")
        assert_frame_equal(expectedDF, resultDF, check_dtype=False)
```

In the notebook, we pass parameters using widgets.
This makes it easy to pass
a local file location in tests, and a remote URL (such as Azure Storage or S3)
in production.

```python
# Databricks notebook source
# This notebook processed the training dataset (imported by Data Factory)
# and computes a cleaned dataset with additional features such as city.
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
```


## Advanced mocking

Sample test case mocking PySpark classes for a notebook connecting to Azure SQL Data Warehouse.

```python
import databricks_test
import pyspark
import pyspark.sql.functions as F
from tempfile import TemporaryDirectory
from pandas.testing import assert_frame_equal
import pandas as pd


def test_sqldw(monkeypatch):
    with databricks_test.session() as dbrickstest, TemporaryDirectory() as tmp:

        out_dir = f"{tmp}/out"

        # Mock SQL DW loader, creating a Spark DataFrame instead
        def mock_load(reader):
            return (
                dbrickstest.spark
                .range(10)
                .withColumn("age", F.col("id") * 6)
                .withColumn("salary", F.col("id") * 10000)
            )

        monkeypatch.setattr(
            pyspark.sql.readwriter.DataFrameReader, "load", mock_load)

        # Mock SQL DW writer, writing to a local Parquet file instead
        def mock_save(writer):
            monkeypatch.undo()
            writer.format("parquet")
            writer.save(out_dir)

        monkeypatch.setattr(
            pyspark.sql.readwriter.DataFrameWriter, "save", mock_save)

        # Run notebook
        dbrickstest.run_notebook(".", "sqldw_notebook")

        # Notebook produces a Parquet file (directory)
        resultDF = pd.read_parquet(out_dir)

        # Compare produced Parquet file and expected CSV file
        expectedDF = pd.read_csv("tests/sqldw_expected.csv")
        assert_frame_equal(expectedDF, resultDF, check_dtype=False)
```

## Issues

Please report issues at [https://github.com/microsoft/DataOps/issues](https://github.com/microsoft/DataOps/issues).
