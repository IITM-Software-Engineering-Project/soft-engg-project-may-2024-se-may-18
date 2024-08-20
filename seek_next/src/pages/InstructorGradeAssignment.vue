<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Grade Assignment: {{ assignmentId }}</v-toolbar-title>
      <v-spacer></v-spacer>

      <!-- View All Courses Button -->
      <v-btn @click="goToDashboard" color="white">
        {{ username }}
      </v-btn>

      <!-- Logout Button -->
      <v-btn @click="logout" color="white" variant="outlined" append-icon="mdi-account-circle">
        <v-icon>mdi-logout</v-icon>
        Logout
      </v-btn>
    </v-app-bar>
    <v-main>
      <v-container>
        <v-row justify="center">
          <v-col cols="12" md="8">
            <v-card>
              <v-card-title class="headline">Grade Assignment</v-card-title>
              <v-divider></v-divider>
              <v-list>
                <v-list-item-group>
                  <v-list-item v-for="(answer, index) in fetchAssignmentAnswers" :key="index">
                    <v-list-item-content>
                      <v-row>
                        <v-col> Student ID: {{ answer.student_id }} </v-col>
                        <v-col class="button-col">
                          <div class="button-container">
                            <v-btn @click="gradeManually(answer)" color="primary">
                              Grade Manually
                            </v-btn>
                            <v-btn @click="gradeUsingAI(answer)" color="secondary">
                              Grade using AI
                            </v-btn>
                          </div>
                        </v-col>
                      </v-row>
                    </v-list-item-content>
                  </v-list-item>
                </v-list-item-group>
              </v-list>
            </v-card>
          </v-col>
        </v-row>
      </v-container>

      <!-- Manual Grading Dialog -->
      <v-dialog v-model="manualGradeDialog" max-width="1200px">
        <v-card>
          <v-card-title>Grade Manually</v-card-title>
          <v-card-text>
            <p>
              <strong>Student Answer:</strong>
              {{ selectedAnswer.assignment_answer }}
            </p>
            <v-text-field v-model="marks" label="Marks"></v-text-field>
            <v-text-field v-model="feedback" label="Feedback"></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="submitManualGrade">Submit</v-btn>
            <v-btn @click="manualGradeDialog = false">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- AI Grading Dialog -->
      <v-dialog v-model="aiGradeDialog" max-width="1200px">
        <v-card>
          <v-card-title>Grade using AI</v-card-title>
          <v-card-text>
            <p>
              <strong>Student Answer:</strong>
              {{ selectedAnswer.assignment_answer }}
            </p>
            <v-textarea v-model="aiPrompt" label="Enter your prompt"></v-textarea>
            <v-btn @click="submitAIGrade(selectedAnswer.assignment_answer)" color="primary">
              Get Response
            </v-btn>

            <!-- Directly bind the value to the model -->
            <v-text-field v-model="marks" label="Marks"
              :value="aiResponse ? aiResponse['score'] : selectedAnswer.marks"></v-text-field>
            <v-textarea v-model="feedback" label="Feedback" :value="aiResponse ? aiResponse['description'] : selectedAnswer.feedback
              "></v-textarea>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="aiGradeDialog = false">Submit</v-btn>
            <v-btn @click="aiGradeDialog = false">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { useRoute, useRouter } from "vue-router";
import axios from "axios"; // Use Axios for API calls
const BASE_URL = "http://localhost:8000";
export default {
  name: "InstructorGradeAssignment",
  data() {
    return {
      aiGradeDialog: false,
      aiPrompt: "",
      aiResponse: null,
      manualGradeDialog: false,
      marks: "",
      feedback: "",
      selectedAnswer: {
        assignment_answer: "",
        marks: "",
        feedback: "",
      },
      selectedQuestion: "",
    };
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const assignmentId = route.params.assignmentId as string;
    const goToDashboard = () => {
      router.push("/instructor-home");
    };

    // Temporary mock data
    const mockAssignmentAnswers = [
      {
        student_id: 11,
        assignment_answer:
          "In past group projects, the main issue often boiled down to poor communication and unclear roles, which are characteristic of the 'Storming' phase in Tuckman’s model. Team members, myself included, were quick to point out others’ mistakes without reflecting on our own shortcomings. This created an environment where criticism was more common than constructive feedback. According to the 10Cs of teamwork, especially 'Clarity' and 'Commitment,' focusing on clear communication and understanding individual responsibilities could have mitigated these problems. By taking more personal accountability and ensuring that everyone was on the same page, the group could have moved more smoothly into the 'Norming' and 'Performing' stages, leading to better project outcomes.",
        marks: null,
        submitted_at: "2024-08-16T10:15:00",
        graded_at: "2024-08-17T14:30:00",
        feedback: "",
      },
      {
        student_id: 12,
        assignment_answer:
          "One of the biggest issues in previous group projects was that team members, including myself, tended to focus on the mistakes of others rather than evaluating our own performance. This often led to conflicts during the 'Storming' phase of Tuckman’s model. For instance, in a marketing project, we spent more time arguing over who was at fault for delays rather than addressing our own shortcomings. The lack of adherence to the 10Cs of teamwork, particularly 'Collaboration' and 'Communication,' resulted in unresolved conflicts and a lack of progress. If we had focused more on personal responsibility and fostering open communication, we could have resolved these issues and moved forward more effectively.",
        marks: null,
        submitted_at: "2024-08-16T11:00:00",
        graded_at: "2024-08-17T15:00:00",
        feedback: "",
      },
      {
        student_id: 13,
        assignment_answer:
          "In group projects, a common problem was that team members, including myself, spent too much time evaluating others' actions rather than our own. For example, during a project, team conflicts arose because we were focused on pointing out others’ mistakes instead of improving our own contributions. This created a toxic environment that hindered our ability to move past the 'Storming' phase of Tuckman’s model. If each member had focused more on their responsibilities, aligned with the 10Cs of teamwork, particularly 'Accountability' and 'Collaboration,' we might have moved to the 'Norming' stage more quickly. This could have led to a more supportive and productive team environment, ultimately resulting in a more successful project outcome.",
        marks: null,
        submitted_at: "2024-08-16T12:00:00",
        graded_at: "2024-08-17T16:00:00",
        feedback: "",
      },
    ];

    return {
      goToDashboard,
      assignmentId,
      mockAssignmentAnswers,
    };
  },
  mounted() {
    this.fetchAssignmentAnswers = this.mockAssignmentAnswers;
  },
  methods: {
    username() {
      return this.$store.getters["auth/user"].username;
    },
    logout() {
      this.$store.dispatch("auth/signOut");
    },
    gradeManually(answer) {
      this.selectedAnswer = answer;
      this.marks = answer.marks;
      this.feedback = answer.feedback;
      this.manualGradeDialog = true;
    },
    gradeUsingAI(answer) {
      this.selectedAnswer = answer;
      this.aiPrompt = "";
      this.aiResponse = null;
      this.marks = answer.marks;
      this.manualGradeDialog = false;
      this.feedback = answer.feedback;
      this.aiGradeDialog = true;
    },
    async submitManualGrade() {
      // Handle manual grade submission
      this.manualGradeDialog = false;
    },
    async submitAIGrade() {
      try {
        const response = await axios.post(
          BASE_URL + "/grade-text-question",
          {
            question: this.aiPrompt,
            answer: this.selectedAnswer.assignment_answer,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        const result = response.data;
        this.aiResponse = result;
      } catch (error) {
        console.error("Error grading with AI:", error);
      }
    },
  },
};
</script>

<style scoped>
.headline {
  font-family: "Montserrat", sans-serif;
  margin-bottom: 20px;
  text-align: center;
}

.v-list-item-title {
  font-weight: 500;
}

.v-card {
  padding: 20px;
}

.v-list-item {
  cursor: pointer;
}

.button-col {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.button-container {
  display: flex;
  gap: 10px;
  /* Add space between buttons */
}
</style>
