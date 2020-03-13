#!/bin/bash

set -eux

conda env create -f diabetes_regression/ci_dependencies.yml

conda activate mlopspython_ci
