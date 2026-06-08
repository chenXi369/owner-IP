<template>
  <div class="projects-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>项目列表</span>
          <div class="header-right">
            <el-select
              v-model="selectedResumeId"
              placeholder="选择简历"
              style="width: 180px; margin-right: 12px"
              @change="loadProjects"
            >
              <el-option
                v-for="resume in resumes"
                :key="resume.id"
                :label="resume.name"
                :value="resume.id"
              />
            </el-select>
            <el-button type="primary" @click="handleAdd">新增项目</el-button>
          </div>
        </div>
      </template>
      
      <el-table :data="projects" stripe v-loading="loading">
        <el-table-column type="index" width="60" />
        <el-table-column prop="title" label="项目名称" width="180" />
        <el-table-column prop="type" label="类型" width="120" />
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
        <el-table-column prop="tech_stack" label="技术栈" width="200">
          <template #default="{ row }">
            <el-tag v-for="tech in row.tech_stack" :key="tech" size="small" style="margin-right: 4px">
              {{ tech }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_featured" label="精选" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_featured ? 'success' : 'info'">
              {{ row.is_featured ? '是' : '否' }}
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
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑项目' : '新增项目'" width="600px">
      <el-form :model="form" label-width="100px" :rules="rules" ref="formRef">
        <el-form-item label="项目名称" prop="title">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="类型">
          <el-input v-model="form.type" placeholder="如：电商平台、管理系统" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="技术栈">
          <el-select
            v-model="form.tech_stack"
            multiple
            filterable
            allow-create
            placeholder="输入技术栈"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="GitHub">
          <el-input v-model="form.github_url" />
        </el-form-item>
        <el-form-item label="演示地址">
          <el-input v-model="form.demo_url" />
        </el-form-item>
        <el-form-item label="精选">
          <el-switch v-model="form.is_featured" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.order" :min="0" />
        </el-form-item>
        <el-form-item label="简历ID" prop="resume_id" v-show="false">
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
import { getProjectsByResume, createProject, updateProject, deleteProject } from '../api/projects'
import { getResumes } from '../api/resume'

const loading = ref(false)
const projects = ref([])
const resumes = ref([])
const selectedResumeId = ref(null)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)
const form = ref({
  id: null,
  title: '',
  type: '',
  description: '',
  tech_stack: [],
  github_url: '',
  demo_url: '',
  is_featured: false,
  order: 0,
  resume_id: 1
})

const rules = {
  title: [{ required: true, message: '请输入项目名称', trigger: 'blur' }],
  resume_id: [{ required: true, message: '请输入简历ID', trigger: 'blur' }]
}

const loadResumes = async () => {
  try {
    const data = await getResumes()
    resumes.value = data || []
    if (resumes.value.length > 0 && !selectedResumeId.value) {
      selectedResumeId.value = resumes.value[0].id
      await loadProjects()
    }
  } catch (error) {
    console.error('加载简历失败:', error)
  }
}

const loadProjects = async () => {
  if (!selectedResumeId.value) return
  loading.value = true
  try {
    const data = await getProjectsByResume(selectedResumeId.value)
    projects.value = data || []
  } catch (error) {
    console.error('加载项目失败:', error)
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  isEdit.value = false
  form.value = {
    id: null,
    title: '',
    type: '',
    description: '',
    tech_stack: [],
    github_url: '',
    demo_url: '',
    is_featured: false,
    order: 0,
    resume_id: selectedResumeId.value
  }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  form.value = { ...row, tech_stack: [...(row.tech_stack || [])] }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  try {
    if (isEdit.value) {
      await updateProject(form.value.id, form.value)
      ElMessage.success('更新成功')
    } else {
      await createProject(form.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadProjects()
  } catch (error) {
    console.error('操作失败:', error)
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该项目吗？', '提示', { type: 'warning' })
    await deleteProject(row.id)
    ElMessage.success('删除成功')
    loadProjects()
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

.projects-page {
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

  .header-right {
    display: flex;
    align-items: center;
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

    .el-select {
      .el-input__wrapper {
        background: $bg-primary;
      }

      .el-select__tags {
        .el-tag {
          background: rgba(99, 102, 241, 0.15);
          border-color: rgba(99, 102, 241, 0.3);
          color: $primary-light;
        }
      }
    }
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
