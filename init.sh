#!/bin/bash

uv init $1 --no-pin-python --vcs git --package

mkdir -pv tests/$(basename $PWD)
touch tests/$(basename $PWD)/test_$(basename $PWD).py
printf 'def test_my_project() -> None:\n\tassert "I <3 python"\n' >> tests/$(basename $PWD)/test_$(basename $PWD).py

uv venv
source .venv/bin/activate

uv python install $2

uv add ruff pytest pytest-cov pytest-mock --dev
uv sync --dev

unlink init.sh
