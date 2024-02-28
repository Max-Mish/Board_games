import {ref} from "vue";
import {defineStore} from "pinia";

export const useProfileStore = defineStore('profile', () => {

        const logged = ref(false);
        const username = ref('');
        const email = ref('');
        const cover_photo = ref('');


        const addInfo = (data) => {
            username.value = data.username;
            email.value = data.email;
            cover_photo.value = data.cover_photo;
            logged.value = true;
        };

        const resetInfo = () => {
            username.value = '';
            email.value = '';
            cover_photo.value = '';
        }

        return {
            logged,
            username,
            email,
            cover_photo,
            addInfo,
            resetInfo
        }
    },
    {
        persist: true,
    });