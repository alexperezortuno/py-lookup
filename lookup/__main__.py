import argparse
from argparse import Namespace

from lookup.email_search import EmailSearch
from lookup.number_search import NumberSearch
from lookup.text_search import TextSearch
from lookup.username_search import UsernameSearch


def main():
    parser = argparse.ArgumentParser(description='Tools for looking up information for a given string')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('-s', '--search', default='', type=str, help='Search for a given string')
    parser.add_argument('--timeout', default=10, type=int, help='Add a timeout for the request')
    parser.add_argument('-e', '--email', default='', type=str, help='Search for a given email')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('--tor', action='store_true', help='Enable Tor proxy')
    parser.add_argument('-n', '--number', default='', type=str, help='Search for a given number')
    parser.add_argument('-u', '--username', default='', type=str, help='Search for a given username')
    parser.add_argument('--webdriver', action='store_true', help='Use webdriver for searching')

    args: Namespace = parser.parse_args()

    if args.search is not None and args.search != '':
        text = TextSearch()
        text.search_ahmia(args)
        text.doxbin_search(args)

    if args.email is not None and args.email != '':
        text = EmailSearch()
        text.check_spotify_email(args)
        text.check_duolingo_email(args)

    if args.number is not None and args.number != '':
        numbers = NumberSearch()
        numbers.number_lookup(args)

    if args.username is not None and args.username != '':
        text = UsernameSearch()
        text.username_lookup(args)


if __name__ == '__main__':
    main()