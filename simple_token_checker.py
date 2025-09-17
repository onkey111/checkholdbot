#!/usr/bin/env python3
"""
Simple Token Transfer Checker
Chỉ check 1 TOKEN TRANSFER gần nhất trên Worldscan

Tác giả: AI Assistant
Ngày: 2025-09-17
"""

import asyncio
import aiohttp
from datetime import datetime, timezone

class SimpleTokenChecker:
    """Simple checker chỉ lấy 1 token transfer gần nhất"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.etherscan.io/v2/api"
        self.world_chain_id = 480
    
    async def get_latest_token_transfer(self, address: str):
        """Lấy 1 token transfer gần nhất"""
        
        url = f"{self.base_url}?chainid={self.world_chain_id}&module=account&action=tokentx&address={address}&startblock=0&endblock=99999999&page=1&offset=1&sort=desc&apikey={self.api_key}"
        
        async with aiohttp.ClientSession() as session:
            try:
                print(f"🔍 Checking latest token transfer for: {address}")
                
                async with session.get(url) as response:
                    data = await response.json()
                    
                    if data.get('status') == '0':
                        print(f"❌ Error: {data.get('message', 'Unknown error')}")
                        return None
                    
                    transfers = data.get('result', [])
                    
                    if not transfers:
                        print("❌ Không tìm thấy token transfers")
                        return None
                    
                    # Lấy transfer đầu tiên (gần nhất)
                    latest = transfers[0]
                    
                    # Format thông tin
                    timestamp = int(latest.get('timeStamp', 0))
                    transfer_date = datetime.fromtimestamp(timestamp, tz=timezone.utc)
                    
                    # Tính age
                    now = datetime.now(timezone.utc)
                    age_seconds = (now - transfer_date).total_seconds()
                    
                    if age_seconds < 3600:  # < 1 hour
                        age_str = f"{int(age_seconds // 60)} phút trước"
                    elif age_seconds < 86400:  # < 1 day
                        age_str = f"{int(age_seconds // 3600)} giờ trước"
                    else:  # >= 1 day
                        age_str = f"{int(age_seconds // 86400)} ngày trước"
                    
                    # Format value
                    value = latest.get('value', '0')
                    decimals = int(latest.get('tokenDecimal', 18))
                    formatted_value = int(value) / (10 ** decimals)
                    
                    result = {
                        'hash': latest.get('hash'),
                        'from': latest.get('from'),
                        'to': latest.get('to'),
                        'token_symbol': latest.get('tokenSymbol'),
                        'value': formatted_value,
                        'date': transfer_date.strftime('%Y-%m-%d %H:%M:%S UTC'),
                        'age': age_str,
                        'block': latest.get('blockNumber')
                    }
                    
                    return result
                    
            except Exception as e:
                print(f"❌ Error: {e}")
                return None

async def main():
    """Hàm chính"""
    
    # Cấu hình
    API_KEY = "BNIYXSEUSR5WB9NPMZACEPXVF5YZ74HNNZ"
    WALLET = "0xde605a918c466e74a2a12865efe616d51391312a"
    
    print("🚀 SIMPLE TOKEN TRANSFER CHECKER")
    print("🌍 World Chain - Chỉ check 1 transfer gần nhất")
    print("=" * 50)
    
    checker = SimpleTokenChecker(API_KEY)
    result = await checker.get_latest_token_transfer(WALLET)
    
    if result:
        print("\n✅ LATEST TOKEN TRANSFER:")
        print("-" * 30)
        print(f"🪙 Token: {result['token_symbol']}")
        print(f"💰 Amount: {result['value']:.6f}")
        print(f"📝 Hash: {result['hash']}")
        print(f"👤 From: {result['from']}")
        print(f"👤 To: {result['to']}")
        print(f"⏰ Time: {result['date']}")
        print(f"🕐 Age: {result['age']}")
        print(f"📦 Block: {result['block']}")
    else:
        print("❌ Không tìm thấy token transfer nào")

if __name__ == "__main__":
    asyncio.run(main())
