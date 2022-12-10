<template>
  <div class="comments-container" style="width:80%; padding-left:300px"
       v-if="!page.frontmatter.hideComment">
    <Giscus id="comments"
            repo="IslamicRevival/IslamicRevival.github.io"
            repoId="R_kgDOIaj3hg"
            category="General"
            categoryId="DIC_kwDOIaj3hs4CS5zb"
            mapping="URL"
            strict="1"
            reactionsEnabled="0"
            emitMetadata="0"
            inputPosition="top"
            lang="en"
            crossorigin="anonymous"
            :theme="isDark ? 'transparent_dark' : 'light'"
            :term="page.title"
            async="true" />
  </div>
</template>

<script setup lang="ts">
import Giscus from '@giscus/vue'
import { useData } from 'vitepress'
const { isDark, page } = useData()
</script>

<style scoped>
.comments-container {
  margin-top: 30px;
}
</style>