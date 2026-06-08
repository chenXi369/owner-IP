<template>
  <el-config-provider :locale="zhCn">
    <router-view v-slot="{ Component }">
      <transition name="page" mode="out-in">
          <component :is="Component" />
      </transition>
    </router-view>
  </el-config-provider>
</template>

<script setup>
import { ElConfigProvider } from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
</style>
