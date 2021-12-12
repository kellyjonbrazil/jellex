"""jellex - query JSON at the command line with python syntax"""

import sys
import argparse
from json.decoder import JSONDecodeError
import jellex
from jello.lib import opts, load_json, pyquery, Json, Schema
from jello.dotmap import DotMap

from pygments.lexers import JsonLexer
from pygments.lexers.python import PythonLexer
from pygments.lexers.javascript import JavascriptLexer

from prompt_toolkit import Application
from prompt_toolkit.formatted_text import to_formatted_text, HTML
from prompt_toolkit.widgets import Frame, TextArea
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout import ScrollablePane, Dimension
from prompt_toolkit.layout.containers import VSplit, HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.margins import NumberedMargin
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next
from prompt_toolkit.lexers import PygmentsLexer


parser = argparse.ArgumentParser(description='Interactive JSON Explorer using Python syntax.')
parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s {version}'.format(version=jellex.__version__),
                    help='version information')
parser.add_argument('filename',
                    help='JSON or JSON Lines file to open')
args = parser.parse_args()

opts.nulls = True

try:
    with open(args.filename) as file:
        file_text = file.read()

except Exception as e:
    print(f'jellex: There was a problem opening that file:\n        {e}', file=sys.stderr)
    sys.exit(1)


def get_item_stats(item):
    items = 0
    size = 0

    if isinstance(item, (bool, float, int, str)) or item is None:
        items = 1
    elif isinstance(item, (list, dict)):
        items = len(item)

    if isinstance(item, str):
        size = len(item)
    elif isinstance(item, (float, int)) and not isinstance(item, bool):
        size = len(str(item))
    elif isinstance(item, list):
        try:
            size = len(''.join(item))
        except Exception:
            size = len(str(item))
    elif isinstance(item, dict):
        size = len(str(item))

    return to_formatted_text(HTML(f'<green><b>items:</b></green> {items}\n<green><b>item size:</b></green> {size}'))


def get_json(data, query):
    """Returns a Tuple of (<JSON Response>, <Stats|Exception Message>)"""
    global last_output
    global response

    try:
        jdata = load_json(data)
        response = pyquery(jdata, query)
        json_out = Json()
        output = json_out.create_json(response)

        # only return the first 10,000 chars for performance reasons for now
        last_output = output[:10000]
        return output[:10000], get_item_stats(response)

    except JSONDecodeError:
        print('jellex: That was not a JSON file.', file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        exception_name = e.__class__.__name__.replace('<', '').replace('>', '')
        exception_message = str(e).replace('<', '').replace('>', '')
        return last_output, to_formatted_text(HTML(f'<red><b>{exception_name}:</b></red>\n<red>{exception_message}</red>'))


def get_schema(data, query):
    """Returns schema output from jello"""
    global last_schema_output
    global response

    try:
        schema_out = Schema()
        output = schema_out.create_schema(response)
        # only return the first 10,000 chars for performance reasons for now
        last_schema_output = output[:10000]
        return output[:10000]
    except Exception:
        last_schema_output


# Initial content
query = Buffer()
query.text = '_'
last_output, status_text = get_json(file_text, query.text)
last_schema_output = get_schema(file_text, query.text)
response = None


def get_completions():
    response
    if response:
        if isinstance(response, (dict, DotMap)):
            return list(response.keys())
        if isinstance(response, list):
            item_list = []
            for i, item in enumerate(response):
                item_list.append(f'[{i}]')
            return item_list

    return []


def update_viewer_window(event):
    # get new JSON output
    global status_text
    _, status_text = get_json(file_text, query.text)
    get_schema(file_text, query.text)

    # re-render the viewer window
    global viewer_window
    viewer_window.text = last_output

    # re-render the schema window
    global schema_window
    schema_window.text = last_schema_output

    # re-render the status window
    global status_window
    status_window.content = FormattedTextControl(status_text)


item_completer = WordCompleter(words=get_completions)
query = Buffer(on_text_changed=update_viewer_window,
               completer=item_completer,
               complete_while_typing=True)

kb = KeyBindings()
kb.add('c-\\')(focus_next)

# Editor Window
editor_window = Window(content=BufferControl(buffer=query,
                                             lexer=PygmentsLexer(PythonLexer),
                                             focus_on_click=True),
                       allow_scroll_beyond_bottom=True,
                       left_margins=[NumberedMargin()],
                       ignore_content_width=True)
editor_scroll = ScrollablePane(show_scrollbar=True,
                               content=editor_window)
editor = Frame(title='Editor',
               body=editor_scroll)


# Viewer Window
viewer_window = TextArea(text=last_output,
                         wrap_lines=False,
                         scrollbar=True,
                         focus_on_click=True,
                         lexer=PygmentsLexer(JsonLexer))
viewer = Frame(title='Viewer',
               body=viewer_window)


# Schema Window
schema_window = TextArea(text=last_output,
                         height=5,
                         wrap_lines=False,
                         scrollbar=True,
                         focus_on_click=True,
                         lexer=PygmentsLexer(JavascriptLexer))
schema = Frame(title='Schema',
               body=schema_window)


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
        schema,
        status
    ]
)

layout = Layout(root_container)
query.insert_text('_')


# Application
app = Application(key_bindings=kb,
                  layout=layout,
                  mouse_support=True,
                  full_screen=True)


@kb.add('c-c')
@kb.add('c-q')
def exit_(event):
    """Pressing Ctrl-Q or Ctrl-C will exit the user interface."""
    event.app.exit(result=query.text)


def main():
    result = app.run()
    result = result.replace("'", '"').strip()

    if result == '' or result == '_':
        print(f"Your query:\n\njello _\n")
    elif '\n' in result:
        print(f"Your query:\n\njello '\\\n{result}'\n")
    else:
        print(f"Your query:\n\njello '{result}'\n")


if __name__ == '__main__':
    main()
