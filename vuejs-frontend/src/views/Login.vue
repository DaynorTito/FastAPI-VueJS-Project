<script setup>

import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = ref({
    email: '',
  password: ''
})

const login = async () => {
  try {
    const response = await axios.post('http://localhost:8000/usuarios/login', form.value)
    const usuarioId = response.data.usuario_id
    localStorage.setItem('usuario_id', usuarioId)
    alert('Login exitoso!')
    router.push('/')
  } catch (error) {
    alert('Error login')
    console.error('Error during login:', error)
  }
}

</script>

<template>
  <div style="max-width: 400px; margin: 0 auto; padding: 20px;">
    <h2>Login</h2>
    <el-form :model="form" @submit.prevent="login">
      <el-form-item label="Email">
        <el-input placeholder="Enter your email" v-model="form.email"/>
      </el-form-item>
      <el-form-item label="Password">
        <el-input type="password" placeholder="Enter your password" v-model="form.password"/>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="login">Login</el-button>
      </el-form-item>
    </el-form>

  </div>
</template>
