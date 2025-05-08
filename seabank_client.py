import requests
import json
import hashlib
import os

class SeABankClient:
    def __init__(self, username, password, account_id, token_file='token.json'):
        """Initialize SeABankClient with credentials and token file."""
        if not username.isupper():
            raise ValueError("Username must be uppercase")
        self.username = username
        self.password = password
        self.account_id = account_id
        self.token_file = token_file
        self.token = self._load_token()

    def _hash_sha256(self, input_string):
        """Generate SHA-256 hash of the input string."""
        return hashlib.sha256(input_string.encode()).hexdigest()

    def _load_token(self):
        """Load token from file if it exists."""
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, 'r') as f:
                    return json.load(f).get('id_token')
            except (json.JSONDecodeError, IOError):
                return None
        return None

    def _save_token(self):
        """Save token to file."""
        try:
            with open(self.token_file, 'w') as f:
                json.dump({'id_token': self.token}, f)
        except IOError as e:
            raise Exception(f"Failed to save token: {e}")

    def login(self):
        """Authenticate with SeABank API and retrieve token."""
        url = "https://ebankbackend.seanet.vn/canhan/api/authenticate-hash"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36"
        }
        payload = {
            "username": self.username,
            "password": self._hash_sha256(self.password),
            "rememberMe": False,
            "context": "cba1d25e-8ae2-4713-bf87-e85d2ff12c86_Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36",
            "channel": "SEAMOBILE3.0",
            "subChannel": "SEANET",
            "passwordType": "HASH",
            "captcha": None,
            "location": None,
            "longitude": None,
            "latitude": None,
            "ipAddress": None,
            "machineName": None,
            "machineType": None,
            "application": None,
            "version": None,
            "contextFull": "cba1d25e-8ae2-4713-bf87-e85d2ff12c86_Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36"
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            token = data.get("data", {}).get("id_token")
            if not token:
                raise Exception("No token received from server")
            self.token = token
            self._save_token()
            return token
        except requests.RequestException as e:
            raise Exception(f"Login failed: {e}")

    def get_transactions(self, start_date, end_date):
        """Fetch transactions for the specified date range."""
        url = "https://ebankms1.seanet.vn/p03/api/p03-statement/get-trans-list-new"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36"
        }
        payload = {
            "accountID": self.account_id,
            "fromDate": start_date,
            "toDate": end_date,
            "language": "GB"
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == "BANKAPI-NEXTGEN-401":
                    self.login()
                    return self.get_transactions(start_date, end_date)
                return data
            elif response.status_code in [400, 401]:
                self.login()
                return self.get_transactions(start_date, end_date)
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch transactions: {e}")

    def send_to_server(self, data, server_url):
        """Send transaction data to the specified server URL."""
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(server_url, headers=headers, json=data)
            response.raise_for_status()
            print(f"Data sent to {server_url}: {response.status_code}")
            return True
        except requests.RequestException as e:
            print(f"Failed to send data to {server_url}: {e}")
            return False