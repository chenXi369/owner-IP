<template>
  <nav class="navigation" :class="{ 'scrolled': isScrolled, 'mobile-open': isMobileOpen }">
    <div class="nav-container">
      <div class="nav-logo">
        <span class="logo-text">DEV</span>
        <span class="logo-dot">.</span>
      </div>

      <button class="mobile-toggle" @click="toggleMobile" aria-label="Toggle menu">
        <span class="hamburger"></span>
      </button>

      <ul class="nav-links">
        <li v-for="(link, index) in navLinks" :key="link.id">
          <a 
            :href="link.href" 
            class="nav-link"
            :class="{ active: activeSection === link.id }"
            @click="handleNavClick(link.id)"
          >
            <span class="link-number">0{{ index + 1 }}</span>
            <span class="link-text">{{ link.text }}</span>
          </a>
        </li>
      </ul>

      <a href="#contact" class="nav-cta" @click="handleNavClick('contact')">
        <span>联系我</span>
      </a>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isScrolled = ref(false)
const isMobileOpen = ref(false)
const activeSection = ref('hero')

const navLinks = [
  { id: 'hero', text: '首页', href: '#hero' },
  { id: 'about', text: '关于我', href: '#about' },
  { id: 'skills', text: '技能', href: '#skills' },
  { id: 'projects', text: '项目', href: '#projects' },
  { id: 'experience', text: '经历', href: '#experience' }
]

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
  
  const sections = document.querySelectorAll('[data-section]')
  sections.forEach(section => {
    const rect = section.getBoundingClientRect()
    if (rect.top <= 200 && rect.bottom >= 200) {
      activeSection.value = section.id
    }
  })
}

const handleNavClick = (id) => {
  isMobileOpen.value = false
  activeSection.value = id
}

const toggleMobile = () => {
  isMobileOpen.value = !isMobileOpen.value
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style lang="scss" scoped>
.navigation {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  padding: 1rem 0;
  transition: all $transition-normal;

  &.scrolled {
    background: rgba(10, 10, 15, 0.9);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    padding: 0.75rem 0;
  }
  
  @media (max-width: 400px) {
    padding: 0.75rem 0;
    
    &.scrolled {
      padding: 0.625rem 0;
    }
  }
}

.nav-container {
  @include container;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  
  @media (max-width: 400px) {
    padding: 0 0.75rem;
    gap: 0.5rem;
  }
}

.nav-logo {
  font-size: 1.5rem;
  font-weight: 700;
  font-family: $font-mono;
  flex-shrink: 0;
  
  .logo-text {
    color: $text-primary;
  }
  
  .logo-dot {
    color: $primary-color;
    animation: blink 1s infinite;
  }
  
  @media (max-width: 400px) {
    font-size: 1.25rem;
  }
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.mobile-toggle {
  display: none;
  width: 32px;
  height: 32px;
  background: transparent;
  position: relative;
  flex-shrink: 0;
  
  @include responsive($breakpoint-md) {
    display: block;
  }
  
  @media (max-width: 400px) {
    width: 28px;
    height: 28px;
  }
  
  .hamburger {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 24px;
    height: 2px;
    background: $text-primary;
    transition: all $transition-normal;
    
    @media (max-width: 400px) {
      width: 20px;
    }
    
    &::before,
    &::after {
      content: '';
      position: absolute;
      width: 24px;
      height: 2px;
      background: $text-primary;
      transition: all $transition-normal;
      
      @media (max-width: 400px) {
        width: 20px;
      }
    }
    
    &::before {
      top: -8px;
    }
    
    &::after {
      top: 8px;
    }
  }
  
  .mobile-open & .hamburger {
    background: transparent;
    
    &::before {
      top: 0;
      transform: rotate(45deg);
    }
    
    &::after {
      top: 0;
      transform: rotate(-45deg);
    }
  }
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 2rem;
  list-style: none;
  
  @include responsive($breakpoint-md) {
    position: fixed;
    top: 60px;
    left: 0;
    right: 0;
    background: rgba(10, 10, 15, 0.98);
    backdrop-filter: blur(20px);
    flex-direction: column;
    padding: 1.5rem 2rem;
    gap: 0.75rem;
    transform: translateY(-100%);
    opacity: 0;
    visibility: hidden;
    transition: all $transition-normal;
    max-height: calc(100vh - 60px);
    overflow-y: auto;
    overflow-x: hidden;
    
    .mobile-open & {
      transform: translateY(0);
      opacity: 1;
      visibility: visible;
    }
    
    // 移动端横向菜单方案
    @media (max-width: 400px) {
      flex-direction: row;
      flex-wrap: nowrap;
      overflow-x: auto;
      overflow-y: hidden;
      justify-content: flex-start;
      padding: 1rem;
      gap: 0.5rem;
      -webkit-overflow-scrolling: touch;
      scroll-behavior: smooth;
      
      // 隐藏滚动条但保留功能
      scrollbar-width: none;
      -ms-overflow-style: none;
      &::-webkit-scrollbar {
        display: none;
      }
      
      li {
        flex-shrink: 0;
      }
    }
  }
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: $text-secondary;
  font-size: 0.875rem;
  font-weight: 500;
  transition: color $transition-fast;
  position: relative;
  white-space: nowrap;
  
  &::after {
    content: '';
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 0;
    height: 2px;
    background: $gradient-primary;
    transition: width $transition-normal;
  }
  
  &:hover,
  &.active {
    color: $text-primary;
    
    &::after {
      width: 100%;
    }
  }
  
  .link-number {
    color: $primary-color;
    font-family: $font-mono;
    font-size: 0.75rem;
  }
  
  .link-text {
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 120px;
    
    @include responsive($breakpoint-md) {
      max-width: none;
      overflow: visible;
    }
    
    @media (max-width: 400px) {
      max-width: 60px;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }
  
  @media (max-width: 400px) {
    padding: 0.5rem 0.75rem;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 6px;
    font-size: 0.8125rem;
    
    &.active {
      background: rgba($primary-color, 0.1);
    }
  }
}

.nav-cta {
  padding: 0.625rem 1.25rem;
  border: 1px solid $primary-color;
  border-radius: 8px;
  color: $primary-color;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all $transition-normal;
  white-space: nowrap;
  
  &:hover {
    background: $primary-color;
    color: white;
    box-shadow: $shadow-glow;
  }
  
  @include responsive($breakpoint-md) {
    display: none;
  }
  
  @media (max-width: 400px) {
    padding: 0.5rem 0.875rem;
    font-size: 0.8125rem;
  }
}
</style>
