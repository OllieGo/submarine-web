# Backend - FastAPI 服务

量化策略系统后端 API 服务，基于 FastAPI 构建，提供数据查询和策略执行接口。

## 📁 目录结构

```
backend/
├── main.py                     # API入口文件（应用初始化、路由注册）
├── api/                        # API路由模块
│   ├── __init__.py
│   ├── auth.py                 # 认证模块（注册、登录、获取用户信息）
│   ├── strategies.py           # 策略模块（策略列表、策略详情）
│   ├── stocks.py               # 股票模块（股票列表、详情、更新）
│   └── backtest.py             # 回溯测试模块（运行、结果、资金曲线、交易、统计）
└── sql/                        # 数据库初始化脚本
    └── init.sql                # 数据库建表语句
```

## 🛠️ 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| FastAPI | 0.x+ | 高性能 Python Web 框架 |
| Uvicorn | 0.x+ | ASGI 服务器 |
| SQLAlchemy | 2.x | ORM 数据库操作 |
| MySQL Connector | 8.x | MySQL 驱动 |
| Pandas | 2.x | 数据处理 |
| PyJWT | 2.x | JWT 认证 |
| Pydantic | 2.x | 数据验证 |

## 🚀 启动方式

### 方式一：通过项目启动脚本（推荐）

```bash
# 项目根目录执行
cd D:\coding\submarine-web
python start.py
```

该脚本会同时启动前端（5173）和后端（3000）服务，按 `Ctrl+C` 停止所有服务。

### 方式二：独立启动后端

```bash
# 进入后端目录
cd D:\coding\submarine-web\backend

# 开发模式（热重载）
uvicorn main:app --host 0.0.0.0 --port 3000 --reload

# 或直接运行
python main.py
```

### 服务地址

| 服务 | 地址 |
|------|------|
| API 服务 | http://localhost:3000 |
| API 文档 | http://localhost:3000/docs |
| ReDoc 文档 | http://localhost:3000/redoc |

## 📊 API 接口

### 认证模块

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/auth/register` | POST | 用户注册 |
| `/api/auth/login` | POST | 用户登录 |
| `/api/auth/me` | GET | 获取当前用户信息（需认证） |

#### 注册请求示例

```json
{
    "username": "testuser",
    "password": "test123",
    "email": "test@example.com",
    "phone": "13800138000"
}
```

#### 登录请求示例

```json
{
    "username": "testuser",
    "password": "test123"
}
```

### 策略管理

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/strategies` | GET | 获取策略列表 |
| `/api/strategies/:code` | GET | 获取策略详情 |

### 股票管理

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/stocks` | GET | 获取股票列表（支持搜索、筛选） |
| `/api/stocks/:code` | GET | 获取股票详情 |
| `/api/stocks/:code` | PUT | 更新股票信息 |

#### 股票列表查询参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| limit | int | 100 | 返回数量 |
| keyword | string | - | 搜索关键词（股票代码或名称） |
| market | string | - | 市场筛选（如 SH、SZ） |

### 回溯测试

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/backtest/results` | GET | 查询回溯结果列表 |
| `/api/backtest/results/:id` | GET | 获取单条回溯结果 |
| `/api/backtest/results` | DELETE | 删除回溯结果（批量） |
| `/api/backtest/equity/:id` | GET | 获取资金曲线 |
| `/api/backtest/trades/:id` | GET | 获取交易记录 |
| `/api/backtest/run` | POST | 执行回溯测试 |
| `/api/backtest/stats` | GET | 获取统计数据 |

#### 执行回溯请求示例

```json
{
    "strategy_type": "dual_ma",
    "ts_code": "000001.SZ",
    "initial_capital": 100000,
    "commission_rate": 0.0003,
    "slippage_rate": 0.001,
    "short_window": 5,
    "long_window": 20,
    "limit": 500
}
```

## 🔧 配置说明

### 数据库连接

后端通过 `submarine/data_handler/storage.py` 中的 `DataStorage` 类连接数据库，配置文件位于：

- `submarine/config/settings.py` - 数据库连接配置

### 数据库初始化

确保 MySQL 数据库中已创建相关表：

```bash
# 创建数据库并执行建表语句
mysql -u username -p < sql/init.sql
```

### JWT 密钥

认证模块使用 JWT 令牌，密钥配置在 `api/auth.py` 中：

```python
SECRET_KEY = "submarine_quant_secret_key_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120
```

## 📝 执行流程

### 回溯测试执行

```
POST /api/backtest/run → subprocess 调用 → python strategy/run_backtest.py → 保存结果到 MySQL
```

### 数据查询流程

```
GET /api/xxx → DataStorage → MySQL 数据库 → 返回 JSON 数据
```

### 认证流程

```
登录 → 获取 JWT Token → 请求时携带 Authorization: Bearer <token> → 验证通过 → 访问受保护接口
```

## 🔌 跨域配置

后端已配置 CORS，允许前端跨域访问：

```python
allow_origins: ["*"]
allow_methods: ["*"]
allow_headers: ["*"]
```

## 📋 依赖安装

```bash
pip install -r requirements.txt
```

如无 `requirements.txt`，可手动安装：

```bash
pip install fastapi uvicorn pandas sqlalchemy mysql-connector-python pydantic python-jose[cryptography]
```

## 🐛 常见问题

### UnicodeEncodeError: 'gbk' codec can't encode character

**原因**：Windows 控制台默认使用 GBK 编码，无法显示 Unicode 字符

**解决**：启动脚本已配置 `encoding='utf-8'`，使用项目启动脚本即可正常运行。

### 数据库连接失败

1. 检查 MySQL 服务是否启动
2. 检查 `submarine/config/settings.py` 中的数据库配置
3. 确保已执行 `sql/init.sql` 创建表结构