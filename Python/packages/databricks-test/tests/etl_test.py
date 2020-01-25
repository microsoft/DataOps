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
