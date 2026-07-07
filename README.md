# Submarine Web

量化策略系统前端项目，基于 Vue 3 + FastAPI 构建的前后端分离架构。

## 📁 项目结构

```
submarine-web/
├── backend/                    # 后端服务 (FastAPI)
│   ├── main.py                 # API入口文件
│   └── README.md               # 后端说明文档
├── frontend/                   # 前端应用 (Vue 3)
│   ├── src/
│   │   ├── api/                # API请求封装
│   │   ├── router/             # Vue Router路由配置
│   │   ├── stores/             # Pinia状态管理
│   │   ├── views/              # 页面组件
│   │   ├── App.vue             # 主应用组件
│   │   ├── main.js             # 入口文件
│   │   └── style.css           # 全局样式
│   ├── vite.config.js          # Vite构建配置
│   ├── jsconfig.json           # 路径别名配置
│   └── README.md               # 前端说明文档
└── README.md                   # 项目说明文档
```

## 🛠️ 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| 前端框架 | Vue | 3.x |
| 构建工具 | Vite | 6.x |
| UI组件库 | Element Plus | 2.x |
| 图表库 | ECharts | 5.x |
| 状态管理 | Pinia | 2.x |
| 路由 | Vue Router | 4.x |
| HTTP请求 | Axios | 1.x |
| 后端框架 | FastAPI | 0.x |
| 数据库 | MySQL | 8.x |

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 18+
- MySQL 8.0+

### 启动步骤

```bash
# 1. 启动后端服务 (端口 3000)
cd backend
python main.py

# 2. 启动前端服务 (端口 5173)
cd frontend
npm install
npm run dev
```

### 访问地址

| 服务 | 地址 |
|------|------|
| 前端页面 | http://localhost:5173 |
| API文档 | http://localhost:3000/docs |

## 📋 功能模块

| 模块 | 路径 | 说明 |
|------|------|------|
| 首页仪表盘 | `/` | 统计概览、最近测试结果、策略列表 |
| 策略管理 | `/strategies` | 策略列表、分类筛选、详情查看 |
| 策略详情 | `/strategies/:code` | 策略参数、相关回溯结果 |
| 回溯结果 | `/backtest` | 测试结果列表、筛选搜索 |
| 回溯详情 | `/backtest/:id` | 资金曲线、绩效指标、交易记录 |
| 执行回溯 | `/run-backtest` | 参数配置、执行回溯测试 |
| 股票池 | `/stocks` | 股票列表、搜索筛选 |

## 📊 后端API

后端服务提供以下API接口：

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/strategies` | GET | 获取策略列表 |
| `/api/strategies/:code` | GET | 获取策略详情 |
| `/api/stocks` | GET | 获取股票列表 |
| `/api/stocks/:code` | GET | 获取股票详情 |
| `/api/backtest/results` | GET | 查询回溯结果 |
| `/api/backtest/equity/:id` | GET | 获取资金曲线 |
| `/api/backtest/trades/:id` | GET | 获取交易记录 |
| `/api/backtest/run` | POST | 执行回溯测试 |
| `/api/backtest/stats` | GET | 获取统计数据 |

## 🔄 数据流

```
前端页面 → API请求 → FastAPI后端 → MySQL数据库
              ↓
          股票数据/策略数据/回溯结果
```

## 📝 开发说明

- 前端使用 Vue 3 Composition API
- 后端使用 FastAPI，通过 subprocess 调用 Python 策略脚本
- 数据库连接配置在 `submarine/config/settings.py` 中
- 前端开发时 Vite 代理 `/api` 请求到后端 `http://localhost:3000`