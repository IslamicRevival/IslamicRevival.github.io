import { h, defineAsyncComponent } from 'vue'
import Theme from 'vitepress/theme'
import Layout from './components/Giscus.vue'
import './styles/vars.css'

// Vuetify
import { createApp } from 'vue'
import App from './components/Form.vue'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
})



export default {
  enhanceApp({ app, router, siteData }) {
    // app is the Vue 3 app instance from `createApp()`. router is VitePress'
    // custom router. `siteData`` is a `ref`` of current site-level metadata.
  },
  ...Theme,
  Layout() {
    return h(Theme.Layout, null, {
      'home-features-after': () => h(Layout),
    })
  }, 
}
