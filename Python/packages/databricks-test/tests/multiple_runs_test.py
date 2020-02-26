import databricks_test
from tempfile import NamedTemporaryFile
import uuid


def run_notebook(notebook, run_num, dbrickstest):

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
        dbrickstest.run_notebook(".", notebook)

        # Notebook writes the input parameter as output file
        with open(tmp_dir.name) as output_file:
            assert input == output_file.read(), f"Run #{run_num} output"


def test_multiple_runs_in_same_session_1():
    with databricks_test.session() as dbrickstest:
        run_notebook("multiple_runs_notebook", 1, dbrickstest)
        run_notebook("multiple_runs_notebook", 2, dbrickstest)

    with databricks_test.session() as dbrickstest:
        run_notebook("multiple_runs_notebook", 3, dbrickstest)


def test_multiple_runs_in_same_session_and_run_other_session():
    with databricks_test.session() as dbrickstest:
        run_notebook("multiple_runs_notebook", 4, dbrickstest)


def test_multiple_runs_in_multiple_test_cases():
    with databricks_test.session() as dbrickstest:
        run_notebook("multiple_runs_notebook2", 5, dbrickstest)


def test_multiple_runs_in_multiple_test_cases2():
    with databricks_test.session() as dbrickstest:
        run_notebook("multiple_runs_notebook2", 6, dbrickstest)
