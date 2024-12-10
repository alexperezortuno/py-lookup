import argparse

from lookup.email_search import EmailSearch
from lookup.text_search import TextSearch


def main():
    parser = argparse.ArgumentParser(description='Tools for looking up information for a given string')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('-s', '--search', default='', type=str, help='Search for a given string')
    parser.add_argument('--timeout', default=10, type=int, help='Add a timeout for the request')
    parser.add_argument('-e', '--email', default='', type=str, help='Search for a given email')

    args = parser.parse_args()

    if args.search is not None and args.search != '':
        text = TextSearch()
        #text.search_ahmia(args.search, args.timeout)
        text.doxbin_search(args.search)

    if args.email is not None:
        text = EmailSearch()
        text.check_spotify_email(args.email)

if __name__ == '__main__':
    main()