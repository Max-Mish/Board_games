<template>
  <router-view :key="$route.fullPath" />
  <div>
    <Navigation></Navigation>
  </div>
  <!-- Product section-->
  <section class="py-5">
    <div class="container px-4 px-lg-5 my-5">
      <div class="row gx-4 gx-lg-5 align-items-center">
        <div class="col-md-6"><img class="card-img-top mb-5 mb-md-0 rounded-5 border border-4 border-grey p-4"
                                   :src="game.cover_photo"
                                   alt="Game Cover"/></div>
        <div class="col-md-6">
          <div class="small mb-1">ID: {{ game.id }}</div>
          <h1 class="display-5 fw-bolder">{{ game.name }}</h1>
          <div class="fs-5 mb-5">
            <span style="color: blue">${{ game.cost }}</span>
            <span class="text-muted small"> per week</span>
          </div>
          <p class="lead">{{ game.description.description_text }}</p>

          <div class="row">
            <div class="col-md-6">
              <div class="mb-2 text-muted small" style="margin-top: 10px; margin-bottom: 10px;">
                <p class="lead">Categories:</p>
                <div v-for="(category, index) in game.category" :key="index">
                  <div style="display: flex; align-items: center;">
                    <span style="color: blueviolet;"> • </span>
                    <span>{{ category.name }}</span>
                    <span style="color: blueviolet;"> • </span>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="mb-2 text-muted small" style="margin-top: 10px; margin-bottom: 10px;">
                <p class="lead">Description:</p>
                <div class="mb-2">
                  <span style="white-space: nowrap;">Number of players: </span>
                  <span style="color:blue">{{ game.description.n_players }}</span>
                </div>
                <div class="mb-2">
                  <span style="white-space: nowrap;">Duration in minutes: </span>
                  <span style="color:blue">{{ game.description.duration }}</span>
                </div>
                <div class="mb-2">
                  <span style="white-space: nowrap;">Difficulty: </span>
                  <span style="color:blue">{{ difficulties[game.description.difficulty] }}</span>
                </div>
              </div>
            </div>
          </div>

          <div v-if="game.is_available">
            <div class="d-flex align-items-center mb-3">
              <span class="display-7 fw-bolder" style="color: green">Game Available</span>
            </div>
            <div class="d-flex align-items-center">
              <button class="btn btn-outline-dark flex-shrink-0" type="button">
                <i class="bi-cart-fill me-1"></i>
                Add to cart
              </button>
            </div>
          </div>
          <div class="d-flex align-items-center mb-3" v-else>
            <span class="display-7 fw-bolder" style="color: red">Game Unavailable</span>
          </div>
        </div>
      </div>
    </div>
  </section>
  <!-- Related items section-->
  <section class="py-5 bg-light">
    <div class="container px-4 px-lg-5 mt-5">
      <h2 class="fw-bolder mb-4">Related products</h2>
      <div class="row gx-4 gx-lg-5 row-cols-2 row-cols-md-3 row-cols-xl-4 justify-content-center">
        <div class="col mb-5" v-for="(game, index) in relatedGames" :key="index">
          <div class="card h-100" >
            <!-- Product image-->
            <img class="card-img-top" :src="game.cover_photo" alt="Related Game Cover"
                 style="width: 230px; height: 230px; background-color: white; display: flex; justify-content: center; align-items: center; max-width: 100%; max-height: 100%; object-fit: contain;"/>
            <!-- Product details-->
            <div class="card-body p-4">
              <div class="text-center">
                <!-- Product name-->
                <h5 class="fw-bolder">{{ game.name }}</h5>
                <!-- Product price-->
                ${{ game.cost }}
              </div>
            </div>
            <!-- Product actions-->
            <div class="card-footer p-4 pt-0 border-top-0 bg-transparent text-center">
              <button class="btn btn-primary btn-sm align-items-center justify-content-center" type="button" @click="onGame(game.id)">Details</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
  <!-- Footer-->
  <div>
    <FooterSmall></FooterSmall>
  </div>
</template>

<script>
import Navigation from "./Navigation.vue";
import Alert from './Alert.vue';
import axios from "axios";
import FooterSmall from "@/components/FooterSmall.vue";

export default {

  name: 'Game',
  data() {
    return {
      gameId: '',
      game: '',
      relatedGames: [],
      difficulties: {1: 'Very Easy', 2: 'Easy', 3: 'Normal', 4: 'Hard', 5: 'Very Hard'}
    }
  },

  components: {
    FooterSmall: FooterSmall,
    Navigation: Navigation,
    alert: Alert,
  },
  created() {
    this.gameId = this.$route.query.id;
    this.getGame();
    this.getRelatedGames();
  },
  methods: {
    getGame() {
      const path = `http://localhost:8000/games/game?id=${this.gameId}`;
      axios.get(path)
          .then((res) => {
            this.game = res.data;
          })
          .catch((error) => {
            console.error(error);
          });
    },
    getRelatedGames() {
      const path = `http://localhost:8000/games/related?id=${this.gameId}`;
      axios.get(path)
          .then((res) => {
            this.relatedGames = res.data;
          })
          .catch((error) => {
            console.error(error);
          });
    },
    onGame(gameId) {
      this.$router.push({
        name: 'Game',
        query: {id: gameId},
      });
    },
  },
}
</script>