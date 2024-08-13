import axios from 'axios';
import { ActionContext } from 'vuex';
import { State } from '../Store';

const BASE_URL = 'http://localhost:8000';

export default {
    async fetchEnrolledCourses({ commit }: ActionContext<State, State>, studentId: string) {
        try {
            const response = await axios.get(`${BASE_URL}/student/enrolled-courses/${studentId}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
                },
            });
            commit('setEnrolledCourses', response.data);
        } catch (error) {
            console.error('Error fetching enrolled courses:', error);
        }
    },
    async fetchAllCourses({ commit }: ActionContext<State, State>,) {
        try {
            const response = await axios.get(`${BASE_URL}/courses/list`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
                },
            });
            commit('setAllCourses', response.data);
        } catch (error) {
            console.error('Error fetching all courses:', error);
        }
    },
    async enrollInCourse({ commit }: ActionContext<State, State>, { studentId, courseId }: { studentId: string, courseId: string }) {
        try {
            const response = await axios.post(`${BASE_URL}/student/enroll`, {
                student_id: studentId,
                course_id: courseId,
            }, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
                },
            });
            console.log(response.data.message);
            commit('addEnrolledCourse', courseId);
        } catch (error) {
            console.error('Error enrolling in course:', error);
            throw error;
        }
    },
};