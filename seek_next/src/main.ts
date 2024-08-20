import { createApp } from 'vue'
import App from './App.vue'
import router from './routes/router.ts'
import { store, key } from './store/store.ts'
import '@mdi/font/css/materialdesignicons.css';
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
  },
})

createApp(App).use(router).use(store, key).use(vuetify).mount('#app')
