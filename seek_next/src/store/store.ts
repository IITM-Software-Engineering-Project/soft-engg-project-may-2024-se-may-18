import { InjectionKey } from "vue";
import { createStore, Store } from "vuex";
import { authModel } from "./modules/auth/auth";
import { studentModel } from "./modules/student/student";
// Import the instructor model once created
// import { instructorModel } from "./modules/instructor/instructor"; 

export class Loading {
  static readonly loading = "loading";
  static readonly loaded = "loaded";
  static readonly error = "error";
}

export interface State {
  // Define only global state properties here, if any
}

export const key: InjectionKey<Store<State>> = Symbol();

export const store = createStore<State>({
  // Define any global state here, if needed
  state: {
  },
  modules: {
    auth: authModel, // Namespaced module
    student: studentModel, // Namespaced module
    // instructor: instructorModel, // Uncomment when you create the instructor model
  },
  // Global mutations
  mutations: {},
  // Global actions
  actions: {},
  // Global getters
  getters: {},
});
