# 🚀 Deploy Telegram Bot lên Render.com

## ✅ Chuẩn bị hoàn tất
- ✅ Code đã được cleanup và push lên GitHub
- ✅ Chỉ giữ lại files cần thiết cho deployment
- ✅ Repository: https://github.com/onkey111/checkholdbot

## 🔧 Bước 1: Tạo Web Service trên Render

### 1.1 Truy cập Render Dashboard
1. Vào [render.com](https://render.com)
2. Đăng nhập hoặc tạo tài khoản miễn phí
3. Connect với GitHub account của bạn

### 1.2 Tạo New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect GitHub repository: `onkey111/checkholdbot`
3. Chọn branch: `master`

### 1.3 Configure Service Settings
```
Name: telegram-bot-pending-orders
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: python bot.py
Plan: Free
```

## 🔑 Bước 2: Set Environment Variables

Trong Render Dashboard, vào **Environment** tab và thêm:

### Required Variables (BẮT BUỘC):
```
TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
TELEGRAM_CHAT_ID=your_actual_chat_id_here
```

### Optional Variables (có defaults):
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

## 🚀 Bước 3: Deploy

1. Click **"Create Web Service"**
2. Render sẽ tự động:
   - Clone repository
   - Install dependencies từ requirements.txt
   - Start bot với `python bot.py`

## 📊 Bước 4: Monitor Deployment

### 4.1 Check Logs
- Vào **Logs** tab để xem deployment progress
- Tìm message: `✅ Bot started successfully`

### 4.2 Test Bot
- Gửi message `/start` cho bot
- Bot sẽ reply với status message

## 🔧 Troubleshooting

### Nếu deployment fail:
1. Check **Logs** tab để xem error
2. Verify environment variables đã set đúng
3. Ensure TELEGRAM_BOT_TOKEN và TELEGRAM_CHAT_ID valid

### Nếu bot không response:
1. Check bot token có đúng không
2. Verify chat ID format (số dương cho personal, số âm cho group)
3. Ensure bot đã được add vào group (nếu dùng group chat)

## 🎯 Kết quả mong đợi

Bot sẽ:
- ✅ Auto start khi deploy
- ✅ Check pending orders mỗi 5 phút
- ✅ Gửi alert khi > 18 orders
- ✅ Gửi status update mỗi 4 giờ
- ✅ Auto restart nếu crash

## 📱 URL Service

Sau khi deploy thành công, bạn sẽ có:
- **Service URL**: `https://your-service-name.onrender.com`
- **Status**: Running 24/7 trên Render free tier

---

**Lưu ý**: Render free tier có thể sleep sau 15 phút không activity. Bot sẽ tự wake up khi có request mới.
