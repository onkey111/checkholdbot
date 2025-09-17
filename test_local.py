#!/usr/bin/env python3
"""
Test script để test bot locally trước khi deploy
Không cần Telegram, chỉ test monitoring logic

Tác giả: AI Assistant
Ngày: 2025-09-17
"""

import asyncio
import os
from monitor import monitor
from config import config

async def test_monitoring():
    """Test monitoring logic"""
    print("🧪 Testing Pending Orders Monitor")
    print("=" * 40)
    
    # Test config
    print(f"📊 Contract: {config.CONTRACT_ADDRESS}")
    print(f"🎯 Threshold: {config.ALERT_THRESHOLD}")
    print(f"⏰ Interval: {config.CHECK_INTERVAL}s")
    print()
    
    # Test API call
    print("🔍 Testing API call...")
    count = await monitor.get_pending_orders_count()
    
    if count is not None:
        print(f"✅ Success! Pending orders: {count}")
        
        # Test alert logic
        should_alert = monitor.should_alert(count)
        print(f"🚨 Should alert: {should_alert}")
        
        # Test message formatting
        info = await monitor.get_detailed_info()
        
        if should_alert:
            alert_msg = monitor.format_alert_message(info)
            print("\n📱 Alert Message:")
            print("-" * 30)
            print(alert_msg)
        
        status_msg = monitor.format_status_message(info)
        print("\n📊 Status Message:")
        print("-" * 30)
        print(status_msg)
        
    else:
        print("❌ Failed to get pending orders")
        print(f"🔄 Error count: {monitor.error_count}")

async def test_multiple_checks():
    """Test multiple checks để xem tracking logic"""
    print("\n🔄 Testing Multiple Checks")
    print("=" * 40)
    
    for i in range(3):
        print(f"\n📊 Check #{i+1}")
        info = await monitor.get_detailed_info()
        count = info['count']
        
        if count is not None:
            print(f"Count: {count}, Previous: {info['previous_count']}, Change: {info['change']}")
            should_alert = monitor.should_alert(count)
            print(f"Should alert: {should_alert}")
        else:
            print("Failed to get count")
        
        await asyncio.sleep(2)  # Wait 2 seconds between checks

async def main():
    """Main test function"""
    print("🎯 Pending Orders Bot - Local Test")
    print("=" * 50)
    
    # Set test environment (không cần Telegram tokens)
    os.environ['LOG_LEVEL'] = 'INFO'
    
    try:
        await test_monitoring()
        await test_multiple_checks()
        
        print("\n✅ All tests completed!")
        print("\n💡 Next steps:")
        print("1. Set TELEGRAM_BOT_TOKEN và TELEGRAM_CHAT_ID")
        print("2. Run: python bot.py")
        print("3. Deploy to Railway")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
