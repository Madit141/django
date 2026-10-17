<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from 'axios';
import _ from 'lodash';

const orders = ref([]);
const customers = ref([]);
const orderToAdd = ref({});
const orderToEdit = ref({});

const customersById = computed(() => {
  return _.keyBy(customers.value, x => x.id);
});

async function fetchOrders() {
  const r = await axios.get("/api/orders/");
  orders.value = r.data;
}

async function fetchCustomers() {
  const r = await axios.get("/api/customers/");
  customers.value = r.data;
}

async function onOrderAdd() {
  await axios.post("/api/orders/", {
    ...orderToAdd.value,
  });
  await fetchOrders();
}

async function onRemoveClick(order) {
  await axios.delete(`/api/orders/${order.id}/`);
  await fetchOrders();
}

async function onOrderEditClick(order) {
  orderToEdit.value = { ...order };
}

async function onUpdateOrder() {
  await axios.put(`/api/orders/${orderToEdit.value.id}/`, {
    ...orderToEdit.value,
  });
  await fetchOrders();
}

onBeforeMount(async () => {
  await fetchOrders();
  await fetchCustomers();
});
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onOrderAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="orderToAdd.address" required />
              <label>Адрес доставки</label>
            </div>
          </div>
          <div class="col-auto">
            <div class="form-floating">
              <select class="form-select" v-model="orderToAdd.customer" required>
                <option :value="c.id" v-for="c in customers">
                  {{ c.first_name }} {{ c.last_name }}
                </option>
              </select>
              <label>Покупатель</label>
            </div>
          </div>
          <div class="col-auto">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>

      <div>
        <div v-for="item in orders" class="order-item">
          <div>Заказ #{{ item.id }} — {{ item.address }}</div>
          <div>
            {{ customersById[item.customer]?.first_name }}
            {{ customersById[item.customer]?.last_name }}
          </div>
          <button
            class="btn btn-success"
            @click="onOrderEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editOrderModal"
          >
            <i class="bi bi-pen-fill"></i>
          </button>
          <button class="btn btn-danger" @click="onRemoveClick(item)">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editOrderModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать заказ</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="row g-2">
              <div class="col-12">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="orderToEdit.address" />
                  <label>Адрес доставки</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <select class="form-select" v-model="orderToEdit.customer">
                    <option :value="c.id" v-for="c in customers">
                      {{ c.first_name }} {{ c.last_name }}
                    </option>
                  </select>
                  <label>Покупатель</label>
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
              @click="onUpdateOrder"
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
.order-item {
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