<template>
  <div class="educations-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>教育背景</span>
          <div class="header-actions">
            <el-select v-model="selectedResumeId" placeholder="选择简历" @change="loadEducations">
              <el-option
                v-for="resume in resumes"
                :key="resume.id"
                :label="resume.name"
                :value="resume.id"
              />
            </el-select>
            <el-button type="primary" @click="handleAdd">新增教育背景</el-button>
          </div>
        </div>
      </template>
      
      <el-table :data="educations" stripe v-loading="loading">
        <el-table-column type="index" width="60" />
        <el-table-column prop="school" label="学校" width="200" />
        <el-table-column prop="degree" label="学历" width="200" />
        <el-table-column prop="period" label="时间段" width="150" />
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
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
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑教育背景' : '新增教育背景'" width="600px">
      <el-form :model="form" label-width="100px" :rules="rules" ref="formRef">
        <el-form-item label="学校" prop="school">
          <el-input v-model="form.school" placeholder="如：北京大学" />
        </el-form-item>
        <el-form-item label="学历" prop="degree">
          <el-input v-model="form.degree" placeholder="如：计算机科学与技术 学士" />
        </el-form-item>
        <el-form-item label="时间段">
          <el-input v-model="form.period" placeholder="如：2018 - 2022" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="在校经历、主修课程等" />
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
import { getEducationsByResume, createEducation, updateEducation, deleteEducation } from '../api/educations'

const loading = ref(false)
const educations = ref([])
const resumes = ref([])
const selectedResumeId = ref(null)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)
const form = ref({
  id: null,
  school: '',
  degree: '',
  period: '',
  description: '',
  order: 0,
  resume_id: null
})

const rules = {
  school: [{ required: true, message: '请输入学校名称', trigger: 'blur' }],
  degree: [{ required: true, message: '请输入学历', trigger: 'blur' }],
  resume_id: [{ required: true, message: '请输入简历ID', trigger: 'blur' }]
}

const loadResumes = async () => {
  try {
    const data = await getResumes()
    resumes.value = data || []
    if (resumes.value.length > 0 && !selectedResumeId.value) {
      selectedResumeId.value = resumes.value[0].id
      await loadEducations()
    }
  } catch (error) {
    console.error('加载简历失败:', error)
  }
}

const loadEducations = async () => {
  if (!selectedResumeId.value) return
  loading.value = true
  try {
    const data = await getEducationsByResume(selectedResumeId.value)
    educations.value = data || []
  } catch (error) {
    console.error('加载教育背景失败:', error)
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  isEdit.value = false
  form.value = {
    id: null,
    school: '',
    degree: '',
    period: '',
    description: '',
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
      await updateEducation(form.value.id, form.value)
      ElMessage.success('更新成功')
    } else {
      await createEducation(form.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadEducations()
  } catch (error) {
    console.error('操作失败:', error)
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该教育背景吗？', '提示', { type: 'warning' })
    await deleteEducation(row.id)
    ElMessage.success('删除成功')
    loadEducations()
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

.educations-page {
  :deep(.el-card) {
    background-color: $bg-card;
    border: 1px solid $border-color;
    border-radius: $border-radius-lg;
    box-shadow: $shadow;

    .el-card__header {
      border-bottom: 1px solid $border-color;
      padding: 20px 24px;
    }
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    span {
      font-size: 18px;
      font-weight: 600;
      color: $text-primary;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 12px;

      .el-select {
        width: 200px;

        .el-input__wrapper {
          background-color: $bg-primary;
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
          background-color: transparent;

          &::placeholder {
            color: $text-muted;
          }
        }

        .el-input__suffix-inner {
          color: $text-muted;
        }
      }
    }

    .el-button {
      background: linear-gradient(135deg, $primary 0%, $primary-dark 100%);
      border: none;
      border-radius: $border-radius;
      padding: 10px 20px;
      font-weight: 500;
      transition: all $transition;

      &:hover {
        transform: translateY(-1px);
        box-shadow: $shadow-glow;
      }
    }
  }

  :deep(.el-table) {
    background-color: transparent;

    &::before {
      display: none;
    }

    .el-table__header-wrapper {
      th.el-table__cell {
        background-color: $bg-secondary;
        color: $text-secondary;
        font-weight: 600;
        border-bottom: 1px solid $border-color;
      }
    }

    .el-table__body-wrapper {
      td.el-table__cell {
        background-color: $bg-card;
        color: $text-primary;
        border-bottom: 1px solid $border-color;
      }

      tr:hover > td.el-table__cell {
        background-color: $bg-hover !important;
      }
    }

    .el-table__row--striped {
      .el-table__cell {
        background-color: $bg-primary !important;
      }
    }
  }

  :deep(.el-dialog) {
    background-color: $bg-card;
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
    .el-textarea__inner,
    .el-input-number .el-input__wrapper {
      background-color: $bg-primary;
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
      background-color: transparent;

      &::placeholder {
        color: $text-muted;
      }
    }

    .el-textarea__inner {
      color: $text-primary;
      background-color: $bg-primary;

      &::placeholder {
        color: $text-muted;
      }
    }

    .el-input-number__decrease,
    .el-input-number__increase {
      background-color: $bg-hover;
      border-color: $border-color;
      color: $text-secondary;

      &:hover {
        color: $text-primary;
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
      color: $danger;

      &:hover {
        color: mix(#fff, $danger, 25%);
      }
    }
  }
}
</style>
