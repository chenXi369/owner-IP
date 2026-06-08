<template>
  <div class="settings-page">
    <el-card class="glass-card">
      <template #header>
        <div class="card-header">
          <span>系统配置</span>
          <el-button type="primary" @click="handleSave" :loading="saving">
            <el-icon><Check /></el-icon> 保存配置
          </el-button>
        </div>
      </template>

      <el-form :model="form" label-width="180px" v-loading="loading">
        <el-alert
          title="配置说明"
          description="以下配置项优先从数据库读取，未设置时回退到环境变量。敏感字段（密钥类）在展示时会被部分掩码。修改后即时生效，无需重启服务。"
          type="info"
          :closable="false"
          style="margin-bottom: 24px"
        />

        <el-divider content-position="left">阿里云 OSS</el-divider>
        <el-form-item
          v-for="item in ossSettings"
          :key="item.key"
          :label="item.label"
        >
          <el-input
            v-model="form[item.key]"
            :placeholder="item.description"
            :show-password="item.is_secret"
            clearable
          />
          <div class="field-desc">{{ item.description }}</div>
        </el-form-item>

        <el-divider content-position="left">阿里云内容安全（绿网）</el-divider>
        <el-form-item
          v-for="item in greenSettings"
          :key="item.key"
          :label="item.label"
        >
          <el-input
            v-model="form[item.key]"
            :placeholder="item.description"
            :show-password="item.is_secret"
            clearable
          />
          <div class="field-desc">{{ item.description }}</div>
        </el-form-item>

        <el-divider content-position="left">安全</el-divider>
        <el-form-item
          v-for="item in securitySettings"
          :key="item.key"
          :label="item.label"
        >
          <el-input
            v-model="form[item.key]"
            :placeholder="item.description"
            :show-password="item.is_secret"
            clearable
          />
          <div class="field-desc">{{ item.description }}</div>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Check } from '@element-plus/icons-vue'
import { getSettings, updateSettings } from '../api/settings'

const loading = ref(false)
const saving = ref(false)
const settings = ref([])
const form = ref({})

const ossSettings = computed(() => settings.value.filter(s => s.key.startsWith('OSS_')))
const greenSettings = computed(() => settings.value.filter(s => s.key.startsWith('GREEN_')))
const securitySettings = computed(() => settings.value.filter(s => !s.key.startsWith('OSS_') && !s.key.startsWith('GREEN_')))

const loadSettings = async () => {
  loading.value = true
  try {
    const data = await getSettings()
    settings.value = data || []
    // 初始化表单（使用实际值，掩码值仅在展示时处理）
    const obj = {}
    data.forEach(item => {
      obj[item.key] = item.has_value ? item.value : ''
    })
    form.value = obj
  } catch (error) {
    console.error('加载配置失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSave = async () => {
  saving.value = true
  try {
    // 只提交有变动的非空值或明确清空的值
    const payload = {}
    settings.value.forEach(item => {
      const newVal = form.value[item.key]
      if (newVal !== item.value) {
        payload[item.key] = newVal || ''
      }
    })
    await updateSettings(payload)
    ElMessage.success('配置已保存并生效')
    await loadSettings()
  } catch (error) {
    console.error('保存配置失败:', error)
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadSettings()
})
</script>

<style scoped lang="scss">
@use '../styles/variables.scss' as *;

.settings-page {
  max-width: 800px;
  margin: 0 auto;

  :deep(.el-card) {
    background: $bg-card;
    border: 1px solid $border-color;
    border-radius: $border-radius-lg;
    box-shadow: $shadow;
    color: $text-primary;

    .el-card__header {
      border-bottom: 1px solid $border-color;
      padding: 18px 24px;
      background: transparent;
    }
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 18px;
    font-weight: 600;
    color: $text-primary;
  }

  :deep(.el-form) {
    .el-form-item__label {
      color: $text-secondary;
      font-weight: 500;
    }

    .el-input__wrapper {
      background: $bg-primary;
      border: 1px solid $border-color;
      box-shadow: none;
      color: $text-primary;
      border-radius: $border-radius-sm;

      &.is-focus {
        border-color: $primary;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
      }

      input {
        color: $text-primary;
        background: transparent;

        &::placeholder {
          color: $text-muted;
        }
      }
    }
  }

  .field-desc {
    font-size: 12px;
    color: $text-muted;
    margin-top: 4px;
    line-height: 1.4;
  }

  :deep(.el-divider) {
    border-color: $border-color;

    .el-divider__text {
      background: $bg-card;
      color: $text-secondary;
      font-size: 14px;
      font-weight: 500;
    }
  }

  :deep(.el-alert) {
    background: rgba(99, 102, 241, 0.08);
    border: 1px solid rgba(99, 102, 241, 0.2);
    color: $text-secondary;

    .el-alert__title {
      color: $primary-light;
      font-weight: 600;
    }
  }
}
</style>
