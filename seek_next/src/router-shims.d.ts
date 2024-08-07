import VueRouter from 'vue-router';

declare module '@vue/runtime-core' {
    interface ComponentCustomProperties {
        $router: VueRouter;
        $route: VueRouter['currentRoute'];
    }
}