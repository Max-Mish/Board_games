<template>
  <div style="margin-bottom: 8%; background-color: #eee;">
    <Navigation></Navigation>
  </div>
  <section class="vh-100">
    <div class="container h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-lg-12 col-xl-11">
          <div class="card text-black" style="border-radius: 50px;">
            <div class="card-body p-md-5">
              <div class="row justify-content-center">
                <div class="col-md-10 col-lg-6 col-xl-5 order-2 order-lg-1">

                  <p class="text-center h1 fw-bold mb-5 mx-1 mx-md-4 mt-4">Sign up</p>

                  <form class="mx-1 mx-md-4">

                    <div class="d-flex flex-row align-items-center mb-4">
                      <i class="fas fa-user fa-lg me-3 fa-fw"></i>
                      <div class="form-outline flex-fill mb-0">
                        <input type="text" id="form3Example1c" class="form-control" v-model="inputForm.username"/>
                        <label class="form-label" for="form3Example1c">Your Username</label>
                      </div>
                    </div>

                    <div class="d-flex flex-row align-items-center mb-4">
                      <i class="fas fa-envelope fa-lg me-3 fa-fw"></i>
                      <div class="form-outline flex-fill mb-0">
                        <input type="email" id="form3Example3c" class="form-control" v-model="inputForm.email"/>
                        <label class="form-label" for="form3Example3c">Your Email</label>
                      </div>
                    </div>

                    <div class="d-flex flex-row align-items-center mb-4">
                      <i class="fas fa-lock fa-lg me-3 fa-fw"></i>
                      <div class="form-outline flex-fill mb-0">
                        <input type="password" id="form3Example4c" class="form-control" v-model="inputForm.password"/>
                        <label class="form-label" for="form3Example4c">Password</label>
                      </div>
                    </div>

                    <div class="d-flex flex-row align-items-center mb-4">
                      <i class="fas fa-key fa-lg me-3 fa-fw"></i>
                      <div class="form-outline flex-fill mb-0">
                        <input type="password" id="form3Example4cd" class="form-control"
                               v-model="inputForm.repeatPassword"/>
                        <label class="form-label" for="form3Example4cd">Repeat your password</label>
                      </div>
                      <span v-if="showPasswordMismatchMessage">Passwords do not match.</span>
                    </div>

                    <div class="form-check d-flex justify-content-center mb-5">
                      <input class="form-check-input me-2" type="checkbox" value="" id="form2Example3c"
                             v-model="checkboxChecked"/>
                      <label class="form-check-label" for="form2Example3">
                        I agree all statements in <a href="https://policies.google.com/terms?hl=en-US">Terms of
                        service</a>
                      </label>
                      <span v-if="showCheckboxMessage">Please check this box to proceed.</span>
                    </div>
                    <alert :message=message v-if="showMessage"></alert>
                    <div class="d-flex justify-content-center mx-4 mb-3 mb-lg-4">
                      <button type="button" class="btn btn-primary btn-lg" @click="register">Register</button>
                    </div>
                  </form>
                </div>
                <div class="col-md-10 col-lg-6 col-xl-7 d-flex align-items-center order-1 order-lg-2">

                  <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-registration/draw1.webp"
                       class="img-fluid" alt="Sample image">

                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
  <div style="margin-top: 15%;">
    <FooterSmall></FooterSmall>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';
import Navigation from "@/components/Navigation.vue";
import FooterSmall from "@/components/FooterSmall.vue";

export default {
  name: 'Registration',
  data() {
    return {
      showMessage: false,
      checkboxChecked: false,
      showCheckboxMessage: false,
      showPasswordMismatchMessage: false,
      message: '',
      status: '',
      inputForm: {
        username: "",
        email: "",
        password: "",
        repeatPassword: "",
      }
    }
  },

  components: {
    FooterSmall: FooterSmall,
    Navigation: Navigation,
    alert: Alert,
  },
  methods: {
    register() {
      if (this.inputForm.username && this.inputForm.email && this.inputForm.password && this.inputForm.repeatPassword) {
        const payload = {
          username: this.inputForm.username,
          email: this.inputForm.email,
          password: this.inputForm.password,
          password_repeat: this.inputForm.repeatPassword,
        };
        this.checkRegistration(payload);
      }
    },
    checkRegistration(payload) {
      const path = 'http://localhost:8000/api/register/';
      const cb = document.querySelector('#form2Example3c');
      if (this.inputForm.password === this.inputForm.repeatPassword) {
        this.showPasswordMismatchMessage = false;
        if (cb.checked) {
          this.showCheckboxMessage = false;
          axios.post(path, payload)
              .then((res) => {
                if (res.data.status === false) {
                  this.message = res.data.message;
                  this.showMessage = true;
                  this.status = false;
                  this.$router.push({name: 'Register'})
                } else {
                  this.status = true;
                  const payload = {
                    email: this.inputForm.email,
                    password: this.inputForm.password,
                  };
                  const path = 'http://localhost:8000/api/token/';
                  axios.post(path, payload)
                      .then((res) => {
                        this.$cookies.set('token', res.data.access)
                        this.$router.push({name: 'Home'});
                      })
                }
              })
              .catch((error) => {
                console.log(error);
                this.message = 'Registration error: Username or email may be in use.';
                this.showMessage = true;
              });
        } else {
          this.showCheckboxMessage = true;
        }
      } else {
        this.showPasswordMismatchMessage = true;
      }
    },
  }
}
</script>