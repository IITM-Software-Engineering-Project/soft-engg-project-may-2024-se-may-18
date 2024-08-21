import axios from 'axios';
import { ActionContext } from 'vuex';
import { State, store, Loading } from '../../store';
import { StudentState } from './student';


const BASE_URL = 'http://localhost:8000';

export default {
    async fetchEnrolledCourses({ commit }: ActionContext<StudentState, State>, studentId: string) {
        try {
            commit('setLoadingFetchingEnrolledCourses', Loading.loading);
            const response = await axios.get(`${BASE_URL}/student/enrolled-courses/${studentId}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
                },
            });
            commit('setEnrolledCourses', response.data);
            commit('setLoadingFetchingEnrolledCourses', Loading.loaded);
        } catch (error) {
            console.error('Error fetching enrolled courses:', error);
            commit('setLoadingFetchingEnrolledCourses', Loading.error);
        }
    },
    async fetchAllCourses({ commit }: ActionContext<StudentState, State>,) {
        try {
            commit('setLoadingFetchingAllCourses', Loading.loading);
            const response = await axios.get(`${BASE_URL}/courses/list`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
                },
            });
            commit('setAllCourses', response.data);
            commit('setLoadingFetchingAllCourses', Loading.loaded);
        } catch (error) {
            console.error('Error fetching all courses:', error);
            commit('setLoadingFetchingAllCourses', Loading.error);
        }
    },
    async enrollInCourse({ commit }: ActionContext<StudentState, State>, { studentId, courseId }: { studentId: string, courseId: string }) {
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