import { createMemoryHistory, createRouter } from 'vue-router'
import TestPage from '../pages/TestPage.vue'

const routes = [
    { path: '/', component: TestPage },
]

const router = createRouter({
    history: createMemoryHistory(),
    routes,
})

export default router;