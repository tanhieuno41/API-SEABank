# SeABank Client

Thư viện Python và tiện ích CLI để truy cập giao dịch ngân hàng từ SeABank thông qua API không chính thức.

## Tính năng

- Đăng nhập tài khoản SeABank với mật khẩu mã hóa SHA-256.
- Lấy danh sách giao dịch trong khoảng thời gian xác định.
- Tự động gửi dữ liệu giao dịch đến server của bạn.
- Tích hợp CLI để chạy định kỳ hoặc theo lệnh.

## Cài đặt

```bash
# Clone repository
git clone https://github.com/yourusername/seabank-client.git
cd seabank-client
pip install .
```

## Cách sử dụng

### Sử dụng thư viện

```python
from seabank_client import SeABankClient

# Khởi tạo client
client = SeABankClient(username="USERNAME", password="PASSWORD", account_number="STK")

# Lấy giao dịch từ ngày 28/04/2025 đến 05/05/2025
transactions = client.get_transactions(start_date="20250428", end_date="20250505")

# Gửi dữ liệu giao dịch đến server
client.send_to_server(transactions, server_url="https://yourserver.com/api")
```

**Lưu ý**: `USERNAME` phải viết in hoa (ví dụ: `HELLO123`).

### Sử dụng CLI

Tệp `cli.py` cung cấp giao diện dòng lệnh để tự động hóa quy trình:

```python
# cli.py
from seabank_client import SeABankClient
import time

client = SeABankClient(username="USERNAME", password="PASSWORD", account_number="STK")

while True:
    transactions = client.get_transactions(start_date="20250428", end_date="20250505")
    client.send_to_server(transactions, server_url="https://yourserver.com/cronjob/seabank")
    time.sleep(3600)  # Chạy mỗi giờ
```

Chạy CLI:

```bash
python cli.py
```

## Cấu hình nâng cao

Để bảo mật, bạn có thể sử dụng biến môi trường hoặc tệp `.env` để lưu thông tin đăng nhập thay vì ghi trực tiếp vào mã.

Ví dụ tệp `.env`:

```
SEABANK_USERNAME=HELLO123
SEABANK_PASSWORD=yourpassword
SEABANK_ACCOUNT_NUMBER=123456789
SEABANK_SERVER_URL=https://yourserver.com/api
```

Tải biến môi trường trong mã:

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

Cài đặt `python-dotenv`:

```bash
pip install python-dotenv
```

## CLI với `argparse`

Nếu muốn sử dụng CLI với các tham số dòng lệnh, bạn có thể dùng `argparse`. Ví dụ:

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

Chạy CLI với `argparse`:

```bash
python cli_advanced.py --username HELLO123 --password yourpassword --account 123456789 --start-date 20250428 --end-date 20250505 --server-url https://yourserver.com/api
```

## Yêu cầu

- Python 3.8+
- Các gói phụ thuộc: `requests`, `python-dotenv` (tùy chọn)

Cài đặt phụ thuộc:

```bash
pip install requests python-dotenv
```

## Giấy phép

MIT License

## Cảnh báo

Đây là thư viện không chính thức và không được SeABank hỗ trợ. Bạn sử dụng phần mềm này với trách nhiệm của riêng mình. Hãy đảm bảo tuân thủ các điều khoản dịch vụ của SeABank.