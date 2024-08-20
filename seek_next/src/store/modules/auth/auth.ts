import authActions from "./authActions";
import authMutations from "./authMutations";

export interface AuthState {
    user: {
        id: string;
        name: string;
        email: string;
        role: string;
    };
    accessToken: string | null;
    isLoggedIn: boolean;
}

const state: AuthState = {
    user: {
        id: "",
        name: "",
        email: "",
        role: "",
    },
    accessToken: null,
    isLoggedIn: false,
};

const mutations = {
    ...authMutations,
};

const actions = {
    ...authActions,
};

const getters = {
    isAuthenticated(state: { isLoggedIn: any; }) {
        return state.isLoggedIn;
    },
    user(state: { user: any; }) {
        return state.user;
    },
};

export const authModel = {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
};
