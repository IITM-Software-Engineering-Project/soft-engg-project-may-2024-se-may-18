<template>
  <v-app>
    <!-- Navigation Bar -->
    <v-app-bar app dark>
      <v-toolbar-title>All Courses</v-toolbar-title>
      <v-spacer></v-spacer>

      <!-- Back to Dashboard Button -->
      <v-btn class="mx-2" style="background-color: #e0e0e0;" @click="goToDashboard">
        Dashboard
      </v-btn>

      <!-- Logout Button -->
      <v-btn class="mx-2" @click="logout" variant="outlined" append-icon="mdi-account-circle">
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
                <v-textarea style="background-color: white;" label="Ask about courses" v-model="prompt" rows="4"
                  outlined dense></v-textarea>
                <v-btn block class="navigation-item" @click="searchCourses" rounded="lg">
                  <v-row style="align-items: center;">
                    <v-col cols="1">
                      <v-icon>mdi-magnify</v-icon>
                    </v-col>
                    <v-col cols="10">
                      <span>Find Courses</span>
                    </v-col>
                  </v-row>
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
                  <v-list-item v-for="course in chatCourses" :key="course.course_id"
                    @click="isEnrolled(course.course_id) ? goToCourse(course.course_id) : null"
                    class="chat-course-item">
                    <v-list-item-content>
                      <v-list-item-title>{{ course.course_title }}</v-list-item-title>
                      <v-list-item-subtitle>{{ course.course_description }}</v-list-item-subtitle>
                    </v-list-item-content>
                    <v-list-item-action>
                      <v-btn v-if="!isEnrolled(course.course_id)" color="success" @click.stop="enroll(course.course_id)"
                        size="x-small">
                        Enroll
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

              <!-- Enrolled Courses -->
              <v-list v-if="enrolledCourses.length > 0">
                <v-list-item-group subheader>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title class="headline">Enrolled Courses</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list-item-group>
                <v-list-item v-for="course in enrolledCourses" :key="course.id" @click="goToCourse(course.id)"
                  class="mx-3 my-5 clickable-item" rounded="lg" style="background-color: #e0e0e0;">
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
                      <v-list-item-subtitle class="font-weight-bold mt-3">
                        Enrolled
                      </v-list-item-subtitle>
                    </v-col>
                  </v-row>
                </v-list-item>
              </v-list>

              <!-- Unenrolled Courses -->
              <v-list v-if="unenrolledCourses.length > 0">
                <v-list-item-group subheader>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title class="headline">Available Courses</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list-item-group>
                <v-list-item v-for="course in unenrolledCourses" :key="course.id" class="mx-3 my-5 " rounded="lg"
                  style="background-color: #e0e0e0;">
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
                        ₹{{ course.price }}
                      </v-list-item-subtitle>

                      <!-- Enroll Button -->
                      <v-btn color="success" @click.stop="enroll(course.id)" size="x-small">
                        Enroll
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-list-item>
              </v-list>

              <v-list-item v-if="allCourses.length === 0 && !loadingState">
                <v-list-item-title>No courses available</v-list-item-title>
              </v-list-item>
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
    unenrolledCourses() {
      return this.allCourses.filter((course: { id: any; }) => !this.enrolledCourses.some((enrolled: { id: any; }) => enrolled.id === course.id));
    },
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
        await this.$store.dispatch('student/enrollInCourse', { studentId: this.$store.state.user.id, courseId });
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
@import url('https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,100..900;1,100..900&family=Montserrat:ital,wght@0,100..900;1,100..900&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900&display=swap');

.headline {
  font-family: 'Montserrat', sans-serif;
  font-weight: 400;
  font-size: 30px;
  margin: 20px 0;
  text-align: center;
}

.font-weight-bold {
  font-weight: 500;
}

.chat-card,
.courses-card {
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background-color: #e0e0e0;
  margin: 20px 0;
}

.chat-response {
  margin-top: 15px;
  font-size: 16px;
  color: #333;
}

.chat-course-item {
  border-bottom: 1px solid #ccc;
  padding: 12px 0;
}

.no-courses {
  text-align: center;
  color: #666;
  font-size: 16px;
}

.v-btn {
  margin-top: 10px;
}

.v-list-item {
  border-radius: 8px;
  background-color: #ffffff;
  margin: 10px 0;
}

.v-list-item:hover {
  background-color: #f5f5f5;
}

.v-alert {
  margin: 20px 0;
}

.v-progress-circular {
  margin: 20px 0;
}
</style>
