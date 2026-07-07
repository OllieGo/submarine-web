# Backend - FastAPI 服务

量化策略系统后端 API 服务，基于 FastAPI 构建，提供数据查询和策略执行接口。

## 📁 目录结构

```
backend/
└── main.py                     # API入口文件
```

## 🛠️ 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| FastAPI | 0.x | 高性能Python Web框架 |
| Uvicorn | 0.x | ASGI服务器 |
| SQLAlchemy | 2.x | ORM数据库操作 |
| MySQL Connector | 8.x | MySQL驱动 |
| Pandas | 2.x | 数据处理 |

## 🚀 启动方式

### 开发环境

```bash
# 安装依赖
pip install fastapi uvicorn pandas sqlalchemy mysql-connector-python

# 启动服务
python main.py

# 或使用 uvicorn
uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```

### 服务地址

| 服务 | 地址 |
|------|------|
| API服务 | http://localhost:3000 |
| API文档 | http://localhost:3000/docs |
| 接口测试 | http://localhost:3000/redoc |

## 📊 API接口

### 策略管理

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/strategies` | GET | 获取策略列表 |
| `/api/strategies/:code` | GET | 获取策略详情 |

### 股票管理

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/stocks` | GET | 获取股票列表 |
| `/api/stocks/:code` | GET | 获取股票详情 |

### 回溯测试

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/backtest/results` | GET | 查询回溯结果 |
| `/api/backtest/results/:id` | GET | 获取单条结果 |
| `/api/backtest/equity/:id` | GET | 获取资金曲线 |
| `/api/backtest/trades/:id` | GET | 获取交易记录 |
| `/api/backtest/run` | POST | 执行回溯测试 |
| `/api/backtest/stats` | GET | 获取统计数据 |

## 🔧 配置说明

后端服务依赖 `submarine` 项目的数据库配置：

1. 确保 `submarine/config/settings.py` 中的数据库配置正确
2. 确保 MySQL 数据库中已创建相关表（参考 `submarine/sql/init.sql`）

### 数据库连接

后端通过 `submarine/data_handler/storage.py` 中的 `DataStorage` 类连接数据库，无需额外配置。

## 📝 执行流程

### 回溯测试执行

```
POST /api/backtest/run → subprocess调用 → python strategy/run_backtest.py → 保存结果到MySQL
```

### 数据查询流程

```
GET /api/xxx → DataStorage → MySQL数据库 → 返回JSON数据
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
pip install fastapi uvicorn pandas sqlalchemy mysql-connector-python pydantic
```