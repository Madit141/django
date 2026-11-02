import { createApp } from 'vue'
import { createPinia } from 'pinia'

import "bootstrap/dist/css/bootstrap.css"
import "bootstrap-icons/font/bootstrap-icons.css"
import "bootstrap/dist/js/bootstrap.js"

import axios from 'axios'
import Cookies from 'js-cookie'

import App from './App.vue'
import router from './router'

axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken')

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')