<template>
  <div>
    <navigation></navigation>
  </div>
  <section style="background-color: #eee;">
    <div class="container py-5">
      <p class="text-center h1 fw-bold mb-5 mx-1 mx-md-4 mt-4">My Bookings</p>
      <div class="row justify-content-center mb-3">
        <div v-if="!token">
          <p class="text-center h3 mt-5" style="color: blue;">Log in to see your bookings.</p>
        </div>
        <div class="col-md-12 col-xl-10" v-else v-for="(booking, index) in bookingsStore.bookings.items" :key="index">
          <div class="card shadow-0 border rounded-3">
            <div class="card-body">
              <div class="row">
                <div class="col-md-12 col-lg-3 col-xl-3 mb-4 mb-lg-0">
                  <div class="bg-image hover-zoom ripple rounded ripple-surface"
                       style="width: 200px; height: 200px; background-color: white; display: flex; justify-content: center; align-items: center;">
                    >
                    <img :src="booking.game.cover_photo"
                         class="w-100" style="max-width: 100%; max-height: 100%; object-fit: contain;"/>
                    <a href="#!">
                      <div class="hover-overlay">
                        <div class="mask" style="background-color: rgba(253, 253, 253, 0.15);"></div>
                      </div>
                    </a>
                  </div>
                </div>
                <div class="col-md-6 col-lg-6 col-xl-6">
                  <h5>{{ booking.game.name }}</h5>
                  <div class="d-flex flex-row">
                    <span>{{ booking.game.publisher }}</span>
                  </div>
                  <div class="mb-2 text-muted small" style="margin-top: 10px; margin-bottom: 10px;">
                    <div v-for="(category, index) in booking.game.category" :key="index">
                      <div style="display: flex; align-items: center;">
                        <span style="color: blueviolet;"> • </span>
                        <span>{{ category.name }}</span>
                        <span style="color: blueviolet;"> • </span>
                      </div>
                    </div>
                  </div>
                  <div class="mb-2 text-muted small" style="margin-top: 10px; margin-bottom: 10px;">
                    <span style="white-space: nowrap;">Number of players: </span>
                    <span style="color:blue">{{ booking.game.description.n_players }}</span>
                    <span class="text-primary"> • </span>
                    <span style="white-space: nowrap;">Duration in minutes: </span>
                    <span style="color:blue">{{ booking.game.description.duration }}</span>
                    <span class="text-primary"> • </span>
                    <span>Difficulty: </span>
                    <span style="color:blue">{{ difficulties[booking.game.description.difficulty] }}</span>
                  </div>
                  <p class="text-truncate mb-4 mb-md-0">
                    {{ booking.game.description.description_text }}
                  </p>
                </div>
                <div class="col-md-6 col-lg-3 col-xl-3 border-sm-start-none border-start">
                  <div class="d-flex flex-row align-items-center mb-1">
                    <h4 class="mb-1 me-1">${{ booking.game.cost }}</h4>
                    <span class="text-muted small">per week</span>
                  </div>
                  <h6>Opening date:
                    <span style="color: blue">{{ booking.opening_date }}</span></h6>
                  <h6>Return date:
                    <span style="color: blue">{{ booking.return_date }}</span></h6>
                  <h6>
                    <p v-if="booking.closing_date">Close date:
                      <span :style="{ color: booking.closing_date < booking.return_date ? 'green' : 'red' }"> {{ booking.closing_date }}</span>
                    </p>
                    <span style="color: red" v-else>Booking not closed yet</span>
                  </h6>
                        <h6>
                    <p v-if="booking.is_paid">
                      <span style="color: green;"> Booking is paid </span>
                    </p>
                    <span style="color: red" v-else>Booking is not paid</span>
                  </h6>
                  <div class="d-flex flex-column mt-4">
                    <button class="btn btn-primary btn-sm" type="button" @click="onGame(booking.game.id)">Details</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
  <div>
    <footerSmall></footerSmall>
  </div>
</template>

<script>
import axios from "axios";
import Alert from '@/components/Alert.vue';
import Navigation from "@/components/Navigation.vue";
import FooterSmall from "@/components/FooterSmall.vue";
import {baseApiUrl} from "@/services/baseApi.js";
import {useBookingsStore} from "@/stores/bookings.js";

export default {

  name: 'Bookings',
  data() {
    return {
      bookingsStore: '',
      token: '',
      difficulties: {1: 'Very Easy', 2: 'Easy', 3: 'Normal', 4: 'Hard', 5: 'Very Hard'}
    }
  },

  components: {
    alert: Alert,
    navigation: Navigation,
    footerSmall: FooterSmall,
  },
  methods: {
    getBookings() {
      const path = `${baseApiUrl}/user_actions/booking/`;
      this.token = this.$cookies.get('token');
      axios.get(path, {
        headers: {"Authorization": `Bearer ${this.token}`}
      })
          .then((res) => {
            this.bookingsStore.resetBookings()
            this.bookingsStore.bookingsReceived(res.data)
          })
          .catch((error) => {
            console.error(error);
          });
    },
    onGame(gameId) {
      this.$router.push({
        name: 'Game',
        query: {id: gameId}
      });
    },
  },
  created() {
    this.bookingsStore = useBookingsStore(this.$pinia);
    this.getBookings();
  },
}
</script>