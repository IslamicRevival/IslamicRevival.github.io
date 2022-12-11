import 'dotenv/config'
import { defineConfig} from 'vitepress'
import { getSideBar }  from  'vitepress-plugin-autobar'
import { SimpleSearch } from "vitepress-plugin-simple-search";

export default defineConfig({
  plugins: [SimpleSearch('/')],
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
    ['script', { type: 'application/javascript' }, `
    setTimeout(function() {
        const searchBox = document.querySelector('.search-text');
        if (searchBox) {
            searchBox.textContent = 'Search (⌘K)';
            document.addEventListener('keydown', (e) => {
                if (e.metaKey && e.keyCode === 75) {
                    searchBox.click();
                }
            });
        }
    }, 200);
    `],
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
      { 	text: 'Contributing', 
		items: [
			{ text: "Add/edit content", link: '/contributing/how-to-content' },
			{ text: "Writing guide", link: '/contributing/writing-guide' },
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
    sidebar:  getSideBar( "./content", {
      ignoreMDFiles: ['index'],
      ignoreDirectory: ['node_modules'],
    }),
  }
})