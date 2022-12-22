import { h, defineAsyncComponent } from 'vue'
import Theme from 'vitepress/theme'
import Layout from './components/Giscus.vue'
import './styles/vars.css'

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
