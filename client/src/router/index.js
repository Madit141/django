import { createRouter, createWebHistory } from 'vue-router'
import ProductsView from '../views/ProductsView.vue';
import ProductTypesView from '../views/ProductTypesView.vue';
import CustomersView from '../views/CustomersView.vue';
import OrdersView from '../views/OrdersView.vue';
import OrderItemsView from '../views/OrderItemsView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "ProductsView",
      component: ProductsView,
    },
    {
      path: "/product-types",
      name: "ProductTypesView",
      component: ProductTypesView,
    },
    {
      path: "/customers",
      name: "CustomersView",
      component: CustomersView,
    },
    {
      path: "/orders",
      name: "OrdersView",
      component: OrdersView,
    },
    {
      path: "/order-items",
      name: "OrderItemsView",
      component: OrderItemsView,
    },
  ],
})

export default router