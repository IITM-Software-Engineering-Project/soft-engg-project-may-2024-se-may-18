<template>
  <v-app>
    <!-- Navigation Bar -->
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Module: {{ moduleTitle }}</v-toolbar-title>
      <v-spacer></v-spacer>

      <!-- Back to Course Modules Button -->
      <v-btn @click="goBackToModules" color="white">
        Back to Modules
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
              <v-card-title class="headline">{{ moduleTitle }}</v-card-title>
              <v-divider></v-divider>

              <!-- Lectures Section -->
              <v-card-subtitle class="mt-3 mb-2">Lectures</v-card-subtitle>
              <v-list two-line>
                <v-list-item v-for="lecture in lectures" :key="lecture.id" class="mt-3">
                  <v-row>
                    <v-col>
                      <v-list-item-title>{{ lecture.title }}</v-list-item-title>
                      <v-list-item-subtitle>
                        <a :href="lecture.url" target="_blank">Watch Lecture</a>
                      </v-list-item-subtitle>
                    </v-col>
                  </v-row>
                </v-list-item>

                <v-list-item v-if="lectures.length === 0">
                  <v-list-item-title>No lectures available</v-list-item-title>
                </v-list-item>
              </v-list>

              <!-- Assignments Section -->
              <v-divider class="my-4"></v-divider>
              <v-card-subtitle class="mb-2">Assignments</v-card-subtitle>
              <v-list two-line>
                <v-list-item v-for="assignment in assignments" :key="assignment.id" class="mt-3">
                  <v-row>
                    <v-col>
                      <v-list-item-title>{{ assignment.title }}</v-list-item-title>
                      <v-list-item-subtitle>{{ assignment.description }}</v-list-item-subtitle>
                      <v-list-item-subtitle>Due Date: {{ formatDueDate(assignment.due_date) }}</v-list-item-subtitle>
                    </v-col>
                  </v-row>
                </v-list-item>

                <v-list-item v-if="assignments.length === 0">
                  <v-list-item-title>No assignments available</v-list-item-title>
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
import { defineComponent } from 'vue';
import axios from 'axios';
import { mapState } from 'vuex';
import { useRoute, useRouter } from 'vue-router';

const BASE_URL = 'http://localhost:8000';

export default defineComponent({
  name: 'ModuleDetails',
  data() {
    return {
      moduleTitle: '',
      lectures: [] as Array<{ id: number; title: string; url: string; transcript: string }>,
      assignments: [] as Array<{
        id: number;
        title: string;
        description: string;
        type: string;
        due_date: string;
      }>,
    };
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const courseId = route.params.courseId;
    const moduleId = route.params.moduleId;

    return { courseId, moduleId, router };
  },
  computed: {
    ...mapState(['user']),
  },
  methods: {
    async fetchModuleContent(moduleId: string) {
      try {
        const response = await axios.get(BASE_URL + `/student/module-content/${moduleId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
          },
        });
        this.lectures = response.data.lectures;
        this.assignments = response.data.assignments;
      } catch (error) {
        console.error('Error fetching module content:', error);
      }
    },
    goBackToModules() {
      this.$router.push(`/course-modules/${this.courseId}`);
    },
    formatDueDate(dueDate: string): string {
      return new Date(dueDate).toLocaleDateString();
    },
    logout() {
      this.$store.dispatch('signOut');
    },
  },
  async mounted() {
    const moduleId = Array.isArray(this.$route.params.moduleId)
      ? this.$route.params.moduleId[0]
      : this.$route.params.moduleId;

    await this.fetchModuleContent(moduleId as string);
    this.moduleTitle = this.$route.params.moduleTitle as string;
  },
});
</script>

<style scoped>
.headline {
  font-family: 'Montserrat', sans-serif;
  margin-bottom: 20px;
  text-align: center;
}

.v-list-item-subtitle {
  word-break: break-word; /* Ensures long words wrap to the next line */
}
</style>
