import databricks_test
from tempfile import NamedTemporaryFile
import uuid


def run_notebook(run_num, dbrickstest):

    input = str(uuid.uuid4())

    with NamedTemporaryFile() as tmp_dir:

        # Provide input and output location as widgets to notebook
        switch = {
            "input": input,
            "output": tmp_dir.name,
        }
        dbrickstest.dbutils.widgets.get.side_effect = lambda x: switch.get(
            x, "")

        # Run notebook
        dbrickstest.run_notebook(".", "multiple_runs_notebook")

        # Notebook produces a Parquet file (directory)
        with open(tmp_dir.name) as output_file:
            assert input == output_file.read(), f"Run #{run_num} output"


def test_multiple_runs():
    with databricks_test.session() as dbrickstest:
        run_notebook(1, dbrickstest)
        run_notebook(2, dbrickstest)

    with databricks_test.session() as dbrickstest:
        run_notebook(3, dbrickstest)
