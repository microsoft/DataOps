import subprocess

subprocess.check_call(["flake8", "--output-file=lint-testresults.xml", "--format", "junit-xml"])
