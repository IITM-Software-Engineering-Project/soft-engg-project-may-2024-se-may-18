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
    <v-container>
        <v-progress-circular color="red" :size="50" indeterminate></v-progress-circular>
    </v-container>
</template>


<style scoped>
.v-progress-circular {
    margin: 1rem;
}
</style>
