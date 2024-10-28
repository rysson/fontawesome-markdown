'Update the icon_list module from the FontAwesome GitHub repo'
import requests
import json
from pathlib import Path
from argparse import ArgumentParser

URI = ('https://raw.githubusercontent.com'
       '/FortAwesome/Font-Awesome/refs/heads/{ref}/metadata/icons.json')


def main(argv=None):
    ap = ArgumentParser()
    ap.add_argument('ref', nargs='?', default='master', help='AwesomeFont version (master, 5.x, 6.x...)')
    op = ap.parse_args(argv)

    icons_json = requests.get(URI.format(ref=op.ref)).json()

    # use only styles for names and aliases
    icons = {
        name: tuple(icon['styles'])
        for icon_name, icon in icons_json.items()
        for name in (icon_name, *(icon.get('aliases', {}).get('names', ())))
    }

    with open(Path(__file__).parent.parent / 'fontawesome_markdown' / 'icon_list.py', 'w') as icons_list_py:
        icons_list_py.write('from __future__ import unicode_literals\n')
        icons_list_py.write('icons = ')
        icons_list_py.write(json.dumps(icons, indent=2))


if __name__ == '__main__':
    main()
