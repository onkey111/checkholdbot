# Hướng Dẫn Toàn Diện Etherscan API V2 - Worldscan & BSCScan 2025

## 📋 Mục Lục
1. [Tổng Quan API V2](#tổng-quan-api-v2)
2. [So Sánh API V1 vs V2](#so-sánh-api-v1-vs-v2)
3. [Worldscan Implementation](#worldscan-implementation)
4. [BSCScan Implementation](#bscscan-implementation)
5. [Bảo Mật và Quyền Riêng Tư](#bảo-mật-và-quyền-riêng-tư)
6. [Code Examples](#code-examples)
7. [Developer Experience](#developer-experience)
8. [Hạn Chế và Thách Thức](#hạn-chế-và-thách-thức)
9. [Best Practices](#best-practices)

---

## 🚀 Tổng Quan API V2

### Etherscan API V2 - Unified Multichain Approach

**Etherscan API V2** là phiên bản mới nhất (2025) cung cấp truy cập thống nhất đến dữ liệu của 50+ blockchain EVM thông qua một API key duy nhất.

#### Đặc Điểm Chính:
- **Unified Endpoint**: `https://api.etherscan.io/v2/api`
- **Single API Key**: Một key cho tất cả chains
- **50+ Chains**: Hỗ trợ Ethereum, BSC, Polygon, Arbitrum, Optimism, World Chain, v.v.
- **Chain ID Parameter**: Sử dụng `chainid` để chỉ định blockchain
- **Backward Compatible**: Tương thích ngược với V1

#### Cấu Trúc URL Mới:
```
https://api.etherscan.io/v2/api?chainid={chain_id}&module={module}&action={action}&apikey={api_key}
```

#### Chain IDs Quan Trọng:
- **Ethereum Mainnet**: 1
- **BSC (Binance Smart Chain)**: 56
- **World Chain Mainnet**: 480
- **Polygon**: 137
- **Arbitrum One**: 42161
- **Optimism**: 10

---

## 🔄 So Sánh API V1 vs V2

### API V1 (Legacy)
```javascript
// V1 - Riêng biệt cho từng chain
const etherscanUrl = "https://api.etherscan.io/api"
const bscscanUrl = "https://api.bscscan.com/api"
const polygonscanUrl = "https://api.polygonscan.com/api"

// Cần nhiều API keys
const ethKey = "ETH_API_KEY"
const bscKey = "BSC_API_KEY"
const polyKey = "POLY_API_KEY"
```

### API V2 (Mới)
```javascript
// V2 - Unified endpoint
const baseUrl = "https://api.etherscan.io/v2/api"
const apiKey = "SINGLE_API_KEY"

// Chỉ cần thay đổi chainid
const ethUrl = `${baseUrl}?chainid=1&module=account&action=balance&apikey=${apiKey}`
const bscUrl = `${baseUrl}?chainid=56&module=account&action=balance&apikey=${apiKey}`
const worldUrl = `${baseUrl}?chainid=480&module=account&action=balance&apikey=${apiKey}`
```

### Lợi Ích Migration V2:
1. **Đơn Giản Hóa**: Một API key thay vì nhiều keys
2. **Tiết Kiệm Chi Phí**: Không cần subscribe nhiều services
3. **Quản Lý Dễ Dàng**: Centralized account management
4. **Consistent Interface**: Cùng endpoints cho tất cả chains
5. **Future-Proof**: Hỗ trợ chains mới tự động

### Migration Deadline:
- **V1 Deprecation**: 31/05/2025
- **Khuyến Nghị**: Migrate ngay để tránh service interruption

---

## 🌍 Worldscan Implementation

### Thông Tin Cơ Bản
- **URL**: https://worldscan.org
- **Chain ID**: 480 (0x1e0)
- **Native Token**: ETH
- **RPC URL**: `https://worldchain-mainnet.g.alchemy.com/public`
- **Built By**: Team Etherscan

### Đặc Điểm Worldscan:
1. **Etherscan-Compatible**: Sử dụng cùng codebase với Etherscan
2. **Layer 2 Features**: Hỗ trợ L1→L2 và L2→L1 transactions
3. **API Registration**: Có thể đăng ký account để sử dụng API
4. **MetaMask Integration**: Built-in wallet connection

### API Endpoints Worldscan:
```javascript
// Lấy balance trên World Chain
const worldBalance = await fetch(
  `https://api.etherscan.io/v2/api?chainid=480&module=account&action=balance&address=${address}&tag=latest&apikey=${apiKey}`
)

// Lấy transactions
const worldTxs = await fetch(
  `https://api.etherscan.io/v2/api?chainid=480&module=account&action=txlist&address=${address}&apikey=${apiKey}`
)
```

### World Chain Network Config:
```javascript
// MetaMask network config
{
  chainId: '0x1e0',
  chainName: 'Worldchain Mainnet',
  nativeCurrency: {
    name: 'ETH',
    symbol: 'ETH',
    decimals: 18
  },
  rpcUrls: ['https://worldchain-mainnet.g.alchemy.com/public'],
  blockExplorerUrls: ['https://worldscan.org']
}
```

---

## 🟡 BSCScan Implementation

### Migration Notice
**BSCScan đã migrate sang Etherscan API V2!**

### Thông Tin Cơ Bản:
- **Chain ID**: 56
- **Native Token**: BNB
- **API Access**: Thông qua Etherscan API V2
- **Legacy URL**: https://api.bscscan.com (deprecated)

### Migration Pattern:
```javascript
// Cũ (V1)
const bscUrl = "https://api.bscscan.com/api?module=account&action=balance&address=${address}&apikey=${bscKey}"

// Mới (V2)
const bscUrl = "https://api.etherscan.io/v2/api?chainid=56&module=account&action=balance&address=${address}&apikey=${ethKey}"
```

### Lợi Ích Migration BSC:
1. **Unified Management**: Quản lý tất cả chains từ một dashboard
2. **Cost Effective**: Không cần riêng BSC subscription
3. **Better Rate Limits**: Shared limits across chains
4. **Consistent Updates**: Cùng feature rollout với Ethereum

---

## 🔒 Bảo Mật và Quyền Riêng Tư

### Rate Limiting
```
API Tier          | Rate Limit      | Daily Limit
------------------|-----------------|-------------
Free              | 5 calls/sec     | 100,000
Standard ($199)   | 10 calls/sec    | 1,000,000
Advanced ($399)   | 25 calls/sec    | 5,000,000
Professional ($999)| 50 calls/sec   | 10,000,000
```

### Security Best Practices:

#### 1. API Key Management
```javascript
// ✅ Đúng - Sử dụng environment variables
const apiKey = process.env.ETHERSCAN_API_KEY

// ❌ Sai - Hardcode trong code
const apiKey = "YourApiKeyToken"
```

#### 2. Rate Limiting Implementation
```javascript
class RateLimiter {
  constructor(callsPerSecond = 5) {
    this.interval = 1000 / callsPerSecond
    this.lastCall = 0
  }
  
  async waitIfNeeded() {
    const now = Date.now()
    const timeSinceLastCall = now - this.lastCall
    
    if (timeSinceLastCall < this.interval) {
      await new Promise(resolve => 
        setTimeout(resolve, this.interval - timeSinceLastCall)
      )
    }
    
    this.lastCall = Date.now()
  }
}
```

#### 3. Error Handling
```javascript
async function safeApiCall(url, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url)
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }
      
      const data = await response.json()
      
      if (data.status === '0') {
        throw new Error(`API Error: ${data.message}`)
      }
      
      return data
    } catch (error) {
      if (i === retries - 1) throw error
      
      // Exponential backoff
      await new Promise(resolve => 
        setTimeout(resolve, Math.pow(2, i) * 1000)
      )
    }
  }
}
```

### Privacy Considerations:

#### 1. Data Collection
- **IP Tracking**: APIs log IP addresses
- **Request Patterns**: Usage patterns có thể được phân tích
- **Address Correlation**: Có thể link addresses với IP

#### 2. Privacy Protection
```javascript
// Sử dụng proxy hoặc VPN
const proxyConfig = {
  proxy: {
    host: 'proxy-server.com',
    port: 8080
  }
}

// Rotate API keys
const apiKeys = ['key1', 'key2', 'key3']
const randomKey = apiKeys[Math.floor(Math.random() * apiKeys.length)]
```

#### 3. Data Minimization
```javascript
// Chỉ request data cần thiết
const minimalParams = {
  module: 'account',
  action: 'balance',
  address: targetAddress,
  tag: 'latest'
  // Không include unnecessary parameters
}
```

---

## 💻 Code Examples

### JavaScript/Node.js Example
```javascript
const EtherscanV2 = require('./etherscan_api_v2_examples.js')

async function main() {
  const config = {
    API_KEY: process.env.ETHERSCAN_API_KEY,
    BASE_URL: 'https://api.etherscan.io/v2/api'
  }
  
  // Lấy balance trên nhiều chains
  const address = '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045'
  const chains = [1, 56, 480] // ETH, BSC, World Chain
  
  const balances = await EtherscanV2.getMultichainBalances(address, chains)
  console.log('Multichain Balances:', balances)
}

main().catch(console.error)
```

### Python Example
```python
import asyncio
from worldscan_bscscan_examples import EtherscanV2Client, ApiConfig, ChainType

async def main():
    config = ApiConfig(
        api_key="YOUR_API_KEY",
        rate_limit_per_second=5
    )
    
    async with EtherscanV2Client(config) as client:
        # Lấy balance trên World Chain
        balance = await client.get_account_balance(
            ChainType.WORLD_CHAIN.value,
            "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
        )
        print(f"World Chain Balance: {balance} wei")

if __name__ == "__main__":
    asyncio.run(main())
```

### cURL Examples
```bash
# Lấy balance trên World Chain
curl "https://api.etherscan.io/v2/api?chainid=480&module=account&action=balance&address=0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045&tag=latest&apikey=YOUR_API_KEY"

# Lấy balance trên BSC
curl "https://api.etherscan.io/v2/api?chainid=56&module=account&action=balance&address=0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045&tag=latest&apikey=YOUR_API_KEY"

# Lấy transactions
curl "https://api.etherscan.io/v2/api?chainid=480&module=account&action=txlist&address=0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045&startblock=0&endblock=99999999&page=1&offset=10&sort=desc&apikey=YOUR_API_KEY"
```

---

## 👨‍💻 Developer Experience

### Điểm Mạnh:
1. **Comprehensive Documentation**: Docs chi tiết và examples
2. **Consistent API Design**: Cùng pattern cho tất cả endpoints
3. **Good Error Messages**: Error messages rõ ràng và actionable
4. **Multiple SDKs**: Hỗ trợ nhiều programming languages
5. **Active Community**: Large developer community và support

### Điểm Cần Cải Thiện:
1. **Rate Limiting**: Free tier khá restrictive (5 calls/sec)
2. **Documentation Fragmentation**: Một số docs chưa update V2
3. **Error Handling**: Một số edge cases chưa được document rõ
4. **SDK Quality**: Official SDKs chưa có cho tất cả languages

### Developer Feedback:
- **Positive**: "API rất stable và reliable"
- **Positive**: "Migration V2 giúp simplify multichain development"
- **Negative**: "Rate limits quá thấp cho development"
- **Negative**: "Pricing khá cao cho small projects"

---

## ⚠️ Hạn Chế và Thách Thức

### Technical Limitations:

#### 1. Rate Limiting
```javascript
// Problem: Free tier chỉ 5 calls/second
const rateLimitError = {
  status: "0",
  message: "Max rate limit reached",
  result: "Max rate limit reached, rate limit of 5/1sec applied"
}

// Solution: Implement proper rate limiting
const rateLimiter = new RateLimiter(5) // 5 calls/sec
await rateLimiter.waitIfNeeded()
```

#### 2. Data Freshness
- **Block Delay**: Data có thể delay 1-2 blocks
- **Indexing Time**: Complex queries có thể mất thời gian index
- **Cache Issues**: Một số endpoints có cache aggressive

#### 3. Pagination Limits
```javascript
// Maximum 10,000 records per call
const maxOffset = 10000

// Cần implement pagination cho large datasets
async function getAllTransactions(address) {
  let allTxs = []
  let page = 1
  
  while (true) {
    const txs = await getTransactions(address, page, maxOffset)
    if (txs.length === 0) break
    
    allTxs.push(...txs)
    page++
  }
  
  return allTxs
}
```

### Business Challenges:

#### 1. Cost Scaling
- **Free Tier**: Chỉ phù hợp cho development/testing
- **Production**: Cần paid plan từ $199/month
- **Enterprise**: Có thể lên đến $999/month

#### 2. Vendor Lock-in
- **API Dependency**: Heavy dependency vào Etherscan
- **Migration Cost**: Khó migrate sang provider khác
- **Service Reliability**: Single point of failure

#### 3. Compliance Issues
- **Data Privacy**: GDPR compliance concerns
- **Geographic Restrictions**: Một số regions bị restrict
- **Terms of Service**: Strict usage terms

### Workarounds và Solutions:

#### 1. Rate Limit Mitigation
```javascript
// Sử dụng multiple API keys
const apiKeys = ['key1', 'key2', 'key3']
let currentKeyIndex = 0

function getNextApiKey() {
  const key = apiKeys[currentKeyIndex]
  currentKeyIndex = (currentKeyIndex + 1) % apiKeys.length
  return key
}
```

#### 2. Caching Strategy
```javascript
const cache = new Map()
const CACHE_TTL = 60000 // 1 minute

async function cachedApiCall(url) {
  const cached = cache.get(url)
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.data
  }
  
  const data = await apiCall(url)
  cache.set(url, { data, timestamp: Date.now() })
  return data
}
```

#### 3. Fallback Providers
```javascript
const providers = [
  { name: 'Etherscan', baseUrl: 'https://api.etherscan.io/v2/api' },
  { name: 'Alchemy', baseUrl: 'https://eth-mainnet.alchemyapi.io/v2' },
  { name: 'Infura', baseUrl: 'https://mainnet.infura.io/v3' }
]

async function resilientApiCall(params) {
  for (const provider of providers) {
    try {
      return await callProvider(provider, params)
    } catch (error) {
      console.warn(`Provider ${provider.name} failed:`, error.message)
    }
  }
  throw new Error('All providers failed')
}
```

---

## 🎯 Best Practices

### 1. API Key Management
```javascript
// Environment-based configuration
const config = {
  development: {
    apiKey: process.env.ETHERSCAN_DEV_KEY,
    rateLimit: 5
  },
  production: {
    apiKey: process.env.ETHERSCAN_PROD_KEY,
    rateLimit: 25
  }
}
```

### 2. Error Handling Strategy
```javascript
class EtherscanError extends Error {
  constructor(message, code, response) {
    super(message)
    this.name = 'EtherscanError'
    this.code = code
    this.response = response
  }
}

async function handleApiResponse(response) {
  if (response.status === '0') {
    const errorCode = response.message.includes('rate limit') ? 'RATE_LIMIT' : 'API_ERROR'
    throw new EtherscanError(response.message, errorCode, response)
  }
  return response.result
}
```

### 3. Monitoring và Logging
```javascript
const logger = require('winston')

class ApiMonitor {
  constructor() {
    this.metrics = {
      totalCalls: 0,
      successfulCalls: 0,
      failedCalls: 0,
      rateLimitHits: 0
    }
  }
  
  logCall(success, error = null) {
    this.metrics.totalCalls++
    
    if (success) {
      this.metrics.successfulCalls++
    } else {
      this.metrics.failedCalls++
      if (error?.code === 'RATE_LIMIT') {
        this.metrics.rateLimitHits++
      }
    }
    
    logger.info('API Metrics', this.metrics)
  }
}
```

### 4. Testing Strategy
```javascript
// Mock cho testing
const mockEtherscanResponse = {
  status: '1',
  message: 'OK',
  result: '1000000000000000000' // 1 ETH in wei
}

// Integration test
describe('Etherscan API V2', () => {
  test('should get account balance', async () => {
    const balance = await getAccountBalance(1, testAddress)
    expect(balance).toBeDefined()
    expect(typeof balance).toBe('string')
  })
})
```

---

## 📞 Liên Hệ và Hỗ Trợ

### Official Resources:
- **Documentation**: https://docs.etherscan.io/etherscan-v2
- **API Plans**: https://etherscan.io/apis
- **Support**: https://etherscan.io/contactus

### Community:
- **Discord**: Etherscan Community Server
- **GitHub**: Example repositories và SDKs
- **Stack Overflow**: Tag `etherscan-api`

---

*Tài liệu này được cập nhật cho phiên bản Etherscan API V2 mới nhất tính đến tháng 9/2025. Vui lòng kiểm tra documentation chính thức để có thông tin mới nhất.*
