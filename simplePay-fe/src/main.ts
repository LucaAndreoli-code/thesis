import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import './service/interceptor'

document.documentElement.setAttribute('data-theme', 'light')

const app = createApp(App)
app.use(router)
app.mount('#app')
