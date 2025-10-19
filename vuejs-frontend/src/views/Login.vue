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
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-lg p-8">
      <h2 class="text-2xl font-bold text-gray-800 text-center mb-6">
        Iniciar Sesión
      </h2>

      <el-form :model="form" @submit.prevent="login" label-position="top">
        <el-form-item label="Email">
          <el-input
            placeholder="Ingresa tu email"
            v-model="form.email"
            clearable
          />
        </el-form-item>

        <el-form-item label="Contraseña">
          <el-input
            type="password"
            placeholder="Ingresa tu contraseña"
            v-model="form.password"
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            class="w-full !bg-indigo-600 hover:!bg-indigo-700 transition"
            @click="login"
          >
            Ingresar
          </el-button>
        </el-form-item>
      </el-form>

      <p class="text-sm text-gray-600 text-center mt-4">
        ¿No tienes cuenta?
        <a href="#" class="text-indigo-600 hover:underline">Regístrate</a>
      </p>
    </div>
  </div>
</template>
