declare module '*.vue' {
    import { DefineComponent } from 'vue'
    // eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/ban-types
    const component: DefineComponent<{}, {}, any>
    export default component
}

declare module "vuex" {
    export * from "vuex/types/index.d.ts";
    export * from "vuex/types/helpers.d.ts";
    export * from "vuex/types/logger.d.ts";
    export * from "vuex/types/vue.d.ts";
}

// import { ComponentCustomProperties } from 'vue'
// import { Store } from 'vuex'

// declare module '@vue/runtime-core' {
//     // Declare your own store states.
//     interface State {
//         count: number
//     }

//     interface ComponentCustomProperties {
//         $store: Store<State>
//     }
// }