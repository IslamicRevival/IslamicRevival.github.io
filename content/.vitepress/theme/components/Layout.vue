<script setup src="https://giscus.app/client.js"
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
import {onMounted, ref } from 'vue'
const giscusRef = ref()
const setAttributes = (el, attrs) => {
    for (const key in attrs) {
        el.setAttribute(key, attrs[key]);
    }
}
const currentTheme = document.documentElement.classList.value === 'dark' ? 'dark_dimmed' : 'light'
const renderGiscus = (currentTheme) => {
    const giscus = document.createElement('script')
    Utils.setAttributes(giscus, giscusConfig(currentTheme))
    giscusRef.value.appendChild(giscus)
}
onMounted(() => {
    renderGiscus(currentTheme)
})

onload(renderGiscus(currentTheme))

</script>

<template>
    <div ref="giscusRef"></div>
</template>

<style scoped>
.comments {
    padding-top: 10px;
}
</style>