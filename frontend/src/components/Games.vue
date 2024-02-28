<template>
  <div>
    <navigation></navigation>
  </div>
  <section style="background-color: #eee;">
    <div class="container py-5">
      <p class="text-center h1 fw-bold mb-5 mx-1 mx-md-4 mt-4">Games</p>
      <div class="row justify-content-center mb-3">
        <div class="col-md-12 col-xl-10" v-for="(game, index) in gamesStore.games.items" :key="index">
          <div class="card shadow-0 border rounded-3">
            <div class="card-body">
              <div class="row">
                <div class="col-md-12 col-lg-3 col-xl-3 mb-4 mb-lg-0">
                  <div class="bg-image hover-zoom ripple rounded ripple-surface"
                       style="width: 200px; height: 200px; background-color: white; display: flex; justify-content: center; align-items: center;">
                    >
                    <img :src="game.cover_photo"
                         class="w-100" style="max-width: 100%; max-height: 100%; object-fit: contain;"/>
                    <a href="#!">
                      <div class="hover-overlay">
                        <div class="mask" style="background-color: rgba(253, 253, 253, 0.15);"></div>
                      </div>
                    </a>
                  </div>
                </div>
                <div class="col-md-6 col-lg-6 col-xl-6">
                  <h5>{{ game.name }}</h5>
                  <div class="d-flex flex-row">
                    <span>{{ game.publisher }}</span>
                  </div>
                  <div class="mb-2 text-muted small" style="margin-top: 10px; margin-bottom: 10px;">
                    <div v-for="(category, index) in game.category" :key="index">
                      <div style="display: flex; align-items: center;">
                        <span style="color: blueviolet;"> • </span>
                        <span>{{ category.name }}</span>
                        <span style="color: blueviolet;"> • </span>
                      </div>
                    </div>
                  </div>
                  <div class="mb-2 text-muted small" style="margin-top: 10px; margin-bottom: 10px;">
                    <span style="white-space: nowrap;">Number of players: </span>
                    <span style="color:blue">{{ game.description.n_players }}</span>
                    <span class="text-primary"> • </span>
                    <span style="white-space: nowrap;">Duration in minutes: </span>
                    <span style="color:blue">{{ game.description.duration }}</span>
                    <span class="text-primary"> • </span>
                    <span>Difficulty: </span>
                    <span style="color:blue">{{ difficulties[game.description.difficulty] }}</span>
                  </div>
                  <p class="text-truncate mb-4 mb-md-0">
                    {{ game.description.description_text }}
                  </p>
                </div>
                <div class="col-md-6 col-lg-3 col-xl-3 border-sm-start-none border-start">
                  <div class="d-flex flex-row align-items-center mb-1">
                    <h4 class="mb-1 me-1">${{ game.cost }}</h4>
                    <span class="text-muted small">per week</span>
                  </div>
                  <h6 :style="{ color: game.is_available ? 'green' : 'red' }">
                    {{ game.is_available ? 'Game Available' : 'Game Unavailable' }}</h6>
                  <div class="d-flex flex-column mt-4">
                    <button class="btn btn-primary btn-sm" type="button" @click="onGame(game.id)">Details</button>
                    <button class="btn btn-outline-primary btn-sm mt-2" type="button" v-if="game.is_available"
                            @click="onCart(game)">
                      Add to cart
                    </button>
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
import Navigation from "@/components/Navigation.vue";
import Alert from '@/components/Alert.vue';
import FooterSmall from "@/components/FooterSmall.vue";
import {useCartStore} from "@/stores/cart.js";
import {useGamesStore} from "@/stores/games.js";
import {baseApiUrl} from '@/services/baseApi';


export default {

  name: 'Games',
  data() {
    return {
      cartStore: '',
      gamesStore: '',
      difficulties: {1: 'Very Easy', 2: 'Easy', 3: 'Normal', 4: 'Hard', 5: 'Very Hard'}
    }
  },

  components: {
    footerSmall: FooterSmall,
    navigation: Navigation,
    alert: Alert,
  },
  methods: {
    getGames() {
      const path = `${baseApiUrl}/games/`;
      axios.get(path)
          .then((res) => {
            this.gamesStore.resetGames()
            this.gamesStore.gamesReceived(res.data)
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
    onCart(game) {
      this.cartStore.addItem(game)
    },
  },
  created() {
    this.gamesStore = useGamesStore(this.$pinia);
    this.cartStore = useCartStore(this.$pinia);
    this.getGames();
  },
}
</script>