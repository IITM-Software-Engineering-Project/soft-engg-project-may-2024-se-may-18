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
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior() {
        return { top: 0, left: 0 }
    }
})

export default router;
