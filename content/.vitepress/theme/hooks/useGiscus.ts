import { computed, watch } from 'vue'
import { useData, useRouter } from 'vitepress'
import { useScriptTag } from '@vueuse/core'
import { setCommentTheme, getCommentTheme } from '../utils/index'


export function useGiscus() {
	const router = useRouter()
	const { isDark, page } = useData()
	const hideCommentRef = computed(() => page.value.frontmatter.hideComment)
	const { load, unload } = useScriptTag('https://giscus.app/client.js', undefined, {
		manual: true,
		attrs: {
			'data-repo': 'IslamicRevival/IslamicRevival.github.io',
			'data-repo-id': 'R_kgDOIaj3hg',
			'data-category': 'General',
			'data-category-id': 'DIC_kwDOIaj3hs4CS5zb',
			'data-mapping': 'title',
			'data-strict': '1',
			'data-reactions-enabled': '1',
			'data-emit-metadata': '0',
			'data-input-position': 'top',
			'data-theme': 'preferred_color_scheme',
			'data-lang': 'en',
			'crossorigin': 'anonymous',
			'async': 'true'
		}
	})

	watch(isDark, (newIsDark) => {
		setCommentTheme(newIsDark)
	}, { immediate: true })

	watch(
		() => router.route.path,
		() => {
			if (!hideCommentRef.value) {
				unload()
				load()
			}
		},
		{ immediate: true }
	)

	return { hideCommentRef }
}