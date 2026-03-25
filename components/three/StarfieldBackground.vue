<template>
  <div ref="containerRef" class="starfield-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'

const containerRef = ref(null)

let scene = null
let camera = null
let renderer = null
let stars = null
let nebula = null
let animationId = null
let mouseX = 0
let mouseY = 0

const createStarfield = () => {
  const geometry = new THREE.BufferGeometry()
  const starCount = 5000
  const positions = new Float32Array(starCount * 3)
  const colors = new Float32Array(starCount * 3)

  for (let i = 0; i < starCount; i++) {
    const i3 = i * 3
    const radius = 50 + Math.random() * 100
    const theta = Math.random() * Math.PI * 2
    const phi = Math.acos(2 * Math.random() - 1)

    positions[i3] = radius * Math.sin(phi) * Math.cos(theta)
    positions[i3 + 1] = radius * Math.sin(phi) * Math.sin(theta)
    positions[i3 + 2] = radius * Math.cos(phi)

    const colorChoice = Math.random()
    if (colorChoice < 0.3) {
      colors[i3] = 0.4
      colors[i3 + 1] = 0.4
      colors[i3 + 2] = 1.0
    } else if (colorChoice < 0.6) {
      colors[i3] = 1.0
      colors[i3 + 1] = 0.4
      colors[i3 + 2] = 0.8
    } else {
      colors[i3] = 0.4
      colors[i3 + 1] = 1.0
      colors[i3 + 2] = 0.9
    }
  }

  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))

  const material = new THREE.PointsMaterial({
    size: 0.15,
    vertexColors: true,
    transparent: true,
    opacity: 0.9,
    blending: THREE.AdditiveBlending,
    sizeAttenuation: true
  })

  return new THREE.Points(geometry, material)
}

const createNebula = () => {
  const geometry = new THREE.BufferGeometry()
  const nebulaCount = 2000
  const positions = new Float32Array(nebulaCount * 3)
  const colors = new Float32Array(nebulaCount * 3)

  for (let i = 0; i < nebulaCount; i++) {
    const i3 = i * 3
    const angle = Math.random() * Math.PI * 2
    const radius = 20 + Math.random() * 60

    positions[i3] = Math.cos(angle) * radius + (Math.random() - 0.5) * 20
    positions[i3 + 1] = (Math.random() - 0.5) * 40
    positions[i3 + 2] = Math.sin(angle) * radius + (Math.random() - 0.5) * 20

    const hue = 0.6 + Math.random() * 0.2
    const color = new THREE.Color()
    color.setHSL(hue, 0.8, 0.5)
    colors[i3] = color.r
    colors[i3 + 1] = color.g
    colors[i3 + 2] = color.b
  }

  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))

  const material = new THREE.PointsMaterial({
    size: 0.5,
    vertexColors: true,
    transparent: true,
    opacity: 0.3,
    blending: THREE.AdditiveBlending,
    sizeAttenuation: true
  })

  return new THREE.Points(geometry, material)
}

const handleResize = () => {
  if (!camera || !renderer) return
  
  camera.aspect = window.innerWidth / window.innerHeight
  camera.updateProjectionMatrix()
  renderer.setSize(window.innerWidth, window.innerHeight)
}

const handleMouseMove = (e) => {
  mouseX = (e.clientX / window.innerWidth) * 2 - 1
  mouseY = -(e.clientY / window.innerHeight) * 2 + 1
}

const init = () => {
  if (!containerRef.value || !process.client) return

  scene = new THREE.Scene()
  
  camera = new THREE.PerspectiveCamera(
    60,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  )
  camera.position.z = 30

  renderer = new THREE.WebGLRenderer({
    antialias: true,
    alpha: true,
    powerPreference: 'high-performance'
  })
  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  containerRef.value.appendChild(renderer.domElement)

  stars = createStarfield()
  scene.add(stars)

  nebula = createNebula()
  scene.add(nebula)

  window.addEventListener('resize', handleResize)
  window.addEventListener('mousemove', handleMouseMove, { passive: true })
  
  animate()
}

const clock = new THREE.Clock()

const animate = () => {
  animationId = requestAnimationFrame(animate)
  
  const elapsed = clock.getElapsedTime()
  
  if (stars) {
    stars.rotation.y = elapsed * 0.02
    stars.rotation.x = Math.sin(elapsed * 0.1) * 0.1
  }
  
  if (nebula) {
    nebula.rotation.y = -elapsed * 0.01
    nebula.rotation.z = Math.cos(elapsed * 0.05) * 0.05
  }
  
  if (camera) {
    camera.position.x += (mouseX * 5 - camera.position.x) * 0.02
    camera.position.y += (mouseY * 3 - camera.position.y) * 0.02
    camera.lookAt(scene.position)
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
    if (containerRef.value && renderer.domElement) {
      containerRef.value.removeChild(renderer.domElement)
    }
  }
  
  if (scene) {
    scene.traverse((object) => {
      if (object.geometry) {
        object.geometry.dispose()
      }
      if (object.material) {
        object.material.dispose()
      }
    })
  }
  
  scene = null
  camera = null
  renderer = null
  stars = null
  nebula = null
}

onMounted(() => {
  init()
})

onUnmounted(() => {
  dispose()
})
</script>

<style lang="scss" scoped>
.starfield-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
}
</style>
