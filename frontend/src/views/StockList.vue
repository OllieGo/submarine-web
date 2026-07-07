<template>
  <div class="stock-list-page">
    <div class="filter-bar">
      <el-input v-model="searchKeyword" placeholder="搜索股票代码或名称" style="width:250px" />
      <el-select v-model="filterMarket" placeholder="选择市场" clearable style="width:120px">
        <el-option label="主板" value="主板" />
        <el-option label="中小板" value="中小板" />
        <el-option label="创业板" value="创业板" />
        <el-option label="科创板" value="科创板" />
      </el-select>
      <div class="filter-actions">
        <el-button type="primary" @click="loadStocks">搜索</el-button>
        <el-button @click="resetFilter">重置</el-button>
      </div>
    </div>
    <el-card>
      <template #header>
        <div class="card-header-inner">
          <h3>股票池</h3>
          <span class="result-count">共 {{ stocks.length }} 只股票</span>
        </div>
      </template>
      <el-table :data="stocks" border>
        <el-table-column prop="ts_code" label="股票代码" width="120" />
        <el-table-column prop="name" label="股票名称" width="120" />
        <el-table-column prop="area" label="地域" width="100" />
        <el-table-column prop="industry" label="所属行业" width="150" />
        <el-table-column prop="market" label="市场类别" width="100" />
        <el-table-column prop="list_date" label="上市日期" width="120" />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <router-link :to="`/stocks/${row.ts_code}`">
              <el-button type="primary" size="small">
                <template #icon>
                  <el-icon><Edit /></el-icon>
                </template>
                编辑
              </el-button>
            </router-link>
          </template>
        </el-table-column>
      </el-table>
      <div v-if="stocks.length === 0" class="empty-tip">暂无股票数据</div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { stockAPI } from '@/api'
import { Edit } from '@element-plus/icons-vue'

const stocks = ref([])
const searchKeyword = ref('')
const filterMarket = ref('')

const loadStocks = async () => {
  try { stocks.value = await stockAPI.getAll(searchKeyword.value, filterMarket.value, 100) } catch (error) { console.error('加载股票失败:', error) }
}

const resetFilter = () => {
  searchKeyword.value = ''
  filterMarket.value = ''
  loadStocks()
}

onMounted(loadStocks)
</script>

<style scoped>
.stock-list-page { padding: 10px 0; }
.filter-bar { display: flex; gap: 12px; margin-bottom: 16px; align-items: center; }
.filter-actions { display: flex; gap: 8px; margin-left: auto; }
.card-header-inner { display: flex; justify-content: space-between; align-items: center; width: 100%; }
.card-header-inner h3 { font-size: 16px; font-weight: 600; margin: 0; }
.result-count { font-size: 14px; color: #999; }
.empty-tip { text-align: center; color: #999; padding: 40px; }
</style>