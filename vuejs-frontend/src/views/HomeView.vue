<script setup>
import { ref } from 'vue'

// Imágenes del carrusel (puedes reemplazarlas por URLs reales o importar assets locales)
const imagenes = ref([
  'https://source.unsplash.com/random/800x300?tech',
  'https://source.unsplash.com/random/800x300?startup',
  'https://source.unsplash.com/random/800x300?business',
])

const posts = [
  {
    id: 1,
    title: 'Boost your conversion rate',
    href: '#',
    description:
      'Illo sint voluptas. Error voluptates culpa eligendi. Hic vel totam vitae illo. Non aliquid explicabo necessitatibus unde. Sed exercitationem placeat consectetur nulla deserunt vel. Iusto corrupti dicta.',
    date: 'Mar 16, 2020',
    datetime: '2020-03-16',
    category: { title: 'Marketing', href: '#' },
    author: {
      name: 'Michael Foster',
      role: 'Co-Founder / CTO',
      href: '#',
      imageUrl:
        'https://images.unsplash.com/photo-1519244703995-f4e0f30006d5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
    },
  },
  {
    id: 2,
    title: 'How to use search engine optimization to drive sales',
    href: '#',
    description: 'Optio cum necessitatibus dolor voluptatum provident commodi et. Qui aperiam fugiat nemo cumque.',
    date: 'Mar 10, 2020',
    datetime: '2020-03-10',
    category: { title: 'Sales', href: '#' },
    author: {
      name: 'Lindsay Walton',
      role: 'Front-end Developer',
      href: '#',
      imageUrl:
        'https://images.unsplash.com/photo-1517841905240-472988babdf9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
    },
  },
  {
    id: 3,
    title: 'Improve your customer experience',
    href: '#',
    description:
      'Cupiditate maiores ullam eveniet adipisci in doloribus nulla minus. Voluptas iusto libero adipisci rem et corporis. Nostrud sint anim sunt aliqua. Nulla eu labore irure incididunt velit cillum quis magna dolore.',
    date: 'Feb 12, 2020',
    datetime: '2020-02-12',
    category: { title: 'Business', href: '#' },
    author: {
      name: 'Tom Cook',
      role: 'Director of Product',
      href: '#',
      imageUrl:
        'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
    },
  },
  {
    id: 4,
    title: 'Improve your customer experience',
    href: '#',
    description:
      'Cupiditate maiores ullam eveniet adipisci in doloribus nulla minus. Voluptas iusto libero adipisci rem et corporis. Nostrud sint anim sunt aliqua. Nulla eu labore irure incididunt velit cillum quis magna dolore.',
    date: 'Feb 12, 2020',
    datetime: '2020-02-12',
    category: { title: 'Business', href: '#' },
    author: {
      name: 'Tom Cook',
      role: 'Director of Product',
      href: '#',
      imageUrl:
        'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
    },
  },
]
</script>

<template>
  <div class="home-container">
    <!-- Hero / Bienvenida -->
    <div class="bg-gray-900 py-24 sm:py-32">
      <div class="mx-auto max-w-7xl px-6 lg:px-8">
        <div class="mx-auto max-w-2xl lg:mx-0">
          <h2 class="text-4xl font-semibold tracking-tight text-pretty text-white sm:text-5xl">From the blog</h2>
          <p class="mt-2 text-lg/8 text-gray-300">Learn how to grow your business with our expert advice.</p>
        </div>
        <div class="mx-auto mt-10 grid max-w-2xl grid-cols-1 gap-x-8 gap-y-16 border-t border-gray-700 pt-10 sm:mt-16 sm:pt-16 lg:mx-0 lg:max-w-none lg:grid-cols-3">
          <article v-for="post in posts" :key="post.id" class="flex max-w-xl flex-col items-start justify-between">
            <div class="flex items-center gap-x-4 text-xs">
              <time :datetime="post.datetime" class="text-gray-400">{{ post.date }}</time>
              <a :href="post.category.href" class="relative z-10 rounded-full bg-gray-800/60 px-3 py-1.5 font-medium text-gray-300 hover:bg-gray-800">{{ post.category.title }}</a>
            </div>
            <div class="group relative grow">
              <h3 class="mt-3 text-lg/6 font-semibold text-white group-hover:text-gray-300">
                <a :href="post.href">
                  <span class="absolute inset-0" />
                  {{ post.title }}
                </a>
              </h3>
              <p class="mt-5 line-clamp-3 text-sm/6 text-gray-400">{{ post.description }}</p>
            </div>
            <div class="relative mt-8 flex items-center gap-x-4 justify-self-end">
              <img :src="post.author.imageUrl" alt="" class="size-10 rounded-full bg-gray-800" />
              <div class="text-sm/6">
                <p class="font-semibold text-white">
                  <a :href="post.author.href">
                    <span class="absolute inset-0" />
                    {{ post.author.name }}
                  </a>
                </p>
                <p class="text-gray-400">{{ post.author.role }}</p>
              </div>
            </div>
          </article>
        </div>
      </div>
    </div>

    
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
