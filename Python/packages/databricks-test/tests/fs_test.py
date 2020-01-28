import databricks_test


def test_fs():
    with databricks_test.session() as dbrickstest:
        # Run notebook
        dbrickstest.run_notebook(".", "fs_notebook")
