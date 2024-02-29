<template>
  <div>
    <navigation></navigation>
  </div>
  <section style="background-color: #eee;">
    <div class="container py-5">
      <div class="row d-flex justify-content-center">
        <div class="col-md-12 col-lg-10 col-xl-8">
          <div class="card">
            <div class="card-body p-md-5">
              <div>
                <h4>Choose Payment Method</h4>
                <p class="text-muted pb-2">
                  Please choose the payment method to start enjoying all the features of our products as soon as
                  possible
                </p>
              </div>

              <div class="px-3 py-4 border border-primary border-2 rounded mt-4 d-flex justify-content-between">
                <input class="form-check-input" type="radio" name="radioNoLabelX" id="radioNoLabel11"
                       aria-label="..." v-model="withBalance" :value="true"/>
                <i class="fa-solid fa-wallet fa-3x" style="color:blue"></i>
                <div class="d-flex flex-row align-items-center">
                  <div class="d-flex flex-column ms-3">
                    <span class="h5 mb-1">Pay with Balance</span>
                    <span class="small text-muted">COMMISSION</span>
                  </div>
                </div>
                <div class="d-flex flex-row align-items-center">
                  <sup class="dollar font-weight-bold text-muted">$</sup>
                  <span class="h2 mx-1 mb-0">{{priceWithBalance}}</span>
                  <span class="text-muted font-weight-bold mt-2">/ year</span>
                </div>
              </div>

              <div class="px-3 py-4 border border-primary border-2 rounded mt-4 d-flex justify-content-between">
                <input class="form-check-input" type="radio" name="radioNoLabelX" id="radioNoLabel11"
                       aria-label="..." v-model="withBalance" :value="false"/>
                <i class="fa-solid fa-credit-card fa-3x" style="color:blue"></i>
                <div class="d-flex flex-row align-items-center">
                  <div class="d-flex flex-column ms-3">
                    <span class="h5 mb-1">Pay with Card</span>
                    <span class="small text-muted">COMMISSION</span>
                  </div>
                </div>
                <div class="d-flex flex-row align-items-center">
                  <sup class="dollar font-weight-bold text-muted">$</sup>
                  <span class="h2 mx-1 mb-0">{{priceWithYookassa}}</span>
                  <span class="text-muted font-weight-bold mt-2">/ year</span>
                </div>
              </div>

              <div v-show="withBalance">
                <h4 class="mt-5">Balance details</h4>
                <div class="mt-4 d-flex justify-content-between align-items-center">
                  <div class="d-flex flex-row align-items-center">
                    <div class="d-flex flex-column ms-3">
                      <span class="small text-muted">Amount: </span>
                      <span class="h5 mb-1">{{ balanceInfo.balance }}</span>
                    </div>
                  </div>
                  <div>
                    <span class="small text-muted">{{ balanceInfo.balance_currency }}</span>
                  </div>
                </div>
              </div>


              <div class="mt-3">
                <button class="btn btn-primary btn-block btn-lg">
                  Proceed to payment <i class="fas fa-long-arrow-alt-right"></i>
                </button>
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
import {useCartStore} from "@/stores/cart.js";

export default {

  name: 'Profile',
  data() {
    return {
      profileStore: '',
      cartStore: '',
      withBalance: false,
      balanceInfo: [],
      priceWithYookassa: 0,
      priceWithBalance: 0,
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
    calculatePriceCommission(service) {
      const path = `${baseApiUrl}/payment_accounts/payment_commission/`;
      const payload = {
        "payment_type": "bank_card",
        "payment_service": service,
        "payment_amount": this.cartStore.totalCost,
      };
      axios.post(path, payload, {
        headers: {"Authorization": `Bearer ${this.$cookies.get('token')}`}
      }).then((res) => {
        const serviceMap = {
          'yookassa': 'priceWithYookassa',
          'from_balance': 'priceWithBalance'
        };
        this[serviceMap[service]] = res.data['amount with commission'];
      }).catch((error) => {
        console.error(error);
      });
    },
  },
  created() {
    this.profileStore = useProfileStore(this.$pinia);
    this.cartStore = useCartStore(this.$pinia);
    this.getBalance();
    this.calculatePriceCommission('yookassa');
    this.calculatePriceCommission('from_balance');
  },
}
</script>