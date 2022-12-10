<script setup>
import {onMounted, ref } from 'vue'
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
    <div ref="giscusRef" class="comments"></div>
</template>

<style scoped>
.comments {
    padding-top: 10px;
}
</style>

