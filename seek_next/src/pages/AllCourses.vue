<template>
  <v-app>
    <!-- Navigation Bar -->
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>All Courses</v-toolbar-title>
      <v-spacer></v-spacer>

      <!-- Back to Dashboard Button -->
      <v-btn @click="goToDashboard" color="white">
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
                  :key="course.id"
                  class="mt-3"
                >
                  <v-row>
                    <v-col>
                      <v-list-item-title>{{ course.title }}</v-list-item-title>
                      <v-list-item-subtitle>
                        {{ course.description }}
                      </v-list-item-subtitle>
                      <v-list-item-subtitle>
                        Total Modules: {{ course.total_modules }}
                      </v-list-item-subtitle>
                    </v-col>
                    <v-col class="text-right">
                      <v-list-item-subtitle class="font-weight-bold">
                        ${{ course.price }}
                      </v-list-item-subtitle>

                      <!-- Enroll Button -->
                       <!-- If enrolled then Go To Course Button -->
                      <v-btn
                        v-if="!isEnrolled(course.id)"
                        color="success"
                        @click="enroll(course.id)"
                        size="x-small"
                      >
                        Enroll
                      </v-btn>
                      <v-btn
                        v-if="isEnrolled(course.id)"
                        color="grey-darken-1"
                        @click="goToCourse(course.id)"
                        size="x-small"
                      >
                        Go to Course
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-list-item>

                <v-list-item v-if="allCourses.length === 0">
                  <v-list-item-title>No courses available</v-list-item-title>
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
  computed: {
    ...mapGetters(['allCourses', 'enrolledCourses']),
  },
  methods: {
    isEnrolled(courseId: string): boolean {
      return this.enrolledCourses.some((course: any) => course.id === courseId);
    },
    goToCourse(courseId: string) {
      // You can add navigation logic here
      console.log(`Navigating to course with ID: ${courseId}`);
    },
    async enroll(courseId: string) {
      const studentId = "11"; // Hardcoded student ID - need to change 
      // try {
      //   await this.$store.dispatch('enrollInCourse', { studentId, courseId });
      //   alert('Enrollment successful');
      // } catch (error) {
      //   console.error('Error enrolling in course:', error);
      //   alert('Enrollment failed');
      // }
      console.log(courseId, studentId);
    },
    goToDashboard() {
      this.$router.push('/student-home');
    },
    logout() {
      this.$store.dispatch('signOut');
    },
  },
  mounted() {
    this.$store.dispatch('fetchAllCourses');
  },
};
</script>

<style scoped>
.headline {
  font-family: 'Montserrat', sans-serif;
  margin-bottom: 20px;
  text-align: center;
}
.font-weight-bold {
  font-weight: bold;
}
</style>
