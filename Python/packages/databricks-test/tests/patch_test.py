import databricks_test


def test_patch():
    with databricks_test.session() as dbrickstest:
        # Provide input and output location as widgets to notebook
        switcher = {
            "input": "input_value",
            "output": "output_value",
        }
        dbrickstest.dbutils.widgets.get.side_effect = lambda x: switcher.get(
            x, "")

        # Run notebook
        dbrickstest.run_notebook(".", "patch_notebook")

    with databricks_test.session() as dbrickstest:
        dbrickstest.run_notebook(".", "patch_notebook2")
