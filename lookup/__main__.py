import argparse
from argparse import Namespace

from lookup.email_search import EmailSearch
from lookup.text_search import TextSearch


def main():
    parser = argparse.ArgumentParser(description='Tools for looking up information for a given string')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('-s', '--search', default='', type=str, help='Search for a given string')
    parser.add_argument('--timeout', default=10, type=int, help='Add a timeout for the request')
    parser.add_argument('-e', '--email', default='', type=str, help='Search for a given email')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('--tor', action='store_true', help='Enable Tor proxy')

    args: Namespace = parser.parse_args()

    if args.search is not None and args.search != '':
        text = TextSearch()
        text.search_ahmia(args)
        text.doxbin_search(args)

    if args.email is not None:
        text = EmailSearch()
        text.check_spotify_email(args)
        text.check_duolingo_email(args)

if __name__ == '__main__':
    main()