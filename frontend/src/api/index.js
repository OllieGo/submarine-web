import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

api.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API Error:', error)
    throw error
  }
)

export const strategyAPI = {
  getAll: (category) => api.get('/strategies', { params: { category } }),
  getByCode: (code) => api.get(`/strategies/${code}`)
}

export const stockAPI = {
  getAll: (keyword, market, limit) => api.get('/stocks', { params: { keyword, market, limit } }),
  getByCode: (code) => api.get(`/stocks/${code}`),
  update: (code, data) => api.put(`/stocks/${code}`, data)
}

export const backtestAPI = {
  getResults: (ts_code, strategy_type, limit) => 
    api.get('/backtest/results', { params: { ts_code, strategy_type, limit } }),
  getResult: (id) => api.get(`/backtest/results/${id}`),
  getEquityCurve: (id) => api.get(`/backtest/equity/${id}`),
  getTrades: (id) => api.get(`/backtest/trades/${id}`),
  run: (params) => api.post('/backtest/run', params),
  getStats: () => api.get('/backtest/stats'),
  deleteResults: (ids) => api.delete('/backtest/results', { data: ids })
}

export default api