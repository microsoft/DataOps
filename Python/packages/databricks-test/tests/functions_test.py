import databricks_test


def test_functions():
    with databricks_test.session() as dbrickstest:
        # Run notebook
        dbrickstest.run_notebook(".", "functions_notebook")
