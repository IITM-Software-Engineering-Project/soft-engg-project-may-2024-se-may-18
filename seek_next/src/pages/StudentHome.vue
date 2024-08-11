<template>
  <v-container>
    <v-row>
      <v-col>
        <h2>Your Enrolled Courses</h2>
        <!-- List of Enrolled Courses -->
        <v-list >
            <v-list-item v-for="course in enrolledCourses" :key="course['id']">
              <v-list-item-title>{{ course['title'] }}</v-list-item-title>
      
            </v-list-item>
            <v-list-item v-if="enrolledCourses.length === 0">
              <v-list-item-title>No courses enrolled</v-list-item-title>
            </v-list-item>
        </v-list>
    
        <!-- Button to View All Courses -->
        <v-btn @click="goToAllCourses" color="primary" class="mt-4">
          View All Courses
        </v-btn>
        <v-btn @click="logout">Logout</v-btn>
      </v-col>
    </v-row>
  </v-container>

</template>

<script lang="ts">
import { mapGetters } from 'vuex'


export default {
  name: 'student-home',
  data() {
    return {
      studentId : '11',
    }
  },

  mounted() {
      this.$store.dispatch('fetchEnrolledCourses', this.studentId);
  },

  computed: {
    ...mapGetters({
      enrolledCourses: 'enrolledCourses',
  }) ,
  },
  methods: {
    goToAllCourses() {
      this.$router.push('/all-courses');
    },
    logout() {
      this.$store.dispatch('signOut')
    }
  },
  
};
</script>

<style scoped>
h2 {
  font-family: 'Montserrat', sans-serif;
  margin-bottom: 20px;
}
</style>
