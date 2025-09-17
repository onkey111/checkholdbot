#!/usr/bin/env python3
"""
Telegram Bot cho Pending Orders Monitor
Main entry point - chạy bot và monitoring loop

Tác giả: AI Assistant
Ngày: 2025-09-17
"""

import asyncio
import logging
from datetime import datetime, timezone
from telegram import Bot
from telegram.error import TelegramError
from config import config
from monitor import monitor

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PendingOrdersBot:
    """Main bot class"""
    
    def __init__(self):
        self.bot = None
        self.chat_id = config.TELEGRAM_CHAT_ID
        self.is_running = False
        self.startup_time = datetime.now(timezone.utc)
        
    async def initialize(self) -> bool:
        """Khởi tạo bot và validate config"""
        try:
            # Validate config
            if not config.validate():
                return False
            
            # Initialize Telegram bot
            self.bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
            
            # Test bot connection
            bot_info = await self.bot.get_me()
            logger.info(f"Bot initialized: @{bot_info.username}")
            
            # Send startup message
            await self.send_startup_message()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize bot: {e}")
            return False
    
    async def send_message(self, message: str, parse_mode: str = 'Markdown') -> bool:
        """Gửi message đến Telegram"""
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=parse_mode
            )
            logger.info("Message sent successfully")
            return True
            
        except TelegramError as e:
            logger.error(f"Telegram error: {e}")
            return False
            
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
    
    async def send_startup_message(self):
        """Gửi message khi bot khởi động"""
        message = f"""
🚀 **{config.BOT_NAME} Started**

✅ Bot is now monitoring pending orders
📊 Alert threshold: {config.ALERT_THRESHOLD}
⏰ Check interval: {config.CHECK_INTERVAL}s
🔗 Contract: `{config.CONTRACT_ADDRESS[:10]}...{config.CONTRACT_ADDRESS[-8:]}`

🎯 Will alert when pending orders > {config.ALERT_THRESHOLD}

#BotStarted #Monitoring
        """.strip()
        
        await self.send_message(message)
    
    async def monitoring_loop(self):
        """Main monitoring loop"""
        logger.info("Starting monitoring loop...")
        
        while self.is_running:
            try:
                # Get current pending orders info
                info = await monitor.get_detailed_info()
                count = info['count']
                
                logger.info(f"Check completed - Pending orders: {count}")
                
                # Check if should send alert
                if monitor.should_alert(count):
                    alert_message = monitor.format_alert_message(info)
                    await self.send_message(alert_message)
                    logger.info(f"Alert sent for {count} pending orders")
                
                # Send periodic status (mỗi 1 giờ)
                if self.should_send_status():
                    status_message = monitor.format_status_message(info)
                    await self.send_message(status_message)
                    logger.info("Status update sent")
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                
                # Send error notification nếu có nhiều lỗi liên tiếp
                if monitor.error_count >= 3:
                    error_message = f"""
❌ **Monitoring Error**

🔄 Consecutive errors: {monitor.error_count}
⏰ Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}
🔧 Error: {str(e)[:100]}...

Bot will continue trying...

#Error #Monitoring
                    """.strip()
                    
                    await self.send_message(error_message)
                    monitor.error_count = 0  # Reset để tránh spam
            
            # Wait before next check
            await asyncio.sleep(config.CHECK_INTERVAL)
    
    def should_send_status(self) -> bool:
        """Kiểm tra có nên gửi status update không (mỗi 1 giờ)"""
        if not monitor.last_check_time:
            return False
            
        # Gửi status mỗi 1 giờ
        time_since_startup = datetime.now(timezone.utc) - self.startup_time
        return time_since_startup.total_seconds() % 3600 < config.CHECK_INTERVAL
    
    async def run(self):
        """Chạy bot"""
        logger.info("Starting Pending Orders Bot...")
        
        # Initialize bot
        if not await self.initialize():
            logger.error("Failed to initialize bot")
            return
        
        # Start monitoring
        self.is_running = True
        
        try:
            await self.monitoring_loop()
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Bot crashed: {e}")
        finally:
            self.is_running = False
            await self.send_message("🛑 **Bot Stopped**\n\nMonitoring has been stopped.\n\n#BotStopped")

async def main():
    """Main function"""
    print(f"""
🎯 Pending Orders Telegram Bot
==============================
{config}
Starting bot...
    """)
    
    bot = PendingOrdersBot()
    await bot.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
