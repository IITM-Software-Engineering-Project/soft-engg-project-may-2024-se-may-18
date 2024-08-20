import axios from 'axios';
import router from '../../../routes/router';
import { ActionContext } from 'vuex';
import { State } from '../../store';
import { AuthState } from './auth';

const BASE_URL = 'http://localhost:8000';

export default {
    async signIn({ commit }: ActionContext<AuthState, State>, credentials: { username: string, password: string }) {
        try {
            const response = await axios.post(BASE_URL + '/sign-in', credentials);
            commit('setUser', {
                id: response.data.id,
                name: response.data.username,
                email: response.data.email,
                role: response.data.role,
            });
            commit('setAccessToken', response.data.access_token);
            commit('setLoggedIn', true);
            if (response.data.role === 'student') {
                router.push('/student-home');
            } else if (response.data.role === 'instructor') {
                router.push('/instructor-home');
            } else {
                router.push('/home');
            }
        } catch (error) {
            console.error(error);
            router.push('/sign-in');
        }
    },

    async signUp({ }, userData: { name: string, email: string, password: string }) {
        try {
            const response = await axios.post(BASE_URL + '/sign-up', userData);
            console.log('Signed up:', response.data);
            router.push('/sign-in');
        } catch (error) {
            console.error(error);
        }
    },

    async signOut({ commit }: ActionContext<AuthState, State>) {
        try {
            // Call signout endpoint (if any)
            // await axios.post('/api/signout');
            commit('clearAuthData');
            console.log('Signed out');
            router.push('/sign-in');
        } catch (error) {
            console.error(error);
        }
    },

    async autoLogin({ commit }: ActionContext<AuthState, State>) {
        const token = localStorage.getItem('accessToken');
        if (token) {
            try {
                const response = await axios.get(BASE_URL + '/verify-token', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                const user = {
                    id: response.data.id,
                    name: response.data.username,
                    email: response.data.email,
                    role: response.data.role,
                };
                commit('setUser', user);
                commit('setAccessToken', token);
                commit('setLoggedIn', true);

                if (user.role === 'student') {
                    router.push('/student-home');
                } else if (user.role === 'instructor') {
                    router.push('/instructor-home');
                } else {
                    router.push('/home');
                }
            } catch (error) {
                commit('clearAuthData');
                console.error('Token verification failed:', error);
                router.push('/sign-in');
            }
        } else {
            commit('clearAuthData');
            router.push('/sign-in');
        }
    },
};
