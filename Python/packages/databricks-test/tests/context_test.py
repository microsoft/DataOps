import databricks_test
from databricks_test import SessionAlreadyExistsException


def test_forbidden_concurrent_sessions():
    with databricks_test.session() as dbrickstest:  # noqa: F841
        try:
            with databricks_test.session() as dbrickstest2:  # noqa: F841
                assert False, "should have failed"
        except SessionAlreadyExistsException:
            pass
