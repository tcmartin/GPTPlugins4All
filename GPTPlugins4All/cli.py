import argparse
import json
from .config import Config  # Import Config class from your package

def main():
    parser = argparse.ArgumentParser(description='GPTPlugins4All CLI')
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for search
    search_parser = subparsers.add_parser('search', help='Search for configs')
    search_parser.add_argument('--query', help='Search query')
    #search_parser.add_argument('--api-key', help='API Key for authentication', default=None)
    search_parser.add_argument('--no-cache', action='store_true', help='Do not use cached results')
    # Nameparser for getting config
    get_parser = subparsers.add_parser('get', help='Get a config')
    get_parser.add_argument('--id', help='Config ID/name')
    # Parse arguments

    args = parser.parse_args()

    if args.command == 'search':
        results = Config.search_configs(args.query, use_cache=not args.no_cache)
        print(json.dumps(results, indent=2))
    elif args.command == 'get':
        config = Config.fetch_config_by_id_or_name(args.id)
        print(json.dumps(config, indent=2))


if __name__ == '__main__':
    main()
