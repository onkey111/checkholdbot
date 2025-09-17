# 🔍 Worldscan Wallet Checker Tool

Tool Python để check Token Transfers (ERC-20) gần nhất và age của ví trên **World Chain** sử dụng **Etherscan API V2**.

## 📋 Tính Năng

- ✅ Check **Token Transfers (ERC-20)** gần nhất
- ✅ Tính **age của ví** (số ngày từ transaction đầu tiên)
- ✅ Hiển thị thông tin chi tiết: hash, from/to, value, timestamp
- ✅ **Retry logic** với exponential backoff
- ✅ **Rate limiting** tuân thủ API limits
- ✅ Export kết quả ra **JSON file**
- ✅ **Error handling** comprehensive

## 🚀 Cài Đặt

### 1. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

### 2. Hoặc cài đặt manual:
```bash
pip install aiohttp
```

## 💻 Cách Sử Dụng

### Method 1: Chạy tool chính
```bash
python worldscan_wallet_checker.py
```

### Method 2: Sử dụng quick runner
```bash
# Sử dụng wallet mặc định
python run_checker.py

# Hoặc specify wallet address
python run_checker.py 0xYOUR_WALLET_ADDRESS
```

## 📊 Kết Quả Mẫu

```
🚀 WORLDSCAN WALLET CHECKER
🔧 Sử dụng Etherscan API V2
🔑 API Key: BNIYXSEUSR...

🔍 Checking wallet: 0xde605a918c466e74a2a12865efe616d51391312a
🌍 Chain: World Chain (ID: 480)
============================================================
📋 Đang lấy Token Transfers (ERC-20)...
✅ Tìm thấy 10 token transfers

📅 Đang tìm giao dịch đầu tiên để tính age...
✅ First transaction: 2025-04-16 04:02:17 UTC
✅ Wallet age: 154 ngày

============================================================
📊 BÁO CÁO VÍ WORLDSCAN
============================================================
🏠 Địa chỉ: 0xde605a918c466e74a2a12865efe616d51391312a
📅 Age: 154 ngày
📅 First transaction: 2025-04-16 04:02:17 UTC
🔢 Total token transfers: 10

🎯 TOKEN TRANSFERS GẦN NHẤT:
------------------------------------------------------------
1. WLD - 8.379360
   📝 Hash: 0x5538be9ddf824ed9c4e7547926bc66ed15f429d9302a31fb551b67b9cd86c75e
   👤 From: 0xde605a918c466e74a2a12865efe616d51391312a
   👤 To: 0xc3dc63f6594e81668e6ad13519b6cbdb3856414f
   ⏰ Time: 2025-09-17 13:37:03 UTC (0 phút trước)
   📦 Block: 19390292

2. WLD - 0.273240
   📝 Hash: 0x5538be9ddf824ed9c4e7547926bc66ed15f429d9302a31fb551b67b9cd86c75e
   👤 From: 0xde605a918c466e74a2a12865efe616d51391312a
   👤 To: 0x77c99d471ccdd8898daaf63ff9044f204065bb35
   ⏰ Time: 2025-09-17 13:37:03 UTC (0 phút trước)
   📦 Block: 19390287
```

## 📁 Files Được Tạo

### 1. `worldscan_wallet_checker.py`
- Tool chính với full functionality
- Async implementation với proper error handling
- Rate limiting và retry logic

### 2. `run_checker.py`
- Quick runner script
- Hỗ trợ command line arguments
- Simplified interface

### 3. `requirements.txt`
- Dependencies cần thiết
- Chỉ cần `aiohttp` cho async HTTP requests

### 4. `wallet_report_[address].json`
- Kết quả export tự động
- Format JSON để dễ parse
- Timestamp khi check

## ⚙️ Cấu Hình

### API Configuration
```python
API_KEY = "BNIYXSEUSR5WB9NPMZACEPXVF5YZ74HNNZ"  # Your API key
WORLD_CHAIN_ID = 480  # World Chain Mainnet
BASE_URL = "https://api.etherscan.io/v2/api"  # Etherscan API V2
```

### Wallet Address
```python
WALLET_ADDRESS = "0xde605a918c466e74a2a12865efe616d51391312a"
```

## 🔧 Customization

### Thay đổi số lượng token transfers hiển thị:
```python
# Trong hàm check_wallet()
wallet_info.latest_token_transfers = [
    self._format_token_transfer(transfer) 
    for transfer in token_transfers[:10]  # Thay 5 thành 10
]
```

### Thay đổi wallet address:
```python
# Trong main() function
WALLET_ADDRESS = "0xYOUR_NEW_WALLET_ADDRESS"
```

### Thay đổi API key:
```python
# Trong main() function
API_KEY = "YOUR_NEW_API_KEY"
```

## 🛠️ Technical Details

### API Endpoints Sử Dụng:
1. **Token Transfers**: `module=account&action=tokentx`
2. **Normal Transactions**: `module=account&action=txlist`

### Chain Information:
- **Chain**: World Chain Mainnet
- **Chain ID**: 480 (0x1e0)
- **Native Token**: ETH
- **Explorer**: https://worldscan.org

### Rate Limiting:
- **Free Tier**: 5 calls/second, 100,000 calls/day
- **Retry Logic**: Exponential backoff (1s, 2s, 4s)
- **Timeout**: 30 seconds per request

## ❗ Lưu Ý

1. **API Key**: Đảm bảo API key có quyền truy cập World Chain
2. **Rate Limits**: Tool tự động handle rate limiting
3. **Network**: Cần internet connection stable
4. **Python Version**: Requires Python 3.7+

## 🐛 Troubleshooting

### Lỗi "Query Timeout":
- API đang overload, tool sẽ tự động retry
- Giảm `offset` parameter nếu cần

### Lỗi "Rate Limit":
- Tool sẽ tự động wait và retry
- Upgrade API plan nếu cần higher limits

### Lỗi "Invalid API Key":
- Kiểm tra API key trong code
- Đảm bảo key có quyền truy cập World Chain

## 📞 Support

Nếu gặp vấn đề:
1. Check API key và permissions
2. Verify wallet address format
3. Check internet connection
4. Review error messages trong console

## 🎯 Example Usage

```bash
# Check wallet mặc định
python worldscan_wallet_checker.py

# Check wallet khác
python run_checker.py 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b

# Install dependencies
pip install -r requirements.txt
```

---

**Tool được phát triển sử dụng Etherscan API V2 mới nhất (2025) cho World Chain Mainnet.**
