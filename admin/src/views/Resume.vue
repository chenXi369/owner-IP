<template>
  <div class="resume-page">
    <el-card class="glass-card">
      <template #header>
        <div class="card-header">
          <span>简历列表</span>
          <el-button type="primary" @click="handleAdd">新增简历</el-button>
        </div>
      </template>
      
      <el-table :data="resumes" stripe v-loading="loading">
        <el-table-column type="index" width="60" />
        <el-table-column prop="name" label="姓名" min-width="100" />
        <el-table-column prop="slug" label="简历ID" min-width="120" />
        <el-table-column prop="title" label="职位" min-width="150" />
        <el-table-column prop="greeting" label="问候语" min-width="120" />
        <el-table-column prop="description" label="简介" show-overflow-tooltip />
        <el-table-column prop="is_active" label="状态" width="120" align="center">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'info'">
              {{ row.is_active ? '已激活' : '未激活' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280">
          <template #default="{ row }">
            <el-button v-if="row.is_active" type="success" link size="small" @click="handlePreview(row)">预览简历</el-button>
            <el-button type="primary" link size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑简历' : '新增简历'" width="600px" :close-on-click-modal="false">
      <el-form :model="form" label-width="100px" :rules="rules" ref="formRef">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="简历ID" prop="slug">
          <el-input v-model="form.slug" placeholder="唯一标识，如：my-resume-2024" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="职位标题" prop="title">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="问候语">
          <el-input v-model="form.greeting" />
        </el-form-item>
        <el-form-item label="个人简介">
          <el-input v-model="form.description" type="textarea" :rows="4" />
        </el-form-item>
        <el-form-item label="头像">
          <el-upload
            class="avatar-uploader"
            :show-file-list="false"
            :http-request="handleAvatarUpload"
            accept="image/*"
          >
            <img v-if="form.avatar_url" :src="form.avatar_url" class="avatar-preview" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="激活状态">
          <el-switch v-model="form.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getResumes, createResume, updateResume, deleteResume } from '../api/resume'
import { uploadImage } from '../api/upload'

const loading = ref(false)
const resumes = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)
const form = ref({
  id: null,
  name: '',
  slug: '',
  title: '',
  greeting: '你好,我是',
  description: '',
  avatar_url: '',
  is_active: false
})

const validateSlug = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请输入简历ID'))
  } else if (!/^[a-zA-Z0-9_-]+$/.test(value)) {
    callback(new Error('只能包含字母、数字、连字符和下划线'))
  } else {
    callback()
  }
}

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  slug: [
    { required: true, message: '请输入简历ID', trigger: 'blur' },
    { validator: validateSlug, trigger: 'blur' }
  ],
  title: [{ required: true, message: '请输入职位标题', trigger: 'blur' }]
}

const loadData = async () => {
  loading.value = true
  try {
    const data = await getResumes()
    resumes.value = data || []
  } catch (error) {
    console.error('加载失败:', error)
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  isEdit.value = false
  form.value = {
    id: null,
    name: '',
    slug: '',
    title: '',
    greeting: '你好,我是',
    description: '',
    avatar_url: '',
    is_active: false
  }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  form.value = { ...row }
  dialogVisible.value = true
}

const handlePreview = (row) => {
  const nuxtBaseUrl = import.meta.env.VITE_NUXT_BASE_URL || 'http://localhost:3000'
  const url = `${nuxtBaseUrl}/${row.user_id}/${row.slug}`
  window.open(url, '_blank')
}

const handleAvatarUpload = async (options) => {
  try {
    const res = await uploadImage(options.file)
    form.value.avatar_url = res.url
    ElMessage.success('上传成功')
  } catch (error) {
    console.error('上传失败:', error)
  }
}

const handleSubmit = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  try {
    if (isEdit.value) {
      await updateResume(form.value.id, form.value)
      ElMessage.success('更新成功')
    } else {
      await createResume(form.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('操作失败:', error)
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该简历吗？', '提示', { type: 'warning' })
    await deleteResume(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch {
    // 取消删除
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
@use '../styles/variables.scss' as *;

.resume-page {
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

    .el-card__body {
      padding: 24px;
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

  :deep(.el-table) {
    background: transparent;
    color: $text-primary;

    &::before {
      display: none;
    }

    .el-table__header-wrapper {
      th.el-table__cell {
        background: $bg-secondary;
        color: $text-secondary;
        font-weight: 600;
        border-bottom: 1px solid $border-color;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 14px 12px;
      }
    }

    .el-table__body-wrapper {
      td.el-table__cell {
        background: transparent;
        color: $text-primary;
        border-bottom: 1px solid $border-color;
        padding: 14px 12px;
        font-size: 14px;
      }

      tr {
        background: transparent;
        transition: background $transition-fast;

        &:hover > td.el-table__cell {
          background: $bg-hover !important;
        }

        &.el-table__row--striped {
          td.el-table__cell {
            background: rgba(30, 41, 59, 0.5);
          }

          &:hover > td.el-table__cell {
            background: $bg-hover !important;
          }
        }
      }
    }

    .el-table__empty-block {
      background: transparent;
      color: $text-muted;
    }
  }

  :deep(.el-dialog) {
    background: $bg-card;
    border: 1px solid $border-color;
    border-radius: $border-radius-lg;
    box-shadow: $shadow-lg;

    .el-dialog__header {
      border-bottom: 1px solid $border-color;
      padding: 20px 24px;
      margin-right: 0;

      .el-dialog__title {
        color: $text-primary;
        font-weight: 600;
      }

      .el-dialog__headerbtn .el-dialog__close {
        color: $text-muted;

        &:hover {
          color: $text-primary;
        }
      }
    }

    .el-dialog__body {
      padding: 24px;
    }

    .el-dialog__footer {
      border-top: 1px solid $border-color;
      padding: 16px 24px;
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

    .el-input-number {
      .el-input__wrapper {
        background: $bg-primary;
      }
    }
  }

  :deep(.el-switch__label) {
    color: $text-secondary;
  }

  :deep(.el-button.is-link) {
    color: $text-secondary;
    font-weight: 500;
    transition: color $transition-fast;

    &.el-button--primary {
      color: $primary-light;

      &:hover {
        color: $primary;
      }
    }

    &.el-button--danger {
      color: #f87171;

      &:hover {
        color: mix(#fff, $danger, 25%);
      }
    }
  }

  :deep(.el-tag) {
    border-radius: $border-radius-sm;
    font-weight: 500;
  }

  .avatar-uploader {
    :deep(.el-upload) {
      width: 120px;
      height: 120px;
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

    .avatar-preview {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .avatar-uploader-icon {
      font-size: 28px;
      color: $text-muted;
    }
  }
}
</style>
