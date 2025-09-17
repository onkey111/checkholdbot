#!/usr/bin/env python3
"""
Pending Orders Monitor
Logic check pending orders từ smart contract

Tác giả: AI Assistant  
Ngày: 2025-09-17
"""

import asyncio
import aiohttp
import logging
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from config import config

# Setup logging
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class PendingOrdersMonitor:
    """Monitor pending orders từ smart contract"""
    
    def __init__(self):
        self.last_count = 0
        self.last_check_time = None
        self.error_count = 0
        
    async def get_pending_orders_count(self) -> Optional[int]:
        """
        Check pending orders count từ contract
        Sử dụng logic từ simple_pending_orders.py
        """
        try:
            url = config.get_api_url()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as response:
                    data = await response.json()
                    
                    # Check for API errors
                    if data.get('error'):
                        logger.error(f"API Error: {data['error']['message']}")
                        return None
                    
                    result = data.get('result', '0x')
                    
                    if not result or result == '0x':
                        logger.warning("No data returned from contract")
                        return 0
                    
                    # Decode array data
                    hex_data = result[2:]  # Remove 0x prefix
                    
                    if len(hex_data) < 128:
                        logger.warning("Insufficient data length")
                        return 0
                    
                    # Array offset (first 32 bytes) - không dùng nhưng cần skip
                    offset = int(hex_data[0:64], 16)
                    
                    # Array length (next 32 bytes) - đây là số pending orders
                    array_length = int(hex_data[64:128], 16)
                    
                    logger.info(f"Successfully retrieved pending orders count: {array_length}")
                    self.error_count = 0  # Reset error count on success
                    
                    return array_length
                    
        except asyncio.TimeoutError:
            logger.error("Timeout while fetching pending orders")
            self.error_count += 1
            return None
            
        except Exception as e:
            logger.error(f"Error fetching pending orders: {e}")
            self.error_count += 1
            return None
    
    async def get_detailed_info(self) -> Dict[str, Any]:
        """Lấy thông tin chi tiết cho notification"""
        count = await self.get_pending_orders_count()
        current_time = datetime.now(timezone.utc)
        
        info = {
            'count': count,
            'timestamp': current_time,
            'formatted_time': current_time.strftime('%Y-%m-%d %H:%M:%S UTC'),
            'previous_count': self.last_count,
            'change': count - self.last_count if count is not None else 0,
            'threshold': config.ALERT_THRESHOLD,
            'contract': config.CONTRACT_ADDRESS,
            'error_count': self.error_count
        }
        
        # Update tracking
        if count is not None:
            self.last_count = count
        self.last_check_time = current_time
        
        return info
    
    def should_alert(self, count: Optional[int]) -> bool:
        """
        Kiểm tra có nên gửi alert không
        - Count > threshold
        - Count khác với lần check trước (tránh spam)
        """
        if count is None:
            return False
            
        # Alert nếu vượt threshold và khác với lần trước
        if count > config.ALERT_THRESHOLD and count != self.last_count:
            return True
            
        return False
    
    def format_alert_message(self, info: Dict[str, Any]) -> str:
        """Format message cho Telegram alert"""
        count = info['count']
        change = info['change']
        
        # Emoji cho trend
        trend_emoji = "📈" if change > 0 else "📉" if change < 0 else "➡️"
        
        # Alert level
        if count > config.ALERT_THRESHOLD + 10:
            alert_level = "🚨 HIGH ALERT"
        elif count > config.ALERT_THRESHOLD + 5:
            alert_level = "⚠️ MEDIUM ALERT"
        else:
            alert_level = "🔔 ALERT"
        
        message = f"""
{alert_level} 🎯

📊 **Pending Orders: {count}**
{trend_emoji} Change: {change:+d} orders
📈 Threshold: {info['threshold']}
⏰ Time: {info['formatted_time']}

🔗 Contract: `{info['contract'][:10]}...{info['contract'][-8:]}`

#PendingOrders #WorldChain #Alert
        """.strip()
        
        return message
    
    def format_status_message(self, info: Dict[str, Any]) -> str:
        """Format message cho status update"""
        count = info['count']
        
        if count is None:
            return f"❌ **Status Check Failed**\n⏰ {info['formatted_time']}\n🔄 Error count: {info['error_count']}"
        
        status_emoji = "✅" if count <= config.ALERT_THRESHOLD else "⚠️"
        
        message = f"""
{status_emoji} **Status Update**

📊 Pending Orders: {count}
📈 Threshold: {info['threshold']}
⏰ Last Check: {info['formatted_time']}
🔄 Monitoring: Active

#Status #PendingOrders
        """.strip()
        
        return message

# Global monitor instance
monitor = PendingOrdersMonitor()
