<template>
  <div class="comments-container"
       v-if="!page.frontmatter.hideComment">
    <Giscus id="comments"
            repo="IslamicRevival/IslamicRevival.github.io"
            repoId="R_kgDOIaj3hg"
            category="General"
            categoryId="DIC_kwDOIaj3hs4CS5zb"
            mapping="title"
            strict="1"
            reactionsEnabled="1"
            emitMetadata="0"
            inputPosition="top"
            lang="en"
            crossorigin="anonymous"
            :theme="isDark ? 'transparent_dark' : 'light'"
            :term="page.title"
            async="true" />
  </div>
</template>

<script setup lang="ts" src='https://giscus.app/client.js'>
import Giscus from '@giscus/vue'
import { useData } from 'vitepress'
const { isDark, page } = useData()
</script>

<style scoped>
.comments-container {
  margin-top: 30px;
}
</style>