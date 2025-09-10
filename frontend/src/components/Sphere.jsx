import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import { Sphere as ThreeSphere, MeshDistortMaterial } from '@react-three/drei'
import * as THREE from 'three'

export default function Sphere() {
  const meshRef = useRef()
  const materialRef = useRef()

  // Create gradient texture for the sphere
  const gradientTexture = useMemo(() => {
    const canvas = document.createElement('canvas')
    canvas.width = 256
    canvas.height = 256
    const ctx = canvas.getContext('2d')
    
    const gradient = ctx.createRadialGradient(128, 128, 0, 128, 128, 128)
    gradient.addColorStop(0, '#00ffff')
    gradient.addColorStop(0.4, '#0080ff')
    gradient.addColorStop(0.8, '#004080')
    gradient.addColorStop(1, '#001040')
    
    ctx.fillStyle = gradient
    ctx.fillRect(0, 0, 256, 256)
    
    const texture = new THREE.CanvasTexture(canvas)
    texture.needsUpdate = true
    return texture
  }, [])

  // Animation loop
  useFrame((state) => {
    if (meshRef.current && materialRef.current) {
      const time = state.clock.elapsedTime
      
      // Breathing/pulsating effect
      const scale = 1 + Math.sin(time * 2) * 0.1
      meshRef.current.scale.setScalar(scale)
      
      // Slow rotation
      meshRef.current.rotation.x = Math.sin(time * 0.5) * 0.2
      meshRef.current.rotation.y += 0.005
      
      // Glowing intensity variation
      materialRef.current.emissiveIntensity = 0.5 + Math.sin(time * 3) * 0.2
    }
  })

  return (
    <group>
      {/* Main glowing sphere */}
      <ThreeSphere ref={meshRef} args={[2, 64, 64]} position={[0, 0, 0]}>
        <MeshDistortMaterial
          ref={materialRef}
          color="#00aaff"
          emissive="#0066cc"
          emissiveIntensity={0.6}
          transparent
          opacity={0.8}
          distort={0.1}
          speed={2}
          roughness={0.1}
          metalness={0.8}
        />
      </ThreeSphere>
      
      {/* Outer glow ring */}
      <ThreeSphere args={[2.5, 32, 32]} position={[0, 0, 0]}>
        <meshBasicMaterial
          color="#00ffff"
          transparent
          opacity={0.1}
          side={THREE.DoubleSide}
        />
      </ThreeSphere>
      
      {/* Inner core */}
      <ThreeSphere args={[1.2, 32, 32]} position={[0, 0, 0]}>
        <meshBasicMaterial
          color="#ffffff"
          transparent
          opacity={0.3}
        />
      </ThreeSphere>
      
      {/* Point lights for additional glow */}
      <pointLight position={[0, 0, 0]} intensity={2} color="#00aaff" />
      <pointLight position={[2, 2, 2]} intensity={1} color="#0066cc" />
      <pointLight position={[-2, -2, -2]} intensity={1} color="#0066cc" />
    </group>
  )
}
