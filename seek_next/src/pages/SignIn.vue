<template>
    <v-container fluid>
        <v-row class="root">
            <v-col cols="6" class="d-flex align-center">
                <v-container class="sign-in align-content-center">
                    <v-row class="d-flex align-center justify-center">
                        <v-col cols="12" class="d-block">
                            <v-card-text class="title text-h2 text-center mb-10">Sign In</v-card-text>

                            <!-- Username Field -->
                            <v-text-field class="input" v-model="username" placeholder="Username" variant="solo" rounded
                                flat></v-text-field>

                            <!-- Password Field with Hide/Show Toggle -->
                            <v-text-field class="input" v-model="password" :type="showPassword ? 'text' : 'password'"
                                variant="solo" :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                placeholder="Password" @click:append-inner="togglePasswordVisibility" rounded
                                flat></v-text-field>

                            <!-- Spacer Container -->
                            <v-container style="height: 40px;"></v-container>
                            <!-- Sign In Button -->
                            <v-row class="d-flex justify-center py-5">
                                <v-btn @click="signIn" size="large" elevation="0" color="white" rounded>
                                    <span style="font-size: 14px;">Sign In</span>
                                </v-btn>
                            </v-row>
                            <v-row class="d-flex justify-center align-center mt-3">
                                <span class="mx-6" style="font-family: 'Poppins', sans-serif;">Don't have an
                                    account?</span>
                                <v-btn size="large" elevation="0" color="white" rounded @click="goToRegister">
                                    <span style="font-size: 14px;">Sign Up</span>
                                </v-btn>
                            </v-row>
                        </v-col>
                    </v-row>
                </v-container>
            </v-col>

            <v-col cols="6" class="d-block align-self-center">
                <v-container class="d-flex justify-center">
                    <v-img src="/src/assets/study_icon.png" width="300" height="300" />
                </v-container>
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
            username: '',
            password: '',
            showPassword: false, // Add a variable to toggle password visibility
        }
    },
    methods: {
        signIn() {
            this.$store.dispatch('auth/signIn', {
                username: this.username,
                password: this.password
            });
        },
        goToRegister() {
            this.$router.push('/sign-up');
        },
        togglePasswordVisibility() {
            this.showPassword = !this.showPassword; // Toggle the password visibility
        }
    }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,100..900;1,100..900&family=Montserrat:ital,wght@0,100..900;1,100..900&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');

.root {
    height: 100vh;
}

.title {
    font-family: "Poppins", sans-serif;
    font-weight: 400;
}

.input {
    margin: 0 20px 0 20px;
    font-family: "Popins", sans-serif;
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
    text-align: center;
}

.v-text-field__input {
    box-shadow: none;
}
</style>
