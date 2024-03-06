import {defineStore} from 'pinia'
import {ref} from "vue";

export const useCheckoutsStore = defineStore('checkouts', () => {

        const items = ref([]);
        const totalItems = ref(0);


        const addItem = (item) => {
            items.value.push(item);
            totalItems.value += 1;
        };

        const removeItem = (item) => {
            items.value = items.value.filter(currItem => currItem !== item);
            totalItems.value -= 1;
        };

        const resetCheckouts = () => {
            items.value = [];
            totalItems.value = 0;
        };

        return {
            items,
            totalItems,
            addItem,
            removeItem,
            resetCheckouts,
        };

    },
    {
        persist: true,
    });