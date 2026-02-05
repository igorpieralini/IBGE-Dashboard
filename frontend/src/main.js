import { createApp } from 'vue'
import { Chart, registerables } from 'chart.js'
import App from './App.vue'
import router from './router'
import './style.css'

Chart.register(...registerables)

createApp(App).use(router).mount('#app')
