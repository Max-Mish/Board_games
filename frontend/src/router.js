import {createRouter, createWebHistory} from 'vue-router'
import Home from "./components/Home.vue";
import Registration from "./components/Registration.vue";
import Login from "./components/Login.vue";
import Games from "./components/Games.vue";
import Bookings from "./components/Bookings.vue";
import Game from "./components/Game.vue";
import Cart from "@/components/Cart.vue";
import Profile from "@/components/Profile.vue";
import Checkout from "@/components/Checkout.vue";


const routes = [
    {path: '/', component: Home, name: 'Home'},
    {path: '/login', component: Login, name: 'Login'},
    {path: '/registration', component: Registration, name: 'Registration'},
    {path: '/profile', component: Profile, name: 'Profile'},
    {path: '/games', component: Games, name: 'Games'},
    {path: '/game', component: Game, name: 'Game'},
    {path: '/bookings', component: Bookings, name: 'Bookings'},
    {path: '/cart', component: Cart, name: 'Cart'},
    {path: '/checkout', component: Checkout, name: 'Checkout'},

]

const router = createRouter({
    routes: routes,
    history: createWebHistory(),
})


export default router