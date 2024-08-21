<template>
  <v-app>
    <!-- Sidebar Navigation -->
    <v-navigation-drawer app permanent :width="400">
      <v-list dense>
        <!-- Logo or Title -->
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="headline">Dashboard</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>

        <!-- Navigation Links -->
        <v-list-item class="navigation-item" rounded="lg" @click="goToAllCourses">
          <v-row style="align-items: center;">
            <v-col cols="1">
              <v-list-item-icon>
                <v-icon>mdi-grid-large</v-icon>
              </v-list-item-icon>
            </v-col>
            <v-col cols="10">
              <v-list-item-content>
                <v-list-item-title>All Courses</v-list-item-title>
              </v-list-item-content>
            </v-col>
          </v-row>
        </v-list-item>

        <v-list-item class="navigation-item" rounded="lg" @click="logout">
          <v-row style="align-items: center;">
            <v-col cols="1">
              <v-list-item-icon>
                <v-icon>mdi-logout</v-icon>
              </v-list-item-icon>
            </v-col>
            <v-col cols="10">
              <v-list-item-content>
                <v-list-item-title>Logout</v-list-item-title>
              </v-list-item-content>
            </v-col>
          </v-row>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main>
      <v-container class="fill-height">
        <v-row>
          <v-col cols="12">
            <h1 class="headline text-h2 my-10">Your Enrolled Courses</h1>

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
            <v-row v-if="loadingState === 'loaded'">
              <v-col cols="12" md="4" v-for="course in enrolledCourses" :key="course.id">
                <v-card flat class="course-tile text-h6 m-6" @click="goToCourse(course.id)" hover>
                  <v-card-title class="course-title" style="font-size: larger; font-weight: 500;">{{ course.title
                    }}</v-card-title>
                  <v-card-subtitle class="course-description" style="margin-bottom: auto;">
                    {{ course.description }}
                  </v-card-subtitle>
                </v-card>
              </v-col>
              <v-col cols="12" v-if="enrolledCourses.length === 0">
                <v-list-item-title>No courses enrolled</v-list-item-title>
              </v-col>
            </v-row>
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
@import url('https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,100..900;1,100..900&family=Montserrat:ital,wght@0,100..900;1,100..900&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900&display=swap');

.headline {
  font-family: 'Jost', sans-serif;
  font-weight: 400;
  font-size: 40px;
  margin: 20px 0;
  text-align: left;
}

.course-tile {
  margin-bottom: 20px;
  padding: 15px;
  border-radius: 10px;
  background-color: #e0e0e0;
  cursor: pointer;
  transition: background-color 0.3s ease;
  height: 250px;
}

.course-description {
  font-size: medium;
  font-weight: 400;
  text-overflow: ellipsis;
}

.course-tile:hover {
  background-color: #e0e0e0;
}

.course-title {
  font-weight: 500;
  white-space: normal;
  word-wrap: break-word;
}

.v-btn {
  margin-top: 10px;
}

.navigation-item {
  margin: 10px 15px;
  border-radius: 8px;
  background-color: #e0e0e0;
  height: 60px
}
</style>
