import baseConfig from '@vue/theme/config'
import { defineConfigWithTheme, HeadConfig, UserConfig } from 'vitepress'
import type { Config } from '@vue/theme'
import { NavItem, SidebarConfig } from '@vue/theme/src/vitepress/config'

const production = process.env.NODE_ENV === 'production'
const title = 'Islamic Revival'
const description = 'A framework to share Islamically scholarly works'
const site = production ? 'https://islamicrevival-ubiquitous-couscous-jvxqj6jppv7256wq-3005.preview.app.github.dev' : 'http://localhost:3000'
const image = `${site}/banner.png`

const head: HeadConfig[] = [
	['meta', { name: 'author', content: 'SirVival' }],
	['meta', { name: 'keywords', content: 'Islam, scholarship, Massari, salafi, madhabs, hadith, quran' }],
	['link', { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }],
	['meta', { name: 'HandheldFriendly', content: 'True' }],
	['meta', { name: 'MobileOptimized', content: '320' }],
	['meta', { name: 'theme-color', content: '#d8b4fe' }],
	['meta', { name: 'twitter:card', content: 'summary_large_image' }],
	['meta', { name: 'twitter:site', content: site }],
	['meta', { name: 'twitter:title', value: title }],
	['meta', { name: 'twitter:description', value: description }],
	['meta', { name: 'twitter:image', content: image }],
	['meta', { property: 'og:type', content: 'website' }],
	['meta', { property: 'og:locale', content: 'en_US' }],
	['meta', { property: 'og:site', content: site }],
	['meta', { property: 'og:site_name', content: title }],
	['meta', { property: 'og:title', content: title }],
	['meta', { property: 'og:image', content: image }],
	['meta', { property: 'og:description', content: description }],
]

const nav: NavItem[] = [
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
]

const sidebar: SidebarConfig = {
	'/': [
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

export default defineConfigWithTheme<Config>({
	extends: baseConfig as () => UserConfig<Config>,
	title,
	head,
	description,
	lang: 'en-US',
	base: '/',
	scrollOffset: 'header',
	srcDir: 'content',

	themeConfig: {
		nav,
		sidebar,

		// algolia: {
		// 	appId: 'UNQJXGJJCM',
		// 	apiKey: '13f1ef823ef6da38d5b51452d5768113',
		// 	indexName: 'preset',
		// },

		socialLinks: [
			{ icon: 'github', link: 'https://github.com/IslamicRevival/IslamicRevival.github.io' },
			{ icon: 'twitter', link: 'https://twitter.com/' },
		],

		// https://github.com/vuejs/theme/pull/44
		// editLink: {
		// 	repo: 'preset/preset',
		// 	text: 'Edit this page on Github',
		// },

		footer: {
			copyright: 'Made with ❤️ by SirVival',
		},
	},

	vite: {
		server: {
			host: true,
			fs: {
				allow: ['../..'],
			},
		},
		build: {
			minify: 'terser',
			chunkSizeWarningLimit: Infinity,
			rollupOptions: {
				output: {
					chunkFileNames: 'assets/chunks/[name].[hash].js',
					manualChunks: (id, ctx) => moveToVendor(id, ctx),
				},
			},
		},
		json: {
			stringify: true,
		},
	},
})

const cache = new Map<string, boolean>()

/**
 * This is temporarily copied from Vite - which should be exported in a
 * future release.
 *
 * @TODO when this is exported by Vite, VitePress should ship a better
 * manual chunk strategy to split chunks for deps that are imported by
 * multiple pages but not all.
 */
function moveToVendor(id: string, { getModuleInfo }: any) {
	if (
		id.includes('node_modules')
    && !/\.css($|\\?)/.test(id)
    && staticImportedByEntry(id, getModuleInfo, cache)
	) {
		return 'vendor'
	}
}

function staticImportedByEntry(
	id: string,
	getModuleInfo: any,
	cache: Map<string, boolean>,
	importStack: string[] = [],
): boolean {
	if (cache.has(id)) {
		return cache.get(id) as boolean
	}
	if (importStack.includes(id)) {
		// circular deps!
		cache.set(id, false)

		return false
	}
	const mod = getModuleInfo(id)
	if (!mod) {
		cache.set(id, false)

		return false
	}

	if (mod.isEntry) {
		cache.set(id, true)

		return true
	}
	const someImporterIs = mod.importers.some((importer: string) =>
		staticImportedByEntry(
			importer,
			getModuleInfo,
			cache,
			importStack.concat(id),
		),
	)
	cache.set(id, someImporterIs)

	return someImporterIs
}
