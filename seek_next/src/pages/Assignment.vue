<template>
  <v-app>
    <!-- Navigation Bar -->
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>{{ assignmentTitle }}</v-toolbar-title>
      <v-spacer></v-spacer>

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
              <v-card-title class="headline">{{ assignmentTitle }}</v-card-title>
              <v-card-subtitle class="mb-3">{{ assignmentDescription }}</v-card-subtitle>

              <!-- Questions Section -->
              <v-form @submit.prevent="submitAssignment">
                <v-list two-line>
                  <v-list-item v-for="question in questions" :key="question.id" class="mt-3">
                    <v-row>
                      <v-col>
                        <v-list-item-title>{{ question.question }}</v-list-item-title>
                        <v-radio-group v-model="userAnswers[question.id]" mandatory>
                          <v-radio v-for="(answer, key) in question.answer_choices" :key="key"
                            :label="`${key}: ${answer}`" :value="key"></v-radio>
                        </v-radio-group>
                      </v-col>
                    </v-row>
                  </v-list-item>
                </v-list>
                <!-- Submit Button -->
                <v-btn type="submit" color="primary" class="mt-4">Submit Assignment</v-btn>
              </v-form>

              <!-- Results Section -->
              <v-card v-if="assignmentSubmitted" class="mt-4">
                <v-card-title>Results</v-card-title>
                <v-card-text>
                  You scored {{ score }} out of {{ questions.length }}.
                </v-card-text>

                <!-- Correct Answers Section -->
                <v-list v-for="question in questions" :key="question.id" class="mt-3">
                  <v-list-item>
                    <v-row>
                      <v-col>
                        <v-list-item-title>{{ question.question }}</v-list-item-title>
                        <v-list-item-subtitle>
                          Correct Answer: {{ question.answer }} - {{ question.answer_choices[question.answer] }}
                        </v-list-item-subtitle>
                      </v-col>
                    </v-row>
                  </v-list-item>
                </v-list>
              </v-card>
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
import { useRoute, useRouter } from 'vue-router';

const BASE_URL = 'http://localhost:8000';

export default defineComponent({
  name: 'Assignment',
  data() {
    return {
      assignmentTitle: '',
      assignmentDescription: '',
      questions: [] as Array<{
        id: number;
        question: string;
        answer_choices: Record<string, string>;
        answer: string;
      }>,
      userAnswers: {} as Record<number, string>, // Stores user-selected answers
      assignmentSubmitted: false, // Track if the assignment is submitted
      score: 0, // Stores the user's score
    };
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const assignmentId = route.params.assignmentId;

    return { assignmentId, router };
  },
  methods: {
    async fetchAssignmentContent(assignmentId: string) {
      try {
        const response = await axios.get(BASE_URL + `/student/assignment-content/${assignmentId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
          },
        });

        this.assignmentTitle = response.data.assignment.title;
        this.assignmentDescription = response.data.assignment.description;
        this.questions = response.data.questions.map((question: any) => ({
          id: question.id,
          question: question.question,
          answer_choices: JSON.parse(question.answer_choices),
          answer: question.answer,
        }));

      } catch (error) {
        console.error('Error fetching assignment content:', error);
      }
    },
    submitAssignment() {
      this.score = 0;
      this.questions.forEach((question) => {
        if (this.userAnswers[question.id] === question.answer) {
          this.score += 1;
        }
      });
      this.assignmentSubmitted = true;
    },
    //   goBackToModule() {
    //     this.router.push(`/course-modules/${this.$route.params.courseId}`);
    //   },
    logout() {
      this.$store.dispatch('auth/signOut');
    },
  },
  mounted() {
    this.fetchAssignmentContent(this.assignmentId.toString());
  },
});
</script>

<style scoped>
/* Styles for the Assignment page */
.v-card {
  margin-bottom: 16px;
}

.v-btn {
  margin-right: 8px;
}

.v-radio-group {
  margin-top: 16px;
}
</style>