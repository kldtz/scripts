# Scripts

Some useful scripts and a test project for [rye](https://github.com/astral-sh/rye).

## Setup

```sh
# Generate lock file and create/update virtualenv
rye sync
```

## Usage

Run registered scripts via `rye`.

```sh
# List availabe scripts
rye run

# Run a script from the list
rye run reddit 
```

## Development

* Add a new module under `src/scripts/`.
* Add an entry under `[project.scripts]` in the [pyproject.toml](pyproject.toml).