# SeABank Client

A Python library and CLI utility for accessing SeABank transactions via an unofficial API.

## Features

- Log in to SeABank account with SHA-256 hashed password.
- Retrieve transaction history for a specified date range.
- Automatically send transaction data to your server.
- Integrated CLI for scheduled or manual execution.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/seabank-client.git
cd seabank-client
pip install .
```

## Usage

### Using the Library

```python
from seabank_client import SeABankClient

# Initialize client
client = SeABankClient(username="USERNAME", password="PASSWORD", account_number="STK")

# Fetch transactions from April 28, 2025 to May 5, 2025
transactions = client.get_transactions(start_date="20250428", end_date="20250505")

# Send transaction data to server
client.send_to_server(transactions, server_url="https://yourserver.com/api")
```

**Note**: `USERNAME` must be in uppercase (e.g., `HELLO123`).

### Using the CLI

The `cli.py` file provides a command-line interface for automation:

```python
# cli.py
from seabank_client import SeABankClient
import time

client = SeABankClient(username="USERNAME", password="PASSWORD", account_number="STK")

while True:
    transactions = client.get_transactions(start_date="20250428", end_date="20250505")
    client.send_to_server(transactions, server_url="https://yourserver.com/cronjob/seabank")
    time.sleep(3600)  # Run every hour
```

Run the CLI:

```bash
python cli.py
```

## Advanced Configuration

For security, you can use environment variables or a `.env` file to store credentials instead of hardcoding them.

Example `.env` file:

```
SEABANK_USERNAME=HELLO123
SEABANK_PASSWORD=yourpassword
SEABANK_ACCOUNT_NUMBER=123456789
SEABANK_SERVER_URL=https://yourserver.com/api
```

Load environment variables in code:

```python
import os
from dotenv import load_dotenv

load_dotenv()

client = SeABankClient(
    username=os.getenv("SEABANK_USERNAME"),
    password=os.getenv("SEABANK_PASSWORD"),
    account_number=os.getenv("SEABANK_ACCOUNT_NUMBER")
)
```

Install `python-dotenv`:

```bash
pip install python-dotenv
```

## CLI with `argparse`

For a more flexible CLI with command-line arguments, use `argparse`. Example:

```python
# cli_advanced.py
import argparse
from seabank_client import SeABankClient

def main():
    parser = argparse.ArgumentParser(description="SeABank Client CLI")
    parser.add_argument("--username", required=True, help="SeABank username (uppercase)")
    parser.add_argument("--password", required=True, help="SeABank password")
    parser.add_argument("--account", required=True, help="SeABank account number")
    parser.add_argument("--start-date", required=True, help="Start date (YYYYMMDD)")
    parser.add_argument("--end-date", required=True, help="End date (YYYYMMDD)")
    parser.add_argument("--server-url", default="https://yourserver.com/api", help="Server URL")

    args = parser.parse_args()

    client = SeABankClient(args.username, args.password, args.account)
    transactions = client.get_transactions(args.start_date, args.end_date)
    client.send_to_server(transactions, args.server_url)

if __name__ == "__main__":
    main()
```

Run the CLI with `argparse`:

```bash
python cli_advanced.py --username HELLO123 --password yourpassword --account 123456789 --start-date 20250428 --end-date 20250505 --server-url https://yourserver.com/api
```

## Requirements

- Python 3.8+
- Dependencies: `requests`, `python-dotenv` (optional)

Install dependencies:

```bash
pip install requests python-dotenv
```

## License

MIT License

## Warning

This is an unofficial library and is not endorsed by SeABank. Use this software at your own risk. Ensure compliance with SeABank's terms of service.