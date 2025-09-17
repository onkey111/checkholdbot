"""
Worldscan & BSCScan API Examples - Python Implementation
Hướng dẫn sử dụng API cho World Chain và Binance Smart Chain

Tác giả: AI Assistant
Ngày: 2025-09-17
"""

import asyncio
import aiohttp
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

# ===== CẤU HÌNH VÀ CONSTANTS =====

class ChainType(Enum):
    """Enum định nghĩa các loại blockchain được hỗ trợ"""
    ETHEREUM = 1
    BSC = 56
    POLYGON = 137
    ARBITRUM = 42161
    OPTIMISM = 10
    WORLD_CHAIN = 480

@dataclass
class ApiConfig:
    """Cấu hình API"""
    api_key: str
    base_url: str = "https://api.etherscan.io/v2/api"
    rate_limit_per_second: int = 5
    max_retries: int = 3
    timeout: int = 30

# ===== RATE LIMITER =====

class RateLimiter:
    """Rate limiter để tuân thủ giới hạn API"""
    
    def __init__(self, calls_per_second: int = 5):
        self.calls_per_second = calls_per_second
        self.last_call_time = 0
        self.call_interval = 1.0 / calls_per_second
    
    async def wait_if_needed(self):
        """Chờ nếu cần thiết để tuân thủ rate limit"""
        current_time = time.time()
        time_since_last_call = current_time - self.last_call_time
        
        if time_since_last_call < self.call_interval:
            wait_time = self.call_interval - time_since_last_call
            await asyncio.sleep(wait_time)
        
        self.last_call_time = time.time()

# ===== MAIN API CLIENT =====

class EtherscanV2Client:
    """Client chính cho Etherscan API V2"""
    
    def __init__(self, config: ApiConfig):
        self.config = config
        self.rate_limiter = RateLimiter(config.rate_limit_per_second)
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.config.timeout)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def _build_url(self, chain_id: int, params: Dict[str, Any]) -> str:
        """Xây dựng URL API với các tham số"""
        base_params = {
            'chainid': chain_id,
            'apikey': self.config.api_key,
            **params
        }
        
        # Loại bỏ các tham số None
        filtered_params = {k: v for k, v in base_params.items() if v is not None}
        
        # Tạo query string
        query_parts = []
        for key, value in filtered_params.items():
            query_parts.append(f"{key}={value}")
        
        query_string = "&".join(query_parts)
        return f"{self.config.base_url}?{query_string}"
    
    async def _make_request(self, url: str) -> Dict[str, Any]:
        """Thực hiện request với retry logic"""
        await self.rate_limiter.wait_if_needed()
        
        for attempt in range(self.config.max_retries):
            try:
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
                        raise Exception(f"API Error: {error_msg}")
                    
                    return data
                    
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                
                if attempt == self.config.max_retries - 1:
                    raise e
                
                # Exponential backoff
                wait_time = 2 ** attempt
                await asyncio.sleep(wait_time)
        
        raise Exception("Max retries exceeded")

# ===== ACCOUNT OPERATIONS =====

    async def get_account_balance(self, chain_id: int, address: str) -> str:
        """
        Lấy số dư native token (ETH/BNB/WLD) của địa chỉ
        
        Args:
            chain_id: ID của blockchain
            address: Địa chỉ ví
            
        Returns:
            Số dư tính bằng wei (string)
        """
        url = self._build_url(chain_id, {
            'module': 'account',
            'action': 'balance',
            'address': address,
            'tag': 'latest'
        })
        
        result = await self._make_request(url)
        return result['result']
    
    async def get_account_transactions(
        self, 
        chain_id: int, 
        address: str, 
        page: int = 1, 
        offset: int = 10,
        start_block: int = 0,
        end_block: int = 99999999
    ) -> List[Dict[str, Any]]:
        """
        Lấy danh sách giao dịch của địa chỉ
        
        Args:
            chain_id: ID của blockchain
            address: Địa chỉ ví
            page: Số trang (bắt đầu từ 1)
            offset: Số giao dịch mỗi trang (tối đa 10000)
            start_block: Block bắt đầu
            end_block: Block kết thúc
            
        Returns:
            Danh sách giao dịch
        """
        url = self._build_url(chain_id, {
            'module': 'account',
            'action': 'txlist',
            'address': address,
            'startblock': start_block,
            'endblock': end_block,
            'page': page,
            'offset': offset,
            'sort': 'desc'
        })
        
        result = await self._make_request(url)
        return result['result']

# ===== TOKEN OPERATIONS =====

    async def get_token_balance(
        self, 
        chain_id: int, 
        contract_address: str, 
        address: str
    ) -> str:
        """
        Lấy số dư token ERC-20
        
        Args:
            chain_id: ID của blockchain
            contract_address: Địa chỉ contract token
            address: Địa chỉ ví
            
        Returns:
            Số dư token (string)
        """
        url = self._build_url(chain_id, {
            'module': 'account',
            'action': 'tokenbalance',
            'contractaddress': contract_address,
            'address': address,
            'tag': 'latest'
        })
        
        result = await self._make_request(url)
        return result['result']
    
    async def get_token_transfers(
        self, 
        chain_id: int, 
        address: str, 
        contract_address: Optional[str] = None,
        page: int = 1,
        offset: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Lấy danh sách token transfers
        
        Args:
            chain_id: ID của blockchain
            address: Địa chỉ ví
            contract_address: Địa chỉ contract (optional)
            page: Số trang
            offset: Số records mỗi trang
            
        Returns:
            Danh sách token transfers
        """
        params = {
            'module': 'account',
            'action': 'tokentx',
            'address': address,
            'startblock': 0,
            'endblock': 99999999,
            'page': page,
            'offset': offset,
            'sort': 'desc'
        }
        
        if contract_address:
            params['contractaddress'] = contract_address
        
        url = self._build_url(chain_id, params)
        result = await self._make_request(url)
        return result['result']

# ===== BLOCK & TRANSACTION OPERATIONS =====

    async def get_latest_block_number(self, chain_id: int) -> int:
        """
        Lấy số block mới nhất
        
        Args:
            chain_id: ID của blockchain
            
        Returns:
            Số block mới nhất
        """
        url = self._build_url(chain_id, {
            'module': 'proxy',
            'action': 'eth_blockNumber'
        })
        
        result = await self._make_request(url)
        return int(result['result'], 16)
    
    async def get_transaction(self, chain_id: int, tx_hash: str) -> Dict[str, Any]:
        """
        Lấy thông tin giao dịch
        
        Args:
            chain_id: ID của blockchain
            tx_hash: Hash giao dịch
            
        Returns:
            Thông tin giao dịch
        """
        url = self._build_url(chain_id, {
            'module': 'proxy',
            'action': 'eth_getTransactionByHash',
            'txhash': tx_hash
        })
        
        result = await self._make_request(url)
        return result['result']

# ===== MULTICHAIN OPERATIONS =====

    async def get_multichain_balances(
        self, 
        address: str, 
        chain_ids: List[int]
    ) -> Dict[int, Dict[str, Any]]:
        """
        Lấy số dư của cùng một địa chỉ trên nhiều chain
        
        Args:
            address: Địa chỉ ví
            chain_ids: Danh sách chain IDs
            
        Returns:
            Dictionary chứa số dư theo chain
        """
        tasks = []
        for chain_id in chain_ids:
            task = self._get_balance_with_error_handling(chain_id, address)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        balances = {}
        for i, result in enumerate(results):
            chain_id = chain_ids[i]
            if isinstance(result, Exception):
                balances[chain_id] = {
                    'balance': None,
                    'error': str(result)
                }
            else:
                balances[chain_id] = {
                    'balance': result,
                    'error': None
                }
        
        return balances
    
    async def _get_balance_with_error_handling(self, chain_id: int, address: str) -> str:
        """Helper method để lấy balance với error handling"""
        try:
            return await self.get_account_balance(chain_id, address)
        except Exception as e:
            raise e

# ===== UTILITY FUNCTIONS =====

def wei_to_ether(wei_amount: str) -> float:
    """Chuyển đổi từ wei sang ether"""
    return int(wei_amount) / 10**18

def format_chain_name(chain_id: int) -> str:
    """Lấy tên chain từ chain ID"""
    chain_names = {
        1: "Ethereum",
        56: "BSC",
        137: "Polygon", 
        42161: "Arbitrum",
        10: "Optimism",
        480: "World Chain"
    }
    return chain_names.get(chain_id, f"Chain {chain_id}")

# ===== VÍ DỤ SỬ DỤNG =====

async def demo_usage():
    """Demo cách sử dụng API"""
    
    # Cấu hình API (thay YOUR_API_KEY bằng key thật)
    config = ApiConfig(
        api_key="YOUR_API_KEY_HERE",
        rate_limit_per_second=5
    )
    
    # Địa chỉ demo (Vitalik Buterin)
    demo_address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    
    async with EtherscanV2Client(config) as client:
        print("=== DEMO ETHERSCAN API V2 - PYTHON ===\n")
        
        try:
            # 1. Lấy số dư trên World Chain
            print("1. Số dư trên World Chain:")
            world_balance = await client.get_account_balance(
                ChainType.WORLD_CHAIN.value, 
                demo_address
            )
            world_balance_eth = wei_to_ether(world_balance)
            print(f"   {world_balance} wei ({world_balance_eth:.6f} ETH)\n")
            
            # 2. Lấy số dư trên BSC
            print("2. Số dư trên BSC:")
            bsc_balance = await client.get_account_balance(
                ChainType.BSC.value, 
                demo_address
            )
            bsc_balance_bnb = wei_to_ether(bsc_balance)
            print(f"   {bsc_balance} wei ({bsc_balance_bnb:.6f} BNB)\n")
            
            # 3. Lấy giao dịch gần nhất trên Ethereum
            print("3. Giao dịch gần nhất trên Ethereum:")
            eth_txs = await client.get_account_transactions(
                ChainType.ETHEREUM.value, 
                demo_address, 
                page=1, 
                offset=3
            )
            
            for i, tx in enumerate(eth_txs[:2]):
                value_eth = wei_to_ether(tx['value'])
                print(f"   TX {i+1}: {tx['hash']}")
                print(f"   Value: {tx['value']} wei ({value_eth:.6f} ETH)")
                print(f"   Gas Used: {tx['gasUsed']}")
                print(f"   Block: {tx['blockNumber']}\n")
            
            # 4. Multichain balance check
            print("4. Số dư trên nhiều chain:")
            chain_ids = [
                ChainType.ETHEREUM.value,
                ChainType.BSC.value,
                ChainType.WORLD_CHAIN.value
            ]
            
            multichain_balances = await client.get_multichain_balances(
                demo_address, 
                chain_ids
            )
            
            for chain_id, data in multichain_balances.items():
                chain_name = format_chain_name(chain_id)
                if data['error']:
                    print(f"   {chain_name}: Error - {data['error']}")
                else:
                    balance_eth = wei_to_ether(data['balance'])
                    print(f"   {chain_name}: {data['balance']} wei ({balance_eth:.6f} native token)")
            
            print("\n=== DEMO HOÀN THÀNH ===")
            
        except Exception as e:
            print(f"Demo failed: {str(e)}")

# ===== MAIN EXECUTION =====

if __name__ == "__main__":
    # Chạy demo
    asyncio.run(demo_usage())
