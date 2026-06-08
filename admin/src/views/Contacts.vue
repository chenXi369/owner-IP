<template>
  <div class="contacts-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>联系方式</span>
          <div class="header-actions">
            <el-select v-model="selectedResumeId" placeholder="选择简历" @change="loadContacts">
              <el-option
                v-for="resume in resumes"
                :key="resume.id"
                :label="resume.name"
                :value="resume.id"
              />
            </el-select>
            <el-button type="primary" @click="handleAdd">新增联系方式</el-button>
          </div>
        </div>
      </template>
      
      <el-table :data="contacts" stripe v-loading="loading">
        <el-table-column type="index" width="60" />
        <el-table-column prop="type" label="类型" width="120">
          <template #default="{ row }">
            <el-tag>{{ row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="label" label="标签" width="120" />
        <el-table-column prop="value" label="内容" />
        <el-table-column prop="order" label="排序" width="80" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑联系方式' : '新增联系方式'" width="500px">
      <el-form :model="form" label-width="100px" :rules="rules" ref="formRef">
        <el-form-item label="类型" prop="type">
          <el-select v-model="form.type" placeholder="选择类型" style="width: 100%">
            <el-option label="邮箱" value="email" />
            <el-option label="电话" value="phone" />
            <el-option label="GitHub" value="github" />
            <el-option label="LinkedIn" value="linkedin" />
            <el-option label="微信" value="wechat" />
            <el-option label="QQ" value="qq" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-input v-model="form.label" placeholder="如：个人邮箱、工作手机" />
        </el-form-item>
        <el-form-item label="内容" prop="value">
          <el-input v-model="form.value" placeholder="如：example@email.com" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.order" :min="0" />
        </el-form-item>
        <el-form-item prop="resume_id" v-show="false">
          <el-input v-model="form.resume_id" />
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
import { getResumes } from '../api/resume'
import { getContactsByResume, createContact, updateContact, deleteContact } from '../api/contacts'

const loading = ref(false)
const contacts = ref([])
const resumes = ref([])
const selectedResumeId = ref(null)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)
const form = ref({
  id: null,
  type: 'email',
  label: '',
  value: '',
  order: 0,
  resume_id: null
})

const rules = {
  type: [{ required: true, message: '请选择类型', trigger: 'change' }],
  value: [{ required: true, message: '请输入内容', trigger: 'blur' }]
}

const loadResumes = async () => {
  try {
    const data = await getResumes()
    resumes.value = data || []
    if (resumes.value.length > 0 && !selectedResumeId.value) {
      selectedResumeId.value = resumes.value[0].id
      await loadContacts()
    }
  } catch (error) {
    console.error('加载简历失败:', error)
  }
}

const loadContacts = async () => {
  if (!selectedResumeId.value) return
  loading.value = true
  try {
    const data = await getContactsByResume(selectedResumeId.value)
    contacts.value = data || []
  } catch (error) {
    console.error('加载联系方式失败:', error)
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  isEdit.value = false
  form.value = {
    id: null,
    type: 'email',
    label: '',
    value: '',
    order: 0,
    resume_id: selectedResumeId.value
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
      await updateContact(form.value.id, form.value)
      ElMessage.success('更新成功')
    } else {
      await createContact(form.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadContacts()
  } catch (error) {
    console.error('操作失败:', error)
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该联系方式吗？', '提示', { type: 'warning' })
    await deleteContact(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch {
    // 取消删除
  }
}

onMounted(() => {
  loadResumes()
})
</script>

<style scoped lang="scss">
@use '../styles/variables.scss' as *;

.contacts-page {
  min-height: 100vh;
  background: $bg-primary;

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

    span {
      letter-spacing: 0.5px;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 12px;

      .el-select {
        width: 200px;

        .el-input__wrapper {
          background: $bg-primary;
          border: 1px solid $border-color;
          box-shadow: none;
          border-radius: $border-radius-sm;

          &.is-focus {
            border-color: $primary;
            box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
          }
        }

        .el-input__inner {
          color: $text-primary;
          background: transparent;

          &::placeholder {
            color: $text-muted;
          }
        }

        .el-input__suffix-inner {
          color: $text-muted;
        }
      }
    }
  }

  :deep(.el-button) {
    border-radius: $border-radius-sm;
    font-weight: 500;
    transition: all $transition-fast;

    &.el-button--primary {
      background: $primary;
      border-color: $primary;
      color: #fff;

      &:hover {
        background: $primary-light;
        border-color: $primary-light;
        transform: translateY(-1px);
        box-shadow: $shadow-glow;
      }
    }

    &.el-button--danger {
      background: $danger;
      border-color: $danger;
      color: #fff;

      &:hover {
        background: #f87171;
        border-color: #f87171;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
      }
    }

    &.el-button--default {
      background: $bg-hover;
      border-color: $border-color;
      color: $text-primary;

      &:hover {
        background: #475569;
        border-color: #475569;
        color: #fff;
      }
    }

    &.is-link {
      background: transparent;
      border: none;
      padding: 4px 8px;

      &.el-button--primary {
        color: $primary-light;

        &:hover {
          color: $primary;
          background: rgba(99, 102, 241, 0.1);
          transform: none;
          box-shadow: none;
        }
      }

      &.el-button--danger {
        color: #f87171;

        &:hover {
          color: $danger;
          background: rgba(239, 68, 68, 0.1);
          transform: none;
          box-shadow: none;
        }
      }
    }
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

  :deep(.el-tag) {
    background: rgba(99, 102, 241, 0.15);
    border-color: rgba(99, 102, 241, 0.3);
    color: $primary-light;
    border-radius: $border-radius-sm;
    font-weight: 500;
    padding: 0 10px;
    height: 28px;
    line-height: 26px;
  }

  :deep(.el-dialog) {
    background: $bg-card;
    border: 1px solid $border-color;
    border-radius: $border-radius-lg;
    box-shadow: $shadow-lg;

    .el-dialog__header {
      border-bottom: 1px solid $border-color;
      padding: 18px 24px;
      margin-right: 0;

      .el-dialog__title {
        color: $text-primary;
        font-weight: 600;
        font-size: 16px;
      }

      .el-dialog__headerbtn {
        top: 18px;
        right: 24px;

        .el-dialog__close {
          color: $text-muted;

          &:hover {
            color: $text-primary;
          }
        }
      }
    }

    .el-dialog__body {
      padding: 24px;
      color: $text-primary;
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
      transition: all $transition-fast;

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

    .el-select {
      .el-input__wrapper {
        background: $bg-primary;
      }
    }
  }

  :deep(.el-select-dropdown) {
    background: $bg-card;
    border: 1px solid $border-color;
    box-shadow: $shadow-lg;
    border-radius: $border-radius-sm;

    .el-select-dropdown__item {
      color: $text-primary;

      &:hover,
      &.hover {
        background: $bg-hover;
      }

      &.selected {
        background: rgba(99, 102, 241, 0.15);
        color: $primary-light;
        font-weight: 600;
      }
    }
  }
}
</style>
