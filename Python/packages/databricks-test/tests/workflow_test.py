import databricks_test


def test_workflow():
    with databricks_test.session() as dbrickstest:
        # Run notebook
        dbrickstest.run_notebook(".", "workflow_notebook")
