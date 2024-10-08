import { createWebHistory, createRouter } from 'vue-router'
import Loading from '../pages/Loading.vue'
import SignIn from '../pages/SignIn.vue'
import SignUp from '../pages/SignUp.vue'
import Home from '../pages/TestPage.vue'
import StudentHome from '../pages/StudentHome.vue'
import AllCourses from '../pages/AllCourses.vue'
import CourseModules from '../pages/CourseModules.vue'
import ModuleDetails from '../pages/ModuleDetails.vue'
import CodeAssignment from '../pages/CodeAssignment.vue'
import InstructorHome from '../pages/InstructorHome.vue'
import InstructorCourseModules from '../pages/InstructorCourseModules.vue'
import InstructorModuleDetails from '../pages/InstructorModuleDetails.vue'
import InstructorGradeAssignment from '../pages/InstructorGradeAssignment.vue'
import Assignment from '../pages/Assignment.vue'
import { store } from '../store/store';

const routes = [
    { path: '/', component: Loading, name: 'Loading' },
    { path: '/sign-in', component: SignIn, name: 'SignIn' },
    { path: '/sign-up', component: SignUp, name: 'SignUp' },
    { path: '/home', component: Home, name: 'Home' },
    { path: '/student-home', component: StudentHome, name: 'StudentHome' },
    { path: '/all-courses', component: AllCourses, name: 'AllCourses' },
    { path: '/course-modules/:courseId', component: CourseModules, name: 'CourseModules' },
    { path: '/code-assignment/:problemId', component: CodeAssignment, name: 'CodeAssignment' },
    { path: '/module-details/:courseId/:moduleId/:moduleTitle', component: ModuleDetails, name: 'ModuleDetails' },
    { path: '/instructor-home', component: InstructorHome, name: 'InstructorHome' },
    { path: '/instructor/course-modules/:courseId', component: InstructorCourseModules, name: 'InstructorCourseModules' },
    { path: '/instructor/module-details/:courseId/:moduleId/:moduleTitle', component: InstructorModuleDetails, name: 'InstructorModuleDetails' },
    { path: '/instructor/grade-assignment/:assignmentId', component: InstructorGradeAssignment, name: 'InstructorGradeAssignment' },
    { path: '/assignment/:assignmentId', component: Assignment, name: 'Assignment' }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior() {
        return { top: 0, left: 0 }
    }
})

router.afterEach(() => {
    try {
        const token = localStorage.getItem('accessToken');
        const user = JSON.parse(localStorage.getItem('user') ?? '{}');
        const isLoggedIn = JSON.parse(localStorage.getItem('isLoggedIn') ?? 'false');


        store.commit('auth/setUser', user);
        store.commit('auth/setAccessToken', token);
        store.commit('auth/setLoggedIn', isLoggedIn);
    }
    catch (e) {
        store.commit('auth/clearAuthData');
        router.push('/sign-in');
    }

});

export default router;
