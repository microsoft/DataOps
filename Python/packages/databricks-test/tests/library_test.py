import databricks_test


def test_library():
    with databricks_test.session() as dbrickstest:
        # Run notebook
        dbrickstest.run_notebook(".", "library_notebook")
