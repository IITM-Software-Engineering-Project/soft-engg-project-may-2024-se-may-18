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
  };