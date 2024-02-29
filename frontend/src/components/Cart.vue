<template>
  <div>
    <navigation></navigation>
  </div>
  <section class="h-100 h-custom" style="background-color: #eee;">
    <div class="container py-5 h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col">
          <div class="card">
            <div class="card-body p-4">

              <div class="row">

                <div class="col-lg-7">
                  <h5 class="mb-3"><a href="" class="text-body" @click="onBack"><i
                      class="fas fa-long-arrow-alt-left me-2"></i>Continue shopping</a></h5>
                  <hr>

                  <div class="d-flex justify-content-between align-items-center mb-4">
                    <div>
                      <p class="mb-1">Shopping cart</p>
                      <p class="mb-0">You have {{ cartStore.totalItems }} items in your cart</p>
                    </div>
                  </div>

                  <div class="card mb-3" v-for="item of cartStore.items">
                    <div class="card-body">
                      <div class="d-flex justify-content-between">
                        <div class="d-flex flex-row align-items-center">
                          <div>
                            <img
                                :src="item.cover_photo"
                                class="img-fluid rounded-3" alt="Shopping item" style="width: 65px;">
                          </div>
                          <div class="ms-3">
                            <h5>{{ item.name }}</h5>
                            <p class="small mb-0">{{ item.publisher }}</p>
                          </div>
                        </div>
                        <div class="d-flex flex-row align-items-center">
                          <div style="width: 50px;">
                            <h5 class="fw-normal mb-0">{{ item.count }}</h5>
                          </div>
                          <div style="width: 80px;">
                            <h5 class="mb-0">{{ item.cost }}$</h5>
                          </div>
                          <datePicker
                              :model-value="itemsInfo[item.id][1]"
                              @update:model-value="(modelData) => handleDate(modelData, item.count, item.id)"
                              required
                              disable-year-select
                              prevent-min-max-navigation
                              ignore-time-validation
                              :range="{ minRange:3, maxRange:14, noDisabledRange: true}"
                              :min-date="new Date()"
                              :max-date="new Date(new Date().setDate(new Date().getDate() + 60))"
                              :state="datesState[item.id]"
                              :clearable="false"
                              :enable-time-picker="false"

                          ></datePicker>
                          <alert :message=dateInputMessage[item.id] v-if="showDateInputMessage[item.id]"></alert>
                          <a class="btn btn-black btn-rounded" href="" style="color: #cecece;"
                             @click="onRemove(item)"><i class="fas fa-trash-alt"></i></a>
                        </div>
                      </div>
                    </div>
                  </div>
                  <alert message='Please select valid dates for bookings.'
                         v-if="showDateErrorMessage"></alert>
                </div>
                <div class="col-lg-5">

                  <div class="card bg-primary text-white rounded-3">
                    <div class="card-body">
                      <div class="d-flex justify-content-between align-items-center mb-4">
                        <h5 class="mb-0">Delivery details</h5>
                        <img :src="profileStore.cover_photo"
                             class="img-fluid rounded-3" style="width: 45px;" alt="Avatar">
                      </div>

                      <p class="small mb-2">Delivery service</p>
                      <a href="" type="submit" class="text-white" @click="cartStore.chooseShipping('DHL')"><i
                          class="fab fa-dhl fa-3x me-3"
                          :class="{ 'text-dark': cartStore.shippingService === 'DHL' }"></i></a>
                      <a href="" type="submit" class="text-white" @click="cartStore.chooseShipping('UPS')"><i
                          class="fab fa-ups fa-2x me-3"
                          :class="{ 'text-dark': cartStore.shippingService === 'UPS' }"></i></a>
                      <a href="" type="submit" class="text-white" @click="cartStore.chooseShipping('FedEx')"><i
                          class="fab fa-fedex fa-2x me-3"
                          :class="{ 'text-dark': cartStore.shippingService === 'FedEx' }"></i></a>
                      <a href="" type="submit" class="text-white" @click="cartStore.chooseShipping('Yandex')"><i
                          class="fab fa-yandex fa-2x text-light"
                          :class="{ 'text-dark': cartStore.shippingService === 'Yandex' }"></i></a>

                      <form class="mt-4">
                        <div class="form-outline form-white mb-4">
                          <input type="text" id="typeName" class="form-control form-control-lg" siez="17"
                                 placeholder="55 Glenlake Parkway NE" v-model="inputForm.streetHouseApp"/>
                          <label class="form-label" for="typeName">Street, house, apartment</label>
                        </div>

                        <div class="form-outline form-white mb-4">
                          <input type="text" id="typeTextStateCity" class="form-control form-control-lg" siez="17"
                                 placeholder="Georgia, Atlanta" minlength="19" maxlength="19"
                                 v-model="inputForm.stateCity"/>
                          <label class=" form-label" for="typeTextStateCity">State and City</label>
                        </div>

                        <div class="row mb-4">
                          <div class="col-md-6">
                            <div class="form-outline form-white">
                              <input type="text" id="typeExp" class="form-control form-control-lg"
                                     placeholder="USA" size="7" minlength="7" maxlength="7"
                                     v-model="inputForm.country"/>
                              <label class="form-label" for="typeExp">Country</label>
                            </div>
                          </div>
                          <div class="col-md-6">
                            <div class="form-outline form-white">
                              <input type="password" id="typeTextIndex" class="form-control form-control-lg"
                                     placeholder="&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;" size="1" minlength="4"
                                     maxlength="6"
                                     v-model="inputForm.index"/>
                              <label class="form-label" for="typeTextIndex">Index</label>
                            </div>
                          </div>
                        </div>

                      </form>

                      <hr class="my-4">

                      <div class="d-flex justify-content-between">
                        <p class="mb-2">Subtotal</p>
                        <p class="mb-2">${{ cartStore.subtotalCost }}</p>
                      </div>

                      <div class="d-flex justify-content-between">
                        <p class="mb-2">Shipping</p>
                        <p class="mb-2">${{ cartStore.shippingCost }}</p>
                      </div>

                      <div class="d-flex justify-content-between mb-4">
                        <p class="mb-2">Total</p>
                        <p class="mb-2">${{ cartStore.totalCost }}</p>
                      </div>

                      <alert message='Please ensure all required fields are filled in before proceeding.'
                             v-if="showInputMessage"></alert>
                      <span v-if="!cartStore.shippingService">Please select a delivery service.</span>
                      <button type="button" class="btn btn-info btn-block btn-lg" v-else @click="onCheckout">
                        <div class="d-flex justify-content-between">
                          <span>${{ cartStore.totalCost }} Checkout</span>
                          <span> <i class="fas fa-long-arrow-alt-right ms-2"></i></span>
                        </div>
                      </button>

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
import Alert from "@/components/Alert.vue";
import Navigation from "@/components/Navigation.vue";
import FooterSmall from "@/components/FooterSmall.vue";
import {useCartStore} from "@/stores/cart.js"
import {useProfileStore} from "@/stores/profile.js";
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import {baseApiUrl} from "@/services/baseApi.js";
import axios from "axios";

export default {

  name: 'Cart',
  data() {
    return {
      cartStore: '',
      profileStore: '',
      showInputMessage: false,
      itemsInfo: {},
      datesState: {},
      dateInputMessage: {},
      showDateInputMessage: {},
      showDateErrorMessage: false,
      inputForm: {
        streetHouseApp: "",
        stateCity: "",
        country: "",
        index: "",
      }
    }
  },

  components: {
    alert: Alert,
    navigation: Navigation,
    footerSmall: FooterSmall,
    datePicker: VueDatePicker,
  },
  methods: {
    onBack() {
      this.$router.back()
    },
    onRemove(item) {
      this.cartStore.removeItem(item)
    },
    onCheckout() {
      const deliveryData = this.getDeliveryData();
      const payload = this.makeBookingsPayload();
      if (deliveryData && payload) {
        this.makeBookings(payload)
        // прокидываем дальше delivery_data
        // this.$router.push({name: 'Checkout'});
      }
    },
    getDeliveryData() {
      this.showInputMessage = false;
      if (this.inputForm.streetHouseApp && this.inputForm.stateCity && this.inputForm.country && this.inputForm.index) {
        return {
          streetHouseApp: this.inputForm.streetHouseApp,
          stateCity: this.inputForm.stateCity,
          country: this.inputForm.country,
          index: this.inputForm.index,
        };
      } else {
        this.showInputMessage = true;
      }
    },
    handleDate(modelData, count, id) {
      this.showDateErrorMessage = false;
      this.itemsInfo[id] = [count, modelData];
      const payload = {
        game_id: id,
        amount: count,
        booked_dates: modelData.map(date => date.toUTCString())
      };
      console.log(payload)
      const path = `${baseApiUrl}/games/items/check_dates`;
      axios.post(path, payload)
          .then((res) => {
            if (res.data.dates_check_status === false) {
              this.datesState[id] = false;
              this.dateInputMessage[id] = res.data.message;
              this.showDateInputMessage[id] = true;
            } else {
              this.datesState[id] = true;
              this.itemsInfo[id][2] = res.data.items_ids
              this.showDateInputMessage[id] = false;
            }
          })
          .catch((error) => {
            console.log(error);
            this.showDateErrorMessage = true;
          });

    },
    makeBookingsPayload() {
      this.showDateErrorMessage = false
      const payload = [];

      for (const [game_id, [quantity, [opening_date, return_date], game_item_ids]] of Object.entries(this.itemsInfo)) {
        if (!game_item_ids || game_item_ids.length === 0 || game_item_ids.length < quantity) {
          this.showDateErrorMessage = true;
          return;
        }

        for (let i = 0; i < quantity; i++) {
          payload.push({
            "game_id": game_id,
            "game_item_id": game_item_ids[i],
            "opening_date": opening_date.toUTCString(),
            "return_date": return_date.toUTCString()
          });
        }
      }
      console.log(payload)
      return payload
    },
    makeBookings(payload) {
      const path = `${baseApiUrl}/user_actions/booking/`;
      axios.post(path, payload, {
        headers: {"Authorization": `Bearer ${this.$cookies.get('token')}`}
      }).then((res) => {
            console.log(res)
          })
          .catch((error) => {
            console.log(error);
          });
    },
  },
  created() {
    this.cartStore = useCartStore(this.$pinia);
    this.profileStore = useProfileStore(this.$pinia);

    const startDate = new Date();
    const endDate = new Date(new Date().setDate(startDate.getDate() + 7));
    const defaultDate = [startDate, endDate];
    for (const item of this.cartStore.items) {
      this.itemsInfo[item.id] = [item.count, defaultDate, []]
      this.datesState[item.id] = null
      this.showDateInputMessage[item.id] = false
      this.dateInputMessage[item.id] = ''
    }
  },
}
</script>