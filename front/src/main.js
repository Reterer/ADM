import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import axios from 'axios'

import VNetworkGraph from "v-network-graph"

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'



const app = createApp(App)

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:5000/';  // the FastAPI backend

app.use(router)
app.use(VNetworkGraph)
app.use(ElementPlus)

app.mount('#app')
