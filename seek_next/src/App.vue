<template>
  <router-view></router-view>
</template>

<script lang="ts">
import './style.css'
import router from './routes/router.ts';

export default {
  name: 'App',
  mounted() {
    localStorage.getItem('token');
    if (localStorage.getItem('token') === null) {
      router.push('/sign-in');
    } else {
      router.push('/home');
    }
  }
}
</script>