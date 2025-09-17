#!/usr/bin/env python3
"""
Configuration cho Telegram Bot
Quản lý environment variables và settings

Tác giả: AI Assistant
Ngày: 2025-09-17
"""

import os
from typing import Optional

# Load environment variables từ .env file
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file
except ImportError:
    # Fallback manual loading nếu không có python-dotenv
    def load_env_file():
        """Load environment variables từ .env file"""
        env_file = '.env'
        if os.path.exists(env_file):
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()

    load_env_file()

class Config:
    """Configuration class cho bot"""
    
    def __init__(self):
        # Telegram Bot Settings
        self.TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
        self.TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
        
        # Etherscan API Settings
        self.ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY', 'BNIYXSEUSR5WB9NPMZACEPXVF5YZ74HNNZ')
        
        # Contract Settings
        self.CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS', '0xde605a918c466e74a2a12865efe616d51391312a')
        self.FUNCTION_SELECTOR = os.getenv('FUNCTION_SELECTOR', '0x7465c5e3')  # getPendingOrderIds()
        
        # Monitoring Settings
        self.CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '300'))  # 5 phút
        self.ALERT_THRESHOLD = int(os.getenv('ALERT_THRESHOLD', '18'))  # Threshold để alert
        
        # API Settings
        self.CHAIN_ID = int(os.getenv('CHAIN_ID', '480'))  # World Chain
        self.API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.etherscan.io/v2/api')
        
        # Bot Settings
        self.BOT_NAME = os.getenv('BOT_NAME', 'Pending Orders Monitor')
        self.TIMEZONE = os.getenv('TIMEZONE', 'UTC')
        
        # Logging
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        
    def validate(self) -> bool:
        """Validate required environment variables"""
        required_vars = [
            ('TELEGRAM_BOT_TOKEN', self.TELEGRAM_BOT_TOKEN),
            ('TELEGRAM_CHAT_ID', self.TELEGRAM_CHAT_ID),
        ]
        
        missing_vars = []
        for var_name, var_value in required_vars:
            if not var_value:
                missing_vars.append(var_name)
        
        if missing_vars:
            print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
            return False
            
        return True
    
    def get_api_url(self) -> str:
        """Tạo API URL cho Etherscan call"""
        return f"{self.API_BASE_URL}?chainid={self.CHAIN_ID}&module=proxy&action=eth_call&to={self.CONTRACT_ADDRESS}&data={self.FUNCTION_SELECTOR}&tag=latest&apikey={self.ETHERSCAN_API_KEY}"
    
    def __str__(self) -> str:
        """String representation (ẩn sensitive data)"""
        return f"""
Config:
  Bot Name: {self.BOT_NAME}
  Contract: {self.CONTRACT_ADDRESS}
  Check Interval: {self.CHECK_INTERVAL}s
  Alert Threshold: {self.ALERT_THRESHOLD}
  Chain ID: {self.CHAIN_ID}
  Timezone: {self.TIMEZONE}
  Log Level: {self.LOG_LEVEL}
"""

# Global config instance
config = Config()
