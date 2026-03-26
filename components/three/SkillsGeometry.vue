<template>
  <div ref="containerRef" class="skills-3d-container">
    <canvas ref="canvasRef" class="skills-canvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as THREE from 'three'
import gsap from 'gsap'

const props = defineProps({
  skills: {
    type: Array,
    default: () => [
      { name: 'Vue.js', level: 95, color: '#42b883' },
      { name: 'React', level: 90, color: '#61dafb' },
      { name: 'Three.js', level: 85, color: '#ff6b6b' },
      { name: 'TypeScript', level: 88, color: '#3178c6' },
      { name: 'Node.js', level: 82, color: '#68a063' },
      { name: 'WebGL', level: 78, color: '#9b59b6' }
    ]
  },
  activeIndex: {
    type: Number,
    default: 0
  }
})

const containerRef = ref(null)
const canvasRef = ref(null)

let scene, camera, renderer, geometries = [], animationId
const clock = new THREE.Clock()
const raycaster = new THREE.Raycaster()
const mouse = new THREE.Vector2()

const createSkillGeometry = (skill, index, total) => {
  const angle = (index / total) * Math.PI * 2
  const radius = 4
  
  const geometryTypes = [
    () => new THREE.IcosahedronGeometry(0.8, 0),
    () => new THREE.OctahedronGeometry(0.8, 0),
    () => new THREE.TetrahedronGeometry(0.9, 0),
    () => new THREE.DodecahedronGeometry(0.7, 0),
    () => new THREE.BoxGeometry(1, 1, 1),
    () => new THREE.TorusGeometry(0.5, 0.2, 8, 16)
  ]
  
  const geometry = geometryTypes[index % geometryTypes.length]()
  
  const material = new THREE.MeshPhongMaterial({
    color: new THREE.Color(skill.color),
    emissive: new THREE.Color(skill.color),
    emissiveIntensity: 0.2,
    shininess: 100,
    transparent: true,
    opacity: 0.9
  })
  
  const mesh = new THREE.Mesh(geometry, material)
  
  mesh.position.x = Math.cos(angle) * radius
  mesh.position.y = Math.sin(angle) * radius * 0.5
  mesh.position.z = Math.sin(angle) * 2
  
  mesh.userData = {
    skill,
    originalPosition: mesh.position.clone(),
    originalScale: 1,
    rotationSpeed: 0.01 + Math.random() * 0.02
  }
  
  const scale = skill.level / 100
  mesh.scale.set(scale, scale, scale)
  mesh.userData.originalScale = scale
  
  return mesh
}

const createConnectingLines = (meshes) => {
  const lines = []
  
  for (let i = 0; i < meshes.length; i++) {
    const nextIndex = (i + 1) % meshes.length
    const points = [
      meshes[i].position.clone(),
      meshes[nextIndex].position.clone()
    ]
    
    const geometry = new THREE.BufferGeometry().setFromPoints(points)
    const material = new THREE.LineBasicMaterial({
      color: 0x6366f1,
      transparent: true,
      opacity: 0.3
    })
    
    const line = new THREE.Line(geometry, material)
    lines.push(line)
  }
  
  return lines
}

const init = () => {
  if (!canvasRef.value || !containerRef.value) return

  const container = containerRef.value
  const width = container.clientWidth || 400
  const height = container.clientHeight || 400

  scene = new THREE.Scene()
  
  camera = new THREE.PerspectiveCamera(
    60,
    width / height,
    0.1,
    100
  )
  camera.position.z = 8

  renderer = new THREE.WebGLRenderer({
    canvas: canvasRef.value,
    antialias: true,
    alpha: true,
    powerPreference: 'high-performance'
  })
  renderer.setSize(width, height)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))

  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5)
  scene.add(ambientLight)

  const pointLight1 = new THREE.PointLight(0x6366f1, 1, 20)
  pointLight1.position.set(5, 5, 5)
  scene.add(pointLight1)

  const pointLight2 = new THREE.PointLight(0x8b5cf6, 1, 20)
  pointLight2.position.set(-5, -5, 5)
  scene.add(pointLight2)

  props.skills.forEach((skill, index) => {
    const mesh = createSkillGeometry(skill, index, props.skills.length)
    geometries.push(mesh)
    scene.add(mesh)
  })

  const lines = createConnectingLines(geometries)
  lines.forEach(line => scene.add(line))

  window.addEventListener('resize', handleResize)
  canvasRef.value.addEventListener('mousemove', handleMouseMove)
  
  animate()
}

const handleResize = () => {
  if (!containerRef.value || !camera || !renderer) return
  
  const width = containerRef.value.clientWidth || 400
  const height = containerRef.value.clientHeight || 400
  
  camera.aspect = width / height
  camera.updateProjectionMatrix()
  renderer.setSize(width, height)
}

const handleMouseMove = (event) => {
  if (!canvasRef.value) return
  
  const rect = canvasRef.value.getBoundingClientRect()
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1
}

const animate = () => {
  animationId = requestAnimationFrame(animate)
  
  const elapsed = clock.getElapsedTime()
  
  geometries.forEach((mesh, index) => {
    mesh.rotation.x += mesh.userData.rotationSpeed
    mesh.rotation.y += mesh.userData.rotationSpeed * 0.5
    
    const floatOffset = Math.sin(elapsed + index) * 0.2
    mesh.position.y = mesh.userData.originalPosition.y + floatOffset
    
    if (index === props.activeIndex) {
      gsap.to(mesh.scale, {
        x: mesh.userData.originalScale * 1.3,
        y: mesh.userData.originalScale * 1.3,
        z: mesh.userData.originalScale * 1.3,
        duration: 0.3
      })
      mesh.material.emissiveIntensity = 0.5
    } else {
      gsap.to(mesh.scale, {
        x: mesh.userData.originalScale,
        y: mesh.userData.originalScale,
        z: mesh.userData.originalScale,
        duration: 0.3
      })
      mesh.material.emissiveIntensity = 0.2
    }
  })
  
  if (renderer && scene && camera) {
    renderer.render(scene, camera)
  }
}

const dispose = () => {
  window.removeEventListener('resize', handleResize)
  
  if (canvasRef.value) {
    canvasRef.value.removeEventListener('mousemove', handleMouseMove)
  }
  
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  
  if (renderer) {
    renderer.dispose()
  }
  
  geometries.forEach(mesh => {
    if (mesh.geometry) mesh.geometry.dispose()
    if (mesh.material) mesh.material.dispose()
  })
  geometries = []
}

watch(() => props.activeIndex, () => {
})

onMounted(() => {
  init()
})

onUnmounted(() => {
  dispose()
})
</script>

<style lang="scss" scoped>
.skills-3d-container {
  width: 100%;
  height: 400px;
  position: relative;
  
  @include responsive($breakpoint-md) {
    height: 500px;
  }
}

.skills-canvas {
  width: 100%;
  height: 100%;
  display: block;
}
</style>
