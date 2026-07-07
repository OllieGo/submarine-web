<template>
  <div class="strategy-detail-page">
    <div class="page-header">
      <el-button @click="goBack">
        <template #icon>
          <el-icon><ArrowLeft /></el-icon>
        </template>
        返回
      </el-button>
      <div class="header-title">
        <h2>{{ strategy.name }}</h2>
        <p>{{ strategy.code }}</p>
      </div>
    </div>
    <div class="content-grid">
      <el-card>
        <template #header>策略信息</template>
        <div class="info-grid">
          <div class="info-item">
            <label>策略编码</label>
            <span>{{ strategy.code }}</span>
          </div>
          <div class="info-item">
            <label>策略名称</label>
            <span>{{ strategy.name }}</span>
          </div>
          <div class="info-item">
            <label>策略分类</label>
            <el-tag>{{ strategy.category }}</el-tag>
          </div>
          <div class="info-item">
            <label>状态</label>
            <el-tag :type="strategy.is_active ? 'success' : 'danger'">{{ strategy.is_active ? '启用' : '禁用' }}</el-tag>
          </div>
        </div>
        <div class="description-section">
          <label>策略描述</label>
          <p>{{ strategy.description }}</p>
        </div>
      </el-card>
      <el-card>
        <template #header>默认参数配置</template>
        <el-form :model="params" label-width="100px">
          <el-form-item v-for="(value, key) in params" :key="key" :label="getParamLabel(key)">
            <el-input :value="value" disabled />
          </el-form-item>
        </el-form>
      </el-card>
    </div>
    <el-card>
      <template #header>相关回溯结果</template>
      <el-table :data="backtestResults" border>
        <el-table-column prop="ts_code" label="股票代码" width="120" />
        <el-table-column prop="stock_name" label="股票名称" width="120" />
        <el-table-column label="总收益率" width="120">
          <template #default="{ row }">
            <span :class="{ positive: row.total_return > 0, negative: row.total_return < 0 }">{{ formatPercent(row.total_return) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="最大回撤" width="120">
          <template #default="{ row }">
            <span class="negative">{{ formatPercent(row.max_drawdown) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="sharpe_ratio" label="夏普比率" width="100" />
        <el-table-column prop="total_trades" label="交易次数" width="100" />
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <router-link :to="`/backtest/${row.id}`" class="btn-view">查看</router-link>
          </template>
        </el-table-column>
      </el-table>
      <div v-if="backtestResults.length === 0" class="empty-tip">暂无相关回溯结果</div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { strategyAPI, backtestAPI } from '@/api'
import { ArrowLeft } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const strategy = ref({})
const params = ref({})
const backtestResults = ref([])

const paramLabels = { short_window: '短期窗口', mid_window: '中期窗口', long_window: '长期窗口', windows: '均线周期', volume_filter: '成交量过滤', volume_ratio: '成交量比率' }
const getParamLabel = (key) => paramLabels[key] || key
const formatPercent = (value) => value ? `${value >= 0 ? '+' : ''}${value.toFixed(2)}%` : '--'
const goBack = () => router.push('/strategies')

const loadData = async () => {
  const code = route.params.code
  try {
    strategy.value = await strategyAPI.getByCode(code)
    if (strategy.value.params) {
      try { params.value = typeof strategy.value.params === 'string' ? JSON.parse(strategy.value.params) : strategy.value.params } catch { params.value = {} }
    }
    backtestResults.value = await backtestAPI.getResults(null, code, 20)
  } catch (error) { console.error('加载数据失败:', error) }
}

onMounted(loadData)
</script>

<style scoped>
.strategy-detail-page { padding: 10px 0; }
.page-header { display: flex; align-items: center; gap: 16px; margin-bottom: 24px; }
.header-title h2 { font-size: 24px; font-weight: 600; margin: 0 0 4px 0; color: #333; }
.header-title p { font-size: 14px; color: #999; margin: 0; }
.content-grid { display: grid; grid-template-columns: 1fr 400px; gap: 20px; margin-bottom: 20px; }
.info-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-bottom: 20px; }
.info-item { display: flex; flex-direction: column; }
.info-item label { font-size: 13px; color: #999; margin-bottom: 4px; }
.info-item span { font-size: 14px; color: #333; }
.description-section { margin-top: 20px; }
.description-section label { font-size: 13px; color: #999; display: block; margin-bottom: 8px; }
.description-section p { font-size: 14px; color: #666; line-height: 1.8; margin: 0; }
.empty-tip { text-align: center; color: #999; padding: 40px; }
.btn-view { color: #409eff; font-size: 14px; text-decoration: none; }
.positive { color: #f56c6c; }
.negative { color: #67c23a; }
</style>