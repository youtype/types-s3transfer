#!/usr/bin/env bash
set -e

ROOT_PATH=$(dirname $(dirname $0))
cd $ROOT_PATH

poetry run npx pyright s3transfer-stubs
poetry run flake8 s3transfer-stubs
poetry run black s3transfer-stubs
poetry run isort s3transfer-stubs
poetry run mypy s3transfer-stubs
poetry run python -m istub -u
