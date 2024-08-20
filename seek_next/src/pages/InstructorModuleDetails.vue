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
                      <v-list-item-title class="text-h5">{{ lecture.title }}</v-list-item-title>
                      <!-- Embedded YouTube Video -->
                      <v-responsive class="my-3">
                        <iframe width="100%" height="315"
                          :src="`https://www.youtube.com/embed/${getYouTubeVideoId(lecture.url)}`" frameborder="0"
                          allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                          allowfullscreen></iframe>
                      </v-responsive>
                      <!-- <v-list-item-subtitle>
                        <a :href="lecture.url" target="_blank">Watch Lecture</a>
                      </v-list-item-subtitle> -->
                      <!-- Summarize Transcript Button -->
                      <v-btn @click="summarizeTranscript(lecture.id)" color="teal-darken-2" class="mt-2">
                        Summarize Transcript
                      </v-btn>
                      <!-- Ask Question Button -->
                      <v-btn @click="openQuestionDialog(lecture.id)" color="secondary" class="mt-2">
                        Ask Question
                      </v-btn>
                      <!-- Response Section -->
                      <v-card v-if="responseTitle[lecture.id]" class="mt-3">
                        <v-card-title>{{ responseTitle[lecture.id] }}</v-card-title>
                        <v-card-text v-html="formatMessage(summaryResponse[lecture.id])"></v-card-text>
                      </v-card>
                      <br />
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
                    <v-col class="text-right">
                      <!-- Button to go to Module -->
                      <v-btn @click="gradeAssignment(assignment.id, assignment.type)" color="#BA68C8" size="small">
                        Grade
                      </v-btn>
                      <v-btn @click="goToAssignments(assignment.id, assignment.type)" color="#BA68C8" size="small">
                        Go to Assignment
                      </v-btn>
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

      <!-- Question Dialog -->
      <v-dialog v-model="questionDialog" max-width="500px">
        <v-card>
          <v-card-title class="headline">Ask a Question</v-card-title>
          <v-card-subtitle>Enter your question related to the transcript:</v-card-subtitle>
          <v-card-text>
            <v-textarea v-model="question" outlined rows="4"></v-textarea>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="submitQuestion" color="primary">Submit</v-btn>
            <v-btn @click="questionDialog = false" color="grey">Cancel</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
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
  name: 'InstructorModuleDetails',
  data() {
    return {
      moduleTitle: '',
      lectures: [] as Array<{ id: number; title: string; url: string; transcript: string }>,
      assignments: [] as Array<{
        id: string;
        title: string;
        description: string;
        type: string;
        due_date: string;
      }>,
      summaryResponse: {} as Record<number, string>, // To store summary responses by lecture ID
      responseTitle: {} as Record<number, string>, // To store the title for the response section
      questionDialog: false, // Controls the visibility of the question dialog
      question: '', // Stores the question entered by the user
      selectedLectureId: null as number | null, // Stores the selected lecture ID for the question dialog
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
      this.$router.push(`/instructor/course-modules/${this.courseId}`);
    },
    goToAssignments(assignmentId: string, assignmentType: string) {
      // this.$router.push(`/assignment-details/${assignmentId}`);
      console.log('Go to module:', assignmentId, assignmentType);
    },
    gradeAssignment(assignmentId: string, assignmentType: string) {
      this.$router.push(`/instructor/grade-assignment/${assignmentId}`);
      console.log('Go to module:', assignmentId, assignmentType);
    },
    formatDueDate(dueDate: string): string {
      return new Date(dueDate).toLocaleDateString();
    },
    logout() {
      this.$store.dispatch('auth/signOut');
    },
    async summarizeTranscript(lectureId: number) {
      try {
        const response = await fetch(`/transcript_data/${lectureId}.txt`);
        if (response.ok) {
          const transcriptData = await response.text();
          if (transcriptData.includes('<!doctype html>')) {
            this.summaryResponse[lectureId] = 'Transcript data not available for this module';
            this.responseTitle[lectureId] = 'Transcript Summary';
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
            this.summaryResponse[lectureId] = this.formatMessage(summaryResponse.data.message);
            this.responseTitle[lectureId] = 'Transcript Summary';
          }
        } else {
          this.summaryResponse[lectureId] = 'Transcript data not available for this module';
          this.responseTitle[lectureId] = 'Transcript Summary';
        }
      } catch (error) {
        console.error('Error summarizing transcript:', error);
        this.summaryResponse[lectureId] = 'Transcript data not available for this module';
        this.responseTitle[lectureId] = 'Transcript Summary';
      }
    },
    openQuestionDialog(lectureId: number) {
      this.selectedLectureId = lectureId;
      this.questionDialog = true;
    },
    async submitQuestion() {
      if (this.selectedLectureId !== null) {
        try {
          const response = await fetch(`/transcript_data/${this.selectedLectureId}.txt`);
          if (response.ok) {
            const transcriptData = await response.text();
            if (transcriptData.includes('<!doctype html>')) {
              this.summaryResponse[this.selectedLectureId] = 'Transcript data not available for this module';
              this.responseTitle[this.selectedLectureId] = 'GenAI Response';
            } else {
              const aiResponse = await axios.post(BASE_URL + '/ai-summarize-transcript', {
                prompt: this.question,
                data: transcriptData,
              }, {
                headers: {
                  Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
                  'Content-Type': 'application/json',
                },
              });
              this.summaryResponse[this.selectedLectureId] = this.formatMessage(aiResponse.data.message);
              this.responseTitle[this.selectedLectureId] = 'GenAI Response';
            }
          } else {
            this.summaryResponse[this.selectedLectureId] = 'Transcript data not available for this module';
            this.responseTitle[this.selectedLectureId] = 'GenAI Response';
          }
        } catch (error) {
          console.error('Error asking question:', error);
          this.summaryResponse[this.selectedLectureId] = 'Transcript data not available for this module';
          this.responseTitle[this.selectedLectureId] = 'GenAI Response';
        }
      }
      this.questionDialog = false;
    },
    formatMessage(message: string): string {
      return message.replace(/\n/g, '<br>');
    },
    getYouTubeVideoId(url: string): string {
      const regex = /(?:https?:\/\/)?(?:www\.)?youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=|\/)([a-zA-Z0-9_-]{11})/;
      const match = url.match(regex);
      return match ? match[1] : '';
    },
  },
  mounted() {
    this.fetchModuleContent(this.moduleId.toString());
    this.moduleTitle = this.$route.params.moduleTitle as string;
  },
});
</script>

<style scoped>
/* Styles for the ModuleDetails page */
.v-list-item {
  border-bottom: 1px solid #ddd;
}

.v-card {
  margin-bottom: 16px;
}

.v-btn {
  margin-right: 8px;
}

.v-dialog .v-card {
  min-width: 400px;
}

.v-card-subtitle {
  font-weight: bold;
}

.text-h5 {
  font-size: 1.25rem;
}

.text-h1 {
  font-size: 2rem;
  font-weight: 700;
}

.text-h4 {
  font-size: 1.5rem;
  font-weight: 400;
}

.v-responsive {
  margin: 0;
}

.v-img {
  margin: 0 auto;
}

.v-dialog .v-card {
  min-width: 400px;
}

.v-btn {
  margin-top: 16px;
}
</style>
