<template>
  <div ref="containerRef" class="particle-cursor-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const containerRef = ref(null)

let canvas = null
let ctx = null
let particles = []
let animationId = null
const mouse = { x: 0, y: 0, lastX: 0, lastY: 0 }

class Particle {
  constructor(x, y, color) {
    this.x = x
    this.y = y
    this.size = Math.random() * 4 + 2
    this.speedX = (Math.random() - 0.5) * 3
    this.speedY = (Math.random() - 0.5) * 3
    this.color = color
    this.life = 1
    this.decay = Math.random() * 0.02 + 0.01
  }

  update() {
    this.x += this.speedX
    this.y += this.speedY
    this.speedX *= 0.98
    this.speedY *= 0.98
    this.life -= this.decay
    this.size *= 0.99
  }

  draw(ctx) {
    ctx.save()
    ctx.globalAlpha = this.life
    ctx.fillStyle = this.color
    ctx.beginPath()
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2)
    ctx.fill()
    ctx.restore()
  }
}

const colors = [
  'rgba(99, 102, 241, 0.8)',
  'rgba(139, 92, 246, 0.8)',
  'rgba(6, 182, 212, 0.8)',
  'rgba(236, 72, 153, 0.8)'
]

const createParticles = (x, y, count = 3) => {
  for (let i = 0; i < count; i++) {
    const color = colors[Math.floor(Math.random() * colors.length)]
    particles.push(new Particle(x, y, color))
  }
}

const resizeCanvas = () => {
  if (!canvas) return
  canvas.width = window.innerWidth
  canvas.height = window.innerHeight
}

const handleMouseMove = (e) => {
  mouse.x = e.clientX
  mouse.y = e.clientY
  
  const dx = mouse.x - mouse.lastX
  const dy = mouse.y - mouse.lastY
  const distance = Math.sqrt(dx * dx + dy * dy)
  
  if (distance > 5) {
    createParticles(mouse.x, mouse.y, Math.min(Math.floor(distance / 10), 5))
  }
  
  mouse.lastX = mouse.x
  mouse.lastY = mouse.y
}

const handleClick = (e) => {
  createParticles(e.clientX, e.clientY, 20)
}

const animate = () => {
  animationId = requestAnimationFrame(animate)
  
  if (!ctx || !canvas) return
  
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  
  particles = particles.filter(p => p.life > 0)
  
  particles.forEach(particle => {
    particle.update()
    particle.draw(ctx)
  })
}

const init = () => {
  if (!process.client || !containerRef.value) return
  
  canvas = document.createElement('canvas')
  canvas.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 9999;
  `
  containerRef.value.appendChild(canvas)
  ctx = canvas.getContext('2d')
  
  resizeCanvas()
  window.addEventListener('resize', resizeCanvas)
  window.addEventListener('mousemove', handleMouseMove)
  window.addEventListener('click', handleClick)
  
  animate()
}

const dispose = () => {
  window.removeEventListener('resize', resizeCanvas)
  window.removeEventListener('mousemove', handleMouseMove)
  window.removeEventListener('click', handleClick)
  
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  
  if (canvas && canvas.parentNode) {
    canvas.parentNode.removeChild(canvas)
  }
  
  canvas = null
  ctx = null
  particles = []
}

onMounted(() => {
  init()
})

onUnmounted(() => {
  dispose()
})
</script>

<style lang="scss" scoped>
.particle-cursor-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 0;
  height: 0;
  z-index: 9999;
  pointer-events: none;
}
</style>
