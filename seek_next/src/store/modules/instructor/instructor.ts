import { Module } from 'vuex';
import instructorActions from '../instructor/instructorActions';
import instructorMutations from '../instructor/instructorMutations';
import { State } from '../../store';

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
    createdCourses(state: InstructorState) {
        return state.createdCourses;
    },
};

export const instructorModel: Module<InstructorState, State> = {
    state,
    mutations,
    actions,
    getters,
};
