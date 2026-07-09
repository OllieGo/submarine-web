import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/strategies',
    name: 'StrategyList',
    component: () => import('@/views/StrategyList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/strategies/:code',
    name: 'StrategyDetail',
    component: () => import('@/views/StrategyDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/backtest',
    name: 'BacktestList',
    component: () => import('@/views/BacktestList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/backtest/:id',
    name: 'BacktestDetail',
    component: () => import('@/views/BacktestDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/run-backtest',
    name: 'RunBacktest',
    component: () => import('@/views/RunBacktest.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/stocks',
    name: 'StockList',
    component: () => import('@/views/StockList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/stocks/:code',
    name: 'StockEdit',
    component: () => import('@/views/StockEdit.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth !== false && !authStore.isLoggedIn()) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && authStore.isLoggedIn()) {
    next('/')
  } else {
    next()
  }
})

export default router