<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
    name: 'Loading',
    mounted() {
        console.log('App mounted')
        this.$store.dispatch('autoLogin')
    },
})
</script>

<template>
    <v-container class="loading-container" fluid>
        <v-row class="fill-height align-center justify-center">
            <v-progress-circular color="blue" :size="50" indeterminate></v-progress-circular>
        </v-row>
    </v-container>
</template>

<style scoped>
.loading-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.v-progress-circular {
    margin: 1rem;
}
</style>
