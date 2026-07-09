import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const username = ref(localStorage.getItem('username') || '')
  const nickName = ref(localStorage.getItem('nickName') || '')

  const isLoggedIn = () => !!token.value

  const login = (newToken, newUsername, newNickName) => {
    token.value = newToken
    username.value = newUsername
    nickName.value = newNickName || newUsername
    localStorage.setItem('token', newToken)
    localStorage.setItem('username', newUsername)
    localStorage.setItem('nickName', nickName.value)
  }

  const logout = () => {
    token.value = ''
    username.value = ''
    nickName.value = ''
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    localStorage.removeItem('nickName')
  }

  return {
    token,
    username,
    nickName,
    isLoggedIn,
    login,
    logout
  }
})