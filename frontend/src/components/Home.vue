<template>
  <div>
    <navigation></navigation>
  </div>
  <div>
    <footerBig></footerBig>
  </div>
</template>

<script>
import Alert from '@/components/Alert.vue';
import Navigation from "@/components/Navigation.vue";
import FooterBig from "@/components/FooterBig.vue";

export default {

  name: 'Home',
  data() {
    return {}
  },

  components: {
    footerBig: FooterBig,
    navigation: Navigation,
    alert: Alert,
  },
  methods: {}
}
</script>