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
      <!-- 管理员：显示所有简历列表 -->
      <el-col :span="12" v-if="isAdmin">
        <el-card class="glass-card">
          <template #header>
            <span>简历列表</span>
          </template>
          <el-table :data="resumes" stripe style="width: 100%">
            <el-table-column prop="name" label="姓名" width="120" />
            <el-table-column prop="title" label="职位" min-width="140" />
            <el-table-column prop="is_active" label="状态" width="90">
              <template #default="{ row }">
                <el-tag :type="row.is_active ? 'success' : 'info'" size="small">
                  {{ row.is_active ? '已激活' : '未激活' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="160">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <!-- 普通用户：显示当前简历信息 -->
      <el-col :span="12" v-else>
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
            <div class="card-header-with-select">
              <span>技能分布</span>
              <el-select
                v-if="isAdmin"
                v-model="selectedResumeId"
                placeholder="选择简历"
                size="small"
                style="width: 160px"
                @change="handleResumeChange"
              >
                <el-option
                  v-for="r in resumes"
                  :key="r.id"
                  :label="r.name"
                  :value="r.id"
                />
              </el-select>
            </div>
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

    <!-- 普通用户显示最新留言，管理员不显示 -->
    <el-row :gutter="20" class="mt-20" v-if="!isAdmin">
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
import { ref, onMounted, computed } from 'vue'
import { Document, Star, Folder, Message, UserFilled } from '@element-plus/icons-vue'
import { useUserStore } from '../stores/user'
import { getActiveResume, getResumes } from '../api/resume'
import { getAllSkills, getSkillStats } from '../api/skills'
import { getAllProjects } from '../api/projects'
import { getMessages } from '../api/messages'
import { getUsers } from '../api/users'

const userStore = useUserStore()
const isAdmin = computed(() => userStore.isAdmin)

const resume = ref(null)
const skills = ref([])
const projects = ref([])
const messages = ref([])
const experiences = ref([])
const educations = ref([])
const contacts = ref([])
const resumes = ref([])
const users = ref([])
const selectedResumeId = ref(null)

const stats = ref([])

const adminStats = computed(() => [
  { title: '简历总数', value: resumes.value.length, icon: 'Document', color: '#6366f1' },
  { title: '技能总数', value: skills.value.length, icon: 'Star', color: '#E6A23C' },
  { title: '项目总数', value: projects.value.length, icon: 'Folder', color: '#409EFF' },
  { title: '用户总数', value: users.value.length, icon: 'UserFilled', color: '#67C23A' }
])

const userStats = computed(() => [
  { title: '技能数量', value: skills.value.length, icon: 'Star', color: '#E6A23C' },
  { title: '项目数量', value: projects.value.length, icon: 'Folder', color: '#409EFF' },
  { title: '工作经历', value: experiences.value.length, icon: 'Document', color: '#67C23A' },
  { title: '未读留言', value: (messages.value || []).filter(m => !m.is_read).length, icon: 'Message', color: '#F56C6C' }
])

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

const loadSkillStats = async (resumeId) => {
  try {
    const data = await getSkillStats(resumeId)
    skills.value = data || []
  } catch (error) {
    console.error('加载技能统计失败:', error)
  }
}

const handleResumeChange = (resumeId) => {
  selectedResumeId.value = resumeId
  loadSkillStats(resumeId)
}

const loadData = async () => {
  try {
    if (isAdmin.value) {
      const [resumeData, skillData, projectData, userData] = await Promise.all([
        getResumes(),
        getAllSkills(),
        getAllProjects(),
        getUsers()
      ])
      resumes.value = resumeData || []
      skills.value = skillData || []
      projects.value = projectData || []
      users.value = userData || []
      stats.value = adminStats.value
    } else {
      const resumeData = await getActiveResume()
      const msgData = await getMessages()
      if (resumeData) {
        resume.value = resumeData.resume
        skills.value = resumeData.skills || []
        projects.value = resumeData.projects || []
        experiences.value = resumeData.experiences || []
        educations.value = resumeData.educations || []
        contacts.value = resumeData.contacts || []
      }
      messages.value = (msgData || []).slice(0, 5)
      stats.value = userStats.value
    }
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

.card-header-with-select {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

p {
  margin: 8px 0;
  color: $text-secondary;
  line-height: 1.6;
}
</style>
