"""jellex - query JSON at the command line with python syntax"""

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


sample_text = '''{"name":"jc","version":"1.15.7","description":"JSON CLI output utility","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","website":"https://github.com/kellyjonbrazil/jc","copyright":"© 2019-2021 Kelly Brazil","license":"MIT License","parser_count":74,"parsers":[{"name":"acpi","argument":"--acpi","version":"1.2","description":"`acpi` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["acpi"]},{"name":"airport","argument":"--airport","version":"1.3","description":"`airport -I` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["darwin"],"magic_commands":["airport -I"]},{"name":"airport_s","argument":"--airport-s","version":"1.4","description":"`airport -s` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["darwin"],"magic_commands":["airport -s"]},{"name":"arp","argument":"--arp","version":"1.7","description":"`arp` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","aix","freebsd","darwin"],"magic_commands":["arp"]},{"name":"blkid","argument":"--blkid","version":"1.4","description":"`blkid` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["blkid"]},{"name":"cksum","argument":"--cksum","version":"1.2","description":"`cksum` and `sum` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["cksum","sum"]},{"name":"crontab","argument":"--crontab","version":"1.5","description":"`crontab` command and file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"],"magic_commands":["crontab"]},{"name":"crontab_u","argument":"--crontab-u","version":"1.6","description":"`crontab` file parser with user support","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"]},{"name":"csv","argument":"--csv","version":"1.2","description":"CSV file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using the python standard csv library","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]},{"name":"date","argument":"--date","version":"2.1","description":"`date` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","freebsd"],"magic_commands":["date"]},{"name":"df","argument":"--df","version":"1.7","description":"`df` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","freebsd"],"magic_commands":["df"]},{"name":"dig","argument":"--dig","version":"2.1","description":"`dig` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","aix","freebsd","darwin","win32","cygwin"],"magic_commands":["dig"]},{"name":"dir","argument":"--dir","version":"1.3","description":"`dir` command parser","author":"Rasheed Elsaleh","author_email":"rasheed@rebelliondefense.com","compatible":["win32"]},{"name":"dmidecode","argument":"--dmidecode","version":"1.3","description":"`dmidecode` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["dmidecode"]},{"name":"dpkg_l","argument":"--dpkg-l","version":"1.1","description":"`dpkg -l` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["dpkg -l"]},{"name":"du","argument":"--du","version":"1.4","description":"`du` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"],"magic_commands":["du"]},{"name":"env","argument":"--env","version":"1.3","description":"`env` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","win32","aix","freebsd"],"magic_commands":["env","printenv"]},{"name":"file","argument":"--file","version":"1.3","description":"`file` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","aix","freebsd","darwin"],"magic_commands":["file"]},{"name":"finger","argument":"--finger","version":"1.1","description":"`finger` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","freebsd"],"magic_commands":["finger"]},{"name":"free","argument":"--free","version":"1.4","description":"`free` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["free"]},{"name":"fstab","argument":"--fstab","version":"1.5","description":"`/etc/fstab` file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","freebsd"]},{"name":"group","argument":"--group","version":"1.3","description":"`/etc/group` file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"]},{"name":"gshadow","argument":"--gshadow","version":"1.2","description":"`/etc/gshadow` file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","aix","freebsd"]},{"name":"hash","argument":"--hash","version":"1.2","description":"`hash` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"]},{"name":"hashsum","argument":"--hashsum","version":"1.1","description":"hashsum command parser (`md5sum`, `shasum`, etc.)","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Parses MD5 and SHA hash program output","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["md5sum","md5","shasum","sha1sum","sha224sum","sha256sum","sha384sum","sha512sum"]},{"name":"hciconfig","argument":"--hciconfig","version":"1.2","description":"`hciconfig` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["hciconfig"]},{"name":"history","argument":"--history","version":"1.5","description":"`history` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Optimizations by https://github.com/philippeitis","compatible":["linux","darwin","cygwin","aix","freebsd"]},{"name":"hosts","argument":"--hosts","version":"1.3","description":"`/etc/hosts` file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]},{"name":"id","argument":"--id","version":"1.3","description":"`id` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"],"magic_commands":["id"]},{"name":"ifconfig","argument":"--ifconfig","version":"1.10","description":"`ifconfig` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using ifconfig-parser from https://github.com/KnightWhoSayNi/ifconfig-parser","compatible":["linux","aix","freebsd","darwin"],"magic_commands":["ifconfig"]},{"name":"ini","argument":"--ini","version":"1.4","description":"INI file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using configparser from the standard library","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]},{"name":"iptables","argument":"--iptables","version":"1.6","description":"`iptables` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["iptables"]},{"name":"iw_scan","argument":"--iw-scan","version":"0.6","description":"`iw dev [device] scan` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Enhancements by Philipp Schmitt (https://pschmitt.dev/)","compatible":["linux"],"magic_commands":["iw dev"]},{"name":"jobs","argument":"--jobs","version":"1.4","description":"`jobs` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["jobs"]},{"name":"kv","argument":"--kv","version":"1.1","description":"Key/Value file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"This is a wrapper for the INI parser","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]},{"name":"last","argument":"--last","version":"1.7","description":"`last` and `lastb` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Enhancements by https://github.com/zerolagtime","compatible":["linux","darwin","aix","freebsd"],"magic_commands":["last","lastb"]},{"name":"ls","argument":"--ls","version":"1.9","description":"`ls` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["ls","vdir"]},{"name":"lsblk","argument":"--lsblk","version":"1.7","description":"`lsblk` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["lsblk"]},{"name":"lsmod","argument":"--lsmod","version":"1.5","description":"`lsmod` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["lsmod"]},{"name":"lsof","argument":"--lsof","version":"1.4","description":"`lsof` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["lsof"]},{"name":"mount","argument":"--mount","version":"1.6","description":"`mount` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","freebsd"],"magic_commands":["mount"]},{"name":"netstat","argument":"--netstat","version":"1.10","description":"`netstat` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","freebsd"],"magic_commands":["netstat"]},{"name":"ntpq","argument":"--ntpq","version":"1.5","description":"`ntpq -p` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","freebsd"],"magic_commands":["ntpq"]},{"name":"passwd","argument":"--passwd","version":"1.3","description":"`/etc/passwd` file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"]},{"name":"ping","argument":"--ping","version":"1.5","description":"`ping` and `ping6` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","freebsd"],"magic_commands":["ping","ping6"]},{"name":"pip_list","argument":"--pip-list","version":"1.4","description":"`pip list` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","win32","aix","freebsd"],"magic_commands":["pip list","pip3 list"]},{"name":"pip_show","argument":"--pip-show","version":"1.2","description":"`pip show` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","win32","aix","freebsd"],"magic_commands":["pip show","pip3 show"]},{"name":"ps","argument":"--ps","version":"1.5","description":"`ps` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["ps"]},{"name":"route","argument":"--route","version":"1.6","description":"`route` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["route"]},{"name":"rpm_qi","argument":"--rpm-qi","version":"1.3","description":"`rpm -qi` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["rpm -qi","rpm -qia","rpm -qai"]},{"name":"sfdisk","argument":"--sfdisk","version":"1.0","description":"`sfdisk` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["sfdisk"]},{"name":"shadow","argument":"--shadow","version":"1.3","description":"`/etc/shadow` file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"]},{"name":"ss","argument":"--ss","version":"1.4","description":"`ss` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["ss"]},{"name":"stat","argument":"--stat","version":"1.8","description":"`stat` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","freebsd"],"magic_commands":["stat"]},{"name":"sysctl","argument":"--sysctl","version":"1.1","description":"`sysctl` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","freebsd"],"magic_commands":["sysctl"]},{"name":"systemctl","argument":"--systemctl","version":"1.4","description":"`systemctl` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["systemctl"]},{"name":"systemctl_lj","argument":"--systemctl-lj","version":"1.5","description":"`systemctl list-jobs` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["systemctl list-jobs"]},{"name":"systemctl_ls","argument":"--systemctl-ls","version":"1.4","description":"`systemctl list-sockets` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["systemctl list-sockets"]},{"name":"systemctl_luf","argument":"--systemctl-luf","version":"1.4","description":"`systemctl list-unit-files` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["systemctl list-unit-files"]},{"name":"systeminfo","argument":"--systeminfo","version":"1.0","description":"`systeminfo` command parser","author":"Jon Smith","author_email":"jon@rebelliondefense.com","compatible":["win32"],"magic_commands":["systeminfo"]},{"name":"time","argument":"--time","version":"1.2","description":"`/usr/bin/time` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"]},{"name":"timedatectl","argument":"--timedatectl","version":"1.4","description":"`timedatectl status` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["timedatectl","timedatectl status"]},{"name":"tracepath","argument":"--tracepath","version":"1.2","description":"`tracepath` and `tracepath6` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["tracepath","tracepath6"]},{"name":"traceroute","argument":"--traceroute","version":"1.3","description":"`traceroute` and `traceroute6` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using the trparse library by Luis Benitez at https://github.com/lbenitez000/trparse","compatible":["linux","darwin","freebsd"],"magic_commands":["traceroute","traceroute6"]},{"name":"ufw","argument":"--ufw","version":"1.0","description":"`ufw status` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["ufw status"]},{"name":"ufw_appinfo","argument":"--ufw-appinfo","version":"1.0","description":"`ufw app info [application]` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["ufw app"]},{"name":"uname","argument":"--uname","version":"1.5","description":"`uname -a` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","freebsd"],"magic_commands":["uname"]},{"name":"upower","argument":"--upower","version":"1.2","description":"`upower` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["upower"]},{"name":"uptime","argument":"--uptime","version":"1.5","description":"`uptime` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["uptime"]},{"name":"w","argument":"--w","version":"1.4","description":"`w` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["w"]},{"name":"wc","argument":"--wc","version":"1.2","description":"`wc` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["wc"]},{"name":"who","argument":"--who","version":"1.4","description":"`who` command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["who"]},{"name":"xml","argument":"--xml","version":"1.5","description":"XML file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using the xmltodict library at https://github.com/martinblech/xmltodict","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]},{"name":"yaml","argument":"--yaml","version":"1.5","description":"YAML file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using the ruamel.yaml library at https://pypi.org/project/ruamel.yaml","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]}]}'''


def get_json(data, query):
    """Returns a Tuple of (<JSON Response>, <Exception Message>)"""
    global last_output

    try:
        jdata = load_json(data)
        response = pyquery(jdata, query)
        json_out = Json()
        output = json_out.create_json(response)
        last_output = output
        return output, ''

    except Exception as e:
        return last_output, str(e)


# Initial content
query = Buffer()
query.text = '_'
last_output, status_text = get_json(sample_text, query.text)
json_text_tokens = list(pygments.lex(last_output, lexer=JsonLexer()))


def update_viewer_window(event):
    # get new JSON output
    global json_text_tokens
    global status_text
    json_response, status_text = get_json(sample_text, query.text)
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
    if '\n' in result:
        print(f"Your query:\n\njello '\\\n{result}'\n")
    else:
        print(f"Your query:\n\njello '{result}'\n")


if __name__ == '__main__':
    main()
