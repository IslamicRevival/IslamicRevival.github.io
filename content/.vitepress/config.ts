import 'dotenv/config'
import { defineConfig} from 'vitepress'
import { getSideBar }  from  './theme/vitepress-plugin-autobar/'

// see vite.config.js for search

export default defineConfig({
  base: '/',
  lang: 'en-US',
  title: 'Islamic Revival',
  description: 'A free framework to share Islamically scholarly works',
  head: [
    [
      'link',
      { rel: 'icon', type: 'image/svg+xml', href: '/vue-quill/logo.svg' },
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
			{ text: 'Misunderstanding Ibada', link: '/articles/misunderstanding_ibada' },
		],
	},
  {
		text: 'Blogging Theology',
		items: [
			{ text: 'Video summaries', link: '/blogging_theology/What_is_Truth_with_Firas_Zahabi' }
		],
	},
  {
    text: 'Contributing', 
    items: [
      { text: "Add/edit content", link: '/contributing/how-to-content' },
      { text: "Writing guide", link: '/contributing/writing-guide' },
    ],
},
{
  text: 'Files',
  items: [
    { text: 'PDFs', link: '/files/pdfs' }
  ],
 },
 {
  text: 'Fiqh & Tafseer',
  items: [
    { text: 'Video summaries', link: '/massari/02_-_Establishing_an_Islamic_State__Is_it_an_Obligation_(Fardh)' }
  ],
},
{
  text: 'Mohammed Hijab',
  items: [
    { text: 'Video Summaries', link: '/hijab/Hard_Questions_to_Hamza_Tzortzis' }
  ],
 },
    ],
    sidebar:  getSideBar( "./content", {
      ignoreMDFiles: ['index'],
      ignoreDirectory: ['node_modules'],
    }),
  }
})