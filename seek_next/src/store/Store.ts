import { InjectionKey } from 'vue';
import { createStore, Store } from 'vuex';
import axios from 'axios';
import router from '../routes/router';

const BASE_URL = 'http://localhost:8000';

// Define your typings for the store state
export interface State {
  user: {
    name: string;
    email: string;
    role: string;
  };
  accessToken: string | null;
  isLoggedIn: boolean;
  enrolledCourses: Course[];
}

export interface ComponentCustomProperties {
  $store: Store<State>
}

interface Course {
  id: string;
  title: string;
}

// Define injection key
export const key: InjectionKey<Store<State>> = Symbol();

export const store = createStore<State>({
  state: {
    user: {
      name: '',
      email: '',
      role: '',
    },
    accessToken: null,
    isLoggedIn: false,
    enrolledCourses: [] as Course[],
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
      localStorage.setItem('user', JSON.stringify(user));
    },
    setAccessToken(state, accessToken) {
      state.accessToken = accessToken;
      localStorage.setItem('accessToken', accessToken);
    },
    setLoggedIn(state, isLoggedIn) {
      state.isLoggedIn = isLoggedIn;
      localStorage.setItem('isLoggedIn', JSON.stringify(isLoggedIn));
    },
    clearAuthData(state) {
      state.user = { name: '', email: '', role: '' };
      state.accessToken = null;
      state.isLoggedIn = false;
      localStorage.removeItem('user');
      localStorage.removeItem('accessToken');
      localStorage.removeItem('isLoggedIn');
    },
    setEnrolledCourses(state, courses) {
      state.enrolledCourses = courses;
    }
  },
  actions: {
    async signIn({ commit }, credentials) {
      try {
        const response = await axios.post(BASE_URL + '/sign-in', credentials);
        // Handle success
        commit('setUser', {
          name: response.data.username, // Adjust based on your actual data structure
          email: response.data.email,
          role: response.data.role
        });
        commit('setAccessToken', response.data.access_token);
        commit('setLoggedIn', true);
        if (response.data.role == 'student') {
          router.push('/student-home')
        } else 
        router.push('/home');
      } catch (error) {
        // Handle error
        console.error(error);
        router.push('/sign-in');
      }
    },
    async signUp({ }, userData) {
      try {
        const response = await axios.post(BASE_URL + '/sign-up', userData);
        console.log('Signed up:', response.data);
        router.push('/sign-in');
      } catch (error) {
        // Handle error
        console.error(error);
      }
    },
    async signOut({ commit }) {
      try {
        // Call signout endpoint (IF ANY)
        //await axios.post('/api/signout');
        commit('clearAuthData');
        console.log('Signed out');
        router.push('/');
      } catch (error) {
        console.error(error);
      }
    },
    async autoLogin({ commit }) {
      // Load token from local storage
      const token = localStorage.getItem('accessToken');
      if (token) {
        try {
          // Call verify token endpoint
          const response = await axios.get(BASE_URL + '/verify-token', {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });

          // Update the store with the response
          const user = {
            name: response.data.username,
            email: response.data.email,
            role: response.data.role
          };
          commit('setUser', user);
          commit('setAccessToken', token);
          commit('setLoggedIn', true);
          if (user.role == 'student') {
            router.push('/student-home')
          } else 
          router.push('/home');
        } catch (error) {
          // If the token is invalid or expired, clear the auth data
          commit('clearAuthData');
          console.error('Token verification failed:', error);
          router.push('/sing-in');
        }
      } else {
        commit('clearAuthData');
        router.push('/sign-in');
      }
    },
    async fetchEnrolledCourses({ commit }, studentId: string) {
      try {
        const response = await axios.get(`${BASE_URL}/student/enrolled-courses/${studentId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
          },
        });
        console.log('Enrolled courses:', response.data);
        commit('setEnrolledCourses', response.data);
      } catch (error) {
        console.error('Error fetching enrolled courses:', error);
      }
    },
  },
  getters: {
    enrolledCourses(state) {
      return state.enrolledCourses;
    },
    isAuthenticated(state) {
      return state.isLoggedIn;
    },
  },
});