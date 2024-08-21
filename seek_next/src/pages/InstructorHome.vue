<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Instructor Dashboard</v-toolbar-title>
      <v-spacer></v-spacer>

      <!-- View All Courses Button -->
      <v-btn @click="goToDashboard" color="white">
        Jane Smith
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
              <v-card-title class="headline">Your Courses</v-card-title>
              <v-divider></v-divider>

              <v-list v-if="instructorCourses.length">
                <v-list-item v-for="course in instructorCourses" :key="course.course_id">
                  <v-list-item-content>
                    <v-row>
                      <v-col>
                        <v-list-item-title>{{
                          course.course_name
                          }}</v-list-item-title>
                        <v-list-item-subtitle>{{
                          course.description
                          }}</v-list-item-subtitle>
                      </v-col>
                      <v-col class="button-col">
                        <div class="button-container">
                          <v-btn icon @click="viewCourse(course.course_id)">
                            <v-icon>mdi-eye</v-icon>
                          </v-btn>
                          <v-btn icon @click="editCourse(course.course_id)">
                            <v-icon>mdi-pencil</v-icon>
                          </v-btn>
                          <v-btn icon @click="deleteCourse(course.course_id)">
                            <v-icon>mdi-delete</v-icon>
                          </v-btn>
                        </div>
                      </v-col>
                    </v-row>
                  </v-list-item-content>
                </v-list-item>
              </v-list>

              <v-alert v-else type="info"> No courses available. </v-alert>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { mapGetters } from "vuex";
import { useRouter } from "vue-router";

export default {
  name: "instructor-home",
  setup() {
    const router = useRouter();
    const goToDashboard = () => {
      router.push("/instructor-home");
    };
    return {
      goToDashboard,
    };
  },
  mounted() {
    this.$store.dispatch("instructor/fetchInstructorCourses", this.$store.getters["auth/user"].id);
  },
  computed: {
    ...mapGetters({
      instructorCourses: "instructor/instructorCourses",
    }),
  },
  methods: {
    username() {
      return this.$store.getters["auth/user"].username;
    },
    viewCourse(courseId: number) {
      this.$router.push(`/instructor/course-modules/${courseId}`);
    },
    editCourse(courseId: number) {
      this.$router.push(`/edit-course/${courseId}`);
    },
    deleteCourse(courseId: number) {
      // Add logic to delete the course here
      console.log(`Course with ID ${courseId} deleted.`);
    },
    logout() {
      this.$store.dispatch("auth/signOut");
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
