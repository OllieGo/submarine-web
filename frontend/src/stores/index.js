import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    selectedStock: null,
    selectedStrategy: null,
    backtestParams: {
      initialCapital: 100000,
      commissionRate: 0.0003,
      slippageRate: 0.001,
      positionSize: 0.95
    }
  }),
  actions: {
    setSelectedStock(stock) {
      this.selectedStock = stock
    },
    setSelectedStrategy(strategy) {
      this.selectedStrategy = strategy
    },
    setBacktestParams(params) {
      this.backtestParams = { ...this.backtestParams, ...params }
    },
    resetBacktestParams() {
      this.backtestParams = {
        initialCapital: 100000,
        commissionRate: 0.0003,
        slippageRate: 0.001,
        positionSize: 0.95
      }
    }
  }
})