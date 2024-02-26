<template>
  <div>
    <Navigation></Navigation>
  </div>
</template>

<script>
import Navigation from "./Navigation.vue";
import Alert from './Alert.vue';
export default {

  name: 'Bookings',
  data() {
    return {
    }
  },

  components: {
    Navigation: Navigation,
    alert: Alert,
  },
  methods: {

  }
}
</script>