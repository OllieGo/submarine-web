<template>
  <div class="dashboard">
    <div class="welcome-section">
      <div class="welcome-content">
        <h1>欢迎回来</h1>
        <p>今天是 {{ currentDate }}，祝您交易顺利</p>
      </div>
    </div>
    <div class="stats-grid">
      <el-card class="stat-card">
        <div class="stat-header">
          <div class="stat-icon blue">📊</div>
          <el-tag size="small" type="info">测试分析</el-tag>
        </div>
        <div class="stat-value-wrap">
          <div class="stat-value">{{ stats.total_tests || 0 }}</div>
          <div class="stat-unit">次</div>
        </div>
        <div class="stat-label">总测试次数</div>
        <div class="stat-trend" :class="stats.test_trend > 0 ? 'positive' : 'negative'">
          <span>{{ stats.test_trend > 0 ? '↑' : '↓' }}</span>
          <span>{{ Math.abs(stats.test_trend) || 0 }}%</span>
          <span class="trend-label">较昨日</span>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-header">
          <div class="stat-icon green">📈</div>
          <el-tag size="small" type="success">市场覆盖</el-tag>
        </div>
        <div class="stat-value-wrap">
          <div class="stat-value">{{ stats.total_stocks || 0 }}</div>
          <div class="stat-unit">只</div>
        </div>
        <div class="stat-label">测试股票数</div>
        <div class="stat-trend" :class="stats.stock_trend > 0 ? 'positive' : 'negative'">
          <span>{{ stats.stock_trend > 0 ? '↑' : '↓' }}</span>
          <span>{{ Math.abs(stats.stock_trend) || 0 }}%</span>
          <span class="trend-label">较昨日</span>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-header">
          <div class="stat-icon orange">⚙️</div>
          <el-tag size="small" type="warning">策略管理</el-tag>
        </div>
        <div class="stat-value-wrap">
          <div class="stat-value">{{ stats.total_strategies || 0 }}</div>
          <div class="stat-unit">个</div>
        </div>
        <div class="stat-label">策略类型</div>
        <div class="stat-trend positive">
          <span>↑</span>
          <span>{{ stats.strategy_trend || 0 }}</span>
          <span class="trend-label">本月新增</span>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-header">
          <div class="stat-icon purple">💰</div>
          <el-tag size="small" :type="stats.avg_return >= 0 ? 'success' : 'danger'">收益分析</el-tag>
        </div>
        <div class="stat-value-wrap">
          <div class="stat-value" :class="{ positive: stats.avg_return > 0, negative: stats.avg_return < 0 }">{{ formatPercent(stats.avg_return) }}</div>
        </div>
        <div class="stat-label">平均收益率</div>
        <div class="stat-trend" :class="stats.return_trend > 0 ? 'positive' : 'negative'">
          <span>{{ stats.return_trend > 0 ? '↑' : '↓' }}</span>
          <span>{{ formatPercent(stats.return_trend) }}</span>
          <span class="trend-label">较上月</span>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-header">
          <div class="stat-icon cyan">📉</div>
          <el-tag size="small" type="info">风险控制</el-tag>
        </div>
        <div class="stat-value-wrap">
          <div class="stat-value negative">{{ formatPercent(stats.max_drawdown || 0) }}</div>
        </div>
        <div class="stat-label">最大回撤</div>
        <div class="stat-trend" :class="stats.drawdown_trend > 0 ? 'positive' : 'negative'">
          <span>{{ stats.drawdown_trend > 0 ? '↑' : '↓' }}</span>
          <span>{{ formatPercent(stats.drawdown_trend) }}</span>
          <span class="trend-label">变化</span>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-header">
          <div class="stat-icon pink">🎯</div>
          <el-tag size="small" type="success">策略效果</el-tag>
        </div>
        <div class="stat-value-wrap">
          <div class="stat-value">{{ (stats.win_rate || 0).toFixed(1) }}%</div>
        </div>
        <div class="stat-label">整体胜率</div>
        <div class="stat-trend" :class="stats.win_trend > 0 ? 'positive' : 'negative'">
          <span>{{ stats.win_trend > 0 ? '↑' : '↓' }}</span>
          <span>{{ stats.win_trend || 0 }}%</span>
          <span class="trend-label">较上月</span>
        </div>
      </el-card>
    </div>
    <div class="content-grid">
      <el-card>
        <template #header>
          <div class="card-header-inner">
            <h3>最近测试结果</h3>
            <router-link to="/backtest" class="view-all">查看全部 →</router-link>
          </div>
        </template>
        <el-table :data="recentResults" border stripe>
          <el-table-column prop="ts_code" label="股票代码" width="120" />
          <el-table-column prop="stock_name" label="股票名称" width="120" />
          <el-table-column label="策略类型" width="130">
            <template #default="{ row }">
              <el-tag :type="getStrategyTagType(row.strategy_type)">{{ getStrategyName(row.strategy_type) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="总收益率" width="130">
            <template #default="{ row }">
              <span :class="{ positive: row.total_return > 0, negative: row.total_return < 0 }">{{ formatPercent(row.total_return) }}</span>
            </template>
          </el-table-column>
          <el-table-column label="最大回撤" width="130">
            <template #default="{ row }">
              <span class="negative">{{ formatPercent(row.max_drawdown) }}</span>
            </template>
          </el-table-column>
          <el-table-column label="交易次数" width="100">
            <template #default="{ row }">
              <el-tag size="small">{{ row.total_trades || 0 }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="测试时间" width="180">
            <template #default="{ row }">
              {{ formatDate(row.test_date) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100">
            <template #default="{ row }">
              <router-link :to="`/backtest/${row.id}`" class="btn-view">查看</router-link>
            </template>
          </el-table-column>
        </el-table>
        <div v-if="recentResults.length === 0" class="empty-tip">暂无测试结果</div>
      </el-card>
      <div class="right-panel">
        <el-card>
          <template #header>
            <div class="card-header-inner">
              <h3>策略列表</h3>
              <router-link to="/strategies" class="view-all">查看全部 →</router-link>
            </div>
          </template>
          <div class="strategy-list">
            <div v-for="strategy in strategies" :key="strategy.code" class="strategy-item">
              <div class="strategy-icon-wrap" :class="getStrategyBgClass(strategy.code)">
                <span class="strategy-icon">{{ getStrategyIcon(strategy.code) }}</span>
              </div>
              <div class="strategy-info">
                <div class="strategy-name">{{ strategy.name }}</div>
                <div class="strategy-desc">{{ strategy.description }}</div>
              </div>
              <router-link :to="`/strategies/${strategy.code}`" class="btn-detail">详情</router-link>
            </div>
          </div>
          <div v-if="strategies.length === 0" class="empty-tip">暂无策略</div>
        </el-card>
        <el-card class="quick-actions">
          <template #header>快捷操作</template>
          <div class="action-grid">
            <router-link to="/run-backtest" class="action-item">
              <div class="action-icon">▶️</div>
              <div class="action-text">执行回溯</div>
            </router-link>
            <router-link to="/stocks" class="action-item">
              <div class="action-icon">📋</div>
              <div class="action-text">股票池</div>
            </router-link>
            <router-link to="/strategies" class="action-item">
              <div class="action-icon">⚙️</div>
              <div class="action-text">策略管理</div>
            </router-link>
            <router-link to="/backtest" class="action-item">
              <div class="action-icon">📈</div>
              <div class="action-text">测试结果</div>
            </router-link>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { backtestAPI, strategyAPI } from '@/api'

const stats = ref({})
const recentResults = ref([])
const strategies = ref([])

const currentDate = computed(() => {
  const now = new Date()
  return `${now.getFullYear()}年${now.getMonth() + 1}月${now.getDate()}日`
})

const strategyNameMap = { dual_ma: '双均线交叉', triple_ma: '三重均线', four_line: '四线多头' }
const strategyIconMap = { dual_ma: '📈', triple_ma: '📊', four_line: '📉' }
const strategyTagType = { dual_ma: 'primary', triple_ma: 'success', four_line: 'warning' }
const strategyBgClass = { dual_ma: 'bg-blue', triple_ma: 'bg-green', four_line: 'bg-orange' }

const getStrategyName = (code) => strategyNameMap[code] || code
const getStrategyIcon = (code) => strategyIconMap[code] || '⚙️'
const getStrategyTagType = (code) => strategyTagType[code] || 'default'
const getStrategyBgClass = (code) => strategyBgClass[code] || 'bg-gray'
const formatPercent = (value) => value ? `${value >= 0 ? '+' : ''}${value.toFixed(2)}%` : '--'
const formatDate = (dateStr) => dateStr ? new Date(dateStr).toLocaleString('zh-CN') : '--'

const loadData = async () => {
  try {
    stats.value = await backtestAPI.getStats()
    recentResults.value = await backtestAPI.getResults(null, null, 10)
    strategies.value = await strategyAPI.getAll()
  } catch (error) { console.error('加载数据失败:', error) }
}

onMounted(loadData)
</script>

<style scoped>
.dashboard { padding: 10px 0; }
.welcome-section { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; padding: 32px; margin-bottom: 24px; }
.welcome-content h1 { font-size: 28px; font-weight: 600; color: #fff; margin: 0 0 8px 0; }
.welcome-content p { font-size: 14px; color: rgba(255, 255, 255, 0.8); margin: 0; }
.stats-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 16px; margin-bottom: 24px; }
.stat-card { padding: 20px; border-radius: 12px; }
.stat-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.stat-icon { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; }
.stat-icon.blue { background: #e6f7ff; }
.stat-icon.green { background: #f6ffed; }
.stat-icon.orange { background: #fff7e6; }
.stat-icon.purple { background: #f9f0ff; }
.stat-icon.cyan { background: #e6fffb; }
.stat-icon.pink { background: #fff0f6; }
.stat-value-wrap { display: flex; align-items: baseline; gap: 4px; }
.stat-value { font-size: 28px; font-weight: 700; color: #333; }
.stat-value.positive { color: #f56c6c; }
.stat-value.negative { color: #67c23a; }
.stat-unit { font-size: 14px; color: #999; }
.stat-label { font-size: 13px; color: #999; margin-top: 8px; }
.stat-trend { display: flex; align-items: center; gap: 4px; margin-top: 8px; font-size: 12px; }
.stat-trend.positive { color: #f56c6c; }
.stat-trend.negative { color: #67c23a; }
.trend-label { color: #999; margin-left: 4px; }
.content-grid { display: grid; grid-template-columns: 1fr 380px; gap: 20px; }
.right-panel { display: flex; flex-direction: column; gap: 20px; }
.card-header-inner { display: flex; justify-content: space-between; align-items: center; width: 100%; }
.card-header-inner h3 { font-size: 16px; font-weight: 600; margin: 0; }
.view-all { font-size: 14px; color: #409eff; text-decoration: none; }
.empty-tip { text-align: center; color: #999; padding: 40px; }
.btn-view { color: #409eff; font-size: 14px; text-decoration: none; }
.strategy-list { display: flex; flex-direction: column; gap: 12px; }
.strategy-item { display: flex; align-items: center; padding: 16px; border-radius: 10px; background: #fafafa; transition: all 0.3s; }
.strategy-item:hover { background: #f0f5ff; }
.strategy-icon-wrap { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 12px; }
.strategy-icon-wrap.bg-blue { background: #e6f7ff; }
.strategy-icon-wrap.bg-green { background: #f6ffed; }
.strategy-icon-wrap.bg-orange { background: #fff7e6; }
.strategy-icon-wrap.bg-gray { background: #f5f5f5; }
.strategy-icon { font-size: 20px; }
.strategy-info { flex: 1; }
.strategy-name { font-size: 14px; font-weight: 600; color: #333; }
.strategy-desc { font-size: 12px; color: #999; margin-top: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.btn-detail { padding: 4px 12px; background: #409eff; color: #fff; font-size: 12px; border-radius: 4px; text-decoration: none; }
.action-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
.action-item { display: flex; flex-direction: column; align-items: center; padding: 20px; border-radius: 10px; background: #f5f7fa; text-decoration: none; transition: all 0.3s; }
.action-item:hover { background: #eef5ff; }
.action-icon { font-size: 28px; margin-bottom: 8px; }
.action-text { font-size: 13px; color: #666; }
.positive { color: #f56c6c; }
.negative { color: #67c23a; }
</style>