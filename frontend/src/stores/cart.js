import {defineStore} from 'pinia'
import {ref} from "vue";

export const useCartStore = defineStore('cart', () => {

        const items = ref([]);
        const totalItems = ref(0);


        const addItem = (item) => {
            let targetItem = items.value.filter(currItem => currItem.id === item.id)[0];

            if (targetItem) targetItem.count += 1;
            else items.value = [...items.value, {...item, count: 1}];

            totalItems.value += 1;
        };

        const removeItem = (item) => {
            let targetItem = items.value.filter(currItem => currItem.id === item.id)[0];

            if (targetItem.count === 1) items.value = items.value.filter(currItem => currItem.id !== item.id);
            else targetItem.count -= 1;

            totalItems.value -= 1;
        };

        const resetCart = () => {
            items.value = [];
            totalItems.value = 0;
        };

        return {
            items,
            totalItems,
            addItem,
            removeItem,
            resetCart,
        };

    },
    {
        persist: true,
    });