import {ref} from "vue";
import {defineStore} from "pinia";

export const useGamesStore = defineStore('games', () => {

        const games = ref({
            items: [],
            currentPageNum: 0,
            limitPerPage: 30,
            hasMore: true
        });


        const gamesReceived = (items) => {
            if (items.length === 0) return games.value.hasMore = false;

            games.value.items = [...games.value.items, ...items];
            games.value.currentPageNum += 1;

        };

        const resetGames = () => {
            games.value = {
                items: [],
                currentPageNum: 0,
                limitPerPage: 30,
                hasMore: true
            }
        }

        return {
            games,
            gamesReceived,
            resetGames,
        }
    },
    {
        persist: true,
    });