#!/usr/bin/env python3
"""
Worldscan Wallet Checker Tool
Sử dụng Etherscan API V2 để check Token Transfers (ERC-20) gần nhất và age của ví

Tác giả: AI Assistant
Ngày: 2025-09-17
"""

import asyncio
import aiohttp
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json

# ===== CẤU HÌNH =====

@dataclass
class WalletInfo:
    """Thông tin ví"""
    address: str
    first_transaction_date: Optional[datetime] = None
    latest_token_transfers: List[Dict] = None
    age_days: Optional[int] = None
    total_token_transfers: int = 0

class WorldscanChecker:
    """Tool check ví trên Worldscan"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.etherscan.io/v2/api"
        self.world_chain_id = 480  # World Chain Mainnet
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def _build_url(self, params: Dict[str, Any]) -> str:
        """Xây dựng URL API"""
        base_params = {
            'chainid': self.world_chain_id,
            'apikey': self.api_key,
            **params
        }
        
        # Loại bỏ các tham số None
        filtered_params = {k: v for k, v in base_params.items() if v is not None}
        
        # Tạo query string
        query_parts = []
        for key, value in filtered_params.items():
            query_parts.append(f"{key}={value}")
        
        query_string = "&".join(query_parts)
        return f"{self.base_url}?{query_string}"
    
    async def _make_request(self, url: str, max_retries: int = 3) -> Dict[str, Any]:
        """Thực hiện request với retry logic"""
        for attempt in range(max_retries):
            try:
                print(f"🔄 Đang gọi API... (attempt {attempt + 1})")
                
                async with self.session.get(url) as response:
                    if response.status != 200:
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message=f"HTTP {response.status}"
                        )
                    
                    data = await response.json()
                    
                    # Kiểm tra lỗi API
                    if data.get('status') == '0':
                        error_msg = data.get('message', data.get('result', 'Unknown API error'))
                        if 'rate limit' in error_msg.lower():
                            print(f"⚠️  Rate limit hit, waiting...")
                            await asyncio.sleep(2)
                            continue
                        raise Exception(f"API Error: {error_msg}")
                    
                    return data
                    
            except Exception as e:
                print(f"❌ Attempt {attempt + 1} failed: {str(e)}")
                
                if attempt == max_retries - 1:
                    raise e
                
                # Exponential backoff
                wait_time = 2 ** attempt
                print(f"⏳ Waiting {wait_time} seconds before retry...")
                await asyncio.sleep(wait_time)
        
        raise Exception("Max retries exceeded")
    
    async def get_token_transfers(
        self, 
        address: str, 
        page: int = 1, 
        offset: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Lấy danh sách token transfers ERC-20
        
        Args:
            address: Địa chỉ ví
            page: Số trang
            offset: Số records mỗi trang
            
        Returns:
            Danh sách token transfers
        """
        url = self._build_url({
            'module': 'account',
            'action': 'tokentx',
            'address': address,
            'startblock': 0,
            'endblock': 99999999,
            'page': page,
            'offset': offset,
            'sort': 'desc'  # Mới nhất trước
        })
        
        result = await self._make_request(url)
        return result.get('result', [])
    
    async def get_normal_transactions(
        self, 
        address: str, 
        page: int = 1, 
        offset: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Lấy danh sách giao dịch thường để tìm transaction đầu tiên
        
        Args:
            address: Địa chỉ ví
            page: Số trang
            offset: Số records mỗi trang
            
        Returns:
            Danh sách giao dịch
        """
        url = self._build_url({
            'module': 'account',
            'action': 'txlist',
            'address': address,
            'startblock': 0,
            'endblock': 99999999,
            'page': page,
            'offset': offset,
            'sort': 'asc'  # Cũ nhất trước để tìm first transaction
        })
        
        result = await self._make_request(url)
        return result.get('result', [])
    
    def _format_token_transfer(self, transfer: Dict) -> Dict:
        """Format thông tin token transfer"""
        try:
            # Chuyển đổi timestamp
            timestamp = int(transfer.get('timeStamp', 0))
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
            value = transfer.get('value', '0')
            decimals = int(transfer.get('tokenDecimal', 18))
            
            try:
                formatted_value = int(value) / (10 ** decimals)
            except:
                formatted_value = 0
            
            return {
                'hash': transfer.get('hash', 'N/A'),
                'from': transfer.get('from', 'N/A'),
                'to': transfer.get('to', 'N/A'),
                'token_name': transfer.get('tokenName', 'Unknown'),
                'token_symbol': transfer.get('tokenSymbol', 'N/A'),
                'value': formatted_value,
                'value_raw': value,
                'date': transfer_date.strftime('%Y-%m-%d %H:%M:%S UTC'),
                'age': age_str,
                'block_number': transfer.get('blockNumber', 'N/A'),
                'contract_address': transfer.get('contractAddress', 'N/A')
            }
        except Exception as e:
            print(f"⚠️  Error formatting transfer: {e}")
            return {
                'hash': transfer.get('hash', 'N/A'),
                'error': str(e),
                'raw_data': transfer
            }
    
    async def check_wallet(self, address: str) -> WalletInfo:
        """
        Check thông tin ví: token transfers gần nhất và age
        
        Args:
            address: Địa chỉ ví
            
        Returns:
            WalletInfo object
        """
        print(f"🔍 Checking wallet: {address}")
        print(f"🌍 Chain: World Chain (ID: {self.world_chain_id})")
        print("=" * 60)
        
        wallet_info = WalletInfo(address=address)
        
        try:
            # 1. Lấy token transfers gần nhất
            print("📋 Đang lấy Token Transfers (ERC-20)...")
            token_transfers = await self.get_token_transfers(address, page=1, offset=10)
            
            if token_transfers:
                wallet_info.total_token_transfers = len(token_transfers)
                wallet_info.latest_token_transfers = [
                    self._format_token_transfer(transfer) 
                    for transfer in token_transfers[:5]  # Chỉ lấy 5 cái gần nhất
                ]
                print(f"✅ Tìm thấy {len(token_transfers)} token transfers")
            else:
                print("❌ Không tìm thấy token transfers")
            
            # 2. Lấy giao dịch đầu tiên để tính age
            print("\n📅 Đang tìm giao dịch đầu tiên để tính age...")
            first_transactions = await self.get_normal_transactions(address, page=1, offset=1)
            
            if first_transactions:
                first_tx = first_transactions[0]
                timestamp = int(first_tx.get('timeStamp', 0))
                wallet_info.first_transaction_date = datetime.fromtimestamp(timestamp, tz=timezone.utc)
                
                # Tính age
                now = datetime.now(timezone.utc)
                age_delta = now - wallet_info.first_transaction_date
                wallet_info.age_days = age_delta.days
                
                print(f"✅ First transaction: {wallet_info.first_transaction_date.strftime('%Y-%m-%d %H:%M:%S UTC')}")
                print(f"✅ Wallet age: {wallet_info.age_days} ngày")
            else:
                print("❌ Không tìm thấy giao dịch nào")
            
            return wallet_info
            
        except Exception as e:
            print(f"❌ Error checking wallet: {e}")
            raise e
    
    def print_wallet_report(self, wallet_info: WalletInfo):
        """In báo cáo ví"""
        print("\n" + "=" * 60)
        print("📊 BÁO CÁO VÍ WORLDSCAN")
        print("=" * 60)
        
        print(f"🏠 Địa chỉ: {wallet_info.address}")
        
        if wallet_info.age_days is not None:
            print(f"📅 Age: {wallet_info.age_days} ngày")
            print(f"📅 First transaction: {wallet_info.first_transaction_date.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        else:
            print("📅 Age: Không xác định được")
        
        print(f"🔢 Total token transfers: {wallet_info.total_token_transfers}")
        
        if wallet_info.latest_token_transfers:
            print("\n🎯 TOKEN TRANSFERS GẦN NHẤT:")
            print("-" * 60)
            
            for i, transfer in enumerate(wallet_info.latest_token_transfers, 1):
                if 'error' in transfer:
                    print(f"{i}. ❌ Error: {transfer['error']}")
                    continue
                
                print(f"{i}. {transfer['token_symbol']} - {transfer['value']:.6f}")
                print(f"   📝 Hash: {transfer['hash']}")
                print(f"   👤 From: {transfer['from']}")
                print(f"   👤 To: {transfer['to']}")
                print(f"   ⏰ Time: {transfer['date']} ({transfer['age']})")
                print(f"   📦 Block: {transfer['block_number']}")
                print()
        else:
            print("\n❌ Không có token transfers")
        
        print("=" * 60)

# ===== MAIN FUNCTION =====

async def main():
    """Hàm chính"""
    # Cấu hình
    API_KEY = "BNIYXSEUSR5WB9NPMZACEPXVF5YZ74HNNZ"
    WALLET_ADDRESS = "0xde605a918c466e74a2a12865efe616d51391312a"
    
    print("🚀 WORLDSCAN WALLET CHECKER")
    print("🔧 Sử dụng Etherscan API V2")
    print(f"🔑 API Key: {API_KEY[:10]}...")
    print()
    
    try:
        async with WorldscanChecker(API_KEY) as checker:
            # Check wallet
            wallet_info = await checker.check_wallet(WALLET_ADDRESS)
            
            # In báo cáo
            checker.print_wallet_report(wallet_info)
            
            # Lưu kết quả ra file JSON
            output_file = f"wallet_report_{WALLET_ADDRESS[-8:]}.json"
            report_data = {
                'address': wallet_info.address,
                'age_days': wallet_info.age_days,
                'first_transaction_date': wallet_info.first_transaction_date.isoformat() if wallet_info.first_transaction_date else None,
                'total_token_transfers': wallet_info.total_token_transfers,
                'latest_token_transfers': wallet_info.latest_token_transfers,
                'checked_at': datetime.now(timezone.utc).isoformat()
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Báo cáo đã được lưu vào: {output_file}")
            
    except Exception as e:
        print(f"❌ Tool failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    # Chạy tool
    exit_code = asyncio.run(main())
    exit(exit_code)
