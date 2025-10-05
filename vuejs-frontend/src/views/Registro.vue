<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = ref({
  nombre: '',
    email: '',
  apellido: '',
  password: ''
})

const register = async () => {
  try {
    await axios.post('http://localhost:8000/usuarios/crear', form.value)
    alert('Registro exitoso! Por favor, inicia sesión.')
    router.push('/login')
  } catch (error) {
    console.error('Error during registration:', error)
  }
}

</script>

<template>
  <div style="max-width: 400px; margin: 0 auto; padding: 20px;">
    <h2>Registro</h2>
    <el-form :model="form" @submit.prevent="register">
        <el-form-item label="Nombre">
        <el-input placeholder="Enter your nombre" v-model="form.nombre"/>
      </el-form-item>
      <el-form-item label="Apellido">
        <el-input placeholder="Enter your apellido"  v-model="form.apellido"/>
      </el-form-item>
      <el-form-item label="Email">
        <el-input placeholder="Enter your email" v-model="form.email"/>
      </el-form-item>
      <el-form-item label="Password">
        <el-input type="password" placeholder="Enter your password" v-model="form.password"/>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="register">Register</el-button>
      </el-form-item>
    </el-form>

  </div>
</template>
