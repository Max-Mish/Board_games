import {defineStore} from 'pinia'
import {ref} from "vue";

export const useCartStore = defineStore('cart', () => {

        const items = ref([]);
        const totalItems = ref(0);
        const subtotalCost = ref(0);
        const totalCost = ref(0);
        const shippingCost = ref(0);
        const shippingService = ref('');


        const addItem = (item) => {
            let targetItem = items.value.filter(currItem => currItem.id === item.id)[0];
            console.log(targetItem)

            if (targetItem) targetItem.count += 1;
            else items.value = [...items.value, {...item, count: 1}];

            totalItems.value += 1;
            subtotalCost.value += item.cost;
            totalCost.value += item.cost
        };

        const removeItem = (item) => {
            let targetItem = items.value.filter(currItem => currItem.id === item.id)[0];

            if (targetItem.count === 1) items.value = items.value.filter(currItem => currItem.id !== item.id);
            else targetItem.count -= 1;

            totalItems.value -= 1;
            subtotalCost.value -= item.cost;
            totalCost.value -= item.cost
        };

        const resetCart = () => {
            items.value = [];
            totalItems.value = 0;
            subtotalCost.value = 0;
            totalCost.value = 0;
            shippingCost.value = 0;
            shippingService.value = ''
        };

        const chooseShipping = (method) => {
            const methods = {'DHL': 5, 'UPS': 3, 'FedEx': 4, 'Yandex': 7};
            shippingService.value = method
            shippingCost.value = methods[method];
            totalCost.value = subtotalCost.value + shippingCost.value
        };

        return {
            items,
            totalItems,
            subtotalCost,
            totalCost,
            shippingCost,
            shippingService,
            addItem,
            removeItem,
            resetCart,
            chooseShipping,
        };

    },
    {
        persist: true,
    });