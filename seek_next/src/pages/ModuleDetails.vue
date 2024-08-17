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
                      <!-- Increased font size for lecture title -->
                      <v-list-item-title class="lecture-title">{{ lecture.title }}</v-list-item-title>
                      <br/>
                      <!-- Embed YouTube player -->
                      <v-list-item-subtitle>
                        <div v-if="isYouTubeUrl(lecture.url)">
                          <iframe
                            :src="getYouTubeEmbedUrl(lecture.url)"
                            width="100%"
                            height="315"
                            frameborder="0"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowfullscreen
                          ></iframe>
                        </div>
                        <a v-else :href="lecture.url" target="_blank" class="watch-lecture-link">Watch Lecture</a>
                      </v-list-item-subtitle>
                      <!-- Summarize Transcript Button -->
                      <v-btn @click="summarizeTranscript(lecture.id)" color="teal-darken-2" class="mt-2" elevation="2">
                        Summarize Transcript
                      </v-btn>
                      <!-- Summary Response Display -->
                      <v-card v-if="summaryResponse[lecture.id]" class="mt-3 summary-card" elevation="2">
                        <v-card-title>Transcript Summary using GenAI</v-card-title>
                        <v-card-text v-html="summaryResponse[lecture.id]" class="summary-text"></v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>
                  <!-- Separator after each lecture -->
                  <v-divider class="my-3"></v-divider>
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
                  <!-- Separator after each assignment -->
                  <v-divider class="my-3"></v-divider>
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
      summaryResponse: {} as Record<number, string>, // To store summary responses by lecture ID
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
    async summarizeTranscript(lectureId: number) {
      try {
        const response = await fetch(`/transcript_data/${lectureId}.txt`);
        if (response.ok) {
          const transcriptData = await response.text();
          if (transcriptData.includes('<!doctype html>')) {
            this.summaryResponse[lectureId] = 'Transcript data not available for this module';
          } else {
            const summaryResponse = await axios.post(BASE_URL + '/ai-summarize-transcript', {
              prompt: 'Summarize the following transcript:',
              data: transcriptData,
            }, {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
                'Content-Type': 'application/json',
              },
            });
            console.log('Summary response:', summaryResponse.data);
            this.summaryResponse[lectureId] = this.formatMessage(summaryResponse.data.message);
          }
        } else {
          this.summaryResponse[lectureId] = 'Transcript data not available for this module';
        }
      } catch (error) {
        console.error('Error summarizing transcript:', error);
        this.summaryResponse[lectureId] = 'Transcript data not available for this module';
      }
    },
    formatMessage(message: string): string {
      return message.replace(/\n/g, '<br>');
    },
    isYouTubeUrl(url: string): boolean {
      return /youtube\.com\/watch\?v=/.test(url) || /youtu\.be/.test(url);
    },
    getYouTubeEmbedUrl(url: string): string {
      const videoId = url.split(/v=|\/videos\/|youtu\.be\//).pop()?.split('&')[0];
      return `https://www.youtube.com/embed/${videoId}`;
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

.v-list-item-title {
  font-size: 1.5rem; /* Increased font size for lecture title */
  font-weight: bold;
}

.watch-lecture-link {
  font-size: 1rem; /* Font size for link */
  color: #1E88E5;
  text-decoration: underline;
}

.summary-card {
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
}

.summary-text {
  font-size: 14px;
  color: #333;
}

.lecture-title {
  text-decoration: underline;
  font-size: 1.5rem;
  font-weight: bold;
}

iframe {
  border-radius: 8px;
}

.v-divider {
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>
