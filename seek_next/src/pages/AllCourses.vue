<template>
    <v-app>
      <!-- Navigation Bar -->
      <v-app-bar app color="primary" dark>
        <v-toolbar-title>All Courses</v-toolbar-title>
        <v-spacer></v-spacer>
  
        <!-- Back to Dashboard Button -->
        <v-btn @click="goToDashboard" color="white">
          <!-- <v-icon left>mdi-view-dashboard</v-icon> -->
          Dashboard
        </v-btn>
  
        <!-- Logout Button -->
        <v-btn @click="logout" color="white" variant="outlined">
          Logout
        </v-btn>
      </v-app-bar>
  
      <!-- Main Content -->
    <v-main>
      <v-container>
        <v-row justify="center">
          <v-col cols="12" md="8">
            <v-card>
              <v-card-title class="headline">Available Courses</v-card-title>
              <v-divider></v-divider>

              <!-- List of All Courses -->
              <v-list two-line>
                <v-list-item
                  v-for="course in allCourses"
                  :key="course['id']"
                  class="mt-3"
                >
                  <v-list-item-content>
                    <v-list-item-title>{{ course['title'] }}</v-list-item-title>
                    <v-list-item-subtitle>{{ course['description'] }}</v-list-item-subtitle>
                    <v-list-item-subtitle>
                      Total Modules: {{ course['total_modules'] }} | Price: ₹{{ course['price'] }}
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>

                <v-list-item v-if="allCourses.length === 0">
                  <v-list-item-content>
                    <v-list-item-title>No courses available</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>
  
  <script lang="ts">
  import { mapGetters } from 'vuex';
  
  export default {
    name: 'AllCourses',
    mounted() {
      this.$store.dispatch('fetchAllCourses');
    },
    computed: {
      ...mapGetters({
        allCourses: 'allCourses',
      }),
    },
    methods: {
      goToDashboard() {
        this.$router.push('/student-home');
      },
      logout() {
        this.$store.dispatch('signOut');
      },
    },
  };
  </script>
  
  <style scoped>
  .headline {
    font-family: 'Montserrat', sans-serif;
    margin-bottom: 20px;
    text-align: center;
  }
  .v-list-item-title {
    font-weight: 500;
  }
  .v-card {
    padding: 20px;
  }
  </style>
  