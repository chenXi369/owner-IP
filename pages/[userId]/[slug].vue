<template>
  <IndexPage :user-id="route.params.userId" />
</template>

<script setup>
import IndexPage from '../index.vue'

const route = useRoute()

// 设置页面元数据
useHead({
  title: '简历展示'
})
</script>
