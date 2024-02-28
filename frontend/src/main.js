import 'bootstrap/dist/css/bootstrap.css';

import {createApp} from 'vue';
import {createPinia} from 'pinia';
import VueCookies from 'vue3-cookies';
import piniaPluginPersistedState from "pinia-plugin-persistedstate"

import App from '@/App.vue';
import router from '@/router.js';

const app = createApp(App);
const pinia = createPinia();
pinia.use(piniaPluginPersistedState)
app.use(router);
app.use(pinia);
app.use(VueCookies, {
    expireTimes: "7d",
    path: "/",
    domain: "",
    secure: true,
    sameSite: "None"
});
app.mount('#app');

import 'bootstrap/dist/js/bootstrap.js';