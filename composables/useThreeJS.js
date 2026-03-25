import * as THREE from 'three'
import { ref, onUnmounted } from 'vue'

export const useThreeJS = () => {
  const scene = ref(null)
  const camera = ref(null)
  const renderer = ref(null)
  const animationId = ref(null)
  const clock = ref(new THREE.Clock())

  const initThree = () => {
    scene.value = new THREE.Scene()
    
    camera.value = new THREE.PerspectiveCamera(
      75,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    )
    camera.value.position.z = 5

    renderer.value = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
      powerPreference: 'high-performance'
    })
    renderer.value.setSize(window.innerWidth, window.innerHeight)
    renderer.value.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    
    window.addEventListener('resize', handleResize)
  }

  const handleResize = () => {
    if (!camera.value || !renderer.value) return
    
    camera.value.aspect = window.innerWidth / window.innerHeight
    camera.value.updateProjectionMatrix()
    renderer.value.setSize(window.innerWidth, window.innerHeight)
  }

  const disposeThree = () => {
    window.removeEventListener('resize', handleResize)
    
    if (animationId.value) {
      cancelAnimationFrame(animationId.value)
    }
    
    if (renderer.value) {
      renderer.value.dispose()
    }
    
    if (scene.value) {
      scene.value.traverse((object) => {
        if (object.geometry) {
          object.geometry.dispose()
        }
        if (object.material) {
          if (Array.isArray(object.material)) {
            object.material.forEach(material => material.dispose())
          } else {
            object.material.dispose()
          }
        }
      })
    }
  }

  const animate = (callback) => {
    const loop = () => {
      animationId.value = requestAnimationFrame(loop)
      const delta = clock.value.getDelta()
      const elapsed = clock.value.getElapsedTime()
      
      if (callback) {
        callback(delta, elapsed)
      }
      
      if (renderer.value && scene.value && camera.value) {
        renderer.value.render(scene.value, camera.value)
      }
    }
    loop()
  }

  return {
    scene,
    camera,
    renderer,
    clock,
    initThree,
    disposeThree,
    animate
  }
}

export const createParticleGeometry = (count, spread) => {
  const geometry = new THREE.BufferGeometry()
  const positions = new Float32Array(count * 3)
  const colors = new Float32Array(count * 3)
  const sizes = new Float32Array(count)

  for (let i = 0; i < count; i++) {
    const i3 = i * 3
    
    positions[i3] = (Math.random() - 0.5) * spread
    positions[i3 + 1] = (Math.random() - 0.5) * spread
    positions[i3 + 2] = (Math.random() - 0.5) * spread
    
    const color = new THREE.Color()
    color.setHSL(0.6 + Math.random() * 0.2, 0.8, 0.6)
    colors[i3] = color.r
    colors[i3 + 1] = color.g
    colors[i3 + 2] = color.b
    
    sizes[i] = Math.random() * 2 + 0.5
  }

  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))
  geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1))

  return geometry
}

export const createParticleMaterial = () => {
  return new THREE.PointsMaterial({
    size: 0.05,
    vertexColors: true,
    transparent: true,
    opacity: 0.8,
    blending: THREE.AdditiveBlending,
    sizeAttenuation: true
  })
}
