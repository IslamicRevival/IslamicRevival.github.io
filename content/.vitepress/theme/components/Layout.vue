<script setup>
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
</script>

<template>
    <div ref="giscusRef"></div>
</template>

<style scoped>
.comments {
    padding-top: 10px;
}
</style>