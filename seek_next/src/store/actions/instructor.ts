import axios from 'axios';
import { ActionContext } from 'vuex';
import { State } from '../Store';

const BASE_URL = 'http://localhost:8000';

export default {
    async fetchInstructorCourses(
      { commit }: ActionContext<State, State>,
      instructorId: number
    ) {
      try {
        const response = await axios.get(`${BASE_URL}/instructor/courses/${instructorId}`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
            },
        });
        commit('setInstructorCourses', response.data);
      } catch (error) {
        console.error('Error fetching enrolled courses:', error);
      }
    },
    async fetchAssignmentAnswers(
        { commit }: ActionContext<State, State>,
        assignmentId: number
      ) {
        try {
          const response = await axios.get(`${BASE_URL}/get-assignment-answers`, {
            params: {
              assignment_id: assignmentId,
            },
            headers: {
              Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
            },
          });
          commit('setAssignmentAnswers', response.data);
        } catch (error) {
          console.error('Error fetching assignment answers:', error);
        }
      },
  };