#!/usr/bin/env python3
"""
Test script để kiểm tra bot trước khi deploy lên Render.com
Kiểm tra tất cả dependencies và configuration

Tác giả: AI Assistant
Ngày: 2025-09-17
"""

import os
import sys
import asyncio
import importlib.util
from pathlib import Path

def check_python_version():
    """Kiểm tra Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major != 3 or version.minor < 8:
        print("   ❌ Python 3.8+ required")
        return False
    print("   ✅ Python version OK")
    return True

def check_dependencies():
    """Kiểm tra tất cả dependencies"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'telegram',
        'aiohttp', 
        'dotenv'
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'dotenv':
                import dotenv
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("   ✅ All dependencies OK")
    return True

def check_files():
    """Kiểm tra các file cần thiết"""
    print("\n📁 Checking required files...")
    
    required_files = [
        'bot.py',
        'config.py', 
        'monitor.py',
        'requirements.txt',
        'runtime.txt',
        'render.yaml',
        '.env.example'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MISSING")
            missing.append(file)
    
    if missing:
        print(f"\n❌ Missing files: {', '.join(missing)}")
        return False
    
    print("   ✅ All files OK")
    return True

def check_environment():
    """Kiểm tra environment variables"""
    print("\n🔧 Checking environment variables...")
    
    # Load .env nếu có
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except:
        pass
    
    required_vars = [
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_CHAT_ID'
    ]
    
    optional_vars = [
        'ETHERSCAN_API_KEY',
        'CONTRACT_ADDRESS',
        'CHECK_INTERVAL',
        'ALERT_THRESHOLD'
    ]
    
    missing_required = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Ẩn sensitive data
            display_value = f"{value[:8]}..." if len(value) > 8 else "***"
            print(f"   ✅ {var}={display_value}")
        else:
            print(f"   ❌ {var} - MISSING")
            missing_required.append(var)
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}={value}")
        else:
            print(f"   ⚠️  {var} - using default")
    
    if missing_required:
        print(f"\n❌ Missing required variables: {', '.join(missing_required)}")
        print("Create .env file with required values")
        return False
    
    print("   ✅ Environment OK")
    return True

async def test_bot_import():
    """Test import bot modules"""
    print("\n🤖 Testing bot imports...")
    
    try:
        from config import config
        print("   ✅ config.py imported")
        
        from monitor import monitor  
        print("   ✅ monitor.py imported")
        
        # Test config validation
        if config.validate():
            print("   ✅ config validation passed")
        else:
            print("   ❌ config validation failed")
            return False
            
        print("   ✅ Bot modules OK")
        return True
        
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False

async def test_telegram_connection():
    """Test Telegram bot connection"""
    print("\n📱 Testing Telegram connection...")
    
    try:
        from telegram import Bot
        from config import config
        
        if not config.TELEGRAM_BOT_TOKEN:
            print("   ⚠️  No bot token, skipping connection test")
            return True
        
        bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
        bot_info = await bot.get_me()
        print(f"   ✅ Connected to @{bot_info.username}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return False

def check_render_config():
    """Kiểm tra Render.com configuration"""
    print("\n🌐 Checking Render.com config...")
    
    # Check render.yaml
    if os.path.exists('render.yaml'):
        print("   ✅ render.yaml exists")
    else:
        print("   ❌ render.yaml missing")
        return False
    
    # Check runtime.txt
    if os.path.exists('runtime.txt'):
        with open('runtime.txt', 'r') as f:
            runtime = f.read().strip()
        print(f"   ✅ runtime.txt: {runtime}")
    else:
        print("   ❌ runtime.txt missing")
        return False
    
    print("   ✅ Render config OK")
    return True

async def main():
    """Main test function"""
    print("🧪 Testing bot for Render.com deployment")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version()),
        ("Dependencies", check_dependencies()),
        ("Required Files", check_files()),
        ("Environment Variables", check_environment()),
        ("Bot Imports", await test_bot_import()),
        ("Telegram Connection", await test_telegram_connection()),
        ("Render Config", check_render_config())
    ]
    
    passed = 0
    total = len(checks)
    
    for name, result in checks:
        if result:
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("✅ All tests passed! Ready for Render.com deployment")
        print("\n🚀 Next steps:")
        print("1. Push code to GitHub")
        print("2. Create Web Service on render.com")
        print("3. Set environment variables")
        print("4. Deploy!")
        return True
    else:
        print("❌ Some tests failed. Fix issues before deploying.")
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n👋 Test interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        sys.exit(1)
