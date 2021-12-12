![Pypi](https://img.shields.io/pypi/v/jellex.svg)

![jellex](https://github.com/kellyjonbrazil/jellex/raw/master/_images/jellex.png)

# Jello Explorer
TUI to filter JSON and JSON Lines data with Python syntax

Here is a video of `jellex` in action: https://youtu.be/-oR0yZ7JaO8

Jello Explorer (`jellex`) is a Text User Interface program to interactively process JSON and JSON Lines at the console using Python syntax. `jellex` uses [`jello`](https://github.com/kellyjonbrazil/jello) on the back-end to run the queries.

## Install
Jello Explorer can be installed via `pip`:
```bash
pip install jellex
```

## Usage
```
jellex file.json
```
An Editor window displays on the left and a Viewer window displays on the right. Schema and Status windows display on the bottom.

The Editor window uses standard EMACS key bindings and allows you to type your Python syntax query. `_` is the sanitized JSON from the file presented as a python dict or list of dicts. You can use dot notation or traditional python bracket notation to access key names.

As you modify your query, the Viewer window will update with the latest results. If there are any errors in the query (syntax errors, etc.), they will be displayed in the Status window at the bottom.

Tab completions are available for current context list indicies and key names.

Use `CTRL-\` to toggle the focus between the Editor, Viewer, and Schema windows.

Use `CTRL-Q` or `CTRL-C`to exit.

> Note: Reserved key names that cannot be accessed using dot notation can be accessed via standard python dictionary notation. (e.g. `_.foo["get"]` instead of `_.foo.get`)

Here is an example after running `jellex twitterdata.json` and modifying the query:

![jellex](https://github.com/kellyjonbrazil/jellex/raw/master/_images/jellex-twitterdata.png)

When you exit (`CTRL-Q` or `CTRL-C`), you will be presented with your `jello` filter:
```
$ jellex twitterdata.json 
Your query:

jello '_[0].user'

$
```
