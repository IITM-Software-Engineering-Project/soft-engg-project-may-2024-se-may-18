import instructorActions from '../instructor/instructorActions';
import instructorMutations from '../instructor/instructorMutations';

export interface InstructorCourse {
    id: string;
    title: string;
    description?: string;
    total_students?: number;
    price?: string;
}

export interface InstructorState {
    createdCourses: InstructorCourse[];
    loading: {
        fetchingCreatedCourses: string;
    };
}

const state: InstructorState = {
    createdCourses: [],
    loading: {
        fetchingCreatedCourses: 'loading',
    },
};

const mutations = {
    ...instructorMutations,
};

const actions = {
    ...instructorActions,
};

const getters = {
    instructorCourses(state: { createdCourses: any; }) {
        return state.createdCourses;
    },
};

export const instructorModel = {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
};
