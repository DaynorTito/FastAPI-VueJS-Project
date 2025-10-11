<script setup>
import { ref } from 'vue'

// Imágenes del carrusel (puedes reemplazarlas por URLs reales o importar assets locales)
const imagenes = ref([
  'https://source.unsplash.com/random/800x300?tech',
  'https://source.unsplash.com/random/800x300?startup',
  'https://source.unsplash.com/random/800x300?business',
])
</script>

<template>
  <div class="home-container">
    <!-- Hero / Bienvenida -->
    <section class="hero">
      <h1>Bienvenido a Nuestra Plataforma</h1>
      <p>Ofrecemos soluciones eficientes para el crecimiento de tu negocio.</p>
    </section>

    <!-- Carrusel de imágenes -->
    <section class="carousel-section">
      <el-carousel height="300px" indicator-position="outside">
        <el-carousel-item v-for="(img, index) in imagenes" :key="index">
          <img :src="img" class="carousel-image" />
        </el-carousel-item>
      </el-carousel>
    </section>

    <!-- Misión y Visión -->
    <section class="info-section">
      <el-row :gutter="40">
        <el-col :span="12">
          <el-card shadow="hover">
            <h2>Misión</h2>
            <p>
              Brindar soluciones innovadoras y personalizadas que impulsen la transformación digital
              de nuestros clientes.
            </p>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card shadow="hover">
            <h2>Visión</h2>
            <p>
              Ser líderes en tecnología y desarrollo de software, reconocidos por nuestra calidad,
              compromiso y enfoque al cliente.
            </p>
          </el-card>
        </el-col>
      </el-row>
    </section>

    <!-- Servicios -->
    <section class="services-section">
      <h2>Nuestros Servicios</h2>
      <el-row :gutter="20" justify="center">
        <el-col :span="6">
          <el-card shadow="hover">
            <h3>Desarrollo Web</h3>
            <p>Diseño y desarrollo de sitios web modernos y funcionales.</p>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <h3>Consultoría Tecnológica</h3>
            <p>Te ayudamos a tomar decisiones estratégicas en tecnología.</p>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <h3>Soporte y Mantenimiento</h3>
            <p>Mantén tus sistemas funcionando de forma óptima.</p>
          </el-card>
        </el-col>
      </el-row>
    </section>
  </div>
</template>

<style scoped>
.home-container {
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
}

.hero {
  text-align: center;
  margin-bottom: 40px;
}

.carousel-section {
  margin-bottom: 60px;
}

.carousel-image {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-radius: 8px;
}

.info-section {
  margin-bottom: 60px;
}

.services-section {
  margin-top: 40px;
  text-align: center;
}
.services-section h2 {
  margin-bottom: 30px;
}
</style>
