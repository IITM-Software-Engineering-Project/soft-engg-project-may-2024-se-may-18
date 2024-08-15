import { createMemoryHistory, createRouter } from 'vue-router'
import Loading from '../pages/Loading.vue'
import SignIn from '../pages/SignIn.vue'
import SignUp from '../pages/SignUp.vue'
import Home from '../pages/TestPage.vue'
import StudentHome from '../pages/StudentHome.vue'
import AllCourses from '../pages/AllCourses.vue'
import CourseModules from '../pages/CourseModules.vue'
import ModuleDetails from '../pages/ModuleDetails.vue'

const routes = [
    { path: '/', component: Loading },
    { path: '/sign-in', component: SignIn },
    { path: '/sign-up', component: SignUp },
    { path: '/home', component: Home },
    { path: '/student-home', component: StudentHome },
    { path: '/all-courses', component: AllCourses },
    { path: '/course-modules/:courseId', component: CourseModules },
    { path: '/module-details/:courseId/:moduleId/:moduleTitle', component: ModuleDetails },
]

const router = createRouter({
    history: createMemoryHistory(),
    routes,
})

export default router;