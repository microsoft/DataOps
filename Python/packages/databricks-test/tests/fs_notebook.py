# Databricks notebook source

# Instrument for unit tests. This is only executed in local unit tests, not in Databricks.
if 'dbutils' not in locals():
    import databricks_test
    databricks_test.inject_variables()

# COMMAND ----------

res = dbutils.fs.help()

res = dbutils.fs.cp("dbfs://src", "dst")
assert isinstance(res, bool) and res
res = dbutils.fs.cp("dbfs://src", "dst", recurse=True)

assert isinstance(res, bool) and res
res = dbutils.fs.head("src")
assert isinstance(res, str) and res == ""
res = dbutils.fs.head("src", maxBytes=100)
assert isinstance(res, str) and res == ""

res = dbutils.fs.ls("dbfs://dir")
assert isinstance(res, list) and res == []

res = dbutils.fs.mkdirs("a/b/c")
assert isinstance(res, bool) and res

res = dbutils.fs.mv("src", "dst")
assert isinstance(res, bool) and res
res = dbutils.fs.mv("src", "dst", recurse=True)
assert isinstance(res, bool) and res

res = dbutils.fs.put("file", "text")
assert isinstance(res, bool) and res
res = dbutils.fs.put("file", "text", overwrite=True)
assert isinstance(res, bool) and res

res = dbutils.fs.rm("dir")
assert isinstance(res, bool) and res
res = dbutils.fs.rm("dir", recurse=True)
assert isinstance(res, bool) and res

res = dbutils.fs.mount("source", "/mnt/point")
assert isinstance(res, bool) and res
res = dbutils.fs.mount("source", "/mnt/point", encryptionType="encr",
                       owner="me", extraConfigs={"key": "value"})
assert isinstance(res, bool) and res

res = dbutils.fs.mounts()
assert isinstance(res, list) and res == []

res = dbutils.fs.refreshMounts()
assert isinstance(res, bool) and res

res = dbutils.fs.unmount("/mnt/point")
assert isinstance(res, bool) and res
