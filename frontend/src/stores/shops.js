import {ref} from "vue";
import {defineStore} from "pinia";

export const useShopsStore = defineStore('shops', () => {

        const shops = ref([]);


        const shopsReceived = (items) => {
            shops.value = [...shops.value, ...items];
        };

        const resetShops = () => {
            shops.value = []
        };

        return {
            shops,
            shopsReceived,
            resetShops,
        }
    },
    {
        persist: true,
    });