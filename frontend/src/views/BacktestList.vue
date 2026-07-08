<template>
  <div class="backtest-list-page">
    <div class="filter-bar">
      <el-select v-model="filterStrategy" placeholder="选择策略类型" clearable style="width:150px">
        <el-option v-for="s in strategies" :key="s.code" :label="s.name" :value="s.code" />
      </el-select>
      <el-input v-model="filterStock" placeholder="搜索股票代码或名称" style="width:250px" />
      <div class="filter-actions">
        <el-button type="primary" @click="loadResults">搜索</el-button>
        <el-button @click="resetFilter">重置</el-button>
      </div>
    </div>
    <div class="action-bar">
      <router-link to="/run-backtest" class="btn-run">
        <el-button type="primary">
          <template #icon>
            <el-icon><Plus /></el-icon>
          </template>
          新增
        </el-button>
      </router-link>
      <el-button type="danger" :disabled="selectedRows.length === 0" @click="deleteSelected">
        <template #icon>
          <el-icon><Delete /></el-icon>
        </template>
        删除
      </el-button>
      <span v-if="selectedRows.length > 0" class="selected-count">已选择 {{ selectedRows.length }} 条</span>
    </div>
    <el-card>
      <template #header>
        <div class="card-header-inner">
          <h3>测试结果列表</h3>
          <span class="result-count">共 {{ backtestResults.length }} 条记录</span>
        </div>
      </template>
      <el-table :data="backtestResults" border @selection-change="handleSelectionChange" empty-text="暂无测试结果">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="ts_code" label="股票代码" width="120" />
        <el-table-column prop="stock_name" label="股票名称" width="120" />
        <el-table-column label="策略类型" width="120">
          <template #default="{ row }">
            <el-tag>{{ getStrategyName(row.strategy_type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="总收益率" width="120">
          <template #default="{ row }">
            <span :class="{ positive: row.total_return > 0, negative: row.total_return < 0 }">{{ formatPercent(row.total_return) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="年化收益率" width="120">
          <template #default="{ row }">
            <span :class="{ positive: row.annualized_return > 0, negative: row.annualized_return < 0 }">{{ formatPercent(row.annualized_return) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="最大回撤" width="120">
          <template #default="{ row }">
            <span class="negative">{{ formatDrawdown(row.max_drawdown) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="sharpe_ratio" label="夏普比率" width="100" />
        <el-table-column label="胜率" width="100">
          <template #default="{ row }">
            {{ formatPercent(row.win_rate) }}
          </template>
        </el-table-column>
        <el-table-column prop="total_trades" label="交易次数" width="100" />
        <el-table-column label="测试时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.test_date) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <router-link :to="`/backtest/${row.id}`" class="btn-view">查看</router-link>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <el-dialog title="确认删除" v-model="deleteDialogVisible" width="400px">
      <p>确定要删除选中的 {{ selectedRows.length }} 条回溯结果吗？此操作不可撤销。</p>
      <template #footer>
        <el-button @click="deleteDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="confirmDelete">确定删除</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { backtestAPI, strategyAPI } from '@/api'
import { Plus, Delete } from '@element-plus/icons-vue'

const backtestResults = ref([])
const strategies = ref([])
const filterStrategy = ref('')
const filterStock = ref('')
const selectedRows = ref([])
const deleteDialogVisible = ref(false)

const strategyNameMap = { dual_ma: '双均线交叉', triple_ma: '三重均线', four_line: '四线多头' }
const getStrategyName = (code) => strategyNameMap[code] || code
const formatPercent = (value) => value ? `${value >= 0 ? '+' : ''}${value.toFixed(2)}%` : '--'
const formatDrawdown = (value) => value ? `${value.toFixed(2)}%` : '--'
const formatDate = (dateStr) => dateStr ? new Date(dateStr).toLocaleString('zh-CN') : '--'

const handleSelectionChange = (rows) => selectedRows.value = rows
const deleteSelected = () => deleteDialogVisible.value = true

const confirmDelete = async () => {
  const ids = selectedRows.value.map(row => row.id)
  try {
    await backtestAPI.deleteResults(ids)
    deleteDialogVisible.value = false
    selectedRows.value = []
    loadResults()
  } catch (error) { console.error('删除失败:', error) }
}

const loadResults = async () => {
  try { backtestResults.value = await backtestAPI.getResults(filterStock.value, filterStrategy.value, 100) } catch (error) { console.error('加载结果失败:', error) }
}

const resetFilter = () => {
  filterStock.value = ''
  filterStrategy.value = ''
  loadResults()
}

const loadStrategies = async () => {
  try { strategies.value = await strategyAPI.getAll() } catch (error) { console.error('加载策略失败:', error) }
}

onMounted(async () => { await loadStrategies(); await loadResults(); })
</script>

<style scoped>
.backtest-list-page { padding: 10px 0; }
.filter-bar { display: flex; gap: 12px; margin-bottom: 12px; align-items: center; }
.action-bar { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
.selected-count { font-size: 14px; color: #999; }
.btn-run { text-decoration: none; }
.filter-actions { display: flex; gap: 8px; }
.card-header-inner { display: flex; justify-content: space-between; align-items: center; width: 100%; }
.card-header-inner h3 { font-size: 16px; font-weight: 600; margin: 0; }
.result-count { font-size: 14px; color: #999; }
.empty-tip { text-align: center; color: #999; padding: 40px; }
.btn-view { color: #409eff; font-size: 14px; text-decoration: none; }
.positive { color: #f56c6c; }
.negative { color: #67c23a; }
</style>