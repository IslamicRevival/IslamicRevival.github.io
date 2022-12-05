import 'dotenv/config'
import { defineConfig} from 'vitepress'


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
    ['meta', { name: 'theme-color', content: '#d8b4fe' }]
  ],
  themeConfig: {
    logo: '/logo.svg',
    editLink: {
      pattern:
        'https://github.com/vueup/vue-quill/edit/beta/docs/content/:path',
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
      { 	text: 'Contributing', 
		items: [
			{ text: "Add/edit content", link: '/how-to-content' },
			{ text: "Writing guide", link: '/writing-guide' },
		],
	},
	{
		text: 'Aqeedah',
		items: [
			{ text: 'Belief', link: '/aqeedah/belief' },
			{ text: 'Iman', link: '/aqeedah/iman' },
		],
	},
	{
		text: 'Concepts',
		items: [
			{ text: 'Actions', link: '/concepts/actions' }
		],
	},
	{
		text: 'Files',
		items: [
			{ text: 'PDFs', link: '/pdfs/' }
		],
	}
    ],
    sidebar: [
      {
        text: 'Contributing',
        items: [
          { text: "Add/edit content", link: '/how-to-content' },
          { text: "Writing guide", link: '/writing-guide' },
        ],
      },
      {
        text: 'Aqeedah',
        items: [
          { text: 'Belief', link: '/aqeedah/belief' },
          { text: 'Iman', link: '/aqeedah/iman' }			
        ],
      },
      {
        text: 'Concepts',
        items: [
          { text: 'Mental Models', link: '/concepts/mental-models' },
          { text: 'Thinking', link: '/concepts/thinking' },
        ],
      }
    ],
  }
})
