<template>
  <div>
    <navigation></navigation>
  </div>
  <section class="vh-100">
    <div class="container h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-md-9 col-lg-7 col-xl-6">
          <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/draw2.webp"
               class="img-fluid" alt="Sample image">
        </div>
        <div class="col-md-8 col-lg-6 col-xl-4 offset-xl-1">
          <form>
            <p class="text-center h1 fw-bold mb-5 mx-1 mx-md-4 mt-4">Sign up</p>
            <!-- Email input -->
            <div class="form-outline mb-4">
              <input type="email" id="form3Example3" class="form-control form-control-lg"
                     placeholder="Enter a valid email address" v-model="inputForm.email"/>
              <label class="form-label" for="form3Example3">Email address</label>
            </div>

            <!-- Password input -->
            <div class="form-outline mb-3">
              <input type="password" id="form3Example4" class="form-control form-control-lg"
                     placeholder="Enter password" v-model="inputForm.password"/>
              <label class="form-label" for="form3Example4">Password</label>
              <alert :message=message v-if="showMessage"></alert>
            </div>

            <div class="text-center text-lg-start mt-4 pt-2">
              <button type="button" class="btn btn-primary btn-lg"
                      style="padding-left: 2.5rem; padding-right: 2.5rem;" @click="onLogin">Login
              </button>
              <p class="small fw-bold mt-2 pt-1 mb-0">Don't have an account? <a href=""
                                                                                class="link-primary"
                                                                                @click="onRegister">Register</a></p>
            </div>

          </form>
        </div>
      </div>
    </div>
  </section>
  <div>
    <footerSmall></footerSmall>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from '@/components/Alert.vue';
import Navigation from "@/components/Navigation.vue";
import FooterSmall from "@/components/FooterSmall.vue";
import {baseApiUrl} from "@/services/baseApi.js";
import {useProfileStore} from "@/stores/profile.js";

export default {
  name: 'Login',
  data() {
    return {
      profileStore: '',
      showMessage: false,
      message: '',
      status: '',
      inputForm: {
        email: "",
        password: ""
      }
    }
  },

  components: {
    footerSmall: FooterSmall,
    navigation: Navigation,
    alert: Alert,
  },

  methods: {
    onLogin() {
      if (this.inputForm.email && this.inputForm.password) {
        const payload = {
          email: this.inputForm.email,
          password: this.inputForm.password,
        };
        this.checkLogin(payload);
      }
    },
    checkLogin(payload) {
      const path = `${baseApiUrl}/api/token/`;
      axios.post(path, payload)
          .then((res) => {
            if (res.data.status === false) {
              this.message = res.data.message;
              this.showMessage = true;
              this.status = false;
              this.$router.push({name: 'Login'})
            } else {
              this.status = true;
              this.$cookies.set('token', res.data.access)
              this.getProfile()
              this.$router.push({name: 'Home'})
            }
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.log(error);
            this.message = 'Login error: Please check your email and password.';
            this.showMessage = true;
          });
    },
    getProfile() {
      const path = `${baseApiUrl}/api/profile/`;
      axios.get(path, {
        headers: {"Authorization": `Bearer ${this.$cookies.get('token')}`}
      }).then((res) => {
        this.profileStore.addInfo(res.data)
      }).catch((error) => {
        console.error(error);
      });
    },
    onRegister() {
      this.$router.push({name: 'Registration'});
    },
  },
  created() {
    this.profileStore = useProfileStore(this.$pinia);
  },
}
</script>