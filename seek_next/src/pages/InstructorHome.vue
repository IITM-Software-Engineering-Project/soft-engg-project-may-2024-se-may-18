<template>
  <v-app>
    <!-- Navigation Bar -->
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Instructor Dashboard</v-toolbar-title>
      <v-spacer></v-spacer>

      <!-- View All Courses Button -->
      <v-btn @click="goToAllCourses" color="white">
        View All Courses
      </v-btn>

      <!-- Logout Button -->
      <v-btn @click="logout" color="white" variant="outlined" append-icon="mdi-account-circle">
        Logout
      </v-btn>
    </v-app-bar>

    <!-- Main Content -->
    <v-main>
      <v-container>
        <v-row justify="center">
          <v-col cols="12" md="8">
            <v-card>
              <v-card-title class="headline">Your Courses</v-card-title>
              <v-divider></v-divider>

              <!-- List of Enrolled Courses -->
              <v-list two-line>
                <v-list-item v-for="course in enrolledCourses" :key="course['id']" class="mt-3">
                  <v-row justify="space-between">
                    <!-- Course Title -->
                    <v-col cols="8">
                      <v-list-item-title>{{ course['title'] }}</v-list-item-title>
                    </v-col>

                    <!-- Go to Course Button -->
                    <v-col cols="4" class="text-right">
                      <v-btn @click="goToCourse(course.id)" color="secondary" size="small">
                        Go to Course
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-list-item>

                <v-list-item v-if="enrolledCourses.length === 0">
                  <v-list-item-title>No courses</v-list-item-title>
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
  name: 'instructor-home',
  mounted() {
    this.$store.dispatch('fetchEnrolledCourses', this.$store.state.user.id);
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
    goToCourse(courseId: string) {
      this.$router.push(`/course-modules/${courseId}`);
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

.text-right {
  text-align: right;
}
</style>
