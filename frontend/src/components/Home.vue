<template>
  <div>
    <Navigation></Navigation>
  </div>
  <div>
    <FooterBig></FooterBig>
  </div>
</template>

<script>
import Navigation from "./Navigation.vue";
import Alert from './Alert.vue';
import FooterBig from "@/components/FooterBig.vue";

export default {

  name: 'Home',
  data() {
    return {}
  },

  components: {
    FooterBig: FooterBig,
    Navigation: Navigation,
    alert: Alert,
  },
  methods: {}
}
</script>