<template>
  <v-app>
    <!-- Navigation Bar -->
    <v-app-bar app dark>
      <v-toolbar-title>Course Modules</v-toolbar-title>
      <v-spacer></v-spacer>

      <!-- Back to Dashboard Button -->
      <v-btn style="background-color: #e0e0e0;" @click="goToDashboard" class="mx-2">
        Dashboard
      </v-btn>

      <!-- Back to Courses Button -->
      <v-btn style="background-color: #e0e0e0;" @click="goToCourses" class="mx-2">
        All Courses
      </v-btn>

      <!-- Logout Button -->
      <v-btn @click="logout" variant="outlined" class="mx-2">
        Logout
      </v-btn>
    </v-app-bar>

    <!-- Main Content -->
    <v-main>
      <v-container fluid>
        <v-row dense>
          <!-- Course Modules -->
          <v-col cols="12" md="8">
            <v-card class="pa-4 rounded-card" outlined>
              <v-card-title class="headline text-h6">
                Modules for {{ courseTitle }}
              </v-card-title>
              <v-divider></v-divider>

              <!-- List of Course Modules -->
              <v-list two-line>
                <v-list-item v-for="module in courseModules" :key="module.id" class="mt-3">
                  <v-row>
                    <v-col>
                      <v-list-item-title class="font-weight-bold text-subtitle-1">
                        {{ module.title }}
                      </v-list-item-title>
                      <v-list-item-subtitle class="text-body-2">
                        {{ module.description }}
                      </v-list-item-subtitle>
                      <v-list-item-subtitle class="text-caption">
                        Lectures: {{ module.total_lectures }} | Assignments: {{
                          module.total_assignments
                        }}
                      </v-list-item-subtitle>
                    </v-col>
                    <v-col class="text-right">
                      <!-- Button to go to Module -->
                      <v-btn @click="goToModule(module.id, module.title)" class="rounded-btn">
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

          <!-- Chat Feature -->
          <v-col cols="12" md="4">
            <v-card class="pa-4 rounded-card" outlined>
              <v-card-title class="headline text-h6">Course Chatbot</v-card-title>
              <v-divider></v-divider>
              <v-textarea label="Type your question about this course here" v-model="prompt" rows="4" outlined
                class="mt-2"></v-textarea>
              <v-btn block class="mt-2 rounded-btn" @click="askAboutCourse">
                Ask
              </v-btn>
              <v-divider class="my-4"></v-divider>
              <div class="chat-response">
                <!-- Use v-html to render formatted message -->
                <div v-if="chatMessage" v-html="formatMessage(chatMessage)"></div>
                <div v-if="!chatMessage" class="no-chat">
                  Type a prompt to get a response
                </div>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

const BASE_URL = "http://localhost:8000";

export default {
  name: "CourseModules",
  setup() {
    const route = useRoute();
    const router = useRouter();
    const courseId = route.params.courseId as string;
    const courseTitle = ref("Course Title");
    const courseModules = ref<any[]>([]);
    const prompt = ref("");
    const chatMessage = ref("");

    const fetchCourseDetails = async () => {
      try {
        const response = await axios.get(
          BASE_URL + `/student/courses/${courseId}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        const courseData = response.data;
        courseTitle.value = courseData.title;

        const modulesResponse = await axios.get(
          BASE_URL + `/student/modules/${courseId}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        courseModules.value = modulesResponse.data;
      } catch (error) {
        console.error("Error fetching course details:", error);
      }
    };

    const askAboutCourse = async () => {
      if (prompt.value.trim() === "") {
        alert("Please enter a prompt");
        return;
      }

      try {
        const response = await axios.post(
          BASE_URL + "/ai-explain-course",
          { prompt: prompt.value },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            params: { course_id: courseId },
          }
        );
        chatMessage.value = response.data.message;
      } catch (error) {
        console.error("Error explaining course:", error);
        alert("Failed to get course explanation");
      }
    };

    const goToDashboard = () => {
      router.push("/student-home");
    };

    const goToCourses = () => {
      router.push("/all-courses");
    };

    const goToModule = (moduleId: string, moduleTitle: string) => {
      router.push(`/module-details/${courseId}/${moduleId}/${moduleTitle}`);
    };

    const formatMessage = (message: string) => {
      return message.replace(/\n/g, "<br>");
    };

    onMounted(() => {
      fetchCourseDetails();
    });

    return {
      courseModules,
      courseTitle,
      prompt,
      chatMessage,
      askAboutCourse,
      goToDashboard,
      goToCourses,
      goToModule,
      formatMessage,
    };
  },
  methods: {
    logout() {
      this.$store.dispatch("auth/signOut");
    },
  },
};
</script>

<style scoped>
.headline {
  font-family: 'Montserrat', sans-serif;
  font-weight: 400;
  font-size: 40px;
  margin: 20px 0;
  text-align: center;
}

.font-weight-bold {
  font-weight: bold;
}

.chat-response {
  min-height: 200px;
  max-height: 400px;
  overflow-y: auto;
  padding: 16px;
}

.no-chat {
  text-align: center;
  color: #888;
}

.v-list-item-subtitle {
  word-break: break-word;
  /* Ensures long words wrap to the next line */
}

.v-btn {
  font-weight: bold;
}

.rounded-btn {
  border-radius: 8px;
  background-color: #e0e0e0;
}

.rounded-card {
  border-radius: 16px;
}

.text-h6 {
  font-family: "Poppins", sans-serif;
}

.text-subtitle-1 {
  font-family: "Poppins", sans-serif;
}

.text-body-2 {
  font-family: "Poppins", sans-serif;
}

.text-caption {
  font-family: "Poppins", sans-serif;
}
</style>
