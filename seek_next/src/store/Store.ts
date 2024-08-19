import { InjectionKey } from "vue";
import { createStore, Store } from "vuex";
import authActions from "./actions/auth";
import courseActions from "./actions/course";
import instructorActions from "./actions/instructor";

export interface State {
  user: {
    id: string;
    name: string;
    email: string;
    role: string;
  };
  accessToken: string | null;
  isLoggedIn: boolean;
  enrolledCourses: Course[];
  allCourses: Course[];
  instructorCourses: Course[];
}

export interface ComponentCustomProperties {
  $store: Store<State>;
}

interface Course {
  id: string;
  title: string;
  description?: string;
  total_modules?: string;
  price?: string;
}

export const key: InjectionKey<Store<State>> = Symbol();

export const store = createStore<State>({
  state: {
    user: {
      id: "",
      name: "",
      email: "",
      role: "",
    },
    accessToken: null,
    isLoggedIn: false,
    enrolledCourses: [] as Course[],
    allCourses: [] as Course[],
    instructorCourses: [] as Course[],
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
      localStorage.setItem("user", JSON.stringify(user));
    },
    setAccessToken(state, accessToken) {
      state.accessToken = accessToken;
      localStorage.setItem("accessToken", accessToken);
    },
    setLoggedIn(state, isLoggedIn) {
      state.isLoggedIn = isLoggedIn;
      localStorage.setItem("isLoggedIn", JSON.stringify(isLoggedIn));
    },
    clearAuthData(state) {
      state.user = { id: "", name: "", email: "", role: "" };
      state.accessToken = null;
      state.isLoggedIn = false;
      localStorage.removeItem("user");
      localStorage.removeItem("accessToken");
      localStorage.removeItem("isLoggedIn");
    },
    setEnrolledCourses(state, courses) {
      state.enrolledCourses = courses;
    },
    setAllCourses(state, courses) {
      state.allCourses = courses;
    },
    addEnrolledCourse(state, courseId) {
      const course = state.allCourses.find((course) => course.id === courseId);
      if (course) {
        state.enrolledCourses.push(course);
      }
    },
    setInstructorCourses(state, courses) {
      state.instructorCourses = courses;
    },
  },
  actions: {
    ...authActions,
    ...courseActions,
    ...instructorActions,
  },
  getters: {
    enrolledCourses(state) {
      return state.enrolledCourses;
    },
    allCourses(state) {
      return state.allCourses;
    },
    instructorCourses(state) {
      return state.instructorCourses;
    },
    isAuthenticated(state) {
      return state.isLoggedIn;
    },
  },
});
