import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

export default function Particles({ count = 50 }) {
  const meshRef = useRef()
  
  // Create particle positions and properties
  const particles = useMemo(() => {
    const positions = new Float32Array(count * 3)
    const colors = new Float32Array(count * 3)
    const sizes = new Float32Array(count)
    
    for (let i = 0; i < count; i++) {
      // Distribute particles in a sphere around the center
      const radius = 10 + Math.random() * 20
      const theta = Math.random() * Math.PI * 2
      const phi = Math.random() * Math.PI
      
      positions[i * 3] = radius * Math.sin(phi) * Math.cos(theta)
      positions[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta)
      positions[i * 3 + 2] = radius * Math.cos(phi)
      
      // Color variations (cyan/blue theme)
      colors[i * 3] = 0.2 + Math.random() * 0.3     // R
      colors[i * 3 + 1] = 0.6 + Math.random() * 0.4 // G
      colors[i * 3 + 2] = 1.0                       // B
      
      // Random sizes
      sizes[i] = Math.random() * 2 + 1
    }
    
    return { positions, colors, sizes }
  }, [count])

  // Animate particles
  useFrame((state) => {
    if (meshRef.current) {
      const time = state.clock.elapsedTime
      const positions = meshRef.current.geometry.attributes.position.array
      
      for (let i = 0; i < count; i++) {
        const i3 = i * 3
        
        // Gentle floating motion
        positions[i3 + 1] += Math.sin(time + i) * 0.002
        
        // Subtle rotation around Y axis
        const x = positions[i3]
        const z = positions[i3 + 2]
        positions[i3] = x * Math.cos(0.0005) - z * Math.sin(0.0005)
        positions[i3 + 2] = x * Math.sin(0.0005) + z * Math.cos(0.0005)
      }
      
      meshRef.current.geometry.attributes.position.needsUpdate = true
    }
  })

  return (
    <points ref={meshRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={particles.positions}
          itemSize={3}
        />
        <bufferAttribute
          attach="attributes-color"
          count={count}
          array={particles.colors}
          itemSize={3}
        />
        <bufferAttribute
          attach="attributes-size"
          count={count}
          array={particles.sizes}
          itemSize={1}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.05}
        transparent
        opacity={0.6}
        vertexColors
        sizeAttenuation
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </points>
  )
}
