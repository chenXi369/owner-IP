<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6" v-for="stat in stats" :key="stat.title">
        <el-card class="stat-card glass-card" shadow="hover">
          <div class="stat-content">
            <el-icon :size="40" :color="stat.color">
              <component :is="stat.icon" />
            </el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-title">{{ stat.title }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-20">
      <el-col :span="12">
        <el-card title="简历信息" class="glass-card">
          <template #header>
            <span>简历信息</span>
          </template>
          <div v-if="resume">
            <p><strong>姓名：</strong>{{ resume.name }}</p>
            <p><strong>职位：</strong>{{ resume.title }}</p>
            <p><strong>状态：</strong>
              <el-tag :type="resume.is_active ? 'success' : 'info'">
                {{ resume.is_active ? '已激活' : '未激活' }}
              </el-tag>
            </p>
            <p><strong>简介：</strong>{{ resume.description }}</p>
          </div>
          <el-empty v-else description="暂无数据" />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="glass-card">
          <template #header>
            <span>技能分布</span>
          </template>
          <div v-if="skills.length > 0">
            <div v-for="skill in skills" :key="skill.id" class="skill-item">
              <span>{{ skill.name }}</span>
              <el-progress :percentage="skill.level" :color="skill.color" />
            </div>
          </div>
          <el-empty v-else description="暂无数据" />
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-20">
      <el-col :span="24">
        <el-card class="glass-card">
          <template #header>
            <span>最新留言</span>
          </template>
          <el-table :data="messages" stripe style="width: 100%">
            <el-table-column prop="name" label="姓名" width="120" />
            <el-table-column prop="email" label="邮箱" width="180" />
            <el-table-column prop="message" label="内容" show-overflow-tooltip />
            <el-table-column prop="created_at" label="时间" width="180">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Document, Star, Folder, Message } from '@element-plus/icons-vue'
import { getActiveResume } from '../api/resume'
import { getMessages } from '../api/messages'

const resume = ref(null)
const skills = ref([])
const projects = ref([])
const messages = ref([])

const stats = ref([
  { title: '技能数量', value: 0, icon: 'Star', color: '#E6A23C' },
  { title: '项目数量', value: 0, icon: 'Folder', color: '#409EFF' },
  { title: '工作经历', value: 0, icon: 'Document', color: '#67C23A' },
  { title: '未读留言', value: 0, icon: 'Message', color: '#F56C6C' }
])

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

const loadData = async () => {
  try {
    const resumeData = await getActiveResume()
    if (resumeData) {
      resume.value = resumeData.resume
      skills.value = resumeData.skills || []
      projects.value = resumeData.projects || []
      
      stats.value[0].value = skills.value.length
      stats.value[1].value = projects.value.length
      stats.value[2].value = (resumeData.experiences || []).length
    }

    const msgData = await getMessages()
    messages.value = (msgData || []).slice(0, 5)
    stats.value[3].value = (msgData || []).filter(m => !m.is_read).length
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
@use '../styles/variables.scss' as *;

.dashboard {
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
      color: $text-primary;
    }

    .el-card__body {
      padding: 24px;
      background: transparent;
      color: $text-primary;
    }
  }

  :deep(.el-empty__description) {
    color: $text-muted;
  }
}

.stat-card {
  margin-bottom: 0;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: $text-primary;
}

.stat-title {
  font-size: 14px;
  color: $text-secondary;
  margin-top: 4px;
}

.mt-20 {
  margin-top: 20px;
}

.skill-item {
  margin-bottom: 12px;
}

.skill-item span {
  display: inline-block;
  width: 80px;
  font-size: 14px;
  color: $text-secondary;
}

p {
  margin: 8px 0;
  color: $text-secondary;
  line-height: 1.6;
}
</style>
