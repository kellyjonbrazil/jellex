"""jellex - query JSON at the command line with python syntax"""

from jello.lib import load_json, pyquery, Json

import pygments
from pygments.lexers import JsonLexer
from pygments.lexers.python import PythonLexer

from prompt_toolkit import Application
from prompt_toolkit.widgets import Frame
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout import ScrollablePane
from prompt_toolkit.layout.containers import VSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.application import get_app
from prompt_toolkit.key_binding import KeyBindings

from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit.lexers import PygmentsLexer


sample_text = '''{
  "name": "jc",
  "version": "1.15.7",
  "description": "JSON CLI output utility",
  "author": "Kelly Brazil",
  "author_email": "kellyjonbrazil@gmail.com",
  "website": "https://github.com/kellyjonbrazil/jc",
  "copyright": "© 2019-2021 Kelly Brazil",
  "license": "MIT License",
  "parser_count": 74,
  "parsers": [
    {
      "name": "acpi",
      "argument": "--acpi",
      "version": "1.2",
      "description": "`acpi` command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "acpi"
      ]
    },
    {
      "name": "airport",
      "argument": "--airport",
      "version": "1.3",
      "description": "`airport -I` command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "darwin"
      ],
      "magic_commands": [
        "airport -I"
      ]
    },
    {
      "name": "systemctl",
      "argument": "--systemctl",
      "version": "1.4",
      "description": "`systemctl` command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "systemctl"
      ]
    },
    {
      "name": "systemctl_lj",
      "argument": "--systemctl-lj",
      "version": "1.5",
      "description": "`systemctl list-jobs` command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "systemctl list-jobs"
      ]
    },
    {
      "name": "systemctl_ls",
      "argument": "--systemctl-ls",
      "version": "1.4",
      "description": "`systemctl list-sockets` command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "systemctl list-sockets"
      ]
    },
    {
      "name": "systemctl_luf",
      "argument": "--systemctl-luf",
      "version": "1.4",
      "description": "`systemctl list-unit-files` command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "systemctl list-unit-files"
      ]
    },
    {
      "name": "systeminfo",
      "argument": "--systeminfo",
      "version": "1.0",
      "description": "`systeminfo` command parser",
      "author": "Jon Smith",
      "author_email": "jon@rebelliondefense.com",
      "compatible": [
        "win32"
      ],
      "magic_commands": [
        "systeminfo"
      ]
    },
    {
      "name": "time",
      "argument": "--time",
      "version": "1.2",
      "description": "`/usr/bin/time` command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "cygwin",
        "aix",
        "freebsd"
      ]
    },
    {
      "name": "timedatectl",
      "argument": "--timedatectl",
      "version": "1.4",
      "description": "`timedatectl status` command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "timedatectl",
        "timedatectl status"
      ]
    },
    {
      "name": "tracepath",
      "argument": "--tracepath",
      "version": "1.2",
      "description": "`tracepath` and `tracepath6` command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "tracepath",
        "tracepath6"
      ]
    },
    {
      "name": "traceroute",
      "argument": "--traceroute",
      "version": "1.3",
      "description": "`traceroute` and `traceroute6` command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "details": "Using the trparse library by Luis Benitez at https://github.com/lbenitez000/trparse",
      "compatible": [
        "linux",
        "darwin",
        "freebsd"
      ],
      "magic_commands": [
        "traceroute",
        "traceroute6"
      ]
    },
    {
      "name": "ufw",
      "argument": "--ufw",
      "version": "1.0",
      "description": "`ufw status` command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "ufw status"
      ]
    },
    {
      "name": "ufw_appinfo",
      "argument": "--ufw-appinfo",
      "version": "1.0",
      "description": "`ufw app info [application]` command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "ufw app"
      ]
    },
    {
      "name": "uname",
      "argument": "--uname",
      "version": "1.5",
      "description": "`uname -a` command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "freebsd"
      ],
      "magic_commands": [
        "uname"
      ]
    },
    {
      "name": "upower",
      "argument": "--upower",
      "version": "1.2",
      "description": "`upower` command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "upower"
      ]
    },
    {
      "name": "uptime",
      "argument": "--uptime",
      "version": "1.5",
      "description": "`uptime` command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "cygwin",
        "aix",
        "freebsd"
      ],
      "magic_commands": [
        "uptime"
      ]
    },
    {
      "name": "w",
      "argument": "--w",
      "version": "1.4",
      "description": "`w` command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "cygwin",
        "aix",
        "freebsd"
      ],
      "magic_commands": [
        "w"
      ]
    },
    {
      "name": "wc",
      "argument": "--wc",
      "version": "1.2",
      "description": "`wc` command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "cygwin",
        "aix",
        "freebsd"
      ],
      "magic_commands": [
        "wc"
      ]
    },
    {
      "name": "who",
      "argument": "--who",
      "version": "1.4",
      "description": "`who` command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "cygwin",
        "aix",
        "freebsd"
      ],
      "magic_commands": [
        "who"
      ]
    },
    {
      "name": "xml",
      "argument": "--xml",
      "version": "1.5",
      "description": "XML file parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "details": "Using the xmltodict library at https://github.com/martinblech/xmltodict",
      "compatible": [
        "linux",
        "darwin",
        "cygwin",
        "win32",
        "aix",
        "freebsd"
      ]
    },
    {
      "name": "yaml",
      "argument": "--yaml",
      "version": "1.5",
      "description": "YAML file parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "details": "Using the ruamel.yaml library at https://pypi.org/project/ruamel.yaml",
      "compatible": [
        "linux",
        "darwin",
        "cygwin",
        "win32",
        "aix",
        "freebsd"
      ]
    }
  ]
}
'''


def get_json(data, query):
    try:
        jdata = load_json(data)
        response = pyquery(jdata, query)
        json_out = Json()
        output = json_out.create_json(response)
        return output
    except Exception as e:
        return str(e)


# Initial content
query = Buffer()
query.text = '_'
json_text_tokens = list(pygments.lex(get_json(sample_text, query.text), lexer=JsonLexer()))


def update_viewer_window(event):
    global json_text_tokens
    json_text_tokens = list(pygments.lex(get_json(sample_text, query.text), lexer=JsonLexer()))
    global viewer_window
    viewer_window.content = FormattedTextControl(PygmentsTokens(json_text_tokens))


query = Buffer(on_text_changed=update_viewer_window)

kb = KeyBindings()

# Editor Window
editor_window = Window(content=BufferControl(buffer=query, lexer=PygmentsLexer(PythonLexer)),
                       allow_scroll_beyond_bottom=True,
                       ignore_content_width=True)
editor_scroll = ScrollablePane(show_scrollbar=True,
                               content=editor_window)
editor = Frame(title='Editor',
               body=editor_scroll)


# Viewer Window
viewer_window = Window(content=FormattedTextControl(PygmentsTokens(json_text_tokens)),
                       allow_scroll_beyond_bottom=True,
                       ignore_content_width=True)
viewer_scroll = ScrollablePane(show_scrollbar=True,
                               content=viewer_window)
viewer = Frame(title='Viewer',
               body=viewer_scroll)


# Main Screen
root_container = VSplit(
    [
        editor,
        viewer
    ]
)

layout = Layout(root_container)
query.insert_text('_')

# Application
app = Application(key_bindings=kb,
                  layout=layout,
                  full_screen=True)


@kb.add('c-q')
def exit_(event):
    """Pressing Ctrl-Q will exit the user interface."""
    event.app.exit(result=query.text)


@kb.add('tab')
def focus_viewer(event):
    """Pressing TAB will change the focus."""
    get_app().layout.focus(viewer_window)


@kb.add('s-tab')
def focus_editor(event):
    """Pressing Shift TAB will change the focus."""
    get_app().layout.focus(editor_window)


def main():
    result = app.run()
    result = result.replace("'", '"')
    print(f"Your query:\n\njello '\\\n{result}'\n")


if __name__ == '__main__':
    main()
