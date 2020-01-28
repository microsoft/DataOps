import databricks_test


def test_widgets():
    with databricks_test.session() as dbrickstest:
        # Run notebook
        dbrickstest.run_notebook(".", "widgets_notebook")
