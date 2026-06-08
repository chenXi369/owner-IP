<template>
  <div class="experiences-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>工作经历</span>
          <div class="header-right">
            <el-select v-model="selectedResumeId" placeholder="选择简历" @change="loadExperiences" style="width: 200px; margin-right: 12px;">
              <el-option v-for="resume in resumes" :key="resume.id" :label="resume.name" :value="resume.id" />
            </el-select>
            <el-button type="primary" @click="handleAdd">新增经历</el-button>
          </div>
        </div>
      </template>
      
      <el-table :data="experiences" stripe v-loading="loading">
        <el-table-column type="index" width="60" />
        <el-table-column prop="position" label="职位" width="180" />
        <el-table-column prop="company" label="公司" width="180" />
        <el-table-column prop="period" label="时间段" width="150" />
        <el-table-column label="职责" show-overflow-tooltip>
          <template #default="{ row }">
            {{ row.details?.join('；') || '-' }}
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
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑工作经历' : '新增工作经历'" width="600px">
      <el-form :model="form" label-width="100px" :rules="rules" ref="formRef">
        <el-form-item label="职位" prop="position">
          <el-input v-model="form.position" />
        </el-form-item>
        <el-form-item label="公司" prop="company">
          <el-input v-model="form.company" />
        </el-form-item>
        <el-form-item label="时间段">
          <el-input v-model="form.period" placeholder="如：2023年10月 - 至今" />
        </el-form-item>
        <el-form-item label="职责详情">
          <div v-for="(detail, index) in form.details" :key="index" class="detail-row">
            <el-input v-model="form.details[index]" placeholder="输入职责描述">
              <template #append>
                <el-button @click="removeDetail(index)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </template>
            </el-input>
          </div>
          <el-button type="primary" link @click="addDetail" style="margin-top: 8px">
            + 添加职责
          </el-button>
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
        <el-form-item label="排序">
          <el-input-number v-model="form.order" :min="0" />
        </el-form-item>
        <el-form-item prop="resume_id" v-show="false">
          <el-input v-model.number="form.resume_id" />
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
import { Delete } from '@element-plus/icons-vue'
import { getExperiencesByResume, createExperience, updateExperience, deleteExperience } from '../api/experiences'
import { getResumes } from '../api/resume'

const loading = ref(false)
const experiences = ref([])
const resumes = ref([])
const selectedResumeId = ref(null)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)
const form = ref({
  id: null,
  position: '',
  company: '',
  period: '',
  details: [''],
  tech_stack: [],
  order: 0,
  resume_id: 1
})

const rules = {
  position: [{ required: true, message: '请输入职位', trigger: 'blur' }],
  company: [{ required: true, message: '请输入公司', trigger: 'blur' }],
  resume_id: [{ required: true, message: '请输入简历ID', trigger: 'blur' }]
}

const loadResumes = async () => {
  loading.value = true
  try {
    const data = await getResumes()
    resumes.value = data || []
    if (resumes.value.length > 0 && !selectedResumeId.value) {
      selectedResumeId.value = resumes.value[0].id
      await loadExperiences()
    }
  } catch (error) {
    console.error('加载简历列表失败:', error)
  } finally {
    loading.value = false
  }
}

const loadExperiences = async () => {
  if (!selectedResumeId.value) return
  loading.value = true
  try {
    const data = await getExperiencesByResume(selectedResumeId.value)
    experiences.value = data || []
  } catch (error) {
    console.error('加载工作经历失败:', error)
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  isEdit.value = false
  form.value = {
    id: null,
    position: '',
    company: '',
    period: '',
    details: [''],
    tech_stack: [],
    order: 0,
    resume_id: selectedResumeId.value
  }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  form.value = {
    ...row,
    details: [...(row.details || [])],
    tech_stack: [...(row.tech_stack || [])]
  }
  dialogVisible.value = true
}

const addDetail = () => {
  form.value.details.push('')
}

const removeDetail = (index) => {
  form.value.details.splice(index, 1)
  if (form.value.details.length === 0) {
    form.value.details.push('')
  }
}

const handleSubmit = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  // 过滤空详情
  form.value.details = form.value.details.filter(d => d.trim())

  try {
    if (isEdit.value) {
      await updateExperience(form.value.id, form.value)
      ElMessage.success('更新成功')
    } else {
      await createExperience(form.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadExperiences()
  } catch (error) {
    console.error('操作失败:', error)
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该工作经历吗？', '提示', { type: 'warning' })
    await deleteExperience(row.id)
    ElMessage.success('删除成功')
    loadExperiences()
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

.experiences-page {

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

    .header-right {
      display: flex;
      align-items: center;
    }

    span {
      font-size: 18px;
      font-weight: 600;
      color: $text-primary;
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

  .detail-row {
    margin-bottom: 12px;

    &:last-child {
      margin-bottom: 0;
    }

    :deep(.el-input__wrapper) {
      background-color: $bg-primary;
    }

    :deep(.el-input-group__append) {
      background-color: $bg-hover;
      border-color: $border-color;
      color: $danger;
      padding: 0 16px;

      .el-button {
        color: $danger;
        border: none;
        background: transparent;

        &:hover {
          color: mix(#fff, $danger, 25%);
        }
      }
    }
  }

  :deep(.el-select) {
    .el-select__tags {
      .el-tag {
        background-color: rgba($primary, 0.15);
        border-color: rgba($primary, 0.3);
        color: $primary-light;
        border-radius: $border-radius-sm;

        .el-tag__close {
          color: $primary-light;
          background-color: transparent;

          &:hover {
            color: $text-primary;
            background-color: rgba($primary, 0.3);
          }
        }
      }
    }

    .el-input__wrapper {
      background-color: $bg-primary;
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
        color: lighten($danger, 10%);
      }
    }
  }
}
</style>
