<template>
  <div class="my-skills-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>我的技能</span>
          <div class="header-actions">
            <el-select
              v-model="selectedResumeId"
              placeholder="选择简历"
              style="width: 200px"
              @change="loadSkills"
            >
              <el-option
                v-for="resume in resumes"
                :key="resume.id"
                :label="resume.name"
                :value="resume.id"
              />
            </el-select>
            <el-button type="primary" @click="handleAdd">新增技能</el-button>
          </div>
        </div>
      </template>

      <el-table :data="skills" stripe v-loading="loading" style="width: 100%">
        <el-table-column type="index" width="60" />
        <el-table-column prop="name" label="技能名称" min-width="120" />
        <el-table-column prop="level" label="熟练度" min-width="200">
          <template #default="{ row }">
            <el-progress :percentage="row.level" :color="row.color" />
          </template>
        </el-table-column>
        <el-table-column prop="color" label="颜色" width="120">
          <template #default="{ row }">
            <el-color-picker v-model="row.color" disabled />
          </template>
        </el-table-column>
        <el-table-column prop="category" label="分类" min-width="100" />
        <el-table-column prop="order" label="排序" width="80" />
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleEdit(row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑技能' : '新增技能'" width="500px">
      <el-form :model="form" label-width="100px" :rules="rules" ref="formRef">
        <el-form-item label="技能名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="熟练度" prop="level">
          <el-slider v-model="form.level" :max="100" show-input />
        </el-form-item>
        <el-form-item label="颜色">
          <el-color-picker v-model="form.color" />
        </el-form-item>
        <el-form-item label="分类">
          <el-input v-model="form.category" placeholder="如：前端、后端" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.order" :min="0" />
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
import { ElMessage } from 'element-plus'
import { getSkillsByResume, createSkill, updateSkill } from '../api/skills'
import { getResumes } from '../api/resume'

const loading = ref(false)
const skills = ref([])
const resumes = ref([])
const selectedResumeId = ref(null)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)
const form = ref({
  id: null,
  name: '',
  level: 80,
  color: '#42b883',
  category: '',
  order: 0
})

const rules = {
  name: [{ required: true, message: '请输入技能名称', trigger: 'blur' }]
}

const loadResumes = async () => {
  try {
    const data = await getResumes()
    resumes.value = Array.isArray(data) ? data : (data?.data || [])
    if (resumes.value.length > 0 && !selectedResumeId.value) {
      selectedResumeId.value = resumes.value[0].id
      await loadSkills()
    }
  } catch (error) {
    console.error('加载简历列表失败:', error)
  }
}

const loadSkills = async () => {
  if (!selectedResumeId.value) return
  loading.value = true
  try {
    const data = await getSkillsByResume(selectedResumeId.value)
    skills.value = Array.isArray(data) ? data : (data?.data || [])
  } catch (error) {
    console.error('加载技能失败:', error)
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  isEdit.value = false
  form.value = {
    id: null,
    name: '',
    level: 80,
    color: '#42b883',
    category: '',
    order: 0
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
      await updateSkill(form.value.id, form.value)
      ElMessage.success('更新成功')
    } else {
      await createSkill({ ...form.value, resume_id: selectedResumeId.value })
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadSkills()
  } catch (error) {
    console.error('操作失败:', error)
  }
}

onMounted(() => {
  loadResumes()
})
</script>

<style scoped lang="scss">
@use '../styles/variables.scss' as *;

.my-skills-page {
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

  .header-actions {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  :deep(.el-select) {
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
    }

    .el-select__caret {
      color: $text-muted;
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

    .el-slider__runway {
      background: $bg-hover;
    }
  }

  :deep(.el-color-picker) {
    .el-color-picker__trigger {
      border-color: $border-color;
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
  }
}
</style>
