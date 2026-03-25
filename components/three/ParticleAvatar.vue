<template>
  <div ref="containerRef" class="particle-avatar-container">
    <canvas ref="canvasRef" class="particle-canvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'

const containerRef = ref(null)
const canvasRef = ref(null)

let scene = null
let camera = null
let renderer = null
let particles = null
let animationId = null
let mouseX = 0
let mouseY = 0
const clock = new THREE.Clock()

const createParticleAvatar = () => {
  const geometry = new THREE.BufferGeometry()
  const particleCount = 8000
  const positions = new Float32Array(particleCount * 3)
  const colors = new Float32Array(particleCount * 3)
  const originalPositions = new Float32Array(particleCount * 3)

  const avatarShape = (x, y) => {
    const r = Math.sqrt(x * x + y * y)
    if (r < 0.8) return true
    if (r < 1.2 && Math.abs(y) < 0.6) return true
    if (Math.abs(x) < 0.3 && y > -1.5 && y < 1.5) return true
    return false
  }

  for (let i = 0; i < particleCount; i++) {
    const i3 = i * 3
    
    let x, y, z
    let valid = false
    
    while (!valid) {
      x = (Math.random() - 0.5) * 3
      y = (Math.random() - 0.5) * 4
      z = (Math.random() - 0.5) * 0.5
      
      valid = avatarShape(x, y)
    }
    
    positions[i3] = x
    positions[i3 + 1] = y
    positions[i3 + 2] = z
    
    originalPositions[i3] = x
    originalPositions[i3 + 1] = y
    originalPositions[i3 + 2] = z
    
    const colorChoice = Math.random()
    if (colorChoice < 0.4) {
      colors[i3] = 0.4
      colors[i3 + 1] = 0.4
      colors[i3 + 2] = 1.0
    } else if (colorChoice < 0.7) {
      colors[i3] = 0.55
      colors[i3 + 1] = 0.36
      colors[i3 + 2] = 0.96
    } else {
      colors[i3] = 0.02
      colors[i3 + 1] = 0.71
      colors[i3 + 2] = 0.83
    }
  }

  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))
  geometry.userData = { originalPositions }

  const material = new THREE.PointsMaterial({
    size: 0.03,
    vertexColors: true,
    transparent: true,
    opacity: 0.9,
    blending: THREE.AdditiveBlending,
    sizeAttenuation: true
  })

  return new THREE.Points(geometry, material)
}

const handleResize = () => {
  if (!canvasRef.value || !camera || !renderer) return
  
  const width = canvasRef.value.clientWidth
  const height = canvasRef.value.clientHeight
  
  camera.aspect = width / height
  camera.updateProjectionMatrix()
  renderer.setSize(width, height)
}

const handleMouseMove = (e) => {
  mouseX = (e.clientX / window.innerWidth) * 2 - 1
  mouseY = -(e.clientY / window.innerHeight) * 2 + 1
}

const init = () => {
  if (!canvasRef.value || !process.client) return

  scene = new THREE.Scene()
  
  camera = new THREE.PerspectiveCamera(
    50,
    canvasRef.value.clientWidth / canvasRef.value.clientHeight,
    0.1,
    100
  )
  camera.position.z = 5

  renderer = new THREE.WebGLRenderer({
    canvas: canvasRef.value,
    antialias: true,
    alpha: true,
    powerPreference: 'high-performance'
  })
  renderer.setSize(canvasRef.value.clientWidth, canvasRef.value.clientHeight)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))

  particles = createParticleAvatar()
  scene.add(particles)

  window.addEventListener('resize', handleResize)
  window.addEventListener('mousemove', handleMouseMove, { passive: true })
  
  animate()
}

const animate = () => {
  animationId = requestAnimationFrame(animate)
  
  const elapsed = clock.getElapsedTime()
  
  if (particles) {
    const positions = particles.geometry.attributes.position.array
    const originalPositions = particles.geometry.userData.originalPositions
    
    for (let i = 0; i < positions.length; i += 3) {
      const mouseInfluence = 0.3
      const dx = mouseX * mouseInfluence
      const dy = mouseY * mouseInfluence
      
      positions[i] = originalPositions[i] + Math.sin(elapsed + i) * 0.05 + dx * 0.1
      positions[i + 1] = originalPositions[i + 1] + Math.cos(elapsed + i) * 0.05 + dy * 0.1
      positions[i + 2] = originalPositions[i + 2] + Math.sin(elapsed * 2 + i) * 0.02
    }
    
    particles.geometry.attributes.position.needsUpdate = true
    
    particles.rotation.y = Math.sin(elapsed * 0.3) * 0.1
  }
  
  if (renderer && scene && camera) {
    renderer.render(scene, camera)
  }
}

const dispose = () => {
  window.removeEventListener('resize', handleResize)
  window.removeEventListener('mousemove', handleMouseMove)
  
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  
  if (renderer) {
    renderer.dispose()
  }
  
  if (particles) {
    if (particles.geometry) particles.geometry.dispose()
    if (particles.material) particles.material.dispose()
  }
  
  scene = null
  camera = null
  renderer = null
  particles = null
}

onMounted(() => {
  init()
})

onUnmounted(() => {
  dispose()
})
</script>

<style lang="scss" scoped>
.particle-avatar-container {
  width: 100%;
  max-width: 400px;
  height: 500px;
  margin: 0 auto;
  position: relative;
  
  @media (min-width: 768px) {
    height: 600px;
  }
}

.particle-canvas {
  width: 100%;
  height: 100%;
  display: block;
}
</style>
