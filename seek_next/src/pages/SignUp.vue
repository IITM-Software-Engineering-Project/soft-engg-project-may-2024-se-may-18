<template>
    <v-container fluid>
        <v-row class="root">
            <v-col cols="6" class="d-flex align-center">
                <v-container class="register align-content-center">
                    <v-row class="d-flex align-center justify-center">
                        <v-col cols="12" class="d-block">
                            <!-- Username Field -->
                            <v-text-field v-model="username" label="Username" outlined dense></v-text-field>
                            <!-- Email Field -->
                            <v-text-field v-model="email" label="Email" outlined dense></v-text-field>
                            <!-- Password Field -->
                            <v-text-field v-model="password" label="Password" outlined dense
                                type="password"></v-text-field>
                            <!-- Confirm Password Field -->
                            <v-text-field v-model="confirmPassword" label="Confirm Password" outlined dense
                                type="password"></v-text-field>
                            <!-- Role Dropdown -->
                            <v-select v-model="role" :items="roles" label="Role" outlined dense></v-select>
                            <v-row class="d-flex justify-center py-5">
                                <v-btn @click="register" color="primary" dark>
                                    Register
                                </v-btn>
                            </v-row>
                            <v-row class="d-flex justify-center mt-3">
                                <span class="px-3">Already have an account?</span>
                                <v-btn @click="goToSignIn" color="primary">
                                    Sign In
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
    name: 'SignUp',
    data() {
        return {
            username: '', // Added username field
            email: '',
            password: '',
            confirmPassword: '',
            role: '', // Added role field
            roles: ['Student', 'Instructor'], // Role options
        }
    },
    methods: {
        register() {
            if (this.password !== this.confirmPassword) {
                console.error('Passwords do not match');
                return;
            }

            if (!this.username || !this.role) {
                console.error('Username and role must be provided');
                return;
            }

            this.$store.dispatch('signIn', {
                username: this.username,
                email: this.email,
                password: this.password,
                role: this.role
            });
        },
        goToSignIn() {
            this.$router.push('/sign-in');
        }
    }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jost:wght@300&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

.root {
    height: 100vh;
}

.register {
    background-color: rgb(228, 228, 228);
    width: 70%;
    height: 80%;
    /* Adjust height for additional fields */
    border-radius: 4%;
}

.banner {
    background-color: rgb(255, 255, 255);
    font-family: "Montserrat", sans-serif;
}
</style>
