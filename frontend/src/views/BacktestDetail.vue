<template>
  <div class="backtest-detail-page">
    <div class="page-header">
      <el-button @click="goBack">
        <template #icon>
          <el-icon><ArrowLeft /></el-icon>
        </template>
        返回
      </el-button>
      <div class="header-title">
        <h2>{{ backtest.stock_name }} - {{ getStrategyName(backtest.strategy_type) }}</h2>
        <p>{{ backtest.ts_code }} | {{ formatDate(backtest.test_date) }}</p>
      </div>
    </div>
    <div class="stats-grid">
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-value" :class="{ positive: backtest.total_return > 0, negative: backtest.total_return < 0 }">{{ formatPercent(backtest.total_return) }}</div>
          <div class="stat-label">总收益率</div>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-value" :class="{ positive: backtest.annualized_return > 0, negative: backtest.annualized_return < 0 }">{{ formatPercent(backtest.annualized_return) }}</div>
          <div class="stat-label">年化收益率</div>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-value negative">{{ formatDrawdown(backtest.max_drawdown) }}</div>
          <div class="stat-label">最大回撤</div>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-value">{{ backtest.sharpe_ratio ? backtest.sharpe_ratio.toFixed(2) : '--' }}</div>
          <div class="stat-label">夏普比率</div>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-value">{{ formatPercent(backtest.win_rate) }}</div>
          <div class="stat-label">胜率</div>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-value">{{ backtest.total_trades || 0 }}</div>
          <div class="stat-label">交易次数</div>
        </div>
      </el-card>
    </div>
    <div class="content-grid">
      <el-card>
        <template #header>收益曲线</template>
        <div ref="chartRef" class="chart-container"></div>
      </el-card>
      <el-card>
        <template #header>测试参数</template>
        <div class="params-list">
          <div class="param-item">
            <label>策略类型</label>
            <el-tag>{{ getStrategyName(backtest.strategy_type) }}</el-tag>
          </div>
          <div class="param-item">
            <label>股票代码</label>
            <span>{{ backtest.ts_code }}</span>
          </div>
          <div class="param-item">
            <label>股票名称</label>
            <span>{{ backtest.stock_name }}</span>
          </div>
          <div class="param-item">
            <label>开始日期</label>
            <span>{{ backtest.start_date }}</span>
          </div>
          <div class="param-item">
            <label>结束日期</label>
            <span>{{ backtest.end_date }}</span>
          </div>
          <div class="param-item">
            <label>初始资金</label>
            <span>{{ backtest.initial_capital ? `¥${backtest.initial_capital.toLocaleString()}` : '--' }}</span>
          </div>
        </div>
      </el-card>
    </div>
    <el-card>
      <template #header>交易记录</template>
      <el-table :data="trades" border>
        <el-table-column prop="trade_date" label="交易日期" width="150" />
        <el-table-column label="类型" width="80">
          <template #default="{ row }">
            <el-tag :type="row.trade_type === 'buy' ? 'success' : 'danger'">{{ row.trade_type === 'buy' ? '买入' : '卖出' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="price" label="价格" width="100">
          <template #default="{ row }">¥{{ row.price }}</template>
        </el-table-column>
        <el-table-column prop="quantity" label="数量" width="100" />
        <el-table-column prop="amount" label="金额" width="120">
          <template #default="{ row }">¥{{ row.amount }}</template>
        </el-table-column>
        <el-table-column prop="commission" label="手续费" width="100">
          <template #default="{ row }">¥{{ row.commission }}</template>
        </el-table-column>
      </el-table>
      <div v-if="trades.length === 0" class="empty-tip">暂无交易记录</div>
    </el-card>
    <el-card>
      <template #header>测试日志</template>
      <div class="log-content">
        <pre>{{ backtest.log || '暂无日志' }}</pre>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { backtestAPI } from '@/api'
import * as echarts from 'echarts'
import { ArrowLeft } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const backtest = ref({})
const trades = ref([])
const chartRef = ref(null)

const strategyNameMap = { dual_ma: '双均线交叉', triple_ma: '三重均线', four_line: '四线多头' }
const getStrategyName = (code) => strategyNameMap[code] || code
const formatPercent = (value) => value ? `${value >= 0 ? '+' : ''}${value.toFixed(2)}%` : '--'
const formatDrawdown = (value) => value ? `${value.toFixed(2)}%` : '--'
const formatDate = (dateStr) => dateStr ? new Date(dateStr).toLocaleString('zh-CN') : '--'
const goBack = () => router.push('/backtest')

const initChart = () => {
  if (!chartRef.value || !backtest.value.equity_curve) return
  const chart = echarts.init(chartRef.value)
  const curve = typeof backtest.value.equity_curve === 'string' ? JSON.parse(backtest.value.equity_curve) : backtest.value.equity_curve
  const dates = curve.map(item => item.date)
  const values = curve.map(item => item.value)
  chart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', data: dates, axisLabel: { rotate: 45, fontSize: 10 } },
    yAxis: { type: 'value', axisLabel: { formatter: '{value}%' } },
    series: [{ name: '收益率', type: 'line', data: values, smooth: true, areaStyle: { opacity: 0.3 }, itemStyle: { color: '#409eff' } }]
  })
  window.addEventListener('resize', () => chart.resize())
}

const loadData = async () => {
  const id = route.params.id
  try {
    backtest.value = await backtestAPI.getResult(id)
    if (backtest.value.trades) {
      trades.value = typeof backtest.value.trades === 'string' ? JSON.parse(backtest.value.trades) : backtest.value.trades
    }
    await nextTick()
    initChart()
  } catch (error) { console.error('加载数据失败:', error) }
}

onMounted(loadData)
</script>

<style scoped>
.backtest-detail-page { padding: 10px 0; }
.page-header { display: flex; align-items: center; gap: 16px; margin-bottom: 24px; }
.header-title h2 { font-size: 24px; font-weight: 600; margin: 0 0 4px 0; color: #333; }
.header-title p { font-size: 14px; color: #999; margin: 0; }
.stats-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 16px; margin-bottom: 24px; }
.stat-card { text-align: center; }
.stat-value { font-size: 20px; font-weight: 700; color: #333; }
.stat-value.positive { color: #67c23a; }
.stat-value.negative { color: #f56c6c; }
.stat-label { font-size: 13px; color: #999; margin-top: 4px; }
.content-grid { display: grid; grid-template-columns: 1fr 350px; gap: 20px; margin-bottom: 20px; }
.chart-container { height: 400px; }
.params-list { display: flex; flex-direction: column; gap: 12px; }
.param-item { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px dashed #e8ecf0; }
.param-item:last-child { border-bottom: none; }
.param-item label { font-size: 13px; color: #999; }
.param-item span { font-size: 14px; color: #333; }
.empty-tip { text-align: center; color: #999; padding: 40px; }
.log-content { background: #f5f7fa; border-radius: 8px; padding: 16px; max-height: 300px; overflow-y: auto; }
.log-content pre { margin: 0; font-family: 'Consolas', monospace; font-size: 13px; color: #333; white-space: pre-wrap; }
</style>