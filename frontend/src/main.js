import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';


axios.defaults.baseURL = 'http://127.0.0.1:5000';  // Set global base URL


const app = createApp(App);

app.config.globalProperties.$axios = axios;  // Make axios available globally
app.use(router);
app.mount('#app');
