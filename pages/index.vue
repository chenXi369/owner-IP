<template>
  <div class="home-page">
    <section id="hero" data-section class="hero-section section">
      <div class="container">
        <div class="hero-content">
          <div class="hero-text">
            <p class="hero-greeting fade-in stagger-1">你好，我是</p>
            <h1 class="hero-name fade-in stagger-2">
              <span class="text-gradient">前端小李</span>
            </h1>
            <h2 class="hero-title fade-in stagger-3">
              <span>{{ displayText }}</span>
              <span class="cursor">|</span>
            </h2>
            <p class="hero-description fade-in stagger-4">
              专注于创建卓越用户体验的全栈开发工程师，<br>
              热爱Three.js 3D可视化与创意交互设计
            </p>
            <div class="hero-cta fade-in stagger-5">
              <a href="#projects" class="btn btn-primary">
                <span>查看项目</span>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
              </a>
              <a href="#contact" class="btn btn-outline">
                <span>联系我</span>
              </a>
            </div>
          </div>
          <div class="hero-visual">
            <ClientOnly>
              <ParticleAvatar />
            </ClientOnly>
          </div>
        </div>
        <div class="scroll-indicator">
          <span>向下滚动</span>
          <div class="scroll-arrow"></div>
        </div>
      </div>
    </section>

    <section id="about" data-section class="about-section section">
      <div class="container">
        <div class="section-header">
          <span class="section-number">01.</span>
          <h2 class="section-title">关于我</h2>
          <p class="section-subtitle">了解我的背景和故事</p>
        </div>
        
        <div class="about-content">
          <div class="about-text">
            <div class="about-card glass-card">
              <p>
                我是一名拥有 <strong>5年+</strong> 经验的全栈开发工程师，专注于前端技术和3D可视化领域。
                我热爱将创意与技术结合，打造令人惊叹的用户体验。
              </p>
              <p>
                在我的职业生涯中，我参与了多个大型项目的开发，包括电商平台、数据可视化系统、
                以及多个创意交互网站。我擅长使用 Vue.js、React、Three.js 等技术栈，
                并持续探索 WebGL、WebXR 等前沿技术。
              </p>
              <p>
                除了编程，我还热衷于分享知识，在技术社区发表过多篇文章，
                并在多个技术大会上进行过演讲。我相信技术可以改变世界，
                而我正在为此贡献自己的力量。
              </p>
            </div>
            
            <div class="about-stats">
              <div class="stat-item">
                <span class="stat-number">5+</span>
                <span class="stat-label">年开发经验</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">50+</span>
                <span class="stat-label">完成项目</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">20+</span>
                <span class="stat-label">技术文章</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">10+</span>
                <span class="stat-label">开源贡献</span>
              </div>
            </div>
          </div>
          
          <div class="about-image">
            <div class="image-frame">
              <div class="image-placeholder">
                <span>照片占位</span>
              </div>
            </div>
            <div class="image-decoration"></div>
          </div>
        </div>
      </div>
    </section>

    <section id="skills" data-section class="skills-section section">
      <div class="container">
        <div class="section-header">
          <span class="section-number">02.</span>
          <h2 class="section-title">技能专长</h2>
          <p class="section-subtitle">我的技术栈和专业能力</p>
        </div>
        
        <div class="skills-content">
          <div class="skills-3d">
            <ClientOnly>
              <SkillsGeometry :active-index="activeSkillIndex" />
            </ClientOnly>
          </div>
          
          <div class="skills-list">
            <div 
              v-for="(skill, index) in skills" 
              :key="skill.name"
              class="skill-item"
              :class="{ active: activeSkillIndex === index }"
              @mouseenter="activeSkillIndex = index"
            >
              <div class="skill-header">
                <span class="skill-icon" :style="{ color: skill.color }">◆</span>
                <span class="skill-name">{{ skill.name }}</span>
                <span class="skill-level">{{ skill.level }}%</span>
              </div>
              <div class="skill-bar">
                <div 
                  class="skill-progress" 
                  :style="{ 
                    width: `${skill.level}%`,
                    background: skill.color 
                  }"
                ></div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="skills-categories">
          <div v-for="category in skillCategories" :key="category.name" class="category-card glass-card">
            <h3 class="category-title">{{ category.name }}</h3>
            <div class="category-tags">
              <span v-for="tag in category.tags" :key="tag" class="tag">{{ tag }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="projects" data-section class="projects-section section">
      <div class="container">
        <div class="section-header">
          <span class="section-number">03.</span>
          <h2 class="section-title">项目作品</h2>
          <p class="section-subtitle">我参与的一些代表性项目</p>
        </div>
        
        <div class="projects-grid">
          <div 
            v-for="project in projects" 
            :key="project.title"
            class="project-card"
            :class="{ 'featured': project.featured }"
          >
            <div class="project-image">
              <div class="image-placeholder">{{ project.title }}</div>
              <div class="project-overlay">
                <div class="project-links">
                  <a v-if="project.github" :href="project.github" class="project-link" target="_blank">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
                    </svg>
                  </a>
                  <a v-if="project.demo" :href="project.demo" class="project-link" target="_blank">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3"/>
                    </svg>
                  </a>
                </div>
              </div>
            </div>
            <div class="project-content">
              <span class="project-type">{{ project.type }}</span>
              <h3 class="project-title">{{ project.title }}</h3>
              <p class="project-description">{{ project.description }}</p>
              <div class="project-tech">
                <span v-for="tech in project.tech" :key="tech" class="tech-tag">{{ tech }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="experience" data-section class="experience-section section">
      <div class="container">
        <div class="section-header">
          <span class="section-number">04.</span>
          <h2 class="section-title">工作经历</h2>
          <p class="section-subtitle">我的职业发展历程</p>
        </div>
        
        <div class="timeline">
          <div v-for="exp in experiences" :key="exp.company" class="timeline-item">
            <div class="timeline-marker"></div>
            <div class="timeline-content glass-card">
              <div class="timeline-header">
                <h3 class="timeline-title">{{ exp.position }}</h3>
                <span class="timeline-company">{{ exp.company }}</span>
              </div>
              <span class="timeline-date">{{ exp.period }}</span>
              <ul class="timeline-details">
                <li v-for="(detail, i) in exp.details" :key="i">{{ detail }}</li>
              </ul>
              <div class="timeline-tech">
                <span v-for="tech in exp.tech" :key="tech" class="tech-tag">{{ tech }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="education-section">
          <h3 class="subsection-title">教育背景</h3>
          <div class="education-cards">
            <div v-for="edu in education" :key="edu.school" class="education-card glass-card">
              <div class="edu-icon">🎓</div>
              <div class="edu-content">
                <h4 class="edu-school">{{ edu.school }}</h4>
                <p class="edu-degree">{{ edu.degree }}</p>
                <span class="edu-period">{{ edu.period }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="contact" data-section class="contact-section section">
      <div class="container">
        <div class="section-header centered">
          <span class="section-number">05.</span>
          <h2 class="section-title">联系我</h2>
          <p class="section-subtitle">期待与您交流合作</p>
        </div>
        
        <div class="contact-content">
          <div class="contact-info">
            <div class="contact-item">
              <div class="contact-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                  <polyline points="22,6 12,13 2,6"/>
                </svg>
              </div>
              <div class="contact-text">
                <span class="contact-label">邮箱</span>
                <a href="mailto:example@email.com">example@email.com</a>
              </div>
            </div>
            
            <div class="contact-item">
              <div class="contact-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/>
                </svg>
              </div>
              <div class="contact-text">
                <span class="contact-label">电话</span>
                <a href="tel:+8612345678900">+86 123 4567 8900</a>
              </div>
            </div>
            
            <div class="contact-item">
              <div class="contact-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/>
                  <circle cx="12" cy="10" r="3"/>
                </svg>
              </div>
              <div class="contact-text">
                <span class="contact-label">地址</span>
                <span>中国 · 北京</span>
              </div>
            </div>
          </div>
          
          <div class="contact-form-wrapper">
            <form class="contact-form glass-card" @submit.prevent="handleSubmit">
              <div class="form-group">
                <label for="name">姓名</label>
                <input type="text" id="name" v-model="form.name" placeholder="请输入您的姓名" required>
              </div>
              <div class="form-group">
                <label for="email">邮箱</label>
                <input type="email" id="email" v-model="form.email" placeholder="请输入您的邮箱" required>
              </div>
              <div class="form-group">
                <label for="message">留言</label>
                <textarea id="message" v-model="form.message" placeholder="请输入您的留言" rows="5" required></textarea>
              </div>
              <button type="submit" class="btn btn-primary submit-btn">
                <span>发送消息</span>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="22" y1="2" x2="11" y2="13"/>
                  <polygon points="22 2 15 22 11 13 2 9 22 2"/>
                </svg>
              </button>
            </form>
          </div>
        </div>
      </div>
    </section>

    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import gsap from 'gsap'
import { useTypewriter } from '~/composables/useAnimation'

const activeSkillIndex = ref(0)

const { displayText, type } = useTypewriter('全栈开发工程师 & 3D可视化专家', 80)

const skills = ref([
  { name: 'Vue.js', level: 95, color: '#42b883' },
  { name: 'React', level: 90, color: '#61dafb' },
  { name: 'Three.js', level: 85, color: '#ff6b6b' },
  { name: 'TypeScript', level: 88, color: '#3178c6' },
  { name: 'Node.js', level: 82, color: '#68a063' },
  { name: 'WebGL', level: 78, color: '#9b59b6' }
])

const skillCategories = ref([
  {
    name: '前端框架',
    tags: ['Vue.js', 'React', 'Nuxt.js', 'Next.js', 'Angular']
  },
  {
    name: '3D & 可视化',
    tags: ['Three.js', 'WebGL', 'D3.js', 'ECharts', 'Canvas']
  },
  {
    name: '后端技术',
    tags: ['Node.js', 'Express', 'Nest.js', 'MongoDB', 'PostgreSQL']
  },
  {
    name: '工具 & 其他',
    tags: ['Git', 'Docker', 'Webpack', 'Vite', 'CI/CD']
  }
])

const projects = ref([
  {
    title: '3D数据可视化平台',
    type: '全栈项目',
    description: '基于Three.js开发的企业级3D数据可视化平台，支持实时数据展示、交互式图表和自定义场景编辑。',
    tech: ['Vue.js', 'Three.js', 'Node.js', 'MongoDB'],
    featured: true,
    github: '#',
    demo: '#'
  },
  {
    title: '电商管理系统',
    type: '前端项目',
    description: '功能完善的电商后台管理系统，包含商品管理、订单处理、数据分析等核心模块。',
    tech: ['React', 'TypeScript', 'Ant Design', 'Redux'],
    featured: true,
    github: '#',
    demo: '#'
  },
  {
    title: '创意作品集网站',
    type: '前端项目',
    description: '个人作品集网站，使用Nuxt.js和Three.js打造沉浸式3D交互体验。',
    tech: ['Nuxt.js', 'Three.js', 'GSAP', 'SCSS'],
    featured: false,
    github: '#',
    demo: '#'
  },
  {
    title: '实时协作工具',
    type: '全栈项目',
    description: '支持多人实时协作的在线白板工具，包含画笔、图形、文本等多种编辑功能。',
    tech: ['Vue.js', 'Socket.io', 'Canvas', 'Node.js'],
    featured: false,
    github: '#',
    demo: '#'
  }
])

const experiences = ref([
  {
    position: '高级前端工程师',
    company: '某科技公司',
    period: '2022.03 - 至今',
    details: [
      '负责公司核心产品的前端架构设计与开发',
      '主导3D可视化模块的技术选型与实现',
      '优化前端性能，页面加载速度提升40%',
      '带领5人团队完成多个重要项目交付'
    ],
    tech: ['Vue.js', 'Three.js', 'TypeScript', 'Node.js']
  },
  {
    position: '前端开发工程师',
    company: '某互联网公司',
    period: '2020.06 - 2022.02',
    details: [
      '参与电商平台前端开发，负责商品展示和购物车模块',
      '开发数据可视化大屏，实现实时数据展示',
      '编写前端组件库，提升团队开发效率'
    ],
    tech: ['React', 'Redux', 'ECharts', 'Webpack']
  },
  {
    position: '初级前端工程师',
    company: '某创业公司',
    period: '2019.07 - 2020.05',
    details: [
      '负责公司官网和后台管理系统的开发',
      '学习并实践Vue.js框架',
      '参与移动端H5页面开发'
    ],
    tech: ['Vue.js', 'JavaScript', 'CSS3', 'jQuery']
  }
])

const education = ref([
  {
    school: '某知名大学',
    degree: '计算机科学与技术 · 本科',
    period: '2015.09 - 2019.06'
  }
])

const form = ref({
  name: '',
  email: '',
  message: ''
})

const handleSubmit = () => {
  console.log('Form submitted:', form.value)
  alert('感谢您的留言！我会尽快回复您。')
  form.value = { name: '', email: '', message: '' }
}

onMounted(() => {
  setTimeout(() => {
    type()
  }, 1000)
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible')
      }
    })
  }, { threshold: 0.1 })
  
  document.querySelectorAll('.glass-card, .project-card, .timeline-item').forEach(el => {
    observer.observe(el)
  })
})
</script>

<style lang="scss" scoped>
.home-page {
  position: relative;
}

.section {
  padding: 60px 0 40px;

  @include responsive($breakpoint-md) {
    padding: 80px 0 60px;
  }

  @include responsive($breakpoint-lg) {
    padding: 100px 0 80px;
  }
}

.section-header {
  margin-bottom: 2rem;

  @include responsive($breakpoint-md) {
    margin-bottom: 2.5rem;
  }
  
  &.centered {
    text-align: center;
  }
  
  .section-number {
    color: $primary-color;
    font-family: $font-mono;
    font-size: 1rem;
    display: block;
    margin-bottom: 0.5rem;
  }
}

.hero-section {
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding-top: 100px;
  padding-bottom: 20px;

  @include responsive($breakpoint-md) {
    padding-top: 70px;
    padding-bottom: 30px;
  }

  @include responsive($breakpoint-lg) {
    padding-top: 80px;
    padding-bottom: 40px;
  }
}

.hero-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 3rem;
  align-items: center;
  
  @include responsive($breakpoint-lg) {
    grid-template-columns: 1fr 1fr;
  }
}

.hero-text {
  .hero-greeting {
    color: $primary-color;
    font-family: $font-mono;
    font-size: 1rem;
    margin-bottom: 1rem;
  }
  
  .hero-name {
    font-size: 3rem;
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 0.5rem;
    
    @include responsive($breakpoint-md) {
      font-size: 4rem;
    }
    
    @include responsive($breakpoint-lg) {
      font-size: 5rem;
    }
  }
  
  .hero-title {
    font-size: 1.5rem;
    color: $text-secondary;
    margin-bottom: 1.5rem;
    min-height: 2rem;
    
    @include responsive($breakpoint-md) {
      font-size: 2rem;
    }
    
    .cursor {
      animation: blink 1s infinite;
    }
  }
  
  .hero-description {
    color: $text-secondary;
    font-size: 1rem;
    line-height: 1.8;
    margin-bottom: 2rem;
    max-width: 500px;
  }
  
  .hero-cta {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
  }
}

.hero-visual {
  display: flex;
  justify-content: center;
  align-items: center;
}

.scroll-indicator {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  color: $text-muted;
  font-size: 0.75rem;
  
  .scroll-arrow {
    width: 24px;
    height: 40px;
    border: 2px solid $text-muted;
    border-radius: 12px;
    position: relative;
    
    &::after {
      content: '';
      position: absolute;
      top: 8px;
      left: 50%;
      transform: translateX(-50%);
      width: 4px;
      height: 8px;
      background: $primary-color;
      border-radius: 2px;
      animation: scrollDown 1.5s infinite;
    }
  }
}

@keyframes scrollDown {
  0% { opacity: 1; top: 8px; }
  100% { opacity: 0; top: 20px; }
}

.about-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;

  @include responsive($breakpoint-lg) {
    grid-template-columns: 1.5fr 1fr;
    gap: 2.5rem;
  }
}

.about-card {
  p {
    margin-bottom: 1rem;
    line-height: 1.8;
    
    &:last-child {
      margin-bottom: 0;
    }
    
    strong {
      color: $primary-color;
    }
  }
}

.about-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-top: 1.5rem;

  @include responsive($breakpoint-md) {
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
  }
  
  .stat-item {
    text-align: center;
    
    .stat-number {
      display: block;
      font-size: 2.5rem;
      font-weight: 700;
      @include text-gradient;
    }
    
    .stat-label {
      color: $text-secondary;
      font-size: 0.875rem;
    }
  }
}

.about-image {
  position: relative;
  
  .image-frame {
    position: relative;
    z-index: 2;
    border-radius: 16px;
    overflow: hidden;
    
    .image-placeholder {
      aspect-ratio: 3/4;
      background: linear-gradient(135deg, rgba($primary-color, 0.1), rgba($secondary-color, 0.1));
      @include flex-center;
      color: $text-muted;
      font-size: 0.875rem;
    }
  }
  
  .image-decoration {
    position: absolute;
    top: 20px;
    left: 20px;
    right: -20px;
    bottom: -20px;
    border: 2px solid $primary-color;
    border-radius: 16px;
    z-index: 1;
  }
}

.skills-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
  margin-bottom: 2.5rem;

  @include responsive($breakpoint-lg) {
    grid-template-columns: 1fr 1fr;
    gap: 2.5rem;
    margin-bottom: 3rem;
  }
}

.skills-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.skill-item {
  padding: 1rem;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all $transition-normal;
  
  &.active,
  &:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba($primary-color, 0.3);
  }
  
  .skill-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
    
    .skill-icon {
      font-size: 0.75rem;
    }
    
    .skill-name {
      flex: 1;
      font-weight: 500;
    }
    
    .skill-level {
      color: $text-muted;
      font-family: $font-mono;
      font-size: 0.875rem;
    }
  }
  
  .skill-bar {
    height: 4px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 2px;
    overflow: hidden;
    
    .skill-progress {
      height: 100%;
      border-radius: 2px;
      transition: width 0.6s ease;
    }
  }
}

.skills-categories {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  
  @include responsive($breakpoint-md) {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .category-card {
    padding: 1.5rem;
    
    .category-title {
      font-size: 0.875rem;
      font-weight: 600;
      margin-bottom: 1rem;
      color: $text-primary;
    }
    
    .category-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
    }
    
    .tag {
      padding: 0.25rem 0.75rem;
      background: rgba($primary-color, 0.1);
      border-radius: 20px;
      font-size: 0.75rem;
      color: $text-secondary;
    }
  }
}

.projects-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;

  @include responsive($breakpoint-md) {
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
  }
}

.project-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  overflow: hidden;
  transition: all $transition-normal;
  
  &:hover {
    transform: translateY(-8px);
    border-color: rgba($primary-color, 0.3);
    box-shadow: $shadow-lg;
    
    .project-overlay {
      opacity: 1;
    }
  }
  
  &.featured {
    grid-column: span 1;
    
    @include responsive($breakpoint-md) {
      grid-column: span 2;
    }
  }
  
  .project-image {
    position: relative;
    aspect-ratio: 16/10;
    overflow: hidden;
    
    .image-placeholder {
      width: 100%;
      height: 100%;
      background: linear-gradient(135deg, rgba($primary-color, 0.2), rgba($secondary-color, 0.2));
      @include flex-center;
      color: $text-muted;
      font-weight: 500;
    }
    
    .project-overlay {
      position: absolute;
      inset: 0;
      background: rgba(0, 0, 0, 0.7);
      @include flex-center;
      opacity: 0;
      transition: opacity $transition-normal;
    }
    
    .project-links {
      display: flex;
      gap: 1rem;
    }
    
    .project-link {
      width: 48px;
      height: 48px;
      @include flex-center;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 50%;
      color: $text-primary;
      transition: all $transition-normal;
      
      &:hover {
        background: $primary-color;
        transform: scale(1.1);
      }
    }
  }
  
  .project-content {
    padding: 1.5rem;
    
    .project-type {
      color: $primary-color;
      font-family: $font-mono;
      font-size: 0.75rem;
    }
    
    .project-title {
      font-size: 1.25rem;
      font-weight: 600;
      margin: 0.5rem 0;
    }
    
    .project-description {
      color: $text-secondary;
      font-size: 0.875rem;
      line-height: 1.6;
      margin-bottom: 1rem;
    }
    
    .project-tech {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      
      .tech-tag {
        padding: 0.25rem 0.75rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 4px;
        font-size: 0.75rem;
        color: $text-muted;
        font-family: $font-mono;
      }
    }
  }
}

.timeline {
  position: relative;
  padding-left: 2rem;
  
  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 2px;
    background: linear-gradient(to bottom, $primary-color, transparent);
  }
}

.timeline-item {
  position: relative;
  margin-bottom: 1.5rem;

  &:last-child {
    margin-bottom: 0;
  }
  
  .timeline-marker {
    position: absolute;
    left: -2.5rem;
    top: 1.5rem;
    width: 16px;
    height: 16px;
    background: $primary-color;
    border-radius: 50%;
    border: 3px solid $dark-bg;
  }
  
  .timeline-content {
    padding: 1.5rem;
    
    .timeline-header {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
      margin-bottom: 0.5rem;
      
      @include responsive($breakpoint-md) {
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
      }
      
      .timeline-title {
        font-size: 1.125rem;
        font-weight: 600;
      }
      
      .timeline-company {
        color: $primary-color;
        font-size: 0.875rem;
      }
    }
    
    .timeline-date {
      color: $text-muted;
      font-family: $font-mono;
      font-size: 0.75rem;
      display: block;
      margin-bottom: 1rem;
    }
    
    .timeline-details {
      list-style: none;
      margin-bottom: 1rem;
      
      li {
        position: relative;
        padding-left: 1.25rem;
        margin-bottom: 0.5rem;
        color: $text-secondary;
        font-size: 0.875rem;
        line-height: 1.6;
        
        &::before {
          content: '▹';
          position: absolute;
          left: 0;
          color: $primary-color;
        }
      }
    }
    
    .timeline-tech {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      
      .tech-tag {
        padding: 0.25rem 0.75rem;
        background: rgba($primary-color, 0.1);
        border-radius: 4px;
        font-size: 0.75rem;
        color: $text-secondary;
        font-family: $font-mono;
      }
    }
  }
}

.education-section {
  margin-top: 3rem;

  @include responsive($breakpoint-md) {
    margin-top: 4rem;
  }

  .subsection-title {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    color: $text-primary;

    @include responsive($breakpoint-md) {
      margin-bottom: 2rem;
    }
  }
}

.education-cards {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  
  @include responsive($breakpoint-md) {
    grid-template-columns: repeat(2, 1fr);
  }
}

.education-card {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  
  .edu-icon {
    font-size: 2rem;
  }
  
  .edu-content {
    .edu-school {
      font-size: 1rem;
      font-weight: 600;
      margin-bottom: 0.25rem;
    }
    
    .edu-degree {
      color: $text-secondary;
      font-size: 0.875rem;
      margin-bottom: 0.5rem;
    }
    
    .edu-period {
      color: $text-muted;
      font-family: $font-mono;
      font-size: 0.75rem;
    }
  }
}

.contact-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;

  @include responsive($breakpoint-lg) {
    grid-template-columns: 1fr 1.5fr;
    gap: 2.5rem;
  }
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;

  @include responsive($breakpoint-md) {
    gap: 1.25rem;
  }
}

.contact-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  
  .contact-icon {
    width: 48px;
    height: 48px;
    @include flex-center;
    background: rgba($primary-color, 0.1);
    border-radius: 12px;
    color: $primary-color;
    flex-shrink: 0;
  }
  
  .contact-text {
    .contact-label {
      display: block;
      color: $text-muted;
      font-size: 0.75rem;
      margin-bottom: 0.25rem;
    }
    
    a, span {
      color: $text-primary;
      font-size: 1rem;
      
      &:hover {
        color: $primary-color;
      }
    }
  }
}

.contact-form {
  padding: 2rem;
  
  .form-group {
    margin-bottom: 1.5rem;
    
    label {
      display: block;
      color: $text-secondary;
      font-size: 0.875rem;
      margin-bottom: 0.5rem;
    }
    
    input, textarea {
      width: 100%;
      padding: 0.875rem 1rem;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 8px;
      color: $text-primary;
      font-family: inherit;
      font-size: 1rem;
      transition: all $transition-fast;
      
      &::placeholder {
        color: $text-muted;
      }
      
      &:focus {
        outline: none;
        border-color: $primary-color;
        background: rgba(255, 255, 255, 0.08);
      }
    }
    
    textarea {
      resize: vertical;
      min-height: 120px;
    }
  }
  
  .submit-btn {
    width: 100%;
    justify-content: center;
  }
}

.glass-card {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.6s ease;
  
  &.visible {
    opacity: 1;
    transform: translateY(0);
  }
}

.project-card {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.6s ease;
  
  &.visible {
    opacity: 1;
    transform: translateY(0);
  }
}

.timeline-item {
  opacity: 0;
  transform: translateX(-30px);
  transition: all 0.6s ease;
  
  &.visible {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
