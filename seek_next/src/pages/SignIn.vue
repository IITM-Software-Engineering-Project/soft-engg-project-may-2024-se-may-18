<template>
    <v-container fluid>
        <v-row class="root">
            <v-col cols="6" class="d-flex align-center">
                <v-container class="sign-in align-content-center">
                    <v-row class="d-flex align-center justify-center">
                        <v-col cols="12" class="d-block">
                            <!-- Username Field -->
                            <v-text-field v-model="username" label="Username" outlined dense></v-text-field>
                            <!-- Password Field -->
                            <v-text-field v-model="password" label="Password" outlined dense
                                type="password"></v-text-field>
                            <v-row class="d-flex justify-center py-5">
                                <v-btn @click="signIn" color="primary" dark>
                                    Sign In
                                </v-btn>
                            </v-row>
                            <v-row class="d-flex justify-center mt-3">
                                <span class="px-3">Don't have an account?</span>
                                <v-btn @click="goToRegister" color="primary">
                                    Register
                                </v-btn>
                            </v-row>
                        </v-col>
                    </v-row>
                </v-container>
            </v-col>
            <v-col cols="6" class="d-block align-self-center">
                <v-container class="banner text-h1">
                    Seek-Next
                </v-container>
                <v-container class="banner text-h4 d-block">
                    AI powered education platform
                </v-container>
            </v-col>
        </v-row>
    </v-container>
</template>

<script lang="ts">
export default {
    name: 'SignIn',
    data() {
        return {
            username: '',  // Changed to username
            password: ''
        }
    },
    methods: {
        signIn() {
            this.$store.dispatch('signIn', {
                username: this.username,
                password: this.password
            });
        },
        goToRegister() {
            this.$router.push('/sign-up');
        }
    }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jost:wght@300&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

.root {
    height: 100vh;
}

.sign-in {
    background-color: rgb(228, 228, 228);
    width: 70%;
    height: 60%;
    border-radius: 4%;
}

.banner {
    background-color: rgb(255, 255, 255);
    font-family: "Montserrat", sans-serif;
}
</style>
