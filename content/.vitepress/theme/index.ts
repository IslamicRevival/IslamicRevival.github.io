import { h, defineAsyncComponent } from 'vue'
import Theme from 'vitepress/theme'
import Layout from './components/Layout.vue'


import './styles/tailwind.css'
import './styles/vars.css'

//import { useGiscus } from './hooks/useGiscus'

//import '@vueup/vue-quill/dist/vue-quill.core.css' // import styles
//import '@vueup/vue-quill/dist/vue-quill.bubble.css' // for bubble theme
//import '@vueup/vue-quill/dist/vue-quill.snow.css' // for snow theme

export default {
  enhanceApp({ app, router, siteData }) {
    // app is the Vue 3 app instance from `createApp()`. router is VitePress'
    // custom router. `siteData`` is a `ref`` of current site-level metadata.
  },
  ...Theme,
  Layout() {
    return h(Theme.Layout, null, {
      'home-features-after': () => h(Layout),
      // 'aside-ads-before': () => h(AsideSponsors)
    //  'home-features-after': () => h(useGiscus()),

    })
  }, 
}
