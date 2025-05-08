# seabank.py

import requests
import json
import time
import hashlib

class SeaBankClient:
    def __init__(self, username, raw_password, account_id, token_file='token.json'):
        self.username = username
        self.raw_password = raw_password
        self.account_id = account_id
        self.token_file = token_file
        self.token = self.load_token()

    def hash_sha256(self, input_string):
        return hashlib.sha256(input_string.encode()).hexdigest()

    def login(self):
        url = "https://ebankbackend.seanet.vn/canhan/api/authenticate-hash"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36"
        }
        payload = {
            "username": self.username,
            "password": self.hash_sha256(self.raw_password),
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
        

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            token = response.json().get("data", {}).get("id_token")
            self.token = token
            self.save_token()
            return token
        else:
            raise Exception(f"Login failed: {response.status_code}")

    def load_token(self):
        try:
            with open(self.token_file, 'r') as f:
                return json.load(f).get('id_token')
        except:
            return None

    def save_token(self):
        with open(self.token_file, 'w') as f:
            json.dump({'id_token': self.token}, f)

    def get_transactions(self, from_date, to_date):
        url = "https://ebankms1.seanet.vn/p03/api/p03-statement/get-trans-list-new"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
            "User-Agent": "Mozilla/5.0..."
        }
        payload = {
            "accountID": self.account_id,
            "fromDate": from_date,
            "toDate": to_date,
            "language": "GB"
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "BANKAPI-NEXTGEN-401":
                self.login()
                return self.get_transactions(from_date, to_date)
            return data
        elif response.status_code in [400, 401]:
            self.login()
            return self.get_transactions(from_date, to_date)
        else:
            raise Exception(f"Lỗi khi lấy dữ liệu: {response.status_code}")

    def send_to_server(self, data, target_url):
        response = requests.post(target_url, headers={"Content-Type": "application/json"}, json=data)
        print(response.content) 
        return response.status_code == 200
