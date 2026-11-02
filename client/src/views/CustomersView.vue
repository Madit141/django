<script setup>
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';

const customers = ref([]);
const customerToAdd = ref({});
const customerToEdit = ref({});
const customerPictureRef = ref();
const customerAddImageUrl = ref();
const customerEditPictureRef = ref();
const customerEditImageUrl = ref();
const modalImageUrl = ref('');

async function fetchCustomers() {
  const r = await axios.get("/api/customers/");
  customers.value = r.data;
}

function customerAddPictureChange() {
  if (customerPictureRef.value?.files[0]) {
    customerAddImageUrl.value = URL.createObjectURL(customerPictureRef.value.files[0]);
  }
}

function customerEditPictureChange() {
  if (customerEditPictureRef.value?.files[0]) {
    customerEditImageUrl.value = URL.createObjectURL(customerEditPictureRef.value.files[0]);
  }
}

function openImageModal(url) {
  modalImageUrl.value = url;
}

async function onCustomerAdd() {
  const formData = new FormData();

  if (customerPictureRef.value?.files[0]) {
    formData.append('photo', customerPictureRef.value.files[0]);
  }

  formData.set('first_name', customerToAdd.value.first_name);
  formData.set('last_name', customerToAdd.value.last_name);
  formData.set('phone', customerToAdd.value.phone);

  await axios.post("/api/customers/", formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });

  customerToAdd.value = {};
  if (customerPictureRef.value) {
    customerPictureRef.value.value = '';
  }
  customerAddImageUrl.value = null;

  await fetchCustomers();
}

async function onRemoveClick(customer) {
  await axios.delete(`/api/customers/${customer.id}/`);
  await fetchCustomers();
}

async function onCustomerEditClick(customer) {
  customerToEdit.value = { ...customer };
  customerEditImageUrl.value = customer.photo;
  if (customerEditPictureRef.value) {
    customerEditPictureRef.value.value = '';
  }
}

async function onUpdateCustomer() {
  const formData = new FormData();
  formData.set('first_name', customerToEdit.value.first_name);
  formData.set('last_name', customerToEdit.value.last_name);
  formData.set('phone', customerToEdit.value.phone);

  if (customerEditPictureRef.value?.files[0]) {
    formData.append('photo', customerEditPictureRef.value.files[0]);
  }

  await axios.patch(`/api/customers/${customerToEdit.value.id}/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    }
  });

  await fetchCustomers();
}

onBeforeMount(async () => {
  await fetchCustomers();
});
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onCustomerAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="customerToAdd.first_name" required />
              <label>Имя</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="customerToAdd.last_name" required />
              <label>Фамилия</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="customerToAdd.phone" required />
              <label>Телефон</label>
            </div>
          </div>
          <div class="col-auto">
            <input
              class="form-control"
              type="file"
              ref="customerPictureRef"
              @change="customerAddPictureChange"
            />
          </div>
          <div class="col-auto" v-if="customerAddImageUrl">
            <img :src="customerAddImageUrl" style="max-height: 60px;" alt="" />
          </div>
          <div class="col-auto">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>

      <div>
        <div v-for="item in customers" class="customer-item">
          <div>{{ item.first_name }} {{ item.last_name }}</div>
          <div>{{ item.phone }}</div>
          <div v-show="item.photo">
            <img
              :src="item.photo"
              style="max-height: 60px; cursor: pointer;"
              alt=""
              data-bs-toggle="modal"
              data-bs-target="#viewCustomerImageModal"
              @click="openImageModal(item.photo)"
              title="Нажмите для увеличения"
            />
          </div>
          <button
            class="btn btn-success"
            @click="onCustomerEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editCustomerModal"
          >
            <i class="bi bi-pen-fill"></i>
          </button>
          <button class="btn btn-danger" @click="onRemoveClick(item)">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editCustomerModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать покупателя</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="row g-2">
              <div class="col-6">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="customerToEdit.first_name" />
                  <label>Имя</label>
                </div>
              </div>
              <div class="col-6">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="customerToEdit.last_name" />
                  <label>Фамилия</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="customerToEdit.phone" />
                  <label>Телефон</label>
                </div>
              </div>
              <div class="col-12">
                <label class="form-label text-muted">Изменить фото:</label>
                <input
                  type="file"
                  class="form-control"
                  ref="customerEditPictureRef"
                  @change="customerEditPictureChange"
                />
              </div>
              <div class="col-12 text-center" v-if="customerEditImageUrl">
                <img :src="customerEditImageUrl" style="max-height: 120px;" class="rounded" alt="" />
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button
              data-bs-dismiss="modal"
              type="button"
              class="btn btn-primary"
              @click="onUpdateCustomer"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal fade" id="viewCustomerImageModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Просмотр фото</h5>
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
.customer-item {
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