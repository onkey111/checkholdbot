# 🎯 Simple Token Transfer Checker

Tool đơn giản để check **1 TOKEN TRANSFER gần nhất** trên Worldscan.

## 📁 Files

### 1. `simple_token_checker.py` (Detailed)
- **Structured code** với class
- **Error handling** đầy đủ
- **Formatted output** đẹp mắt
- **~80 lines** code

### 2. `check_latest_token.py` (Ultra Simple)
- **Minimal code** chỉ ~40 lines
- **Single function** approach
- **Quick execution** < 5 seconds
- **Essential info** only

## 🚀 Cách Sử Dụng

### Option 1: Detailed Version
```bash
python simple_token_checker.py
```

### Option 2: Ultra Simple
```bash
python check_latest_token.py
```

## 📊 Output Mẫu

```
🎯 LATEST TOKEN TRANSFER:
🪙 WLD: 5.000000
⏰ 2 phút trước
📝 0xdd2f780ff096dac2d308e23b8ba3778a281cda522e818a0673d54d8b572657a3
👤 From: 0xaa73fe4bdd62a093eec8796446bdb99c617578cb
👤 To: 0xde605a918c466e74a2a12865efe616d51391312a
```

## ⚙️ Configuration

Để check wallet khác, edit trong file:

```python
# Thay đổi wallet address
WALLET = "0xYOUR_WALLET_ADDRESS"

# Thay đổi API key (nếu cần)
API_KEY = "YOUR_API_KEY"
```

## 📋 Requirements

```bash
pip install aiohttp
```

## 🎯 Features

- ✅ **1 token transfer** gần nhất only
- ✅ **Fast execution** (~3-5 seconds)
- ✅ **Minimal code** dễ hiểu
- ✅ **Real-time data** từ Worldscan
- ✅ **Age calculation** (phút/giờ/ngày trước)
- ✅ **Value formatting** human-readable

## 🔧 Technical

- **API**: Etherscan API V2
- **Chain**: World Chain (ID: 480)
- **Endpoint**: `tokentx` với `offset=1`
- **Sort**: `desc` (newest first)

---

**Perfect cho việc check nhanh 1 token transfer gần nhất!** 🚀
