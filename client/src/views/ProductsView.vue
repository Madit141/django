<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from 'axios';
import _ from 'lodash';

const products = ref([]);
const productTypes = ref([]);
const productToAdd = ref({});
const productToEdit = ref({});

const productTypesById = computed(() => {
  return _.keyBy(productTypes.value, x => x.id);
});

async function fetchProducts() {
  const r = await axios.get("/api/products/");
  products.value = r.data;
}

async function fetchProductTypes() {
  const r = await axios.get("/api/product-types/");
  productTypes.value = r.data;
}

async function onProductAdd() {
  await axios.post("/api/products/", {
    ...productToAdd.value,
  });
  await fetchProducts();
}

async function onRemoveClick(product) {
  await axios.delete(`/api/products/${product.id}/`);
  await fetchProducts();
}

async function onProductEditClick(product) {
  productToEdit.value = { ...product };
}

async function onUpdateProduct() {
  await axios.put(`/api/products/${productToEdit.value.id}/`, {
    ...productToEdit.value,
  });
  await fetchProducts();
}

onBeforeMount(async () => {
  await fetchProducts();
  await fetchProductTypes();
});
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onProductAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="productToAdd.name"
                required
              />
              <label>Название товара</label>
            </div>
          </div>
          <div class="col-auto">
            <div class="form-floating">
              <input
                type="number"
                class="form-control"
                v-model="productToAdd.quantity"
                required
              />
              <label>Количество</label>
            </div>
          </div>
          <div class="col-auto">
            <div class="form-floating">
              <select class="form-select" v-model="productToAdd.category" required>
                <option :value="t.id" v-for="t in productTypes">
                  {{ t.name }}
                </option>
              </select>
              <label>Категория</label>
            </div>
          </div>
          <div class="col-auto">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>

      <div>
        <div v-for="item in products" class="product-item">
          <div>{{ item.name }}</div>
          <div>Кол-во: {{ item.quantity }}</div>
          <div>{{ productTypesById[item.category]?.name }}</div>
          <button
            class="btn btn-success"
            @click="onProductEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editProductModal"
          >
            <i class="bi bi-pen-fill"></i>
          </button>
          <button class="btn btn-danger" @click="onRemoveClick(item)">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editProductModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать товар</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="row g-2">
              <div class="col-12">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="productToEdit.name" />
                  <label>Название товара</label>
                </div>
              </div>
              <div class="col-6">
                <div class="form-floating">
                  <input type="number" class="form-control" v-model="productToEdit.quantity" />
                  <label>Количество</label>
                </div>
              </div>
              <div class="col-6">
                <div class="form-floating">
                  <select class="form-select" v-model="productToEdit.category">
                    <option :value="t.id" v-for="t in productTypes">
                      {{ t.name }}
                    </option>
                  </select>
                  <label>Категория</label>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button
              data-bs-dismiss="modal"
              type="button"
              class="btn btn-primary"
              @click="onUpdateProduct"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.product-item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
  display: grid;
  grid-template-columns: 1fr auto auto auto auto;
  gap: 16px;
  align-items: center;
}
</style>