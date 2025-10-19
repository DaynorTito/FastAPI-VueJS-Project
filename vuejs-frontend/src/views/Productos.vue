<script setup>
import { ElMessage, ElMessageBox } from 'element-plus';
import { onMounted, ref, watch } from 'vue';
import axios from 'axios';

const productos = ref([]);
const editIndex = ref(null);
const editProducto = ref({
  nombre: '',
  precio: 0,
  stock: 0
});

const idUsuario = localStorage.getItem('usuario_id') || 1;

const crearModalVisible = ref(false);
const nuevoProducto = ref({
  nombre: '',
  precio: 0,
  stock: 0,
  usuario_id: idUsuario,
  categorias_id: []
});

// Filtros de búsqueda
const filtros = ref({
  nombre: '',
  precio_min: null,
  precio_max: null,
  usuario_id: idUsuario
});

const mostrarFiltros = ref(false);

const cargarProductos = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/productos/listar-usuario/${idUsuario}`);
    productos.value = response.data;
  } catch (error) {
    console.error('Error loading productos:', error);
    ElMessage.error('Error al cargar productos');
  }
};

const buscarProductos = async () => {
  try {
    const params = {};
    
    if (filtros.value.nombre) params.nombre = filtros.value.nombre;
    if (filtros.value.precio_min !== null && filtros.value.precio_min !== '') 
      params.precio_min = filtros.value.precio_min;
    if (filtros.value.precio_max !== null && filtros.value.precio_max !== '') 
      params.precio_max = filtros.value.precio_max;
    if (filtros.value.usuario_id) params.usuario_id = filtros.value.usuario_id;

    const response = await axios.get('http://localhost:8000/productos/busqueda-productos', { params });
    productos.value = response.data;
  } catch (error) {
    console.error('Error searching productos:', error);
    ElMessage.error('Error al buscar productos');
  }
};

const limpiarFiltros = () => {
  filtros.value = {
    nombre: '',
    precio_min: null,
    precio_max: null,
    usuario_id: idUsuario
  };
  cargarProductos();
};

const eliminarProducto = async (productoId) => {
  try {
    await ElMessageBox.confirm('¿Estás seguro de que deseas eliminar este producto?', 'Confirmar', {
      confirmButtonText: 'Sí',
      cancelButtonText: 'No',
      type: 'warning',
    });

    await axios.delete(`http://localhost:8000/productos/eliminar/${productoId}`);
    productos.value = productos.value.filter(producto => producto.id !== productoId);
    ElMessage.success('Producto eliminado');
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Error deleting producto:', error);
      ElMessage.error('Error al eliminar producto');
    }
  }
};

const crearProducto = async () => {
  try {
    if (!nuevoProducto.value.nombre || !nuevoProducto.value.precio) {
      ElMessage.warning('Por favor completa todos los campos');
      return;
    }

    const response = await axios.post('http://localhost:8000/productos/crear', nuevoProducto.value);
    productos.value.push({ ...nuevoProducto.value, id: response.data.producto_id });
    nuevoProducto.value = { nombre: '', precio: 0, usuario_id: idUsuario, categorias_id: [] };
    crearModalVisible.value = false;
    ElMessage.success('Producto creado');
  } catch (error) {
    console.error('Error creating producto:', error);
    ElMessage.error('Error al crear producto');
  }
};

const guardarEdicion = async (index) => {
  try {
    const producto = productos.value[index];
    console.log( "ENVIO EDICION PRODUCT: ",editProducto.value);
    await axios.put(`http://localhost:8000/productos/editar/${producto.id}`, editProducto.value);
    productos.value[index] = { ...producto, ...editProducto.value };
    editIndex.value = null;
    ElMessage.success('Producto actualizado');
  } catch (error) {
    console.error('Error updating producto:', error);
    ElMessage.error('Error al actualizar producto');
  }
};

const iniciarEdicion = (index) => {
  editIndex.value = index;
  editProducto.value = { ...productos.value[index] };
};

const iniciarEdicionStock = async (index) => {
  try {

      const producto = productos.value[index];
      editProducto.value.stock = producto.stock - 1;
      await axios.put(`http://localhost:8000/productos/editar/${producto.id}`, {
        stock: producto.stock - 1
      });
      productos.value[index] = { ...producto, ...editProducto.value };
      editIndex.value = null;
    } catch (error) {
      console.error('Error updating producto:', error);
      ElMessage.error('Error al actualizar producto');
    }
};

// Búsqueda en tiempo real
watch(() => filtros.value.nombre, (newVal) => {
  if (newVal === '') {
    cargarProductos();
  }
});

onMounted(() => {
  cargarProductos();
});
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
    <!-- Header -->
    <div class="max-w-7xl mx-auto mb-6">
      <div class="bg-white rounded-2xl shadow-sm p-6 border border-slate-200">
        <div class="flex justify-between items-center mb-6">
          <div>
            <h1 class="text-3xl font-bold text-slate-800">Productos</h1>
            <p class="text-slate-500 mt-1">Gestiona tu catálogo de productos</p>
          </div>
          <button 
            @click="crearModalVisible = true"
            class="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white px-6 py-3 rounded-xl font-semibold shadow-lg shadow-blue-500/30 transition-all duration-200 hover:scale-105 flex items-center gap-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            Crear Producto
          </button>
        </div>

        <!-- Barra de Búsqueda -->
        <div class="space-y-4">
          <div class="flex gap-3">
            <div class="flex-1 relative">
              <svg class="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
              <input
                v-model="filtros.nombre"
                @keyup.enter="buscarProductos"
                type="text"
                placeholder="Buscar productos por nombre..."
                class="w-full pl-12 pr-4 py-3 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
              />
            </div>
            <button
              @click="buscarProductos"
              class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-semibold transition-all duration-200 flex items-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
              Buscar
            </button>
            <button
              @click="mostrarFiltros = !mostrarFiltros"
              class="bg-slate-100 hover:bg-slate-200 text-slate-700 px-6 py-3 rounded-xl font-semibold transition-all duration-200 flex items-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"></path>
              </svg>
              Filtros
            </button>
          </div>

          <!-- Filtros Avanzados -->
          <div 
            v-show="mostrarFiltros"
            class="bg-slate-50 rounded-xl p-4 border border-slate-200 space-y-3"
          >
            <div class="text-sm font-semibold text-slate-700 mb-3">Filtros Avanzados</div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-600 mb-2">Precio Mínimo</label>
                <div class="relative">
                  <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500">$</span>
                  <input
                    v-model.number="filtros.precio_min"
                    type="number"
                    placeholder="0"
                    class="w-full pl-8 pr-4 py-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                  />
                </div>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-600 mb-2">Precio Máximo</label>
                <div class="relative">
                  <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500">$</span>
                  <input
                    v-model.number="filtros.precio_max"
                    type="number"
                    placeholder="999999"
                    class="w-full pl-8 pr-4 py-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                  />
                </div>
              </div>
            </div>
            <div class="flex gap-2 pt-2">
              <button
                @click="buscarProductos"
                class="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2.5 rounded-lg font-medium transition-all duration-200"
              >
                Aplicar Filtros
              </button>
              <button
                @click="limpiarFiltros"
                class="flex-1 bg-slate-200 hover:bg-slate-300 text-slate-700 px-4 py-2.5 rounded-lg font-medium transition-all duration-200"
              >
                Limpiar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Contador de Resultados -->
    <div class="max-w-7xl mx-auto mb-4">
      <p class="text-slate-600 text-sm">
        Se encontraron <span class="font-semibold text-slate-800">{{ productos.length }}</span> productos
      </p>
    </div>

    <!-- Grid de Productos -->
    <div class="max-w-7xl mx-auto">
      <div v-if="productos.length === 0" class="text-center py-16">
        <svg class="w-24 h-24 mx-auto text-slate-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path>
        </svg>
        <h3 class="text-xl font-semibold text-slate-700 mb-2">No se encontraron productos</h3>
        <p class="text-slate-500">Intenta ajustar los filtros de búsqueda</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <div 
          v-for="(producto, index) in productos" 
          :key="producto.id"
          class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
        >
          <!-- Card Header -->
          <div class="bg-gradient-to-r from-slate-50 to-slate-100 p-4 border-b border-slate-200">
            <div v-if="editIndex !== index" class="font-semibold text-lg text-slate-800 truncate">
              {{ producto.nombre }}
            </div>
            <input
              v-else
              v-model="editProducto.nombre"
              placeholder="Nombre del producto"
              class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
            />
          </div>

          <!-- Card Body -->
          <div class="p-6">
            <div class="mb-6">
              <div class="text-sm text-slate-500 mb-1">Precio</div>
              <div v-if="editIndex !== index" class="text-3xl font-bold text-slate-800">
                ${{ producto.precio.toLocaleString() }}
              </div>
              <input
                v-else
                v-model.number="editProducto.precio"
                type="number"
                placeholder="0.00"
                class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all text-lg font-semibold"
              />
            </div>

             <div class="mb-6">
              <div class="text-sm text-slate-500 mb-1">Stock</div>
              <div v-if="editIndex !== index" class="text-3xl font-bold text-slate-800">
                Cantidad: {{ producto.stock.toLocaleString() }}
              </div>
              <input
                v-else
                v-model.number="editProducto.stock"
                type="number"
                placeholder="0.00"
                class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all text-lg font-semibold"
              />
            </div>

            <!-- Acciones -->
            <div class="flex gap-2">
              <button
                v-if="editIndex !== index"
                @click="iniciarEdicion(index)"
                class="flex-1 bg-blue-50 hover:bg-blue-100 text-blue-700 px-4 py-2.5 rounded-lg font-medium transition-all duration-200 flex items-center justify-center gap-2"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                </svg>
                Editar
              </button>
              <button
                v-if="editIndex !== index"
                @click="iniciarEdicionStock(index)"
                class="flex-1 bg-blue-50 hover:bg-blue-100 text-blue-700 px-4 py-2.5 rounded-lg font-medium transition-all duration-200 flex items-center justify-center gap-2"
              >
                Reducir stock
              </button>
              <button
                v-else
                @click="guardarEdicion(index)"
                class="flex-1 bg-green-50 hover:bg-green-100 text-green-700 px-4 py-2.5 rounded-lg font-medium transition-all duration-200 flex items-center justify-center gap-2"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Guardar
              </button>
              <button
                @click="eliminarProducto(producto.id)"
                class="bg-red-50 hover:bg-red-100 text-red-700 px-4 py-2.5 rounded-lg font-medium transition-all duration-200"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Crear Producto -->
    <div 
      v-if="crearModalVisible"
      class="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
      @click.self="crearModalVisible = false"
    >
      <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full overflow-hidden transform transition-all">
        <!-- Modal Header -->
        <div class="bg-gradient-to-r from-blue-600 to-blue-700 p-6 text-white">
          <h2 class="text-2xl font-bold">Crear Nuevo Producto</h2>
          <p class="text-blue-100 mt-1">Completa la información del producto</p>
        </div>

        <!-- Modal Body -->
        <div class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-2">
              Nombre del Producto
            </label>
            <input
              v-model="nuevoProducto.nombre"
              type="text"
              placeholder="Ej: Laptop HP"
              class="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
            />
          </div>

          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-2">
              Stock
            </label>
            <div class="relative">
              <input
                v-model.number="nuevoProducto.stock"
                type="number"
                placeholder="0"
                class="w-full pl-8 pr-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-2">
              Precio
            </label>
            <div class="relative">
              <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 font-semibold">$</span>
              <input
                v-model.number="nuevoProducto.precio"
                type="number"
                placeholder="0.00"
                class="w-full pl-8 pr-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
              />
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="bg-slate-50 px-6 py-4 flex gap-3 justify-end border-t border-slate-200">
          <button
            @click="crearModalVisible = false"
            class="px-6 py-2.5 bg-white border border-slate-300 text-slate-700 rounded-lg font-medium hover:bg-slate-50 transition-all"
          >
            Cancelar
          </button>
          <button
            @click="crearProducto"
            class="px-6 py-2.5 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white rounded-lg font-semibold shadow-lg shadow-blue-500/30 transition-all"
          >
            Crear Producto
          </button>
        </div>
      </div>
    </div>
  </div>
</template>