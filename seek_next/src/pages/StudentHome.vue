<template>
  <v-app>
    <!-- Navigation Bar -->
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Student Dashboard</v-toolbar-title>
      <v-spacer></v-spacer>

      <!-- View All Courses Button -->
      <v-btn @click="goToAllCourses" color="white">
        <v-icon>mdi-book-open-page-variant</v-icon>
        View All Courses
      </v-btn>

      <!-- Logout Button -->
      <v-btn @click="logout" color="white" variant="outlined">
        <v-icon>mdi-logout</v-icon>
        Logout
      </v-btn>
    </v-app-bar>

    <!-- Main Content -->
    <v-main>
      <v-container>
        <v-row justify="center">
          <v-col cols="12" md="8">
            <v-card>
              <v-card-title class="headline">Your Enrolled Courses</v-card-title>
              <v-divider></v-divider>

              <!-- List of Enrolled Courses -->
              <v-list two-line>
                <v-list-item
                  v-for="course in enrolledCourses"
                  :key="course['id']"
                  class="mt-3"
                >
                  <v-list-item-content>
                    <v-list-item-title>{{ course['title'] }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>

                <v-list-item v-if="enrolledCourses.length === 0">
                  <v-list-item-content>
                    <v-list-item-title>No courses enrolled</v-list-item-title>
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
  name: 'student-home',
  data() {
    return {
      studentId: '11',
    };
  },
  mounted() {
    this.$store.dispatch('fetchEnrolledCourses', this.studentId);
  },
  computed: {
    ...mapGetters({
      enrolledCourses: 'enrolledCourses',
    }),
  },
  methods: {
    goToAllCourses() {
      this.$router.push('/all-courses');
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
