# 🚀 Deploy Telegram Bot lên Render.com

## 📋 Chuẩn bị

### 1. Tạo tài khoản Render.com
- Truy cập [render.com](https://render.com)
- Đăng ký tài khoản miễn phí
- Connect với GitHub account

### 2. Push code lên GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

## 🔧 Deploy Steps

### 1. Tạo Web Service trên Render

1. **Login vào Render Dashboard**
   - Vào [dashboard.render.com](https://dashboard.render.com)

2. **Tạo New Web Service**
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Chọn repository chứa bot code

3. **Configure Service**
   ```
   Name: telegram-bot-pending-orders
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python bot.py
   Plan: Free
   ```

### 2. Set Environment Variables

Trong Render Dashboard, vào **Environment** tab và thêm:

#### Required Variables:
```
TELEGRAM_BOT_TOKEN=your_actual_bot_token
TELEGRAM_CHAT_ID=your_actual_chat_id
```

#### Optional Variables (có defaults):
```
ETHERSCAN_API_KEY=BNIYXSEUSR5WB9NPMZACEPXVF5YZ74HNNZ
CONTRACT_ADDRESS=0xde605a918c466e74a2a12865efe616d51391312a
FUNCTION_SELECTOR=0x7465c5e3
CHECK_INTERVAL=300
ALERT_THRESHOLD=18
CHAIN_ID=480
API_BASE_URL=https://api.etherscan.io/v2/api
BOT_NAME=Pending Orders Monitor
TIMEZONE=UTC
LOG_LEVEL=INFO
```

### 3. Deploy

1. **Auto Deploy**
   - Render sẽ tự động deploy khi có commit mới
   - Hoặc click "Manual Deploy" để deploy ngay

2. **Monitor Logs**
   - Vào **Logs** tab để xem deployment progress
   - Kiểm tra bot có start thành công không

## 📱 Kiểm tra Bot

### 1. Check Logs
```
🎯 Pending Orders Telegram Bot (Render.com)
==========================================
Config:
  Bot Name: Pending Orders Monitor
  Contract: 0xde605a918c466e74a2a12865efe616d51391312a
  Check Interval: 300s
  Alert Threshold: 18
  Chain ID: 480
  Timezone: UTC
  Log Level: INFO

Starting bot...
```

### 2. Check Telegram
Bot sẽ gửi startup message:
```
🚀 Pending Orders Monitor Started

✅ Bot is now monitoring pending orders
📊 Alert threshold: 18
⏰ Check interval: 300s
🔗 Contract: 0xde605a91...1391312a
🌐 Platform: Render.com (oregon)
🏷️ Service: telegram-bot-pending-orders

🎯 Will alert when pending orders > 18

#BotStarted #Monitoring #Render
```

## 🔄 Auto-Deploy Setup

### 1. Enable Auto Deploy
- Trong Render Dashboard → **Settings**
- Enable "Auto-Deploy" từ GitHub
- Mỗi khi push code mới, bot sẽ tự động redeploy

### 2. Branch Protection
```
Auto-Deploy Branch: main
```

## ⚠️ Render.com Free Tier Limitations

### 1. Sleep Mode
- **App sẽ "ngủ" sau 15 phút không activity**
- **Giải pháp**: Bot sẽ tự động wake up khi có request

### 2. Monthly Limits
- **750 giờ/tháng** (đủ cho 1 app chạy 24/7)
- **Bandwidth**: 100GB/tháng

### 3. Cold Start
- App có thể mất 30-60 giây để wake up từ sleep mode

## 🛠️ Troubleshooting

### 1. Bot không start
```bash
# Check logs trong Render Dashboard
# Thường do missing environment variables
```

### 2. Bot bị disconnect
```bash
# Render free tier có thể restart app
# Bot sẽ tự động reconnect
```

### 3. Memory issues
```bash
# Free tier có 512MB RAM
# Bot này chỉ dùng ~50MB, should be fine
```

## 📊 Monitoring

### 1. Render Dashboard
- **Metrics**: CPU, Memory usage
- **Logs**: Real-time application logs
- **Events**: Deploy history

### 2. Telegram Notifications
- Bot sẽ gửi status updates
- Error notifications nếu có vấn đề

## 🔄 Updates

### 1. Code Updates
```bash
git add .
git commit -m "Update bot features"
git push origin main
# Render sẽ tự động deploy
```

### 2. Environment Variables
- Update trong Render Dashboard
- Restart service để apply changes

---

## 🎯 So sánh với Railway

| Feature | Render.com | Railway |
|---------|------------|---------|
| Free Tier | 750h/month | $5 credit |
| Sleep Mode | 15 min | No sleep |
| Setup | Easy | Very Easy |
| Logs | Good | Excellent |
| Performance | Good | Better |

**Kết luận**: Render.com tốt cho development và testing, Railway tốt hơn cho production.
