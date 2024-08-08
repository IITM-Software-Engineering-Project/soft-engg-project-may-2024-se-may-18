import { createMemoryHistory, createRouter } from 'vue-router'
import Loading from '../pages/Loading.vue'
import SignIn from '../pages/SignIn.vue'
import SignUp from '../pages/SignUp.vue'
// import Home from '../pages/TestPage.vue'

const routes = [
    { path: '/', component: Loading },
    { path: '/sign-in', component: SignIn },
    { path: '/sign-up', component: SignUp },
    // { path: '/home', component: Home },
]

const router = createRouter({
    history: createMemoryHistory(),
    routes,
})

export default router;