import databricks_test


def test_secrets():
    with databricks_test.session() as dbrickstest:
        # Run notebook
        dbrickstest.run_notebook(".", "secrets_notebook")
