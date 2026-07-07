# Frontend - Vue 3 应用

量化策略系统前端应用，基于 Vue 3 + Ant Design Vue 构建的管理后台。

## 📁 目录结构

```
frontend/
├── src/
│   ├── api/                    # API请求封装
│   │   └── index.js             # 接口定义
│   ├── router/                 # Vue Router配置
│   │   └── index.js            # 路由定义
│   ├── stores/                 # Pinia状态管理
│   │   └── index.js            # 全局状态
│   ├── views/                  # 页面组件
│   │   ├── Dashboard.vue       # 首页仪表盘
│   │   ├── StrategyList.vue    # 策略列表
│   │   ├── StrategyDetail.vue  # 策略详情
│   │   ├── BacktestList.vue    # 回溯结果列表
│   │   ├── BacktestDetail.vue  # 回溯详情
│   │   ├── RunBacktest.vue     # 执行回溯测试
│   │   └── StockList.vue       # 股票池
│   ├── App.vue                 # 主应用组件
│   ├── main.js                 # 入口文件
│   └── style.css               # 全局样式
├── public/                     # 静态资源
├── index.html                  # HTML模板
├── vite.config.js              # Vite配置
├── jsconfig.json               # 路径别名配置
└── package.json                # 依赖配置
```

## 🛠️ 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Vue | 3.x | 前端框架 |
| Vite | 6.x | 构建工具 |
| Ant Design Vue | 3.x | UI组件库 |
| ECharts | 5.x | 图表库 |
| Pinia | 2.x | 状态管理 |
| Vue Router | 4.x | 路由管理 |
| Axios | 1.x | HTTP请求 |

## 🚀 启动方式

### 开发环境

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview
```

### 服务地址

| 服务 | 地址 |
|------|------|
| 开发环境 | http://localhost:5173 |
| 生产构建 | dist/ 目录 |

## 📊 页面功能

### 首页仪表盘 (`/`)
- 统计概览卡片（总测试次数、测试股票数、策略类型、平均收益率）
- 最近测试结果表格
- 策略列表快速入口

### 策略管理 (`/strategies`)
- 策略列表展示
- 分类筛选和关键词搜索
- 策略详情查看
- 快速执行回溯测试

### 策略详情 (`/strategies/:code`)
- 策略基本信息
- 默认参数配置展示
- 相关回溯结果列表

### 回溯结果 (`/backtest`)
- 测试结果列表
- 按策略类型和股票筛选
- 查看详情入口

### 回溯详情 (`/backtest/:id`)
- 资金曲线图（ECharts）
- 绩效指标面板
- 交易记录表格

### 执行回溯 (`/run-backtest`)
- 策略类型选择
- 股票代码选择
- 参数配置（初始资金、佣金率、滑点率等）
- 策略参数配置（均线窗口等）
- 执行测试并展示结果

### 股票池 (`/stocks`)
- 股票列表展示
- 关键词搜索和市场筛选
- 搜索和重置按钮
- 快速执行回溯测试

## 🔧 配置说明

### Vite配置 (`vite.config.js`)

```javascript
server: {
  port: 5173,
  proxy: {
    '/api': {
      target: 'http://localhost:3000',
      changeOrigin: true
    }
  }
}
```

前端开发时，`/api` 请求会自动代理到后端服务 `http://localhost:3000`。

### 路径别名 (`jsconfig.json`)

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
```

使用 `@` 作为 `src/` 目录的别名。

## 📝 API封装

前端API封装在 `src/api/index.js`：

```javascript
export const strategyAPI = {
  getAll: (category) => api.get('/strategies', { params: { category } }),
  getByCode: (code) => api.get(`/strategies/${code}`)
}

export const stockAPI = { ... }

export const backtestAPI = { ... }
```

## 🎨 组件规范

- 使用 Vue 3 Composition API
- 页面组件放在 `src/views/`
- 公共组件放在 `src/components/`
- 样式使用 scoped style
- 路由使用懒加载

## 📋 依赖列表

```bash
# 核心依赖
vue@3.x
vue-router@4.x
pinia@2.x
ant-design-vue@3.x
echarts@5.x
axios@1.x

# 开发依赖
@vitejs/plugin-vue@5.x
vite@6.x
```

## 🔄 开发流程

1. 启动后端服务（端口 3000）
2. 启动前端开发服务器（端口 5173）
3. 访问 http://localhost:5173
4. 修改代码后自动热更新

## 🎯 Ant Design Vue 组件使用规范

### 常用组件

| 组件 | 说明 | 替换 Element Plus |
|------|------|-------------------|
| `a-card` | 卡片容器 | `el-card` |
| `a-table` | 数据表格 | `el-table` |
| `a-form` | 表单 | `el-form` |
| `a-form-item` | 表单项 | `el-form-item` |
| `a-input` | 输入框 | `el-input` |
| `a-select` | 下拉选择 | `el-select` |
| `a-select-option` | 选项 | `el-option` |
| `a-button` | 按钮 | `el-button` |
| `a-tag` | 标签 | `el-tag` |
| `a-input-number` | 数字输入 | `el-input-number` |
| `a-switch` | 开关 | `el-switch` |
| `a-tooltip` | 提示 | `el-tooltip` |
| `a-layout` | 布局 | 自定义布局 |
| `a-layout-sider` | 侧边栏 | 自定义侧边栏 |
| `a-layout-header` | 头部 | 自定义头部 |
| `a-layout-content` | 内容区 | 自定义内容区 |
| `a-menu` | 菜单 | 自定义菜单 |
| `a-menu-item` | 菜单项 | 自定义菜单项 |

### 组件使用示例

**表格组件**
```vue
<a-table :columns="columns" :data-source="data" :pagination="false">
  <template #bodyCell="{ column, record }">
    <template v-if="column.key === 'action'">
      <a-button size="small">操作</a-button>
    </template>
  </template>
</a-table>
```

**表单组件**
```vue
<a-form :model="form" :label-col="{ span: 6 }" :wrapper-col="{ span: 18 }">
  <a-form-item label="名称">
    <a-input v-model:value="form.name" />
  </a-form-item>
</a-form>
```

**按钮组件**
```vue
<a-button type="primary">主要按钮</a-button>
<a-button>普通按钮</a-button>
```

**标签组件**
```vue
<a-tag>普通标签</a-tag>
<a-tag color="success">成功标签</a-tag>
<a-tag color="error">错误标签</a-tag>
```

### 布局组件

使用 Ant Design Vue 的布局组件实现响应式布局：

```vue
<a-layout class="app-layout">
  <a-layout-sider class="sidebar">侧边栏</a-layout-sider>
  <a-layout>
    <a-layout-header>头部</a-layout-header>
    <a-layout-content>内容</a-layout-content>
  </a-layout>
</a-layout>
```

### 图标使用

从 `@ant-design/icons-vue` 导入图标：

```vue
<script setup>
import { LeftOutlined, PlusOutlined } from '@ant-design/icons-vue'
</script>

<template>
  <a-button>
    <template #icon>
      <LeftOutlined />
    </template>
    返回
  </a-button>
</template>
```

## 📐 页面布局优化

### 滚动优化

主内容区域使用 `overflow-y: auto` 实现独立滚动，避免页面整体滚动：

```css
.content {
  padding: 24px;
  overflow-y: auto;
  height: calc(100vh - 64px);
}
```

### 响应式设计

- 使用 Flexbox 布局实现弹性布局
- 使用 Grid 布局实现多列布局
- 侧边栏支持折叠功能

### 表格固定列宽

表格列使用固定宽度，确保数据展示整齐：

```javascript
const columns = [
  { title: '股票代码', dataIndex: 'ts_code', key: 'ts_code', width: 120 },
  { title: '股票名称', dataIndex: 'name', key: 'name', width: 120 }
]
```