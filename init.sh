#!/bin/bash

project = $(basename $PWD)

uv init $1 --no-pin-python --vcs git --package

mkdir -pv $"tests/{$project}/"
printf 'def test_my_project() -> None:\n    assert "I <3 python"\n' >> $"tests/{$project}/test_{$project}.py"

uv python install $2

uv venv
source .venv/bin/activate

uv add ruff pytest pytest-cov pytest-mock honk-parser --dev
uv sync --dev

unlink init.sh
