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
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="title" label="职位" width="180" />
        <el-table-column prop="greeting" label="问候语" width="150" />
        <el-table-column prop="description" label="简介" show-overflow-tooltip />
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'info'">
              {{ row.is_active ? '已激活' : '未激活' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑简历' : '新增简历'" width="600px">
      <el-form :model="form" label-width="100px" :rules="rules" ref="formRef">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" />
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
        <el-form-item label="头像URL">
          <el-input v-model="form.avatar_url" />
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
import { getResumes, createResume, updateResume, deleteResume } from '../api/resume'

const loading = ref(false)
const resumes = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)
const form = ref({
  id: null,
  name: '',
  title: '',
  greeting: '你好,我是',
  description: '',
  avatar_url: '',
  is_active: true
})

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
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
    title: '',
    greeting: '你好,我是',
    description: '',
    avatar_url: '',
    is_active: true
  }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  form.value = { ...row }
  dialogVisible.value = true
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
  padding: 24px;

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
}
</style>
