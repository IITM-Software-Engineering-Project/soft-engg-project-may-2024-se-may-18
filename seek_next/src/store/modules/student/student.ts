import { Module } from 'vuex';
import { State } from '../../store';
import courseActions from './studentActions';
import courseMutations from './studentMutations';

export class Loading {
    static readonly loading = "loading";
    static readonly loaded = "loaded";
    static readonly error = "error";
}

export interface Course {
    id: string;
    title: string;
    description?: string;
    total_modules?: string;
    price?: string;
}

export interface StudentState {
    enrolledCourses: Course[];
    allCourses: Course[];
    loading: {
        fetchingEnrolledCourses: string;
        fetchingAllCourses: string;
    };
}

const state: StudentState = {
    enrolledCourses: [],
    allCourses: [],
    loading: {
        fetchingEnrolledCourses: Loading.loading,
        fetchingAllCourses: Loading.loading,
    },
};

const mutations = {
    ...courseMutations,
};

const actions = {
    ...courseActions,
};

const getters = {
    enrolledCourses(state: { enrolledCourses: any; }) {
        return state.enrolledCourses;
    },
    allCourses(state: { allCourses: any; }) {
        return state.allCourses;
    },
};

export const studentModel: Module<StudentState, State> = {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
};
