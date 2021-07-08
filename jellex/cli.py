"""jellex - query JSON at the command line with python syntax"""

import sys
import argparse
from json.decoder import JSONDecodeError
import jellex
from jello.lib import load_json, pyquery, Json

import pygments
from pygments.lexers import JsonLexer
from pygments.lexers.python import PythonLexer

from prompt_toolkit import Application
from prompt_toolkit.widgets import Frame
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout import ScrollablePane, Dimension
from prompt_toolkit.layout.containers import VSplit, HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.application import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit.lexers import PygmentsLexer


parser = argparse.ArgumentParser(description='Interactive JSON Explorer using Python syntax.')
parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s {version}'.format(version=jellex.__version__),
                    help='version information')
parser.add_argument('filename',
                    help='JSON or JSON Lines file to open')
args = parser.parse_args()


try:
    with open(args.filename) as file:
        file_text = file.read()

except Exception as e:
    print(f'jellex: There was a problem opening that file:\n        {e}', file=sys.stderr)
    sys.exit(1)

def get_json(data, query):
    """Returns a Tuple of (<JSON Response>, <Exception Message>)"""
    global last_output

    try:
        jdata = load_json(data)
        response = pyquery(jdata, query)
        json_out = Json()
        output = json_out.create_json(response)

        # only return the first 10,000 chars for performance reasons for now
        last_output = output[:10000]
        return output[:10000], ''

    except JSONDecodeError:
        print('jellex: That was not a JSON file.', file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        return last_output, f'{e.__class__.__name__}:\n{e}'


# Initial content
query = Buffer()
query.text = '_'
last_output, status_text = get_json(file_text, query.text)
json_text_tokens = list(pygments.lex(last_output, lexer=JsonLexer()))


def update_viewer_window(event):
    # get new JSON output
    global json_text_tokens
    global status_text
    json_response, status_text = get_json(file_text, query.text)
    json_text_tokens = list(pygments.lex(json_response, lexer=JsonLexer()))

    # re-render the viewer window
    global viewer_window
    viewer_window.content = FormattedTextControl(PygmentsTokens(json_text_tokens))

    # re-render the status window
    global status_window
    status_window.content = FormattedTextControl(status_text)


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


# Status Window
status_dimension = Dimension(min=2, max=2, preferred=2)
status_window = Window(content=FormattedTextControl(status_text),
                       height=status_dimension)
status = Frame(title='Status',
               body=status_window)


# Main Screen
root_container = HSplit(
    [
        VSplit([editor, viewer]),
        status
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

    if result == '' or result == '_':
        print(f"Your query:\n\njello _\n")
    elif '\n' in result:
        print(f"Your query:\n\njello '\\\n{result}'\n")
    else:
        print(f"Your query:\n\njello '{result}'\n")


if __name__ == '__main__':
    main()
