# GPT Plugins 4All

GPT Plugins 4All is a Python library designed to facilitate the integration of GPT and other large language models with various APIs, leveraging OpenAPI specifications. This library simplifies the process of parsing OpenAPI specs, managing different authentication methods, and dynamically interacting with APIs based on model responses.

## Features

- Parse and validate OpenAPI 3.1.0 specifications.
- Handle diverse authentication methods, including OAuth 2.0, Basic Auth, Header Auth, and Query Parameter Auth.
- Generate structured API representations for AI interactions.
- Dynamically construct API calls based on OpenAPI specs.
- Support OAuth2.0 flow for token acquisition and usage.

## Installation

Install GPT Plugins 4All using pip:

```bash
pip install GPTPlugins4All
```

## Quick Start

### Initializing with an OpenAPI Specification

```python
from GPTPlugins4All.config import Config

# Initialize the Config object with your OpenAPI spec
spec_string = """..."""  # Your OpenAPI spec as a string
config = Config(spec_string)
```

### Adding Authentication Methods

#### Add Basic Authentication

```python
config.add_auth_method("BASIC", {"key": "your_api_key"})
```

#### Add OAuth Configuration

```python
config.add_auth_method("OAUTH", {
    "client_id": "your_client_id",
    "client_secret": "your_client_secret",
    "auth_url": "https://example.com/auth",
    "token_url": "https://example.com/token",
    "redirect_uri": "https://yourapp.com/oauth-callback",
    "scope": "read write"
})
```

### Generating Simplified API Representations

```python
simplified_api = config.generate_simplified_api_representation()
print(simplified_api)
```

### OAuth Flow

```python
auth_url = config.start_oauth_flow()
# Redirect the user to auth_url...

tokens = config.handle_oauth_callback(code_from_redirect)
```

### Making API Calls

```python
response = config.make_api_call("/endpoint", "GET", {"param": "value"})
```

## Documentation

For detailed documentation, please refer to [Link to documentation].

## Contributing

Contributions are welcome! Please check out the [contributing guidelines](CONTRIBUTING.md).

## License

GPT Plugins 4All is released under the [MIT License](LICENSE).