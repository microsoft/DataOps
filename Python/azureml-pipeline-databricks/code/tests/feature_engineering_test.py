import pandas as pd
from tempfile import TemporaryDirectory
import databricks_test
from pandas.testing import assert_frame_equal


def test_feature_engineering(mocker):
    mocker.patch("azureml.core.Run")

    # Read test input sample data
    df = pd.read_csv("code/tests/testdata/feature_engineering/input.csv")

    with databricks_test.session() as dbrickstest, \
            TemporaryDirectory() as csv_dir:

        in_file = f"{csv_dir}/input"
        out_dir = f"{csv_dir}/output"

        # Write test input sample data as parquet
        df.to_parquet(in_file, compression='gzip')

        # Provide input and output location as widgets to notebook
        switcher = {
            "training": "code/tests/testdata/feature_engineering/input.csv",
            "feature_engineered": out_dir,
        }
        dbrickstest.dbutils.widgets.get = lambda x: switcher.get(x, "")

        capture_files = {}

        def mock_cp(src, dst, capture_files=capture_files):
            prefix = "file:"
            assert src.startswith(prefix)
            capture_files[dst] = pd.read_csv(src)
            return True

        dbrickstest.dbutils.fs.cp.side_effect = mock_cp

        # Run notebook
        dbrickstest.run_notebook("./code/prepare", "feature_engineering")

    expected_name = "engineered.csv"
    expected_file = "%s/%s" % (out_dir, expected_name)
    assert expected_file in capture_files
    resultDF = capture_files[expected_file]

    # Compare produced and expected CSV files
    expectedDF = pd.read_csv(
        "code/tests/testdata/feature_engineering/expected.csv")
    assert_frame_equal(
        expectedDF, resultDF, check_dtype=False, check_categorical=False)
