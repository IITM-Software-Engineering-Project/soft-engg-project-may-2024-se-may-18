import axios from 'axios';
import { ActionContext } from 'vuex';
import { InstructorState } from './instructor';
import { State } from '../../store';

const BASE_URL = 'http://localhost:8000';

export default {
    async fetchCreatedCourses({ commit }: ActionContext<InstructorState, State>, instructorId: string) {
        try {
            commit('setLoadingFetchingCreatedCourses', 'loading');
            const response = await axios.get(`${BASE_URL}/instructor/created-courses/${instructorId}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
                },
            });
            commit('setCreatedCourses', response.data);
            commit('setLoadingFetchingCreatedCourses', 'loaded');
        } catch (error) {
            console.error('Error fetching created courses:', error);
            commit('setLoadingFetchingCreatedCourses', 'error');
        }
    },
    async fetchInstructorCourses(
        { commit }: ActionContext<InstructorState, State>,
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
        { commit }: ActionContext<InstructorState, State>,
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
