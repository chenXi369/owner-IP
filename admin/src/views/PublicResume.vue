<template>
  <div class="public-resume-page">
    <div v-if="loading" class="loading-wrapper">
      <el-icon size="32" class="is-loading"><Loading /></el-icon>
      <span>加载中...</span>
    </div>

    <div v-else-if="!resume" class="empty-wrapper">
      <el-empty description="简历不存在或已被删除" />
    </div>

    <template v-else>
      <!-- 个人信息卡片 -->
      <el-card class="profile-card">
        <div class="profile-header">
          <el-avatar :size="80" :src="resume.avatar_url" v-if="resume.avatar_url">
            <el-icon size="40"><User /></el-icon>
          </el-avatar>
          <div class="profile-info">
            <h1 class="profile-name">{{ resume.greeting }} {{ resume.name }}</h1>
            <p class="profile-title">{{ resume.title }}</p>
            <p class="profile-desc">{{ resume.description }}</p>
          </div>
        </div>
      </el-card>

      <!-- 技能分布 -->
      <el-card v-if="skills.length > 0" class="section-card">
        <template #header>
          <div class="section-title">技能专长</div>
        </template>
        <div class="skills-grid">
          <div v-for="skill in skills" :key="skill.id" class="skill-item">
            <div class="skill-header">
              <span class="skill-name">{{ skill.name }}</span>
              <span class="skill-level">{{ skill.level }}%</span>
            </div>
            <el-progress :percentage="skill.level" :color="skill.color" :stroke-width="10" />
            <el-tag v-if="skill.category" size="small" class="skill-category">{{ skill.category }}</el-tag>
          </div>
        </div>
      </el-card>

      <!-- 工作经历 -->
      <el-card v-if="experiences.length > 0" class="section-card">
        <template #header>
          <div class="section-title">工作经历</div>
        </template>
        <div class="timeline">
          <div v-for="exp in experiences" :key="exp.id" class="timeline-item">
            <div class="timeline-dot" />
            <div class="timeline-content">
              <h3>{{ exp.position }}</h3>
              <p class="timeline-company">{{ exp.company }} · {{ exp.period }}</p>
              <ul v-if="exp.details?.length">
                <li v-for="(detail, idx) in exp.details" :key="idx">{{ detail }}</li>
              </ul>
              <div v-if="exp.tech_stack?.length" class="tech-tags">
                <el-tag v-for="tech in exp.tech_stack" :key="tech" size="small">{{ tech }}</el-tag>
              </div>
            </div>
          </div>
        </div>
      </el-card>

      <!-- 项目展示 -->
      <el-card v-if="projects.length > 0" class="section-card">
        <template #header>
          <div class="section-title">项目经历</div>
        </template>
        <div class="project-list">
          <div v-for="proj in projects" :key="proj.id" class="project-item">
            <div class="project-header">
              <h3>{{ proj.title }}</h3>
              <el-tag v-if="proj.is_featured" type="success" size="small">精选</el-tag>
            </div>
            <p class="project-type">{{ proj.type }}</p>
            <p class="project-desc">{{ proj.description }}</p>
            <div v-if="proj.tech_stack?.length" class="tech-tags">
              <el-tag v-for="tech in proj.tech_stack" :key="tech" size="small">{{ tech }}</el-tag>
            </div>
            <div class="project-links" v-if="proj.github_url || proj.demo_url">
              <a v-if="proj.github_url" :href="proj.github_url" target="_blank" class="link">
                <el-icon><Link /></el-icon> GitHub
              </a>
              <a v-if="proj.demo_url" :href="proj.demo_url" target="_blank" class="link">
                <el-icon><View /></el-icon> 演示地址
              </a>
            </div>
          </div>
        </div>
      </el-card>

      <!-- 教育背景 -->
      <el-card v-if="educations.length > 0" class="section-card">
        <template #header>
          <div class="section-title">教育背景</div>
        </template>
        <div class="education-list">
          <div v-for="edu in educations" :key="edu.id" class="education-item">
            <h3>{{ edu.school }}</h3>
            <p>{{ edu.degree }} · {{ edu.period }}</p>
            <p v-if="edu.description" class="edu-desc">{{ edu.description }}</p>
          </div>
        </div>
      </el-card>

      <!-- 联系方式 -->
      <el-card v-if="contacts.length > 0" class="section-card">
        <template #header>
          <div class="section-title">联系方式</div>
        </template>
        <div class="contact-list">
          <div v-for="contact in contacts" :key="contact.id" class="contact-item">
            <el-icon size="18"><component :is="getContactIcon(contact.type)" /></el-icon>
            <span class="contact-label">{{ contact.label }}</span>
            <span class="contact-value">{{ contact.value }}</span>
          </div>
        </div>
      </el-card>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Loading, Link, View, Message, Phone, Location, Link as LinkIcon } from '@element-plus/icons-vue'
import { getPublicResume } from '../api/resume'

const route = useRoute()
const loading = ref(true)
const resume = ref(null)
const skills = ref([])
const projects = ref([])
const experiences = ref([])
const educations = ref([])
const contacts = ref([])

const getContactIcon = (type) => {
  const map = {
    email: 'Message',
    phone: 'Phone',
    address: 'Location',
    github: 'LinkIcon',
    wechat: 'ChatDotRound',
    qq: 'ChatSquare',
    blog: 'EditPen',
    website: 'LinkIcon'
  }
  return map[type] || 'InfoFilled'
}

const loadResume = async () => {
  loading.value = true
  try {
    const userId = route.params.userId
    const slug = route.params.resumeSlug
    const data = await getPublicResume(userId, slug)
    resume.value = data.resume
    skills.value = data.skills || []
    projects.value = data.projects || []
    experiences.value = data.experiences || []
    educations.value = data.educations || []
    contacts.value = data.contacts || []
  } catch (error) {
    ElMessage.error('加载简历失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadResume()
})
</script>

<style scoped lang="scss">
.public-resume-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
  padding: 40px 24px;
  max-width: 900px;
  margin: 0 auto;
}

.loading-wrapper,
.empty-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  color: rgba(255, 255, 255, 0.6);
  gap: 16px;
}

.profile-card {
  background: rgba(30, 41, 59, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  margin-bottom: 24px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);

  :deep(.el-card__body) {
    padding: 32px;
  }
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 24px;
}

.profile-info {
  flex: 1;
}

.profile-name {
  font-size: 28px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 8px;
}

.profile-title {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.7);
  margin: 0 0 12px;
}

.profile-desc {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.5);
  margin: 0;
  line-height: 1.6;
}

.section-card {
  background: rgba(30, 41, 59, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  margin-bottom: 24px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);

  :deep(.el-card__header) {
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding: 20px 24px;
  }

  :deep(.el-card__body) {
    padding: 24px;
  }
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #fff;
}

.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.skill-item {
  background: rgba(15, 23, 42, 0.5);
  border-radius: 12px;
  padding: 16px;
}

.skill-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.skill-name {
  font-size: 15px;
  font-weight: 500;
  color: #fff;
}

.skill-level {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
}

.skill-category {
  margin-top: 8px;
  background: rgba(99, 102, 241, 0.15);
  border-color: rgba(99, 102, 241, 0.3);
  color: #a5b4fc;
}

.timeline {
  position: relative;
  padding-left: 24px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 6px;
  top: 8px;
  bottom: 8px;
  width: 2px;
  background: rgba(99, 102, 241, 0.3);
}

.timeline-item {
  position: relative;
  margin-bottom: 24px;
}

.timeline-dot {
  position: absolute;
  left: -22px;
  top: 6px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #6366f1;
  border: 2px solid #0f172a;
}

.timeline-content {
  h3 {
    font-size: 16px;
    font-weight: 600;
    color: #fff;
    margin: 0 0 4px;
  }
}

.timeline-company {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  margin: 0 0 12px;
}

.timeline-content ul {
  margin: 0 0 12px;
  padding-left: 18px;
}

.timeline-content li {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 4px;
  line-height: 1.5;
}

.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;

  :deep(.el-tag) {
    background: rgba(99, 102, 241, 0.15);
    border-color: rgba(99, 102, 241, 0.3);
    color: #a5b4fc;
  }
}

.project-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.project-item {
  background: rgba(15, 23, 42, 0.5);
  border-radius: 12px;
  padding: 20px;
}

.project-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;

  h3 {
    font-size: 16px;
    font-weight: 600;
    color: #fff;
    margin: 0;
  }
}

.project-type {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
  margin: 0 0 8px;
}

.project-desc {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  margin: 0 0 12px;
  line-height: 1.6;
}

.project-links {
  display: flex;
  gap: 16px;
  margin-top: 12px;
}

.link {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #818cf8;
  text-decoration: none;
  transition: color 0.2s;

  &:hover {
    color: #a5b4fc;
  }
}

.education-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.education-item {
  background: rgba(15, 23, 42, 0.5);
  border-radius: 12px;
  padding: 16px;

  h3 {
    font-size: 16px;
    font-weight: 600;
    color: #fff;
    margin: 0 0 4px;
  }

  p {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.6);
    margin: 0;
  }
}

.edu-desc {
  margin-top: 8px !important;
  color: rgba(255, 255, 255, 0.5) !important;
  line-height: 1.5;
}

.contact-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 12px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 10px;
  padding: 12px 16px;
  color: rgba(255, 255, 255, 0.8);

  .el-icon {
    color: #818cf8;
  }
}

.contact-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
  min-width: 50px;
}

.contact-value {
  font-size: 14px;
  color: #fff;
}

@media (max-width: 600px) {
  .profile-header {
    flex-direction: column;
    text-align: center;
  }

  .skills-grid {
    grid-template-columns: 1fr;
  }

  .contact-list {
    grid-template-columns: 1fr;
  }
}
</style>
