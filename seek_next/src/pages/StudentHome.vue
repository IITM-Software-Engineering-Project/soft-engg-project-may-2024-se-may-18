<template>
  <v-container>
    <v-row>
      <v-col>
        <h2>Your Enrolled Courses</h2>
        <!-- List of Enrolled Courses -->
        <v-list dense>
          <v-list-item v-for="course in enrolledCourses" :key="course.id">
            <v-list-item-content>
              <v-list-item-title>{{ course.title }}</v-list-item-title>
              <v-list-item-subtitle>{{ course.description }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
        <!-- Button to View All Courses -->
        <v-btn @click="goToAllCourses" color="primary" class="mt-4">
          View All Courses
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import { useStore } from 'vuex';
import { State } from '../store/Store.ts'; // Import the State interface

export default defineComponent({
  name: 'student-home',
  setup() {
    const store = useStore<State>();
    const studentId = '11'; // Replace with dynamic student ID if needed

    onMounted(() => {
      store.dispatch('fetchEnrolledCourses', studentId);
    });

    return {
      enrolledCourses: store.getters.enrolledCourses,
    };
  },
  methods: {
    goToAllCourses() {
      this.$router.push('/all-courses');
    },
  },
});
</script>

<style scoped>
h2 {
  font-family: 'Montserrat', sans-serif;
  margin-bottom: 20px;
}
</style>
