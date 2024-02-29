import {ref} from "vue";
import {defineStore} from "pinia";

export const useBookingsStore = defineStore('bookings', () => {

        const bookings = ref({
            items: [],
            currentPageNum: 0,
            limitPerPage: 30,
            hasMore: true
        });


        const bookingsReceived = (items) => {
            if (items.length === 0) return bookings.value.hasMore = false;
            bookings.value.items = [...bookings.value.items, ...items];
            bookings.value.currentPageNum += 1;

        };

        const resetBookings = () => {
            bookings.value = {
                items: [],
                currentPageNum: 0,
                limitPerPage: 30,
                hasMore: true
            }
        }

        return {
            bookings,
            bookingsReceived,
            resetBookings,
        }
    },
    {
        persist: true,
    });