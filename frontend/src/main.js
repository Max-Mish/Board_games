import 'bootstrap/dist/css/bootstrap.css';

import {createApp} from 'vue';
import VueCookies from 'vue3-cookies'

import App from './App.vue';
import router from "@/router.js";

const app = createApp(App);
app.use(router);
app.use(VueCookies, {
    expireTimes: "7d",
    path: "/",
    domain: "",
    secure: true,
    sameSite: "None"
});
app.mount('#app');

import 'bootstrap/dist/js/bootstrap.js';