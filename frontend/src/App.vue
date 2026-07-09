<template>
  <template v-if="!isAuthPage">
    <el-container class="app-layout">
      <el-aside class="sidebar" width="200px">
        <div class="logo">
          <h2>🔍 潜望量化</h2>
        </div>
        <el-menu
          mode="inline"
          :default-active="currentKey"
          class="nav-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="/">
            <span class="icon">🏠</span>
            <span>首页仪表盘</span>
          </el-menu-item>
          <el-menu-item index="/strategies">
            <span class="icon">⚙️</span>
            <span>策略管理</span>
          </el-menu-item>
          <el-menu-item index="/backtest">
            <span class="icon">📈</span>
            <span>回溯结果</span>
          </el-menu-item>
          <el-menu-item index="/run-backtest">
            <span class="icon">▶️</span>
            <span>执行回溯</span>
          </el-menu-item>
          <el-menu-item index="/stocks">
            <span class="icon">📋</span>
            <span>股票池</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container class="main-container">
        <el-header class="header">
          <div class="header-title">
            <h1>{{ pageTitle }}</h1>
          </div>
          <div class="header-right">
            <span class="username">{{ authStore.nickName || authStore.username }}</span>
            <el-button text @click="handleLogout">退出登录</el-button>
          </div>
        </el-header>
        <div class="tabs-container">
          <el-tabs
            v-model="activeTabKey"
            class="app-tabs"
            @tab-click="handleTabClick"
            @tab-remove="handleCloseTab"
          >
            <el-tab-pane
              v-for="tab in tabs"
              :key="tab.key"
              :name="tab.key"
              :label="tab.title"
              :closable="tabs.length > 1"
            >
            </el-tab-pane>
          </el-tabs>
        </div>
        <el-main class="content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </template>
  <router-view v-else />
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const activeTabKey = ref('/')

const pageTitles = {
  '/': '首页仪表盘',
  '/strategies': '策略管理',
  '/backtest': '回溯结果',
  '/run-backtest': '执行回溯测试',
  '/stocks': '股票池'
}

const tabs = ref([
  { key: '/', title: '首页仪表盘' }
])

const pageTitle = computed(() => {
  const path = route.path
  if (path.startsWith('/strategies/')) return '策略详情'
  if (path.startsWith('/backtest/')) return '回溯详情'
  return pageTitles[path] || '潜望量化'
})

const isAuthPage = computed(() => {
  const authPaths = ['/login', '/register']
  return authPaths.includes(route.path)
})

const currentKey = computed(() => {
  const path = route.path
  if (path.startsWith('/strategies/')) return '/strategies'
  if (path.startsWith('/backtest/') && path !== '/run-backtest') return '/backtest'
  return path
})

const handleMenuSelect = (key) => {
  const exists = tabs.value.find(tab => tab.key === key)
  if (!exists) {
    tabs.value.push({ key, title: pageTitles[key] || key })
  }
  activeTabKey.value = key
  router.push(key)
}

const handleTabClick = (tab) => {
  router.push(tab.paneName)
}

const handleCloseTab = (key) => {
  if (tabs.value.length === 1) return
  const index = tabs.value.findIndex(tab => tab.key === key)
  if (index > -1) {
    tabs.value.splice(index, 1)
    if (activeTabKey.value === key) {
      const newIndex = index < tabs.value.length ? index : tabs.value.length - 1
      activeTabKey.value = tabs.value[newIndex].key
      router.push(tabs.value[newIndex].key)
    }
  }
}

watch(
  () => route.path,
  (newPath) => {
    const normalizedPath = newPath.startsWith('/strategies/') ? '/strategies' :
                          (newPath.startsWith('/backtest/') && newPath !== '/run-backtest') ? '/backtest' : newPath
    if (activeTabKey.value !== normalizedPath) {
      activeTabKey.value = normalizedPath
    }
    const exists = tabs.value.find(tab => tab.key === normalizedPath)
    if (!exists && pageTitles[normalizedPath]) {
      tabs.value.push({ key: normalizedPath, title: pageTitles[normalizedPath] })
    }
  }
)

const handleLogout = () => {
  authStore.logout()
  ElMessage.success('已退出登录')
  router.push('/login')
}

onMounted(() => {
  const path = route.path
  const normalizedPath = path.startsWith('/strategies/') ? '/strategies' :
                        (path.startsWith('/backtest/') && path !== '/run-backtest') ? '/backtest' : path
  activeTabKey.value = normalizedPath
})
</script>

<style scoped>
.app-layout {
  height: 100vh;
  background-color: #f5f7fa;
}

.sidebar {
  background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
  color: #fff;
  overflow: hidden;
}

.logo {
  padding: 16px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo h2 {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: #fff;
}

.nav-menu {
  border-right: none;
  background: transparent;
  height: calc(100vh - 52px);
}

.nav-menu :deep(.el-menu-item) {
  color: #b8c5d6;
  margin: 4px 8px;
  border-radius: 8px;
  transition: all 0.3s;
}

.nav-menu :deep(.el-menu-item:hover) {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.nav-menu :deep(.el-menu-item.is-active) {
  background: #007bff !important;
  color: #fff !important;
}

.nav-menu .icon {
  font-size: 16px;
  margin-right: 8px;
}

.main-container {
  overflow: hidden;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  background: #fff;
  border-bottom: 1px solid #e8ecf0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  height: 64px;
  line-height: 64px;
}

.header-title h1 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.username {
  font-size: 14px;
  color: #666;
}

.tabs-container {
  background: #fff;
  border-bottom: 1px solid #e8ecf0;
}

.app-tabs :deep(.el-tabs__nav-wrap) {
  padding-left: 16px;
}

.app-tabs :deep(.el-tabs__item) {
  padding: 12px 20px;
  margin-right: 8px;
}

.content {
  padding: 24px;
  overflow-y: auto;
  height: calc(100vh - 64px - 48px);
}
</style>