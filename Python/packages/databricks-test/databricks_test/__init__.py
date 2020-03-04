from unittest.mock import MagicMock
import inspect
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from tempfile import TemporaryDirectory
import importlib
import sys
import os
import pathlib


globalSession = None


class FS(object):
    def __init__(self):
        self.help = MagicMock()
        self.cp = MagicMock(return_value=True)
        self.head = MagicMock(return_value="")
        self.ls = MagicMock(return_value=[])
        self.mkdirs = MagicMock(return_value=True)
        self.mv = MagicMock(return_value=True)
        self.put = MagicMock(return_value=True)
        self.rm = MagicMock(return_value=True)
        self.mount = MagicMock(return_value=True)
        self.mounts = MagicMock(return_value=[])
        self.refreshMounts = MagicMock(return_value=True)
        self.unmount = MagicMock(return_value=True)


class WorkflowInterrupted(Exception):
    pass


class Workflow(object):
    def __init__(self):
        self.help = MagicMock()
        self.run = MagicMock(return_value="")

    def exit(self, value: str):
        raise WorkflowInterrupted


class Widgets(object):
    def __init__(self):
        self.help = MagicMock()
        self.combobox = MagicMock()
        self.dropdown = MagicMock()
        self.get = MagicMock(return_value="")
        self.getArgument = MagicMock(return_value="")
        self.multiselect = MagicMock()
        self.remove = MagicMock()
        self.removeAll = MagicMock()
        self.text = MagicMock()


class Secrets(object):
    def __init__(self):
        self.help = MagicMock()
        self.get = MagicMock(return_value="")
        self.getBytes = MagicMock(return_value=bytearray())
        self.list = MagicMock(return_value=[])
        self.listScopes = MagicMock(return_value=[])


class Library(object):
    def __init__(self):
        self.help = MagicMock()
        self.install = MagicMock(return_value=True)
        self.installPyPI = MagicMock(return_value=True)
        self.list = MagicMock(return_value=[])
        self.restartPython = MagicMock()


class DbUtils(object):
    def __init__(self):
        self.fs = FS()
        self.notebook = Workflow()
        self.widgets = Widgets()
        self.secrets = Secrets()
        self.library = Library()


class Session():
    def __init__(self, hivedir):
        self.display = MagicMock()
        self.displayHTML = MagicMock()
        self.dbutils = DbUtils()

        hivedirUrl = pathlib.Path(hivedir).as_uri()
        self.spark = (SparkSession.builder
                      .master("local")
                      .appName("test-pyspark")
                      .config("spark.sql.warehouse.dir", hivedirUrl)
                      .enableHiveSupport()
                      .getOrCreate())

    def run_notebook(self, dir, script):
        """
        Run a script such as a Databricks notebook
        """
        try:
            with add_path(os.path.abspath(dir)):
                if script not in sys.modules:
                    # Import will run the script only the first time
                    importlib.import_module(script)
                else:
                    # If script was already imported, reload it to rerun it

                    # Per importlib docs: When a module is reloaded, its
                    # dictionary (global variables) is retained.
                    # Delete dbutils to ensure inject_variables gets called.
                    del sys.modules[script].dbutils

                    # Reload the notebook module
                    importlib.reload(sys.modules[script])
        except WorkflowInterrupted:
            pass


def inject_variables():
    """
    Inject (real or mocked) variables in notebook scope, as Databricks does.
    """
    stack = inspect.stack()
    fvar = stack[1].frame.f_locals
    fvar['display'] = globalSession.display
    fvar['displayHTML'] = globalSession.displayHTML
    fvar['dbutils'] = globalSession.dbutils
    fvar['spark'] = globalSession.spark
    fvar['sc'] = globalSession.spark.sparkContext
    fvar['sqlContext'] = globalSession.spark
    fvar['table'] = globalSession.spark.table
    fvar['sql'] = globalSession.spark.sql
    fvar['udf'] = udf


class SessionAlreadyExistsException(Exception):
    pass


class session():
    """
    Context manager to override mocks within test scope
    """

    def __enter__(self):
        global globalSession
        if globalSession:
            raise SessionAlreadyExistsException("A session already exists")
        self.tmpdir = TemporaryDirectory()
        globalSession = Session(self.tmpdir.name)
        return globalSession

    def __exit__(self, exc_type, exc_value, traceback):
        global globalSession
        globalSession = None
        del self.tmpdir


class add_path():
    """
    Context manager to temporarily add an entry to sys.path
    """

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        sys.path.insert(0, self.path)

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            sys.path.remove(self.path)
        except ValueError:
            pass
