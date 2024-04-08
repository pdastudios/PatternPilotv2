// src/main.js

import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // Adjust the path if your router.js is in a subdirectory

const app = createApp(App);
app.use(router);
app.mount('#app');
