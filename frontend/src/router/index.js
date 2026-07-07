import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue')
  },
  {
    path: '/strategies',
    name: 'StrategyList',
    component: () => import('@/views/StrategyList.vue')
  },
  {
    path: '/strategies/:code',
    name: 'StrategyDetail',
    component: () => import('@/views/StrategyDetail.vue')
  },
  {
    path: '/backtest',
    name: 'BacktestList',
    component: () => import('@/views/BacktestList.vue')
  },
  {
    path: '/backtest/:id',
    name: 'BacktestDetail',
    component: () => import('@/views/BacktestDetail.vue')
  },
  {
    path: '/run-backtest',
    name: 'RunBacktest',
    component: () => import('@/views/RunBacktest.vue')
  },
  {
    path: '/stocks',
    name: 'StockList',
    component: () => import('@/views/StockList.vue')
  },
  {
    path: '/stocks/:code',
    name: 'StockEdit',
    component: () => import('@/views/StockEdit.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router