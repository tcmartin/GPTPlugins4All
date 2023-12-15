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
    # Subparser for fetching user's configs
    user_configs_parser = subparsers.add_parser('my-configs', help='Fetch your own configs')
    user_configs_parser.add_argument('--api-key', required=True, help='API Key for authentication')

    # Subparser for submitting new config by URL
    submit_config_parser = subparsers.add_parser('submit-config', help='Submit a new config by URL')
    submit_config_parser.add_argument('--url', required=True, help='URL of the plugin JSON')
    submit_config_parser.add_argument('--auth-type', default='none', help='Authentication type (default: none)')
    submit_config_parser.add_argument('--visibility', default='private', help='Config visibility (default: private)')
    submit_config_parser.add_argument('--api-key', required=True, help='API Key for authentication')
    # Parse arguments

    args = parser.parse_args()

    if args.command == 'search':
        results = Config.search_configs(args.query, use_cache=not args.no_cache)
        print(json.dumps(results, indent=2))
    elif args.command == 'get':
        config = Config.fetch_config_by_id_or_name(args.id)
        print(json.dumps(config, indent=2))
    elif args.command == 'my-configs':
        user_configs = Config.fetch_user_configs(args.api_key)
        print(json.dumps(user_configs, indent=2))
    elif args.command == 'submit-config':
        new_config = Config.create_config_from_url(args.api_key, args.url, args.auth_type, args.visibility)
        print(json.dumps(new_config, indent=2))
    else:
        #show help with argument options
        parser.print_help()
        





if __name__ == '__main__':
    main()
