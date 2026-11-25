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
const activeProductForAlbum = ref(null);
const albumFileRef = ref();
const users = ref([]);
const selectedUser = ref('');
const stats = ref({});

const productTypesById = computed(() => {
  return _.keyBy(productTypes.value, x => x.id);
});

async function fetchStats() {
  const params = {};
  if (selectedUser.value) {
    params.user = selectedUser.value;
  }
  const r = await axios.get("/api/products/stats/", { params });
  stats.value = r.data;
}

async function fetchProducts() {
  const params = {};
  if (selectedUser.value) {
    params.user = selectedUser.value;
  }
  const r = await axios.get("/api/products/", { params });
  products.value = r.data;
  await fetchStats();
}

async function fetchProductTypes() {
  const r = await axios.get("/api/product-types/");
  productTypes.value = r.data;
}

async function fetchUsers() {
  const r = await axios.get("/api/users/");
  users.value = r.data;
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

function openAlbumModal(product) {
  activeProductForAlbum.value = product;
}

async function onAddAlbumPhoto() {
  if (!albumFileRef.value?.files[0] || !activeProductForAlbum.value) return;

  const formData = new FormData();
  formData.append('product', activeProductForAlbum.value.id);
  formData.append('image', albumFileRef.value.files[0]);

  await axios.post('/api/product-images/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });

  if (albumFileRef.value) {
    albumFileRef.value.value = '';
  }

  await fetchProducts();
  activeProductForAlbum.value = products.value.find(p => p.id === activeProductForAlbum.value.id);
}

async function onDeleteAlbumPhoto(photoId) {
  await axios.delete(`/api/product-images/${photoId}/`);
  await fetchProducts();
  activeProductForAlbum.value = products.value.find(p => p.id === activeProductForAlbum.value.id);
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
  await fetchUsers();
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

      <div class="row my-2" v-if="users.length > 0">
        <div class="col-auto">
          <div class="form-floating">
            <select class="form-select" v-model="selectedUser" @change="fetchProducts">
              <option value="">Все пользователи</option>
              <option :value="u.id" v-for="u in users" :key="u.id">
                {{ u.username }}
              </option>
            </select>
            <label>Пользователь</label>
          </div>
        </div>
      </div>
      <div class="alert alert-light border my-2 d-flex gap-4">
        <div><strong>Всего товаров:</strong> {{ stats.count ?? 0 }}</div>
        <div><strong>Среднее кол-во:</strong> {{ stats.avg ? stats.avg.toFixed(2) : 0 }}</div>
        <div><strong>Макс. кол-во:</strong> {{ stats.max ?? 0 }}</div>
        <div><strong>Мин. кол-во:</strong> {{ stats.min ?? 0 }}</div>
      </div>
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
            class="btn btn-outline-info"
            @click="openAlbumModal(item)"
            data-bs-toggle="modal"
            data-bs-target="#albumModal"
            title="Открыть альбом"
          >
            <i class="bi bi-images"></i>
            <span class="ms-1 badge bg-info text-dark" v-if="item.images?.length">
              {{ item.images.length }}
            </span>
          </button>
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
    <div class="modal fade" id="albumModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content" v-if="activeProductForAlbum">
          <div class="modal-header">
            <h5 class="modal-title">Альбом: {{ activeProductForAlbum.name }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            
            <div v-if="!activeProductForAlbum.images || activeProductForAlbum.images.length === 0" class="text-center py-4 text-muted">
              В альбоме пока нет фотографий
            </div>

            <div v-else id="carouselAlbumControls" class="carousel slide bg-dark rounded p-2" data-bs-ride="carousel">
              <div class="carousel-inner text-center">
                <div
                  v-for="(img, idx) in activeProductForAlbum.images"
                  :key="img.id"
                  :class="['carousel-item', { active: idx === 0 }]"
                >
                  <img
                    :src="img.image"
                    class="d-block mx-auto img-fluid rounded"
                    style="max-height: 400px; object-fit: contain;"
                    alt=""
                  />
                  <div class="mt-2">
                    <button class="btn btn-sm btn-outline-danger" @click="onDeleteAlbumPhoto(img.id)">
                      <i class="bi bi-trash"></i> Удалить фото
                    </button>
                  </div>
                </div>
              </div>
              <button class="carousel-control-prev" type="button" data-bs-target="#carouselAlbumControls" data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Назад</span>
              </button>
              <button class="carousel-control-next" type="button" data-bs-target="#carouselAlbumControls" data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Вперед</span>
              </button>
            </div>

            <hr />

            <div class="row g-2 align-items-center">
              <div class="col">
                <label class="form-label mb-1">Добавить фото в альбом:</label>
                <input class="form-control" type="file" ref="albumFileRef" />
              </div>
              <div class="col-auto align-self-end">
                <button class="btn btn-primary" @click="onAddAlbumPhoto">
                  <i class="bi bi-upload"></i> Загрузить
                </button>
              </div>
            </div>

          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
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
  grid-template-columns: 1fr auto auto auto auto auto auto;
  gap: 16px;
  align-items: center;
}
</style>