#!/usr/bin/env python3
"""
Deploy helper script cho Render.com
Tự động hóa quá trình chuẩn bị deploy

Tác giả: AI Assistant  
Ngày: 2025-09-17
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(cmd, description=""):
    """Chạy command và hiển thị kết quả"""
    if description:
        print(f"🔄 {description}...")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Success")
            if result.stdout.strip():
                print(f"   📝 {result.stdout.strip()}")
            return True
        else:
            print(f"   ❌ Failed: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def check_git_status():
    """Kiểm tra Git status"""
    print("📋 Checking Git status...")
    
    # Check if git repo exists
    if not os.path.exists('.git'):
        print("   ❌ Not a Git repository")
        print("   💡 Run: git init")
        return False
    
    # Check for uncommitted changes
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if result.stdout.strip():
        print("   ⚠️  Uncommitted changes found:")
        print(f"   📝 {result.stdout.strip()}")
        return False
    
    print("   ✅ Git status clean")
    return True

def create_env_template():
    """Tạo .env template nếu chưa có"""
    print("📝 Creating .env template...")
    
    if os.path.exists('.env'):
        print("   ✅ .env already exists")
        return True
    
    if not os.path.exists('.env.example'):
        print("   ❌ .env.example not found")
        return False
    
    # Copy .env.example to .env
    try:
        with open('.env.example', 'r') as src:
            content = src.read()
        
        with open('.env', 'w') as dst:
            dst.write(content)
        
        print("   ✅ .env created from template")
        print("   ⚠️  Please edit .env with your actual values")
        return True
        
    except Exception as e:
        print(f"   ❌ Error creating .env: {e}")
        return False

def validate_render_files():
    """Validate các file cần thiết cho Render"""
    print("🔍 Validating Render files...")
    
    required_files = {
        'requirements.txt': 'Python dependencies',
        'runtime.txt': 'Python version',
        'render.yaml': 'Render configuration',
        'bot.py': 'Main bot file'
    }
    
    missing = []
    for file, desc in required_files.items():
        if os.path.exists(file):
            print(f"   ✅ {file} ({desc})")
        else:
            print(f"   ❌ {file} missing ({desc})")
            missing.append(file)
    
    if missing:
        print(f"   ❌ Missing files: {', '.join(missing)}")
        return False
    
    print("   ✅ All Render files present")
    return True

def show_deployment_checklist():
    """Hiển thị checklist cho deployment"""
    print("\n" + "="*60)
    print("🚀 RENDER.COM DEPLOYMENT CHECKLIST")
    print("="*60)
    
    checklist = [
        "✅ Code pushed to GitHub",
        "🌐 Render.com account created", 
        "🔗 GitHub connected to Render",
        "📝 Environment variables ready",
        "🤖 Telegram bot token obtained",
        "💬 Telegram chat ID obtained"
    ]
    
    for item in checklist:
        print(f"   {item}")
    
    print("\n📋 DEPLOYMENT STEPS:")
    steps = [
        "1. Go to dashboard.render.com",
        "2. Click 'New +' → 'Web Service'", 
        "3. Connect your GitHub repository",
        "4. Configure service:",
        "   - Name: telegram-bot-pending-orders",
        "   - Environment: Python 3",
        "   - Build Command: pip install -r requirements.txt",
        "   - Start Command: python bot.py",
        "   - Plan: Free",
        "5. Set environment variables:",
        "   - TELEGRAM_BOT_TOKEN=your_token",
        "   - TELEGRAM_CHAT_ID=your_chat_id",
        "6. Click 'Create Web Service'",
        "7. Monitor deployment logs",
        "8. Check Telegram for startup message"
    ]
    
    for step in steps:
        print(f"   {step}")

def show_environment_variables():
    """Hiển thị environment variables cần set"""
    print("\n" + "="*60)
    print("🔧 ENVIRONMENT VARIABLES FOR RENDER")
    print("="*60)
    
    print("\n📋 REQUIRED (must set in Render dashboard):")
    required = [
        "TELEGRAM_BOT_TOKEN=your_actual_bot_token",
        "TELEGRAM_CHAT_ID=your_actual_chat_id"
    ]
    
    for var in required:
        print(f"   {var}")
    
    print("\n📋 OPTIONAL (have defaults, can override):")
    optional = [
        "ETHERSCAN_API_KEY=BNIYXSEUSR5WB9NPMZACEPXVF5YZ74HNNZ",
        "CONTRACT_ADDRESS=0xde605a918c466e74a2a12865efe616d51391312a",
        "CHECK_INTERVAL=300",
        "ALERT_THRESHOLD=18",
        "BOT_NAME=Pending Orders Monitor"
    ]
    
    for var in optional:
        print(f"   {var}")

def main():
    """Main deployment preparation function"""
    print("🎯 Render.com Deployment Helper")
    print("="*50)
    
    # Run pre-deployment checks
    checks = [
        ("Validate Render files", validate_render_files()),
        ("Create .env template", create_env_template()),
        ("Check Git status", check_git_status())
    ]
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    print(f"\n📊 Pre-deployment checks: {passed}/{total} passed")
    
    if passed == total:
        print("✅ All checks passed!")
        
        # Show deployment info
        show_deployment_checklist()
        show_environment_variables()
        
        print("\n" + "="*60)
        print("🎯 READY FOR DEPLOYMENT!")
        print("="*60)
        print("📖 For detailed instructions, see: README_RENDER.md")
        print("🧪 To test locally first, run: python test_render_deploy.py")
        
    else:
        print("❌ Some checks failed. Please fix issues before deploying.")
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Deployment preparation cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
