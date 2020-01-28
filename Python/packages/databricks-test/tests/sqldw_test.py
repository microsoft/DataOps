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
