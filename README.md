# Metrics viewer

## Environment setting

To create a new virtual environment with all dependencies in it, execute (virtualenv should be installed):
```commandline
make env-create
```

## Formatting and linting

To apply isort and black, execute:
```commandline
make format
```

To check isort, black (without changing files) and flake8, execute:
```commandline
make check-lint
```

## Running

To run an application in created virtual environment, execute:
```commandline
make run
```

It forward you to a local link, go to it and enjoy!