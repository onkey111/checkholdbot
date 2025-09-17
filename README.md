# 🎯 Pending Orders Telegram Bot

Bot Telegram tự động monitor pending orders và gửi thông báo khi total > 18.

## 🚀 Features

- ✅ **Auto Monitor**: Check pending orders mỗi 5 phút
- ✅ **Smart Alerts**: Thông báo khi vượt threshold (18 orders)
- ✅ **No Spam**: Chỉ alert khi có thay đổi
- ✅ **Error Handling**: Robust error recovery
- ✅ **Status Updates**: Periodic status reports
- ✅ **Railway Ready**: Deploy lên Railway ngay

## 📋 Requirements

### 1. Tạo Telegram Bot

1. Mở Telegram, tìm `@BotFather`
2. Gửi `/newbot`
3. Đặt tên bot và username
4. Lưu **Bot Token** (dạng: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### 2. Lấy Chat ID

**Option 1: Personal Chat**
1. Gửi message cho bot của bạn
2. Vào: `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates`
3. Tìm `"chat":{"id":123456789}` - đây là Chat ID

**Option 2: Group Chat**
1. Add bot vào group
2. Gửi message trong group
3. Check getUpdates như trên
4. Chat ID sẽ là số âm (dạng: `-123456789`)

## 🛠️ Local Setup

### 1. Install Dependencies
```bash
cd telegram_bot
pip install -r requirements.txt
```

### 2. Environment Variables
```bash
# Copy template
cp .env.example .env

# Edit .env file
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### 3. Test Local
```bash
python bot.py
```

## 🚂 Railway Deployment

### 1. Tạo Railway Project

1. Vào [railway.app](https://railway.app)
2. Login với GitHub
3. Click **"New Project"**
4. Chọn **"Deploy from GitHub repo"**
5. Connect repo này

### 2. Set Environment Variables

Trong Railway Dashboard → Variables:

**REQUIRED:**
```
TELEGRAM_BOT_TOKEN = your_bot_token_from_botfather
TELEGRAM_CHAT_ID = your_chat_id_or_group_id
```

**OPTIONAL (có defaults):**
```
ETHERSCAN_API_KEY = BNIYXSEUSR5WB9NPMZACEPXVF5YZ74HNNZ
CONTRACT_ADDRESS = 0xde605a918c466e74a2a12865efe616d51391312a
CHECK_INTERVAL = 300
ALERT_THRESHOLD = 18
LOG_LEVEL = INFO
```

### 3. Deploy

1. Railway sẽ auto-deploy khi push code
2. Check logs trong Railway Dashboard
3. Bot sẽ gửi startup message khi ready

## 📊 Bot Messages

### Startup Message
```
🚀 Pending Orders Monitor Started

✅ Bot is now monitoring pending orders
📊 Alert threshold: 18
⏰ Check interval: 300s
🔗 Contract: 0xde605a91...391312a

🎯 Will alert when pending orders > 18
```

### Alert Message
```
🚨 HIGH ALERT 🎯

📊 Pending Orders: 23
📈 Change: +5 orders
📈 Threshold: 18
⏰ Time: 2025-09-17 14:30:00 UTC

🔗 Contract: 0xde605a91...391312a

#PendingOrders #WorldChain #Alert
```

### Status Update (mỗi 1 giờ)
```
✅ Status Update

📊 Pending Orders: 15
📈 Threshold: 18
⏰ Last Check: 2025-09-17 14:30:00 UTC
🔄 Monitoring: Active

#Status #PendingOrders
```

## ⚙️ Configuration

### Thay đổi Threshold
```bash
# Railway Environment Variables
ALERT_THRESHOLD = 25  # Alert khi > 25 instead of 18
```

### Thay đổi Check Interval
```bash
CHECK_INTERVAL = 180  # Check mỗi 3 phút instead of 5
```

### Multiple Chat IDs
Hiện tại support 1 chat. Để support nhiều chats, edit `config.py`:
```python
TELEGRAM_CHAT_ID = "123456789,987654321,-111222333"
```

## 🔧 Troubleshooting

### Bot không gửi message
1. Check Bot Token đúng chưa
2. Check Chat ID đúng chưa
3. Đảm bảo bot đã được start (`/start`)
4. Check Railway logs

### API Errors
1. Check Etherscan API key
2. Check contract address
3. Check network connectivity

### Railway Deployment Issues
1. Check environment variables
2. Check Railway logs
3. Ensure Procfile exists
4. Check requirements.txt

## 📁 File Structure

```
telegram_bot/
├── bot.py              # Main bot logic
├── config.py           # Configuration & env vars
├── monitor.py          # Pending orders monitoring
├── requirements.txt    # Dependencies
├── Procfile           # Railway deployment
├── railway.json       # Railway config
├── .env.example       # Environment template
└── README.md          # This file
```

## 🎯 Technical Details

- **Language**: Python 3.8+
- **Framework**: python-telegram-bot 20.7
- **HTTP Client**: aiohttp 3.9.1
- **Architecture**: Async/await
- **Deployment**: Railway
- **Monitoring**: Every 5 minutes
- **Error Recovery**: Exponential backoff

## 📈 Monitoring Logic

1. **Check Contract**: Call `getPendingOrderIds()` function
2. **Parse Response**: Decode hex data to get array length
3. **Compare Threshold**: Alert if count > 18
4. **Track Changes**: Only alert on changes (no spam)
5. **Error Handling**: Retry on failures
6. **Status Updates**: Periodic health reports

---

**Ready to deploy! 🚀**

Bot sẽ tự động monitor và thông báo khi có nhiều hơn 18 pending orders.
