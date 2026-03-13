[private]
default:
    @just --list --unsorted

install:
    uv sync

format:
    uv run ruff format .

lint:
    uv run ruff check --fix .

typecheck:
    uv run basedpyright app/*/src/

test pkg="*" *args="":
    uv run pytest app/{{pkg}}/tests/ -v --tb=short {{args}}

test-cov:
    uv run pytest app/*/tests/ --cov --tb=short

run *args="":
    uv run python -m chatbot {{args}}

update:
    uv lock --upgrade

clean:
    rm -rf dist/ build/ .pytest_cache/ .basedpyright/
    find . -type d -name __pycache__ -exec rm -rf {} +
