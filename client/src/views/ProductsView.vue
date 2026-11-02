<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from 'axios';
import _ from 'lodash';

const products = ref([]);
const productTypes = ref([]);
const productToAdd = ref({});
const productToEdit = ref({});
const productPictureRef = ref();
const productAddImageUrl = ref();
const productEditPictureRef = ref();
const productEditImageUrl = ref();
const modalImageUrl = ref('');

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

function productAddPictureChange() {
  if (productPictureRef.value?.files[0]) {
    productAddImageUrl.value = URL.createObjectURL(productPictureRef.value.files[0]);
  }
}

function productEditPictureChange() {
  if (productEditPictureRef.value?.files[0]) {
    productEditImageUrl.value = URL.createObjectURL(productEditPictureRef.value.files[0]);
  }
}

function openImageModal(url) {
  modalImageUrl.value = url;
}

async function onProductAdd() {
  const formData = new FormData();

  if (productPictureRef.value?.files[0]) {
    formData.append('image', productPictureRef.value.files[0]);
  }

  formData.set('name', productToAdd.value.name);
  formData.set('quantity', productToAdd.value.quantity);
  formData.set('category', productToAdd.value.category);

  await axios.post("/api/products/", formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });

  productToAdd.value = {};
  if (productPictureRef.value) {
    productPictureRef.value.value = '';
  }
  productAddImageUrl.value = null;

  await fetchProducts();
}

async function onRemoveClick(product) {
  await axios.delete(`/api/products/${product.id}/`);
  await fetchProducts();
}

async function onProductEditClick(product) {
  productToEdit.value = { ...product };
  productEditImageUrl.value = product.image;
  if (productEditPictureRef.value) {
    productEditPictureRef.value.value = '';
  }
}

async function onUpdateProduct() {
  const formData = new FormData();
  formData.set('name', productToEdit.value.name);
  formData.set('quantity', productToEdit.value.quantity);
  formData.set('category', productToEdit.value.category);

  if (productEditPictureRef.value?.files[0]) {
    formData.append('image', productEditPictureRef.value.files[0]);
  }

  await axios.patch(`/api/products/${productToEdit.value.id}/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    }
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
            <input
              class="form-control"
              type="file"
              ref="productPictureRef"
              @change="productAddPictureChange"
            />
          </div>
          <div class="col-auto" v-if="productAddImageUrl">
            <img :src="productAddImageUrl" style="max-height: 60px;" alt="" />
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
          <div v-show="item.image">
            <img
              :src="item.image"
              style="max-height: 60px; cursor: pointer;"
              alt=""
              data-bs-toggle="modal"
              data-bs-target="#viewProductImageModal"
              @click="openImageModal(item.image)"
              title="Нажмите для увеличения"
            />
          </div>
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
              <div class="col-12">
                <label class="form-label text-muted">Изменить картинку:</label>
                <input
                  type="file"
                  class="form-control"
                  ref="productEditPictureRef"
                  @change="productEditPictureChange"
                />
              </div>
              <div class="col-12 text-center" v-if="productEditImageUrl">
                <img :src="productEditImageUrl" style="max-height: 120px;" class="rounded" alt="" />
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
    <div class="modal fade" id="viewProductImageModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Просмотр изображения</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body text-center p-2">
            <img :src="modalImageUrl" class="img-fluid rounded" style="max-height: 75vh;" alt="" />
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
  grid-template-columns: 1fr auto auto auto auto auto;
  gap: 16px;
  align-items: center;
}
</style>