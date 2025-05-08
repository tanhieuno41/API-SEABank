# cli.py
from seabank import SeaBankClient
import time

client = SeaBankClient("username", "password", "stk")

while True:
    transactions = client.get_transactions("20250428", "20250505")
    client.send_to_server(transactions, "https://exp.com/cronjob/seabank")
    time.sleep(10)
