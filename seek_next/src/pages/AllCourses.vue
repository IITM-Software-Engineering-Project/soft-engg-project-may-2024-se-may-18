<template>
  <v-app>
    <!-- Navigation Bar -->
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>All Courses</v-toolbar-title>
      <v-spacer></v-spacer>

      <!-- Back to Dashboard Button -->
      <v-btn class="mx-2" @click="goToDashboard" color="white">
        Dashboard
      </v-btn>

      <!-- Logout Button -->
      <v-btn class="mx-2" @click="logout" color="white" variant="outlined" append-icon="mdi-account-circle">
        <v-icon>mdi-logout</v-icon>
        Logout
      </v-btn>

    </v-app-bar>

    <!-- Main Content -->
    <v-main>
      <v-container fluid>
        <v-row dense>

          <!-- Chat Feature -->
          <v-col cols="12" md="3">
            <v-card outlined class="chat-card">
              <v-card-title class="headline">
                Course Helper Chatbot
              </v-card-title>
              <v-card-text>
                <v-textarea label="Ask about courses" v-model="prompt" rows="4" outlined dense></v-textarea>
                <v-btn color="deep-purple-lighten-2" block class="mt-2" @click="searchCourses">
                  Find Courses
                </v-btn>

                <!-- Loading Indicator for Search -->
                <v-row v-if="searchLoading" justify="center" class="mt-2">
                  <v-col class="d-flex justify-center">
                    <v-progress-circular indeterminate color="primary"></v-progress-circular>
                  </v-col>
                </v-row>

                <v-divider class="my-4"></v-divider>

                <!-- Error Message for Search -->
                <v-alert v-if="searchError" type="error" dismissible>
                  {{ searchError }}
                </v-alert>

                <!-- Chat Response -->
                <div v-if="chatMessage && !searchError" class="chat-response">
                  <strong>{{ chatMessage }}</strong>
                </div>
                <v-list v-if="chatCourses.length > 0 && !searchError">
                  <v-list-item v-for="course in chatCourses" :key="course.course_id" class="chat-course-item">
                    <v-list-item-content>
                      <v-list-item-title>{{ course.course_title }}</v-list-item-title>
                      <v-list-item-subtitle>{{ course.course_description }}</v-list-item-subtitle>
                    </v-list-item-content>
                    <v-list-item-action class="my-3">
                      <v-btn v-if="!isEnrolled(course.course_id)" color="success" @click="enroll(course.course_id)"
                        size="x-small">
                        Enroll
                      </v-btn>
                      <v-btn v-if="isEnrolled(course.course_id)" color="grey-darken-1"
                        @click="goToCourse(course.course_id)" size="x-small">
                        Go to Course
                      </v-btn>
                    </v-list-item-action>
                  </v-list-item>
                </v-list>
                <div v-if="chatCourses.length === 0 && chatMessage && !searchError" class="no-courses">
                  No courses found
                </div>
              </v-card-text>
            </v-card>
          </v-col>

          <!-- Available Courses List -->
          <v-col cols="12" md="8">
            <v-card outlined class="courses-card">
              <v-card-title class="headline">Available Courses</v-card-title>

              <!-- Loading Indicator for Courses -->
              <v-row justify="center" v-if="loadingState === 'loading'" class="loading-container mb-3">
                <v-col class="d-flex justify-center">
                  <v-progress-circular indeterminate color="primary"></v-progress-circular>
                </v-col>
              </v-row>

              <v-divider v-if="!loadingState"></v-divider>

              <!-- Error Message -->
              <v-alert v-if="loadingState === 'error'" type="error" dismissible>
                Error fetching courses.
                <v-btn @click="retryFetchCourses" color="primary">
                  Retry
                </v-btn>
              </v-alert>

              <!-- List of Available Courses -->
              <v-list v-if="loadingState === 'loaded'" two-line>
                <v-list-item v-for="course in allCourses" :key="course.id" class="mt-3">
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
                      <v-btn v-if="!isEnrolled(course.id)" color="success" @click="enroll(course.id)" size="x-small">
                        Enroll
                      </v-btn>
                      <v-btn v-if="isEnrolled(course.id)" color="grey-darken-1" @click="goToCourse(course.id)"
                        size="x-small">
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
import { mapGetters, mapState } from 'vuex';
import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

export default {
  name: 'AllCourses',
  data() {
    return {
      prompt: '',
      chatMessage: '',
      chatCourses: [] as Array<{ course_id: number, course_title: string, course_description: string, price: number }>,
      searchLoading: false,
      searchError: '' as string,
    };
  },
  computed: {
    ...mapGetters('student', ['allCourses', 'enrolledCourses']),
    ...mapState('student', {
      loadingState: (state: any) => state.loading.fetchingAllCourses,
    }),
  },
  methods: {
    isEnrolled(courseId: number): boolean {
      return this.enrolledCourses.some((course: any) => course.id === courseId);
    },
    goToCourse(courseId: number) {
      this.$router.push(`/course-modules/${courseId}`);
    },
    async enroll(courseId: number) {
      try {
        await this.$store.dispatch('student/senrollInCourse', { studentId: this.$store.state.user.id, courseId });
        alert('Enrollment successful');
      } catch (error) {
        console.error('Error enrolling in course:', error);
        alert('Enrollment failed');
      }
    },
    goToDashboard() {
      this.$router.push('/student-home');
    },
    logout() {
      this.$store.dispatch('auth/signOut');
    },
    async searchCourses() {
      if (this.prompt.trim() === '') {
        alert('Please enter a prompt');
        return;
      }

      this.searchLoading = true;
      this.searchError = '';

      try {
        const response = await axios.post(BASE_URL + '/ai-search-courses', { prompt: this.prompt }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
          },
        });
        this.chatMessage = response.data.message;
        this.chatCourses = response.data.data;
      } catch (error) {
        console.error('Error searching courses:', error);
        this.searchError = 'Failed to search courses';
      } finally {
        this.searchLoading = false;
      }
    },
    retryFetchCourses() {
      this.$store.dispatch('student/fetchAllCourses');
    },
  },
  mounted() {
    this.$store.dispatch('student/fetchAllCourses');
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

.chat-card {
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.courses-card {
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  min-height: fit-content;
}

.chat-response {
  margin-top: 15px;
  font-size: 14px;
  color: #555;
}

.chat-course-item {
  border-bottom: 1px solid #eee;
  padding: 8px 0;
}

.no-courses {
  text-align: center;
  color: #999;
  font-size: 14px;
}
</style>
