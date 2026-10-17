<script setup>
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';

const productTypes = ref([]);
const typeToAdd = ref({});
const typeToEdit = ref({});

async function fetchProductTypes() {
  const r = await axios.get("/api/product-types/");
  productTypes.value = r.data;
}

async function onTypeAdd() {
  await axios.post("/api/product-types/", {
    ...typeToAdd.value,
  });
  await fetchProductTypes();
}

async function onRemoveClick(item) {
  await axios.delete(`/api/product-types/${item.id}/`);
  await fetchProductTypes();
}

async function onTypeEditClick(item) {
  typeToEdit.value = { ...item };
}

async function onUpdateType() {
  await axios.put(`/api/product-types/${typeToEdit.value.id}/`, {
    ...typeToEdit.value,
  });
  await fetchProductTypes();
}

onBeforeMount(async () => {
  await fetchProductTypes();
});
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onTypeAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="typeToAdd.name"
                required
              />
              <label>Название типа</label>
            </div>
          </div>
          <div class="col-auto">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>

      <div>
        <div v-for="item in productTypes" class="type-item">
          <div>{{ item.name }}</div>
          <button
            class="btn btn-success"
            @click="onTypeEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editTypeModal"
          >
            <i class="bi bi-pen-fill"></i>
          </button>
          <button class="btn btn-danger" @click="onRemoveClick(item)">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editTypeModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать тип</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="typeToEdit.name" />
              <label>Название типа</label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button
              data-bs-dismiss="modal"
              type="button"
              class="btn btn-primary"
              @click="onUpdateType"
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
.type-item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 16px;
  align-items: center;
}
</style>