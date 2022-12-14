import 'dotenv/config'
import { defineConfig} from 'vitepress'
import { getSideBar }  from  './theme/vitepress-plugin-autobar/'

// see vite.config.js for search

export default defineConfig({
  base: '/',
  lang: 'en-US',
  title: 'Islamic Revival',
  cleanUrls: 'with-subfolders',
  description: 'A free framework to share Islamically scholarly works',
  head: [
    [
      'link',
      { rel: 'icon', type: 'image/svg+xml', href: '/vue-quill/logo.svg' },
    ],
    [
      'script',
      { async: true, src: 'https://www.googletagmanager.com/gtag/js?id=G-7M5QP5LNSL' }
    ],
    [
      'script',
      {},
      "window.dataLayer = window.dataLayer || [];\nfunction gtag(){dataLayer.push(arguments);}\ngtag('js', new Date());\ngtag('config', 'G-7M5QP5LNSL');"
    ],
    ['meta', { name: 'author', content: 'SirVival' }],
    ['meta', { name: 'keywords', content: 'Islam, scholarship, Massari, salafi, madhabs, hadith, quran' }],
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }],
    ['meta', { name: 'HandheldFriendly', content: 'True' }],
    ['meta', { name: 'MobileOptimized', content: '320' }],
    ['meta', { name: 'theme-color', content: '#d8b4fe' }],
  ],
  themeConfig: {
    logo: '/logo.svg',
    editLink: {
      pattern:
        'https://github.com/IslamicRevival/IslamicRevival.github.io/edit/main/content/:path',
      text: 'Edit this page on GitHub',
    },
		socialLinks: [
			{ icon: 'github', link: 'https://github.com/IslamicRevival/IslamicRevival.github.io' },
			{ icon: 'twitter', link: 'https://twitter.com/' },
		],
    footer: {
      copyright: 'As-salamu alaykum! Content by SirVival',
    },

    nav: [
  {
    text: 'Articles', 
    items: [
      { text: "Add/edit content", link: '/articles/how-to-content' },
      { text: "Writing guide", link: '/articles/writing-guide' },
      { text: 'Misunderstanding Ibada', link: '/articles/misunderstanding_ibada' },
    ],
},
{ text: 'Blog. Theology', link: '/blogging_theology/' },

{
  text: 'Files', link: '/files/pdfs' 
 },
 {
  text: 'Fiqh & Tafseer',link: '/massari/' 
},
{
  text: 'Mohd. Hijab', link: '/hijab/' 
 },
 {
  text: 'Sapience', link: '/sapience/'
 },
 { text: 'Thgt Advtr.', link: '/thought_adventure/' },
    ],
    sidebar:  getSideBar( "./content", {
      ignoreMDFiles: ['index'],
      ignoreDirectory: ['node_modules'],
    }),
  }
})