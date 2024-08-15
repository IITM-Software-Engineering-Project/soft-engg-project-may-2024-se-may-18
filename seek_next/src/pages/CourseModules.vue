<template>
    <v-app>
      <!-- Navigation Bar -->
      <v-app-bar app color="primary" dark>
        <v-toolbar-title>Course Modules</v-toolbar-title>
        <v-spacer></v-spacer>
        
        <!-- Back to Dashboard Button -->
        <v-btn @click="goToDashboard" color="white">
            Dashboard
        </v-btn>

        <!-- Back to Courses Button -->
        <v-btn @click="goToCourses" color="white">
          All Courses
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
                <v-card-title class="headline">Modules for {{ courseTitle }}</v-card-title>
                <v-divider></v-divider>
  
                <!-- List of Course Modules -->
                <v-list two-line>
                  <v-list-item v-for="module in courseModules" :key="module.title" class="mt-3">
                    <v-row>
                      <v-col>
                        <v-list-item-title>{{ module.title }}</v-list-item-title>
                        <v-list-item-subtitle>{{ module.description }}</v-list-item-subtitle>
                        <v-list-item-subtitle>
                          Lectures: {{ module.total_lectures }} | Assignments: {{ module.total_assignments }}
                        </v-list-item-subtitle>
                      </v-col>
                      <v-col class="text-right">
                        <!-- Button to go to Module -->
                        <v-btn @click="goToModule(module.id, module.title)" color="#BA68C8" size="small">
                          Go to Module
                        </v-btn>
                      </v-col>
                    </v-row>
                  </v-list-item>
  
                  <v-list-item v-if="courseModules.length === 0">
                    <v-list-item-title>No modules available</v-list-item-title>
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
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

export default {
name: 'CourseModules',
methods: {
    logout() {
    this.$store.dispatch('signOut');
    },
    // goToModule(moduleId: string) {
    // console.log('Go to module:', moduleId);
    // this.$router.push(`/module-details/${useRoute().params.courseId}/${moduleId}`);
    // },
},
setup() {
    const route = useRoute();
    const router = useRouter();
    const courseId = route.params.courseId as string;
    const courseTitle = ref('Course Title');
    const courseModules = ref<any[]>([]);

    const fetchCourseDetails = async () => {
    try {
        const response = await axios.get(BASE_URL + `/student/courses/${courseId}`, {
        headers: {
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
        },
        });
        const courseData = response.data;
        courseTitle.value = courseData.title;

        const modulesResponse = await axios.get(BASE_URL + `/student/modules/${courseId}`, {
        headers: {
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
        },
        });
        courseModules.value = modulesResponse.data;
    } catch (error) {
        console.error('Error fetching course details:', error);
    }
    };
    
    const goToDashboard = () => {
    router.push('/student-home');
    };

    const goToCourses = () => {
    router.push('/all-courses');
    };

    const goToModule = (moduleId: string, moduleTitle: string) => {
    router.push(`/module-details/${courseId}/${moduleId}/${moduleTitle}`);
    };

    onMounted(() => {
    fetchCourseDetails();
    });

    return {
    courseModules,
    courseTitle,
    goToDashboard,
    goToCourses,
    goToModule,
    };
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