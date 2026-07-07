<template>
  <div class="strategy-list-page">
    <div class="filter-bar">
      <el-select v-model="filterCategory" placeholder="选择分类" clearable style="width:150px">
        <el-option label="均线策略" value="均线策略" />
      </el-select>
      <el-input v-model="searchKeyword" placeholder="搜索策略名称或编码" style="width:250px" />
    </div>
    <el-card>
      <template #header>
        <div class="card-header-inner">
          <h3>策略列表</h3>
        </div>
      </template>
      <el-table :data="filteredStrategies" border>
        <el-table-column prop="code" label="策略编码" width="120" />
        <el-table-column prop="name" label="策略名称" width="150" />
        <el-table-column label="分类" width="100">
          <template #default="{ row }">
            <el-tag>{{ row.category }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="策略描述" />
        <el-table-column label="默认参数" width="200">
          <template #default="{ row }">
            <el-tooltip :content="row.params">
              <span class="params-text">{{ formatParams(row.params) }}</span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">{{ row.is_active ? '启用' : '禁用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <router-link :to="`/strategies/${row.code}`" class="btn-edit">详情</router-link>
            <el-button type="primary" size="small" @click="runStrategy(row)">回溯</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div v-if="strategies.length === 0" class="empty-tip">暂无策略数据</div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { strategyAPI } from '@/api'

const router = useRouter()
const strategies = ref([])
const filterCategory = ref('')
const searchKeyword = ref('')

const filteredStrategies = computed(() => strategies.value.filter(item => {
  const matchCategory = !filterCategory.value || item.category === filterCategory.value
  const matchKeyword = !searchKeyword.value || item.name.includes(searchKeyword.value) || item.code.includes(searchKeyword.value)
  return matchCategory && matchKeyword
}))

const formatParams = (params) => {
  if (!params) return '--'
  try {
    const obj = typeof params === 'string' ? JSON.parse(params) : params
    return Object.keys(obj).slice(0, 3).join(', ') + (Object.keys(obj).length > 3 ? '...' : '')
  } catch {
    return params.substring(0, 20) + '...'
  }
}

const runStrategy = (strategy) => router.push({ path: '/run-backtest', query: { strategy: strategy.code } })

const loadStrategies = async () => {
  try { strategies.value = await strategyAPI.getAll() } catch (error) { console.error('加载策略失败:', error) }
}

onMounted(loadStrategies)
</script>

<style scoped>
.strategy-list-page { padding: 10px 0; }
.filter-bar { display: flex; gap: 12px; margin-bottom: 16px; }
.card-header-inner { display: flex; justify-content: space-between; align-items: center; width: 100%; }
.card-header-inner h3 { font-size: 16px; font-weight: 600; margin: 0; }
.empty-tip { text-align: center; color: #999; padding: 40px; }
.btn-edit { color: #409eff; font-size: 14px; margin-right: 8px; text-decoration: none; }
.params-text { color: #666; font-size: 13px; }
</style>