<template>
	<Layout>
		<template #doc-after>
			<Comment v-if="!hideCommentRef" />
		</template>
	</Layout>
</template>

<script lang="ts" setup>
import { useGiscus } from '../hooks/useGiscus'
//import Theme from 'vitepress/theme'
//const { Layout } = Theme
const { hideCommentRef } = useGiscus()
</script>
