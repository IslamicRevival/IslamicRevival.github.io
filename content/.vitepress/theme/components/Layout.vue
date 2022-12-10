
	<Layout>
		<template #doc-after>
			<Comment v-if="!hideCommentRef" />
			
		</template>
	</Layout>
</template>


<script lang="ts" setup src="https://giscus.app/client.js"
        data-repo="IslamicRevival/IslamicRevival.github.io"
        data-repo-id="R_kgDOIaj3hg"
        data-category="General"
        data-category-id="DIC_kwDOIaj3hs4CS5zb"
        data-mapping="pathname"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="bottom"
        data-theme="preferred_color_scheme"
        data-lang="en"
        crossorigin="anonymous"
        async>
</script>

/*
<script lang="ts" setup>
import { useGiscus } from '../hooks/useGiscus'
//import Theme from 'vitepress/theme'
//const { Layout } = Theme
const { hideCommentRef } = useGiscus()
</script>

*/