#!/usr/bin/env bash
set -e

ROOT_PATH=$(dirname $(dirname $0))
cd $ROOT_PATH

npx pyright s3transfer-stubs
flake8 s3transfer-stubs
black s3transfer-stubs
isort s3transfer-stubs
mypy s3transfer-stubs
python -m istub -u
