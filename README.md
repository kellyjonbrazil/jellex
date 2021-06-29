![Tests](https://github.com/kellyjonbrazil/jellex/workflows/Tests/badge.svg?branch=master)
![Pypi](https://img.shields.io/pypi/v/jellex.svg)

# Jello Explorer
TUI to filter JSON and JSON Lines data with Python syntax

`jellex` is a Text User Interface program to interactively process JSON and JSON Lines at the console using Python syntax. `jellex` uses [`jello`](https://github.com/kellyjonbrazil/jello) on the back-end to run the queries.

JSON or JSON Lines can be piped into `jellex` (JSON Lines are automatically slurped into a list of dictionaries) and are available as the variable `_`. Processed data can be output as JSON, JSON Lines, bash array lines, or a grep-able schema.

## Install
You can install `jellex` via `pip`, via OS Package Repository, MSI installer for Windows, or by downloading the correct binary for your architecture and running it anywhere on your filesystem.

### Usage
```
cat data.json | jellex [OPTIONS] [QUERY]
``` 
`QUERY` is optional and can be most any valid python code. `_` is the sanitized JSON from STDIN presented as a python dict or list of dicts. If `QUERY` is omitted then the original JSON input will simply be pretty printed. You can use dot notation or traditional python bracket notation to access key names.

After entering the command, a TUI with two columns will display. The `QUERY` will be on the left and the resulting filtered JSON will display on the right. You can interactively modify your query and the filtered output will automatically refresh.

Use [CTRL]-[C] to exit.

> Note: Reserved key names that cannot be accessed using dot notation can be accessed via standard python dictionary notation. (e.g. `_.foo["get"]` instead of `_.foo.get`)


A simple query:
```bash
cat data.json | jellex _.foo
```
or
```bash
cat data.json | jellex '_["foo"]'
```

#### Options
- `-c` compact print JSON output instead of pretty printing
- `-i` initialize environment with a custom config file
- `-l` lines output (suitable for bash array assignment)
- `-m` monochrome output
- `-n` print selected `null` values
- `-r` raw output of selected strings (no quotes)
- `-s` print the JSON schema in grep-able format
- `-t` print type annotations in schema view
- `-h` help
- `-v` version info
