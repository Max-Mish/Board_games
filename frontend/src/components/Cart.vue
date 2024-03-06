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
                            <h5 class="mb-0">{{ itemsInfo[item.id][3] }}$</h5>
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
                              :disabled-dates="disabledDates[item.id]"
                              :state="datesState[item.id]"
                              :clearable="false"
                              :enable-time-picker="false"
                              :start-time="{ hours: 0, minutes: 0 }"

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

                      <button type="button" class="btn btn-info btn-block btn-lg" @click="onToggleDelivery">
                        <div class="d-flex justify-content-between">
                          <span>{{ isPickup ? 'Change to Express delivery' : 'Change to In-store Pickup' }}</span>
                          <span><i
                              :class="isPickup ? 'fas fa-shipping-fast pe-2 ms-2' : 'fa-solid fa-store pe-2 ms-2'"></i></span>
                        </div>
                      </button>

                      <div v-if="!isPickup">
                        <form class="mt-4">
                          <div class="mt-4" v-if="useDaData">
                            <div class="form-outline form-white mb-4">
                              <label class="form-label" for="typeName">Address</label>
                              <daDataNext v-model="addressDaData" placeholder="Input Address"
                                          class="form-control form-control-lg"
                                          siez="17"></daDataNext>
                            </div>

                            <p>{{ addressDaData }}</p>

                          </div>
                          <div v-if="!useDaData">
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
                          </div>
                        </form>


                        <p class="small mb-2">Delivery service</p>
                        <a href="" type="button" class="text-white" @click.prevent="onDelivery('DHL')"><i
                            class="fab fa-dhl fa-3x me-3"
                            :class="{ 'text-dark': shippingService === 'DHL' }"></i></a>
                        <a href="" type="button" class="text-white" @click.prevent="onDelivery('UPS')"><i
                            class="fab fa-ups fa-2x me-3"
                            :class="{ 'text-dark': shippingService === 'UPS' }"></i></a>
                        <a href="" type="button" class="text-white" @click.prevent="onDelivery('FedEx')"><i
                            class="fab fa-fedex fa-2x me-3"
                            :class="{ 'text-dark': shippingService === 'FedEx' }"></i></a>
                        <a href="" type="button" class="text-white" @click.prevent="onDelivery('Yandex')"><i
                            class="fab fa-yandex fa-2x text-light"
                            :class="{ 'text-dark': shippingService === 'Yandex' }"></i></a>

                      </div>

                      <div class="mt-5" v-else>
                        <div class="card mb-3" v-for="(shop, index) of shopsStore.shops" :key="index">
                          <div class="card border-primary border-3 m-2" v-if="selectedPickup[index]">
                          </div>
                          <div class="card-body">
                            <a href="" class="stretched-link" @click.prevent="onTogglePickup(index)"></a>
                            <div class="d-flex justify-content-between">
                              <div class="d-flex flex-row align-items-center">
                                <div class="ms-3">
                                  <h5>{{ shop.address }}</h5>
                                  <p class="small mb-0">{{ shop.email }}</p>
                                  <p class="small mb-0">+{{ shop.phone_number }}</p>
                                </div>
                              </div>
                              <div class="d-flex flex-row align-items-center">
                                <div style="width: 80px;">
                                  <h5 class="mb-0">{{ shop.open_hours }}</h5>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      <hr class="my-4">

                      <div class="d-flex justify-content-between">
                        <p class="mb-2">Subtotal</p>
                        <p class="mb-2">${{ subtotalCost }}</p>
                      </div>

                      <div class="d-flex justify-content-between">
                        <p class="mb-2">Shipping</p>
                        <p class="mb-2">${{ shippingCost }}</p>
                      </div>

                      <div class="d-flex justify-content-between mb-4">
                        <p class="mb-2">Total</p>
                        <p class="mb-2">${{ totalCost }}</p>
                      </div>


                      <alert message='Please ensure all required fields are filled in before proceeding.'
                             v-if="showInputMessage"></alert>
                      <span v-if="!shippingService">Please select a delivery service.</span>
                      <button type="button" class="btn btn-info btn-block btn-lg" v-else @click="onCheckout">
                        <div class="d-flex justify-content-between">
                          <span>${{ totalCost }} Checkout</span>
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
import {useShopsStore} from "@/stores/shops.js";
import {useCheckoutsStore} from "@/stores/checkouts.js";
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import {baseApiUrl} from "@/services/baseApi.js";
import axios from "axios";
import {DaDataNext, useDaData} from 'vue-dadata-3'

export default {

  name: 'Cart',
  data() {
    return {
      cartStore: '',
      profileStore: '',
      shopsStore: '',
      checkoutsStore: '',
      showInputMessage: false,
      itemsInfo: {},
      disabledDates: {},
      datesState: {},
      dateInputMessage: {},
      showDateInputMessage: {},
      showDateErrorMessage: false,
      inputForm: {
        streetHouseApp: "",
        stateCity: "",
        country: "",
        index: "",
      },
      isPickup: true,
      selectedPickup: [],
      useDaData: true,
      addressDaData: '',
      shippingService: '',
      shippingCost: 0,
      subtotalCost: 0,
      totalCost: 0,
      bookingsIds: []
    }
  },

  components: {
    alert: Alert,
    navigation: Navigation,
    footerSmall: FooterSmall,
    datePicker: VueDatePicker,
    daDataNext: DaDataNext,
  },
  methods: {
    updateCart() {
      const path = `${baseApiUrl}/games/`;
      axios.get(path)
          .then((res) => {
            const games = res.data;
            const gamesCart = this.cartStore.items;
            this.cartStore.resetCart();
            for (const item of gamesCart) {
              for (const game of games) {
                if (item.id === game['id']) {
                  for (let i = 0; i < item.count; i++) {
                    this.cartStore.addItem(game);
                  }
                }
              }
            }
            this.recalculateCost()
          })
          .catch((error) => {
            console.error(error);
          });
    },

    recalculateCost() {
      this.totalCost -= this.subtotalCost
      this.subtotalCost = Object.values(this.itemsInfo).reduce((sum, itemInfo) => sum + itemInfo[3], 0);
      this.totalCost += this.subtotalCost
    },

    onBack() {
      this.$router.back()
    },
    onRemove(item) {
      this.cartStore.removeItem(item)
    },

    onTogglePickup(index) {
      this.selectedPickup = this.selectedPickup.fill(false);
      this.selectedPickup[index] = true;
      const address = this.shopsStore.shops[index]['address']
      const method = 'Pickup'
      this.getDeliveryCost(method, address)
    },

    onToggleDelivery() {
      this.isPickup = !this.isPickup;
    },

    onDelivery(method) {
      const address = this.getDeliveryData();
      if (!address) return;
      this.getDeliveryCost(method, address)
    },


    onCheckout() {
      const deliveryData = this.isPickup ? this.getPickupData() : this.getDeliveryData();
      const payload = this.makeBookingsPayload();
      // this.cartStore.resetCart();
      if (deliveryData && payload) {
        this.makeBookings(payload);
        const checkout = {
          'bookingsIds': this.bookingsIds,
          'totalCost': this.totalCost,
          'deliveryData': deliveryData,
          'shippingService': this.shippingService
        }
        this.checkoutsStore.addItem(checkout);
        this.$router.push({name: 'Checkout'});
      }
    },

    getShops() {
      const path = `${baseApiUrl}/stores/`;
      axios.get(path)
          .then((res) => {
            this.shopsStore.resetShops()
            this.shopsStore.shopsReceived(res.data)
          })
          .catch((error) => {
            console.error(error);
          });
    },

    getPickupData() {
      const index = this.selectedPickup.indexOf(true)
      return this.shopsStore.shops[index]['address']
    },

    getDeliveryData() {
      this.showInputMessage = false;
      if (!useDaData) {
        if (this.inputForm.streetHouseApp && this.inputForm.stateCity && this.inputForm.country && this.inputForm.index) {
          return Object.values(this.inputForm).join(", ");
        } else {
          this.showInputMessage = true;
        }
      } else {
        if (this.addressDaData) {
          return this.addressDaData;
        } else {
          this.showInputMessage = true;
        }
      }
    },

    getDeliveryCost(method, address) {
      const payload = {
        "name": method,
        "address": address
      }
      const path = `${baseApiUrl}/purchases/delivery_service/`;
      axios.post(path, payload, {
        headers: {"Authorization": `Bearer ${this.$cookies.get('token')}`}
      }).then((res) => {
        this.shippingService = method;
        this.shippingCost = res.data['delivery_cost'];
        this.totalCost = this.subtotalCost + this.shippingCost
      })
          .catch((error) => {
            console.log(error);
          });
    },

    getDisabledDates(id) {
      const payload = {
        "game_id": id
      };
      const path = `${baseApiUrl}/games/items/disabled_dates/`;
      axios.post(path, payload)
          .then((res) => {
            this.disabledDates[id] = res.data.dates.map(date => new Date(Date.parse(date)));
          })
          .catch((error) => {
            console.log(error);
            throw error;

          });
    },

    handleDate(modelData, count, id) {
      this.showDateErrorMessage = false;
      this.itemsInfo[id] = [count, modelData];
      const payload = {
        game_id: id,
        amount: count,
        booked_dates: modelData.map(date => date.toDateString())
      };
      const path = `${baseApiUrl}/games/items/check_dates/`;
      axios.post(path, payload)
          .then((res) => {
            if (res.data.dates_check_status === false) {
              this.datesState[id] = false;
              this.dateInputMessage[id] = res.data.message;
              this.showDateInputMessage[id] = true;
            } else {
              this.datesState[id] = true;
              this.itemsInfo[id][2] = res.data.items_ids;
              const dates_delta = Math.ceil(Math.abs(this.itemsInfo[id][1][1] - this.itemsInfo[id][1][0]) / (1000 * 60 * 60 * 24)) + 1;
              this.itemsInfo[id][3] = Math.ceil((this.cartStore.items.find(item => item.id === id).cost / 7 * dates_delta) * this.itemsInfo[id][0]);
              this.recalculateCost()
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
            "opening_date": opening_date.toDateString(),
            "return_date": return_date.toDateString()
          });
        }
      }
      return payload
    },

    makeBookings(payload) {
      const path = `${baseApiUrl}/user_actions/booking/`;
      axios.post(path, payload, {
        headers: {"Authorization": `Bearer ${this.$cookies.get('token')}`}
      }).then((res) => {
        this.bookingsIds = res.data.map(booking => booking.id);
      })
          .catch((error) => {
            console.log(error);
            throw error;
          });
    },
  },

  created() {
    this.cartStore = useCartStore(this.$pinia);
    this.profileStore = useProfileStore(this.$pinia);
    this.shopsStore = useShopsStore(this.$pinia);
    this.checkoutsStore = useCheckoutsStore(this.$pinia);

    this.updateCart()

    this.getShops();
    this.selectedPickup = new Array(this.shopsStore.shops.length).fill(false);


    const startDate = new Date();
    const endDate = new Date(new Date().setDate(startDate.getDate() + 6));
    const defaultDate = [startDate, endDate];
    for (const item of this.cartStore.items) {
      this.itemsInfo[item.id] = [item.count, defaultDate, [], item.cost * item.count]
      this.getDisabledDates(item.id)
      this.datesState[item.id] = null
      this.showDateInputMessage[item.id] = false
      this.dateInputMessage[item.id] = ''
    }

    this.recalculateCost()
  },
}
</script>