![Pypi](https://img.shields.io/pypi/v/jellex.svg)

# Jello Explorer
TUI to filter JSON and JSON Lines data with Python syntax

Here is a video of `jellex` in action: https://youtu.be/9VCXjINa74E

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
An Editor window displays on the left, a Viewer window displays on the right, and a Status window displays on the bottom.

The Editor window uses standard EMACS key bindings and allows you to type your Python syntax query. `_` is the sanitized JSON from the file presented as a python dict or list of dicts. You can use dot notation or traditional python bracket notation to access key names.

As you modify your query, the Viewer window will update with the latest results. If there are any errors in the query (syntax errors, etc.), they will be displayed in the Status window at the bottom.

Use `CTRL-Q` to exit.

> Note: Reserved key names that cannot be accessed using dot notation can be accessed via standard python dictionary notation. (e.g. `_.foo["get"]` instead of `_.foo.get`)

Here is an example after running `jellex twitterdata.json` and modifying the query:
```python
┌────────────────| Editor |────────────────┐┌───────────────| Viewer |────────────────┐
│_[0].user                                ^││{                                       ^│
│                                          ││  "follow_request_sent": false,          │
│                                          ││  "has_extended_profile": false,         │
│                                          ││  "profile_use_background_image": true,  │
│                                          ││  "default_profile_image": false,        │
│                                          ││  "id": 851336634,                       │
│                                          ││  "profile_background_image_url_https":  │
│                                          ││  "verified": true,                      │
│                                          ││  "profile_text_color": "333333",        │
│                                          ││  "profile_image_url_https": "https://pb │
│                                          ││  "profile_sidebar_fill_color": "DDEEF6" │
│                                          ││  "entities": {                          │
│                                          ││    "url": {                             │
│                                          ││      "urls": [                          │
│                                          ││        {                                │
│                                          ││          "url": "http://t.co/fvHMZhwmP4 │
│                                          ││          "indices": [                   │
│                                          ││            0,                           │
│                                          ││            22                           │
│                                          ││          ],                             │
│                                          ││          "expanded_url": "http://www.20 │
│                                          ││          "display_url": "20minutos.com" │
│                                          ││        }                                │
│                                          ││      ]                                  │
│                                          ││    },                                   │
│                                          ││    "description": {                     │
│                                         v││      "urls": [                         v│
└──────────────────────────────────────────┘└─────────────────────────────────────────┘
┌─────────────────────────────────────| Status |──────────────────────────────────────┐
│                                                                                     │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```
When you exit (`CTRL-Q`), you will be presented with your `jello` filter:
```
$ jellex twitterdata.json 
Your query:

jello '_[0].user'

$
```

## TODO
The project is at a very simple working state. Here are some short-term plans:

- Allow scrolling of the Viewer window
- Allow switching to `vi` key bindings
- Allow saving of the input file
- Allow opening another file within the UI
- Status bar showing the mode and filename, stats, etc.
