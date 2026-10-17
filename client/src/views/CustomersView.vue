<script setup>
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';

const customers = ref([]);
const customerToAdd = ref({});
const customerToEdit = ref({});

async function fetchCustomers() {
  const r = await axios.get("/api/customers/");
  customers.value = r.data;
}

async function onCustomerAdd() {
  await axios.post("/api/customers/", {
    ...customerToAdd.value,
  });
  await fetchCustomers();
}

async function onRemoveClick(customer) {
  await axios.delete(`/api/customers/${customer.id}/`);
  await fetchCustomers();
}

async function onCustomerEditClick(customer) {
  customerToEdit.value = { ...customer };
}

async function onUpdateCustomer() {
  await axios.put(`/api/customers/${customerToEdit.value.id}/`, {
    ...customerToEdit.value,
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
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>

      <div>
        <div v-for="item in customers" class="customer-item">
          <div>{{ item.first_name }} {{ item.last_name }}</div>
          <div>{{ item.phone }}</div>
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
  </div>
</template>

<style lang="scss" scoped>
.customer-item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
  display: grid;
  grid-template-columns: 1fr auto auto auto;
  gap: 16px;
  align-items: center;
}
</style>