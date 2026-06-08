<template>
  <div class="profile-page">
    <el-card class="glass-card">
      <template #header>
        <div class="card-header">
          <span>个人中心</span>
        </div>
      </template>

      <el-form :model="form" label-width="120px" :rules="rules" ref="formRef" v-loading="loading">
        <el-form-item label="个人简介" prop="about_text">
          <el-input
            v-model="form.about_text"
            type="textarea"
            :rows="6"
            placeholder="请输入关于我的个人简介，支持多段描述..."
          />
        </el-form-item>

        <el-form-item label="个人照片">
          <el-upload
            class="photo-uploader"
            :show-file-list="false"
            :http-request="handlePhotoUpload"
            accept="image/*"
          >
            <img v-if="form.photo_url" :src="form.photo_url" class="photo-preview" />
            <div v-else class="photo-upload-placeholder">
              <el-icon :size="28"><Plus /></el-icon>
              <span>点击上传</span>
            </div>
          </el-upload>
        </el-form-item>

        <el-divider content-position="left">数据统计</el-divider>

        <div class="stats-row">
          <el-form-item label="年开发经验">
            <el-input v-model="form.years_exp" placeholder="如: 5+">
              <template #append>年</template>
            </el-input>
          </el-form-item>

          <el-form-item label="完成项目">
            <el-input v-model="form.projects_count" placeholder="如: 50+">
              <template #append>个</template>
            </el-input>
          </el-form-item>
        </div>

        <div class="stats-row">
          <el-form-item label="技术文章">
            <el-input v-model="form.articles_count" placeholder="如: 20+">
              <template #append>篇</template>
            </el-input>
          </el-form-item>

          <el-form-item label="开源贡献">
            <el-input v-model="form.contributions_count" placeholder="如: 10+">
              <template #append>个</template>
            </el-input>
          </el-form-item>
        </div>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">保存修改</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getProfile, updateProfile } from '../api/profile'
import { uploadImage } from '../api/upload'

const loading = ref(false)
const submitting = ref(false)
const formRef = ref(null)

const form = ref({
  about_text: '',
  photo_url: '',
  years_exp: '0',
  projects_count: '0',
  articles_count: '0',
  contributions_count: '0'
})

const rules = {
  about_text: [{ required: true, message: '请输入个人简介', trigger: 'blur' }]
}

const loadProfile = async () => {
  loading.value = true
  try {
    const data = await getProfile()
    if (data) {
      form.value = {
        about_text: data.about_text || '',
        photo_url: data.photo_url || '',
        years_exp: data.years_exp || '0',
        projects_count: data.projects_count || '0',
        articles_count: data.articles_count || '0',
        contributions_count: data.contributions_count || '0'
      }
    }
  } catch (error) {
    console.error('加载个人信息失败:', error)
  } finally {
    loading.value = false
  }
}

const handlePhotoUpload = async (options) => {
  try {
    const res = await uploadImage(options.file)
    form.value.photo_url = res.url
    ElMessage.success('上传成功')
  } catch (error) {
    console.error('上传失败:', error)
  }
}

const handleSubmit = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    await updateProfile(form.value)
    ElMessage.success('保存成功')
  } catch (error) {
    console.error('保存失败:', error)
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadProfile()
})
</script>

<style scoped lang="scss">
@use '../styles/variables.scss' as *;

.profile-page {
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
    font-size: 18px;
    font-weight: 600;
    color: $text-primary;
  }

  .stats-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0 24px;

    @media (max-width: 640px) {
      grid-template-columns: 1fr;
    }
  }

  :deep(.el-form) {
    .el-form-item__label {
      color: $text-secondary;
      font-weight: 500;
    }

    .el-input__wrapper,
    .el-textarea__inner {
      background: $bg-primary;
      border: 1px solid $border-color;
      box-shadow: none;
      color: $text-primary;
      border-radius: $border-radius-sm;

      &.is-focus,
      &:focus {
        border-color: $primary;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
      }

      input,
      textarea {
        color: $text-primary;
        background: transparent;

        &::placeholder {
          color: $text-muted;
        }
      }
    }
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

  :deep(.el-input-group__append) {
    background: $bg-secondary;
    border-color: $border-color;
    color: $text-secondary;
  }

  .photo-uploader {
    :deep(.el-upload) {
      width: 200px;
      height: 260px;
      border: 1px dashed $border-color;
      border-radius: $border-radius-lg;
      background: $bg-primary;
      cursor: pointer;
      transition: border-color $transition-fast;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;

      &:hover {
        border-color: $primary;
      }
    }

    .photo-preview {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .photo-upload-placeholder {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
      color: $text-muted;

      span {
        font-size: 13px;
      }
    }
  }
}
</style>
