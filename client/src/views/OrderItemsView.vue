<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from 'axios';
import _ from 'lodash';

const orderItems = ref([]);
const orders = ref([]);
const products = ref([]);
const itemToAdd = ref({});
const itemToEdit = ref({});

const ordersById = computed(() => {
  return _.keyBy(orders.value, x => x.id);
});

const productsById = computed(() => {
  return _.keyBy(products.value, x => x.id);
});

async function fetchOrderItems() {
  const r = await axios.get("/api/order-items/");
  orderItems.value = r.data;
}

async function fetchOrders() {
  const r = await axios.get("/api/orders/");
  orders.value = r.data;
}

async function fetchProducts() {
  const r = await axios.get("/api/products/");
  products.value = r.data;
}

async function onOrderItemAdd() {
  await axios.post("/api/order-items/", {
    ...itemToAdd.value,
  });
  await fetchOrderItems();
}

async function onRemoveClick(item) {
  await axios.delete(`/api/order-items/${item.id}/`);
  await fetchOrderItems();
}

async function onItemEditClick(item) {
  itemToEdit.value = { ...item };
}

async function onUpdateItem() {
  await axios.put(`/api/order-items/${itemToEdit.value.id}/`, {
    ...itemToEdit.value,
  });
  await fetchOrderItems();
}

onBeforeMount(async () => {
  await fetchOrderItems();
  await fetchOrders();
  await fetchProducts();
});
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onOrderItemAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <select class="form-select" v-model="itemToAdd.order" required>
                <option :value="o.id" v-for="o in orders">
                  Заказ #{{ o.id }} ({{ o.address }})
                </option>
              </select>
              <label>Заказ</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <select class="form-select" v-model="itemToAdd.product" required>
                <option :value="p.id" v-for="p in products">
                  {{ p.name }}
                </option>
              </select>
              <label>Товар</label>
            </div>
          </div>
          <div class="col-auto">
            <div class="form-floating">
              <input type="number" class="form-control" v-model="itemToAdd.count" required />
              <label>Количество</label>
            </div>
          </div>
          <div class="col-auto">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>

      <div>
        <div v-for="item in orderItems" class="order-pos-item">
          <div>{{ productsById[item.product]?.name }}</div>
          <div>Кол-во: {{ item.count }}</div>
          <div>Заказ #{{ item.order }} ({{ ordersById[item.order]?.address }})</div>
          <button
            class="btn btn-success"
            @click="onItemEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editOrderItemModal"
          >
            <i class="bi bi-pen-fill"></i>
          </button>
          <button class="btn btn-danger" @click="onRemoveClick(item)">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editOrderItemModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать позицию заказа</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="row g-2">
              <div class="col-12">
                <div class="form-floating">
                  <select class="form-select" v-model="itemToEdit.order">
                    <option :value="o.id" v-for="o in orders">
                      Заказ #{{ o.id }} ({{ o.address }})
                    </option>
                  </select>
                  <label>Заказ</label>
                </div>
              </div>
              <div class="col-6">
                <div class="form-floating">
                  <select class="form-select" v-model="itemToEdit.product">
                    <option :value="p.id" v-for="p in products">
                      {{ p.name }}
                    </option>
                  </select>
                  <label>Товар</label>
                </div>
              </div>
              <div class="col-6">
                <div class="form-floating">
                  <input type="number" class="form-control" v-model="itemToEdit.count" />
                  <label>Количество</label>
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
              @click="onUpdateItem"
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
.order-pos-item {
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