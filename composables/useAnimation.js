import { ref, onMounted, onUnmounted, watch } from 'vue'
import gsap from 'gsap'

export const useScrollAnimation = () => {
  const scrollY = ref(0)
  const scrollProgress = ref(0)
  const currentSection = ref(0)

  const handleScroll = () => {
    if (!process.client) return
    scrollY.value = window.scrollY
    const docHeight = document.documentElement.scrollHeight - window.innerHeight
    scrollProgress.value = scrollY.value / docHeight
    
    const sections = document.querySelectorAll('[data-section]')
    sections.forEach((section, index) => {
      const rect = section.getBoundingClientRect()
      if (rect.top <= window.innerHeight / 2 && rect.bottom >= window.innerHeight / 2) {
        currentSection.value = index
      }
    })
  }

  onMounted(() => {
    if (!process.client) return
    window.addEventListener('scroll', handleScroll, { passive: true })
  })

  onUnmounted(() => {
    if (!process.client) return
    window.removeEventListener('scroll', handleScroll)
  })

  return {
    scrollY,
    scrollProgress,
    currentSection
  }
}

export const useIntersectionObserver = (options = {}) => {
  const elements = ref([])
  const observer = ref(null)

  const defaultOptions = {
    threshold: 0.1,
    rootMargin: '0px',
    ...options
  }

  const observe = (el) => {
    if (!el) return
    elements.value.push(el)
    
    if (observer.value) {
      observer.value.observe(el)
    }
  }

  const unobserve = (el) => {
    if (!el || !observer.value) return
    observer.value.unobserve(el)
    elements.value = elements.value.filter(e => e !== el)
  }

  onMounted(() => {
    if (!process.client) return
    observer.value = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible')
          
          const delay = entry.target.dataset.delay || 0
          gsap.fromTo(
            entry.target,
            { opacity: 0, y: 50 },
            { 
              opacity: 1, 
              y: 0, 
              duration: 0.8, 
              delay: parseFloat(delay),
              ease: 'power3.out'
            }
          )
        }
      })
    }, defaultOptions)
  })

  onUnmounted(() => {
    if (!process.client) return
    if (observer.value) {
      observer.value.disconnect()
    }
  })

  return {
    observe,
    unobserve
  }
}

export const useMousePosition = () => {
  const mouseX = ref(0)
  const mouseY = ref(0)
  const normalizedX = ref(0)
  const normalizedY = ref(0)

  const handleMouseMove = (e) => {
    mouseX.value = e.clientX
    mouseY.value = e.clientY
    normalizedX.value = (e.clientX / window.innerWidth) * 2 - 1
    normalizedY.value = -(e.clientY / window.innerHeight) * 2 + 1
  }

  onMounted(() => {
    if (!process.client) return
    window.addEventListener('mousemove', handleMouseMove, { passive: true })
  })

  onUnmounted(() => {
    if (!process.client) return
    window.removeEventListener('mousemove', handleMouseMove)
  })

  return {
    mouseX,
    mouseY,
    normalizedX,
    normalizedY
  }
}

export const useParallax = (intensity = 0.1) => {
  const { normalizedX, normalizedY } = useMousePosition()
  const parallaxX = ref(0)
  const parallaxY = ref(0)

  const updateParallax = () => {
    parallaxX.value = normalizedX.value * intensity * 100
    parallaxY.value = normalizedY.value * intensity * 100
  }

  watch([normalizedX, normalizedY], updateParallax)

  return {
    parallaxX,
    parallaxY
  }
}

export const useTypewriter = (text, speed = 50) => {
  const displayText = ref('')
  const isTyping = ref(false)
  const isComplete = ref(false)

  const type = async () => {
    isTyping.value = true
    isComplete.value = false
    displayText.value = ''

    for (let i = 0; i < text.length; i++) {
      await new Promise(resolve => setTimeout(resolve, speed))
      displayText.value += text[i]
    }

    isTyping.value = false
    isComplete.value = true
  }

  const reset = () => {
    displayText.value = ''
    isTyping.value = false
    isComplete.value = false
  }

  return {
    displayText,
    isTyping,
    isComplete,
    type,
    reset
  }
}
