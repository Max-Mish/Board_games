<template>
  <!-- Navbar -->
  <nav class="navbar navbar-expand-lg fixed-top bg-light navbar-light">
    <div class="container">
      <a class="navbar-brand" href="#"
      ><img
          id="Board-Games-logo"
          src="https://images.twinkl.co.uk/tw1n/image/private/t_630/u/builder/board-games-logo-colour-cmyk-1687979724.png"
          alt="Board Games Logo"
          draggable="false"
          height="70"
      /></a>
      <button
          class="navbar-toggler"
          type="button"
          data-mdb-toggle="collapse"
          data-mdb-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
      >
        <i class="fas fa-bars"></i>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav ms-auto align-items-center">
          <li class="nav-item">
            <a class="nav-link mx-2" href="" @click="onHome"><i class="fa-solid fa-house pe-2"></i>Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link mx-2" href="" @click="onGames"><i class="fa-solid fa-chess-board pe-2"></i>Games</a>
          </li>
          <li class="nav-item">
            <a class="nav-link mx-2" href="" @click="onBookings"><i class="fas fa-heart pe-2"></i>My Bookings</a>
          </li>
          <li class="nav-item ms-3" v-if="showSignIn">
            <a class="btn btn-black btn-rounded" href="" @click="onLogin">Sign in</a>
          </li>
          <li class="nav-item d-flex align-items-center dropdown" v-else>
            <form class="d-flex me-auto">
              <button class="btn btn-outline-dark" type="submit" @click="onCart">
                <i class="bi-cart-fill me-1 fa-solid fa-cart-shopping pe-1"></i>
                Cart
                <span class="badge bg-dark text-white ms-1 rounded-pill">0</span>
              </button>
            </form>
            <a
                class="nav-link dropdown-toggle d-flex align-items-center hidden-arrow"
                href="#"
                id="navbarDropdownMenuLink"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
            >
              <img
                  :src="cover_photo ? cover_photo : 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQHUyeHkZzAKI4scD3H59lC92acZj35vp_cFC-jq1Vp4Q&s'"
                  class="rounded-circle"
                  height="30"
                  alt=""
                  loading="lazy"
              />
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
              <li ><a class="dropdown-item" href="#" @click="onProfile">My profile</a></li>
              <li><a class="dropdown-item" href="#" @click="onSettings">Settings</a></li>
              <li><a class="dropdown-item" href="#" @click="onLogout">Logout</a></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <!-- Navbar -->
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {

  name: 'Navigation',
  data() {
    return {
      showMessage: false,
      logged: false,
      token: '',
      username: '',
      email: '',
      cover_photo: '',
      message: '',
      status: '',
    }
  },

  components: {
    alert: Alert,
  },
  created() {
    const path = 'http://localhost:8000/api/profile/';
    this.token = this.$cookies.get('token');
    axios.get(path, {
      headers: {"Authorization": `Bearer ${this.token}`}
    }).then((res) => {
      this.logged = true;
      this.username = res.data.username
      this.email = res.data.email
      this.cover_photo = res.data.cover_photo
    }).catch((error) => {
      this.logged = false;
    });
  },
  computed: {
    showSignIn() {
      this.token = this.$cookies.get('token');
      this.logged = !!this.token;
      console.log(this.token);
      return !this.logged;
    }
  },
  methods: {
    onLogin() {
      this.$router.push({name: 'Login'});
    },
    onLogout() {
      this.$cookies.set('token', '');
      this.$router.push({name: 'Login'});
    },
    onHome() {
      this.$router.push({name: 'Home'});
    },
    onGames() {
      this.$router.push({name: 'Games'});
    },
    onBookings() {
      this.$router.push({name: 'Bookings'});
    },
    onProfile() {
      this.$router.push({name: 'Profile'});
    },
    onSettings() {
      this.$router.push({name: 'Settings'});
    },
    onCart() {
      this.$router.push({name: 'Cart'})
    },
  },
}
</script>