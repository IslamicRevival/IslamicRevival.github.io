import 'dotenv/config'
import { defineConfig} from 'vitepress'
import { getSideBar }  from  './theme/vitepress-plugin-autobar/'

// see vite.config.js for search

export default defineConfig({
  base: '/',
  lang: 'en-US',
  title: 'Islamic Revival',
  cleanUrls: 'with-subfolders',
  description: 'Islamic Revival - AI & NLP framework for Islamic knowledge sharing & archiving',
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
      'function modifyYTiframeseektime(param) {\
        let iframe = document.querySelector("iframe");\
        let iframeorigsrc = iframe.src;\
        let url = new URL(iframeorigsrc);\
        let search_params = new URLSearchParams(url.search);\
        search_params.set("autoplay", "1");\
        search_params.set("start", param);\
        url.search = search_params.toString();\
        iframe.src = url.toString();}'
    ],
    [
      'script',
      {},
      "window.dataLayer = window.dataLayer || [];\nfunction gtag(){dataLayer.push(arguments);}\ngtag('js', new Date());\ngtag('config', 'G-7M5QP5LNSL');"
    ],
    [
      'script',
      { async: true, src: 'https://cse.google.com/cse.js?cx=9205c02114fb34820' } 
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
