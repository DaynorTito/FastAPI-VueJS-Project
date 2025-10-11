

<script setup>
import { ref } from 'vue'

const activeIndex = ref('1')
const activeIndex2 = ref('1')
const handleSelect = (key, keyPath) => {
  console.log(key, keyPath)
}
</script>

<template>

  <div class="h-6" />
  <el-menu
    :default-active="activeIndex2"
    class="el-menu-demo"
    mode="horizontal"
    background-color="#545c64"
    text-color="#fff"
    active-text-color="#ffd04b"
    @select="handleSelect"
  >
      <el-menu-item index="1" @click="$router.push('/')">Home</el-menu-item>
    <el-menu-item index="2" @click="$router.push('/login')">Login</el-menu-item>
    <el-menu-item index="3" @click="$router.push('/registro')">Registro</el-menu-item>
    <el-menu-item index="4" @click="$router.push('/productos')">Productos</el-menu-item>

  </el-menu>
</template>

