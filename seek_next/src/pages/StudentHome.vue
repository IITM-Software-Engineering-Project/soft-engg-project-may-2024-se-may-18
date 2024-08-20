<template>
  <v-app>
    <!-- Navigation Bar -->
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Student Dashboard</v-toolbar-title>
      <v-spacer></v-spacer>

      <!-- View All Courses Button -->
      <v-btn class="mx-2" @click="goToAllCourses" color="white">
        <v-icon class="mx-3">mdi-book-open-page-variant</v-icon>
        View All Courses
      </v-btn>

      <!-- Logout Button -->
      <v-btn class="mx-2" @click="logout" color="white" variant="outlined" append-icon="mdi-account-circle">
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

              <!-- Loading Indicator -->
              <v-row justify="center" v-if="loadingState === 'loading'">
                <v-progress-circular indeterminate color="primary"></v-progress-circular>
              </v-row>

              <!-- Error Message -->
              <v-alert v-if="loadingState === 'error'" type="error" dismissible>
                Error fetching courses.
                <v-btn class="mx-4" @click="retryFetchCourses" color="primary">
                  Retry
                </v-btn>
              </v-alert>

              <!-- List of Enrolled Courses -->
              <v-list v-if="loadingState === 'loaded'" two-line>
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
                  <v-list-item-title>No courses enrolled</v-list-item-title>
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
import { mapGetters, mapState } from 'vuex';

export default {
  name: 'StudentHome',
  mounted() {
    this.fetchEnrolledCourses();
  },
  computed: {
    ...mapGetters('student', ['enrolledCourses']),
    ...mapState('student', {
      loadingState: (state: any) => state.loading.fetchingEnrolledCourses,
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
      this.$store.dispatch('auth/signOut');
    },
    fetchEnrolledCourses() {
      this.$store.dispatch('student/fetchEnrolledCourses', this.$store.state.auth.user.id);
    },
    retryFetchCourses() {
      this.fetchEnrolledCourses();
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
