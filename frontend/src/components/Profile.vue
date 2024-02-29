<template>
  <div>
    <navigation></navigation>
  </div>
  <section style="background-color: #eee;">
    <div class="container py-5">
      <div class="row">
        <div class="col-lg-4">
          <div class="card mb-4">
            <div class="card-body text-center">
              <img
                  :src="profileStore.cover_photo ? profileStore.cover_photo : 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQHUyeHkZzAKI4scD3H59lC92acZj35vp_cFC-jq1Vp4Q&s'"
                  alt="avatar"
                  class="rounded-circle img-fluid" style="width: 150px;">
              <h5 class="my-3">{{ profileStore.username }}</h5>
              <p class="text-muted mb-1"></p>
              <p class="text-muted mb-4"></p>
              <div class="d-flex justify-content-center mb-2">
                <button type="button" class="btn btn-primary">Change photo</button>
                <button type="button" class="btn btn-outline-primary ms-1">Delete Profile</button>
              </div>
            </div>
          </div>
<!--          <div class="card mb-4 mb-lg-0">-->
<!--            <div class="card-body p-0">-->
<!--              <ul class="list-group list-group-flush rounded-3">-->
<!--                <li class="list-group-item d-flex justify-content-between align-items-center p-3">-->
<!--                  <i class="fas fa-globe fa-lg text-warning"></i>-->
<!--                  <p class="mb-0">https://mdbootstrap.com</p>-->
<!--                </li>-->
<!--                <li class="list-group-item d-flex justify-content-between align-items-center p-3">-->
<!--                  <i class="fab fa-github fa-lg" style="color: #333333;"></i>-->
<!--                  <p class="mb-0">mdbootstrap</p>-->
<!--                </li>-->
<!--                <li class="list-group-item d-flex justify-content-between align-items-center p-3">-->
<!--                  <i class="fab fa-twitter fa-lg" style="color: #55acee;"></i>-->
<!--                  <p class="mb-0">@mdbootstrap</p>-->
<!--                </li>-->
<!--                <li class="list-group-item d-flex justify-content-between align-items-center p-3">-->
<!--                  <i class="fab fa-instagram fa-lg" style="color: #ac2bac;"></i>-->
<!--                  <p class="mb-0">mdbootstrap</p>-->
<!--                </li>-->
<!--                <li class="list-group-item d-flex justify-content-between align-items-center p-3">-->
<!--                  <i class="fab fa-facebook-f fa-lg" style="color: #3b5998;"></i>-->
<!--                  <p class="mb-0">mdbootstrap</p>-->
<!--                </li>-->
<!--              </ul>-->
<!--            </div>-->
<!--          </div>-->
        </div>
        <div class="col-lg-8">
          <div class="card mb-4">
            <div class="card-body">
              <div class="row">
                <div class="col-sm-3">
                  <p class="mb-0">Username</p>
                </div>
                <div class="col-sm-9">
                  <p class="text-muted mb-0">{{ profileStore.username }}</p>
                </div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-3">
                  <p class="mb-0">Email</p>
                </div>
                <div class="col-sm-9">
                  <p class="text-muted mb-0">{{ profileStore.email }}</p>
                </div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-3">
                  <p class="mb-0">Address</p>
                </div>
                <div class="col-sm-9">
                  <p class="text-muted mb-3">Bay Area, San Francisco, CA</p>
                </div>
              </div>
            </div>
            <div class="d-flex justify-content-center mb-3">
              <button type="button" class="btn btn-primary">Change profile info</button>
              <button type="button" class="btn btn-outline-primary ms-1">Change password</button>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6">
              <div class="card mb-4 mb-md-0">
                <div class="card-body">
                  <p class="mb-4"><span class="text-primary font-italic me-1">Account</span>
                  </p>
                  <p class="mb-1" style="font-size: .77rem;">Balance</p>
                  <div class="row">
                    <div class="col-sm-3">
                      <p class="mb-0">Amount</p>
                    </div>
                    <div class="col-sm-9">
                      <p class="text-muted mb-3">{{balanceInfo.balance}}</p>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-sm-3">
                      <p class="mb-0">Currency</p>
                    </div>
                    <div class="col-sm-9">
                      <p class="text-muted mb-3">{{balanceInfo.balance_currency}}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card mb-4 mb-md-0">
                <div class="card-body">
                  <p class="mb-4"><span class="text-primary font-italic me-1">Balance Changes</span>
                  </p>
                  <p class="mb-1" style="font-size: .77rem;">Balance</p>
                  <div class="row">
                    <div class="col-sm-3">
                      <p class="mb-0">Amount</p>
                    </div>
                    <div class="col-sm-9">
                      <p class="text-muted mb-3">{{balanceInfo.balance}}</p>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-sm-3">
                      <p class="mb-0">Currency</p>
                    </div>
                    <div class="col-sm-9">
                      <p class="text-muted mb-3">{{balanceInfo.balance_currency}}</p>
                    </div>
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
import Alert from '@/components/Alert.vue';
import Navigation from "@/components/Navigation.vue";
import FooterSmall from "@/components/FooterSmall.vue";
import {useProfileStore} from "@/stores/profile.js";
import {baseApiUrl} from "@/services/baseApi.js";
import axios from "axios";

export default {

  name: 'Profile',
  data() {
    return {
      profileStore: '',
      balanceInfo: [],
    }
  },

  components: {
    footerSmall: FooterSmall,
    navigation: Navigation,
    alert: Alert,
  },
  methods: {
    getBalance() {
      const path = `${baseApiUrl}/payment_accounts/balance/`;
      axios.get(path, {
        headers: {"Authorization": `Bearer ${this.$cookies.get('token')}`}
      }).then((res) => {
        this.balanceInfo = res.data
      }).catch((error) => {
        console.error(error);
      });
    },
  },
  created() {
    this.profileStore = useProfileStore(this.$pinia);
    this.getBalance();
  },
}
</script>