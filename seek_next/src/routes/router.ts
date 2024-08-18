import { createMemoryHistory, createRouter } from 'vue-router'
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
    { path: '/', component: Loading },
    { path: '/sign-in', component: SignIn },
    { path: '/sign-up', component: SignUp },
    { path: '/home', component: Home },
    { path: '/student-home', component: StudentHome },
    { path: '/all-courses', component: AllCourses },
    { path: '/course-modules/:courseId', component: CourseModules },
    { path: '/code-assignment/:problemId', component: CodeAssignment },
    { path: '/module-details/:courseId/:moduleId/:moduleTitle', component: ModuleDetails },
    { path: '/instructor-home', component: InstructorHome },
    { path: '/instructor/course-modules/:courseId', component: InstructorCourseModules },
    { path: '/instructor/module-details/:courseId/:moduleId/:moduleTitle', component: InstructorModuleDetails },
    { path: '/instructor/grade-assignment/:assignmentId', component: InstructorGradeAssignment },
]

const router = createRouter({
    history: createMemoryHistory(),
    routes,
})

export default router;