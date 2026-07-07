<template>
  <div class="stock-edit-page">
    <div class="page-header">
      <el-button @click="goBack">
        <template #icon>
          <el-icon><ArrowLeft /></el-icon>
        </template>
        返回
      </el-button>
      <div class="header-title">
        <h2>{{ stock.name || '编辑股票' }}</h2>
        <p>{{ stock.ts_code }}</p>
      </div>
    </div>
    <el-card>
      <el-form :model="form" label-width="120px">
        <el-form-item label="股票代码" required>
          <el-input v-model="form.ts_code" disabled />
        </el-form-item>
        <el-form-item label="股票名称" required>
          <el-input v-model="form.name" placeholder="请输入股票名称" />
        </el-form-item>
        <el-form-item label="地域">
          <el-input v-model="form.area" placeholder="请输入地域" />
        </el-form-item>
        <el-form-item label="所属行业">
          <el-input v-model="form.industry" placeholder="请输入所属行业" />
        </el-form-item>
        <el-form-item label="市场类别">
          <el-select v-model="form.market" placeholder="请选择市场类别">
            <el-option label="主板" value="主板" />
            <el-option label="中小板" value="中小板" />
            <el-option label="创业板" value="创业板" />
            <el-option label="科创板" value="科创板" />
          </el-select>
        </el-form-item>
        <el-form-item label="上市日期">
          <el-date-picker v-model="form.list_date" type="date" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="上市状态">
          <el-select v-model="form.list_status">
            <el-option label="上市" value="L" />
            <el-option label="退市" value="D" />
            <el-option label="暂停上市" value="P" />
          </el-select>
        </el-form-item>
        <el-form-item label="全称">
          <el-input v-model="form.fullname" placeholder="请输入股票全称" />
        </el-form-item>
        <el-form-item label="是否沪深港通">
          <el-select v-model="form.is_hs">
            <el-option label="是" value="H" />
            <el-option label="否" value="N" />
          </el-select>
        </el-form-item>
      </el-form>
      <div class="action-bar">
        <el-button type="primary" @click="saveStock">保存</el-button>
        <el-button @click="goBack">取消</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { stockAPI } from '@/api'
import { ArrowLeft } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const stock = ref({})
const form = ref({ ts_code: '', name: '', area: '', industry: '', market: '', list_date: '', list_status: 'L', fullname: '', is_hs: 'N' })

const goBack = () => router.push('/stocks')

const loadStock = async () => {
  const code = route.params.code
  try {
    stock.value = await stockAPI.getByCode(code)
    form.value = {
      ts_code: stock.value.ts_code || '',
      name: stock.value.name || '',
      area: stock.value.area || '',
      industry: stock.value.industry || '',
      market: stock.value.market || '',
      list_date: stock.value.list_date || '',
      list_status: stock.value.list_status || 'L',
      fullname: stock.value.fullname || '',
      is_hs: stock.value.is_hs || 'N'
    }
  } catch (error) { console.error('加载股票失败:', error) }
}

const saveStock = async () => {
  try {
    await stockAPI.update(form.value.ts_code, form.value)
    router.push('/stocks')
  } catch (error) { console.error('保存失败:', error) }
}

onMounted(loadStock)
</script>

<style scoped>
.stock-edit-page { padding: 10px 0; }
.page-header { display: flex; align-items: center; gap: 16px; margin-bottom: 24px; }
.header-title h2 { font-size: 24px; font-weight: 600; margin: 0 0 4px 0; color: #333; }
.header-title p { font-size: 14px; color: #999; margin: 0; }
.action-bar { display: flex; justify-content: flex-end; gap: 12px; padding-top: 20px; }
</style>