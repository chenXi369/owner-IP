<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-content">
        <div class="footer-brand">
          <div class="footer-logo">
            <span class="logo-text">星辰简历</span>
            <span class="logo-dot">.</span>
          </div>
          <p class="footer-tagline">创造卓越的用户体验</p>
        </div>

        <div class="footer-links">
          <div class="footer-section">
            <h4>导航</h4>
            <ul>
              <li><a href="#about">关于我</a></li>
              <li><a href="#skills">技能</a></li>
              <li><a href="#projects">项目</a></li>
              <li><a href="#experience">经历</a></li>
            </ul>
          </div>

          <div class="footer-section">
            <h4>联系方式</h4>
            <ul v-if="displayContacts.length > 0">
              <li v-for="contact in displayContacts" :key="contact.id">
                <a v-if="contact.type === 'email'" :href="`mailto:${contact.value}`">邮箱：{{ contact.value }}</a>
                <a v-else-if="contact.type === 'phone'" :href="`tel:${contact.value}`">电话：{{ contact.value }}</a>
                <a v-else-if="contact.type === 'github'" target="_blank" :href="contact.value">Gitee：{{ contact.value }}</a>
              </li>
            </ul>
            <ul v-else>
              <li>暂无联系方式</li>
            </ul>
          </div>

        </div>
      </div>

      <div class="footer-bottom">
        <p>&copy; {{ currentYear }} 星辰简历. 保留所有权利.</p>
        <p>使用 Nuxt.js + Three.js 构建</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  contacts: {
    type: Array,
    default: () => []
  }
})

const currentYear = new Date().getFullYear()

// 用于在联系方式区域展示的联系人
const displayContacts = computed(() => {
  return props.contacts
})
</script>

<style lang="scss" scoped>
.footer {
  background: $darker-bg;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  padding: 4rem 0 2rem;
}

.footer-container {
  @include container;
}

.footer-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 3rem;
  margin-bottom: 3rem;
  
  @include responsive($breakpoint-lg) {
    grid-template-columns: 1fr 2fr;
  }
}

.footer-brand {
  .footer-logo {
    font-size: 2rem;
    font-weight: 700;
    font-family: $font-mono;
    margin-bottom: 0.5rem;
    
    .logo-text {
      color: $text-primary;
    }
    
    .logo-dot {
      color: $primary-color;
    }
  }
  
  .footer-tagline {
    color: $text-secondary;
    font-size: 0.875rem;
  }
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
}

.footer-section {
  h4 {
    color: $text-primary;
    font-size: 0.875rem;
    font-weight: 600;
    margin-bottom: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  
  ul {
    list-style: none;
    
    li {
      margin-bottom: 0.5rem;
      
      a {
        color: $text-secondary;
        font-size: 0.875rem;
        transition: color $transition-fast;
        
        &:hover {
          color: $primary-color;
        }
      }
    }
  }
}

.footer-bottom {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  text-align: center;
  
  @include responsive($breakpoint-md) {
    flex-direction: row;
    justify-content: space-between;
  }
  
  p {
    color: $text-muted;
    font-size: 0.75rem;
  }
}
</style>
