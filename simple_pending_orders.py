#!/usr/bin/env python3
"""
Simple Pending Orders Checker
Đơn giản check getPendingOrderIds từ proxy contract

Tác giả: AI Assistant
Ngày: 2025-09-17
"""

import asyncio
import aiohttp

async def get_pending_orders():
    """Check pending orders đơn giản"""
    
    # Config
    API_KEY = "BNIYXSEUSR5WB9NPMZACEPXVF5YZ74HNNZ"
    CONTRACT = "0xde605a918c466e74a2a12865efe616d51391312a"
    FUNCTION_SELECTOR = "0x7465c5e3"  # getPendingOrderIds()
    
    # API call
    url = f"https://api.etherscan.io/v2/api?chainid=480&module=proxy&action=eth_call&to={CONTRACT}&data={FUNCTION_SELECTOR}&tag=latest&apikey={API_KEY}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            
            if data.get('error'):
                print(f"❌ Error: {data['error']['message']}")
                return
            
            result = data.get('result', '0x')
            
            if not result or result == '0x':
                print("❌ No data returned")
                return
            
            # Decode array
            hex_data = result[2:]  # Remove 0x
            
            # Array offset (first 32 bytes)
            offset = int(hex_data[0:64], 16)
            
            # Array length (next 32 bytes)
            array_length = int(hex_data[64:128], 16)
            
            # Extract order IDs
            order_ids = []
            for i in range(array_length):
                start = 128 + (i * 64)
                if start + 64 <= len(hex_data):
                    order_id = int(hex_data[start:start + 64], 16)
                    order_ids.append(order_id)
            
            # Print results - chỉ hiển thị tổng số
            print("🎯 PENDING ORDERS:")
            print(f"📊 Total: {array_length}")

if __name__ == "__main__":
    asyncio.run(get_pending_orders())
