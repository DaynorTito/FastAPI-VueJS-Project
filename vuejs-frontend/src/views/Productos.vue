<script setup>
import { ElMessage, ElMessageBox } from 'element-plus';
import { onMounted, ref } from 'vue';
import axios from 'axios'
import { id } from 'element-plus/es/locales.mjs';



const productos = ref([]);

const editIndex = ref(null);

const editProducto = ref({
    nombre: '',
    precio: 0,
});


const idUsuario = localStorage.getItem('usuario_id') || 1;

const crearModalVisible = ref(false);

const nuevoProducto = ref({
    nombre: '',
    precio: 0,
    usuario_id: idUsuario,
    categorias_id: []
});


const cargarProductos = async () => {
    try {
        const response = await axios.get(`http://localhost:8000/productos/listar-usuario/${idUsuario}`);
        productos.value = response.data;
    } catch (error) {
        console.error('Error loading productos:', error);
        ElMessage.error('Error loading productos');
    }
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
        console.error('Error deleting producto:', error);
        ElMessage.error('Error deleting producto');
    }
};

const crearProducto = async () => {
    try {
        const response = await axios.post('http://localhost:8000/productos/crear', nuevoProducto.value);
        productos.value.push({ ...nuevoProducto.value, id: response.data.producto_id });
        nuevoProducto.value = { nombre: '', precio: 0, usuario_id: idUsuario, categorias_id: [] };
        crearModalVisible.value = false;
        ElMessage.success('Producto creado');
    } catch (error) {
        console.error('Error creating producto:', error);
        ElMessage.error('Error creating producto');
    }
};

const guardarEdicion = async (index) => {
    try {
        const producto = productos.value[index];
        await axios.put(`http://localhost:8000/productos/editar/${producto.id}`, editProducto.value);
        productos.value[index] = { ...producto, ...editProducto.value };
        editIndex.value = null;
        ElMessage.success('Producto actualizado');
    } catch (error) {
        console.error('Error updating producto:', error);
        ElMessage.error('Error updating producto');
    }
};

const iniciarEdicion = (index) => {
    editIndex.value = index;
    editProducto.value = { ...productos.value[index] };
};

onMounted(() => {
    cargarProductos();
});

</script>

<template>
  <div class="productos-container">
    <div class="header">
      <h1>Productos</h1>
      <el-button type="primary" @click="crearModalVisible = true">Crear Producto</el-button>
    </div>

    <el-row :gutter="20">
      <el-col :span="6" v-for="(producto, index) in productos" :key="producto.id">
        <el-card shadow="hover" class="producto-card">
          <template #header>
            <div class="card-header">
              <div class="producto-nombre">
                <span v-if="editIndex !== index">{{ producto.nombre }}</span>
                <el-input
                  v-else
                  v-model="editProducto.nombre"
                  placeholder="Nombre"
                  size="small"
                />
              </div>
              <div class="acciones">
                <el-button
                  v-if="editIndex !== index"
                  type="primary"
                  size="small"
                  icon="el-icon-edit"
                  @click="iniciarEdicion(index)"
                >
                  Editar
                </el-button>
                <el-button
                  v-else
                  type="success"
                  size="small"
                  icon="el-icon-check"
                  @click="guardarEdicion(index)"
                >
                  Guardar
                </el-button>
                <el-button
                  type="danger"
                  size="small"
                  icon="el-icon-delete"
                  @click="eliminarProducto(producto.id)"
                >
                  Eliminar
                </el-button>
              </div>
            </div>
          </template>

          <div class="producto-precio">
            <p v-if="editIndex !== index">Precio: ${{ producto.precio }}</p>
            <el-input
              v-else
              v-model.number="editProducto.precio"
              placeholder="Precio"
              type="number"
              size="small"
            />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Diálogo para Crear Producto -->
    <el-dialog title="Crear Producto" v-model="crearModalVisible" width="30%">
      <el-form label-position="top" :model="nuevoProducto">
        <el-form-item label="Nombre">
          <el-input v-model="nuevoProducto.nombre" placeholder="Nombre" />
        </el-form-item>
        <el-form-item label="Precio">
          <el-input v-model.number="nuevoProducto.precio" placeholder="Precio" type="number" />
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="crearModalVisible = false">Cancelar</el-button>
          <el-button type="primary" @click="crearProducto">Crear</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.productos-container {
  padding: 24px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.producto-card {
  transition: all 0.3s ease-in-out;
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.producto-nombre {
  flex-grow: 1;
  font-weight: bold;
}

.acciones {
  display: flex;
  gap: 8px;
}

.producto-precio {
  margin-top: 16px;
  font-size: 14px;
}

</style>