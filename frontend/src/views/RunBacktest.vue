<template>
  <div class="run-backtest-page">
    <div class="content-grid">
      <div class="left-panel">
        <el-card>
          <template #header>测试配置</template>
          <el-form :model="form" label-width="120px">
            <el-form-item label="策略类型" required>
              <el-select v-model="form.strategy_type" placeholder="请选择策略">
                <el-option v-for="s in strategies" :key="s.code" :label="s.name" :value="s.code" />
              </el-select>
            </el-form-item>
            <el-form-item label="股票代码" required>
              <el-select v-model="form.ts_code" placeholder="请选择股票" filterable style="width:100%">
                <el-option v-for="stock in stocks" :key="stock.ts_code" :label="`${stock.ts_code} - ${stock.name}`" :value="stock.ts_code" />
              </el-select>
            </el-form-item>
            <el-form-item label="开始日期">
              <el-date-picker v-model="form.start_date" type="date" value-format="YYYY-MM-DD" />
            </el-form-item>
            <el-form-item label="结束日期">
              <el-date-picker v-model="form.end_date" type="date" value-format="YYYY-MM-DD" />
            </el-form-item>
            <el-form-item label="初始资金">
              <el-input-number v-model="form.initial_capital" :min="10000" :step="10000" />
            </el-form-item>
            <el-form-item label="交易手续费">
              <el-input-number v-model="form.commission_rate" :min="0" :max="1" :step="0.0001" />
            </el-form-item>
          </el-form>
        </el-card>
        <el-card>
          <template #header>策略参数</template>
          <el-form :model="strategyParams" label-width="120px">
            <el-form-item v-for="(value, key) in strategyParams" :key="key" :label="getParamLabel(key)">
              <el-input-number v-model="strategyParams[key]" :min="1" :step="1" />
            </el-form-item>
          </el-form>
        </el-card>
      </div>
      <div class="right-panel">
        <el-card>
          <template #header>操作</template>
          <div class="action-buttons">
            <el-button type="primary" :loading="isRunning" @click="runBacktest">
              <template #icon>
                <el-icon><VideoPlay /></el-icon>
              </template>
              执行回溯
            </el-button>
            <el-button @click="resetForm">重置参数</el-button>
          </div>
          <div class="info-box">
            <h4>注意事项</h4>
            <ul>
              <li>回溯测试仅基于历史数据</li>
              <li>测试结果不代表未来表现</li>
              <li>建议使用较长时间周期测试</li>
            </ul>
          </div>
        </el-card>
      </div>
    </div>
    <div v-if="result" class="result-section">
      <el-card>
        <template #header>测试结果</template>
        <div class="result-stats">
          <div class="result-item">
            <span class="label">总收益率</span>
            <span class="value" :class="{ positive: result.total_return > 0, negative: result.total_return < 0 }">{{ formatPercent(result.total_return) }}</span>
          </div>
          <div class="result-item">
            <span class="label">年化收益率</span>
            <span class="value" :class="{ positive: result.annualized_return > 0, negative: result.annualized_return < 0 }">{{ formatPercent(result.annualized_return) }}</span>
          </div>
          <div class="result-item">
            <span class="label">最大回撤</span>
            <span class="value negative">{{ formatPercent(result.max_drawdown) }}</span>
          </div>
          <div class="result-item">
            <span class="label">夏普比率</span>
            <span class="value">{{ result.sharpe_ratio ? result.sharpe_ratio.toFixed(2) : '--' }}</span>
          </div>
          <div class="result-item">
            <span class="label">胜率</span>
            <span class="value">{{ formatPercent(result.win_rate) }}</span>
          </div>
          <div class="result-item">
            <span class="label">交易次数</span>
            <span class="value">{{ result.total_trades || 0 }}</span>
          </div>
        </div>
        <div class="result-actions">
          <el-button type="primary" @click="saveResult">保存结果</el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { backtestAPI, strategyAPI, stockAPI } from '@/api'
import { VideoPlay } from '@element-plus/icons-vue'

const route = useRoute()
const strategies = ref([])
const stocks = ref([])
const isRunning = ref(false)
const result = ref(null)

const form = ref({ strategy_type: '', ts_code: '', start_date: '', end_date: '', initial_capital: 100000, commission_rate: 0.0003 })
const strategyParams = ref({})

const paramLabels = { short_window: '短期窗口', mid_window: '中期窗口', long_window: '长期窗口', windows: '均线周期', volume_filter: '成交量过滤', volume_ratio: '成交量比率' }
const getParamLabel = (key) => paramLabels[key] || key
const formatPercent = (value) => value ? `${value >= 0 ? '+' : ''}${value.toFixed(2)}%` : '--'

const loadStrategies = async () => {
  try { strategies.value = await strategyAPI.getAll() } catch (error) { console.error('加载策略失败:', error) }
}

const loadStocks = async () => {
  try { stocks.value = await stockAPI.getAll() } catch (error) { console.error('加载股票失败:', error) }
}

const loadStrategyParams = async (code) => {
  try {
    const strategy = await strategyAPI.getByCode(code)
    if (strategy.params) {
      strategyParams.value = typeof strategy.params === 'string' ? JSON.parse(strategy.params) : strategy.params
    }
  } catch (error) { console.error('加载策略参数失败:', error) }
}

const runBacktest = async () => {
  if (!form.value.strategy_type || !form.value.ts_code) { return }
  isRunning.value = true
  try {
    result.value = await backtestAPI.run(form.value, strategyParams.value)
  } catch (error) { console.error('执行回溯失败:', error) } finally { isRunning.value = false }
}

const saveResult = async () => {
  if (!result.value) return
  try {
    await backtestAPI.save(result.value)
    result.value = null
  } catch (error) { console.error('保存结果失败:', error) }
}

const resetForm = () => {
  form.value = { strategy_type: '', ts_code: '', start_date: '', end_date: '', initial_capital: 100000, commission_rate: 0.0003 }
  strategyParams.value = {}
  result.value = null
}

watch(() => form.value.strategy_type, async (newVal) => {
  if (newVal) await loadStrategyParams(newVal)
})

onMounted(async () => {
  await loadStrategies()
  await loadStocks()
  if (route.query.strategy) form.value.strategy_type = route.query.strategy
})
</script>

<style scoped>
.run-backtest-page { padding: 10px 0; }
.content-grid { display: grid; grid-template-columns: 1fr 400px; gap: 20px; margin-bottom: 20px; }
.action-buttons { display: flex; flex-direction: column; gap: 12px; }
.info-box { margin-top: 20px; padding: 16px; background: #fff7e6; border-radius: 8px; }
.info-box h4 { font-size: 14px; font-weight: 600; margin: 0 0 12px 0; color: #d48806; }
.info-box ul { margin: 0; padding-left: 20px; }
.info-box li { font-size: 13px; color: #666; margin-bottom: 8px; }
.result-section { margin-top: 24px; }
.result-stats { display: grid; grid-template-columns: repeat(6, 1fr); gap: 20px; margin-bottom: 20px; }
.result-item { text-align: center; padding: 16px; background: #f5f7fa; border-radius: 8px; }
.result-item .label { font-size: 13px; color: #999; display: block; margin-bottom: 8px; }
.result-item .value { font-size: 20px; font-weight: 700; color: #333; }
.result-item .value.positive { color: #67c23a; }
.result-item .value.negative { color: #f56c6c; }
.result-actions { display: flex; justify-content: flex-end; }
</style>