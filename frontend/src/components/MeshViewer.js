import React, { useRef, useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Text, Box } from '@react-three/drei';
import styled from 'styled-components';
import * as THREE from 'three';
import axios from 'axios';

const ViewerContainer = styled.div`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  height: 600px;
  display: flex;
  flex-direction: column;
`;

const Title = styled.h2`
  color: #333;
  margin-bottom: 20px;
  font-size: 1.5rem;
  font-weight: 600;
`;

const CanvasContainer = styled.div`
  flex: 1;
  border-radius: 10px;
  overflow: hidden;
  background: #f8f9fa;
  position: relative;
`;

const LoadingOverlay = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(248, 249, 250, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
`;

const LoadingText = styled.div`
  color: #666;
  font-size: 1.1rem;
  font-weight: 500;
`;

const EmptyState = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #666;
  text-align: center;
`;

const EmptyIcon = styled.div`
  font-size: 4rem;
  margin-bottom: 20px;
  opacity: 0.5;
`;

const EmptyText = styled.div`
  font-size: 1.1rem;
  margin-bottom: 10px;
`;

const EmptySubtext = styled.div`
  font-size: 0.9rem;
  opacity: 0.7;
`;

const Controls = styled.div`
  display: flex;
  gap: 10px;
  margin-top: 15px;
  flex-wrap: wrap;
`;

const ControlButton = styled.button`
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  color: #495057;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s ease;

  &:hover {
    background: #e9ecef;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

// Simple mesh component for demonstration
function SimpleMesh({ meshData }) {
  const meshRef = useRef();
  
  useEffect(() => {
    if (meshRef.current && meshData) {
      // Add some animation or interaction here
      meshRef.current.rotation.y = 0;
    }
  }, [meshData]);

  return (
    <mesh ref={meshRef} rotation={[0, 0, 0]}>
      <boxGeometry args={[2, 2, 0.2]} />
      <meshStandardMaterial color="#667eea" wireframe />
    </mesh>
  );
}

// STL loader component (simplified for demo)
function STLMesh({ meshId }) {
  const [geometry, setGeometry] = useState(null);
  const meshRef = useRef();

  useEffect(() => {
    if (meshId) {
      // In a real implementation, you would load the STL file here
      // For now, we'll create a simple geometry
      const geo = new THREE.BoxGeometry(2, 2, 0.2);
      setGeometry(geo);
    }
  }, [meshId]);

  if (!geometry) return null;

  return (
    <mesh ref={meshRef}>
      <primitive object={geometry} />
      <meshStandardMaterial color="#667eea" wireframe />
    </mesh>
  );
}

function MeshViewer({ mesh, isGenerating }) {
  const [viewMode, setViewMode] = useState('wireframe');
  const [showAxes, setShowAxes] = useState(true);

  const handleDownload = async (fileType) => {
    if (!mesh?.mesh_id) return;
    
    try {
      const response = await axios.get(`/mesh/${mesh.mesh_id}/download/${fileType}`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${mesh.mesh_id}.${fileType}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Download failed:', error);
    }
  };

  return (
    <ViewerContainer>
      <Title>Mesh Visualization</Title>
      
      <CanvasContainer>
        {isGenerating ? (
          <LoadingOverlay>
            <LoadingText>Generating mesh...</LoadingText>
          </LoadingOverlay>
        ) : mesh ? (
          <Canvas camera={{ position: [5, 5, 5], fov: 50 }}>
            <ambientLight intensity={0.5} />
            <directionalLight position={[10, 10, 5]} intensity={1} />
            
            {mesh.mesh_id ? (
              <STLMesh meshId={mesh.mesh_id} />
            ) : (
              <SimpleMesh meshData={mesh} />
            )}
            
            {showAxes && <axesHelper args={[2]} />}
            
            <OrbitControls
              enablePan={true}
              enableZoom={true}
              enableRotate={true}
            />
          </Canvas>
        ) : (
          <EmptyState>
            <EmptyIcon>🔷</EmptyIcon>
            <EmptyText>No mesh loaded</EmptyText>
            <EmptySubtext>Generate a mesh using the form on the left to see it visualized here</EmptySubtext>
          </EmptyState>
        )}
      </CanvasContainer>

      {mesh && (
        <Controls>
          <ControlButton onClick={() => setViewMode(viewMode === 'wireframe' ? 'solid' : 'wireframe')}>
            {viewMode === 'wireframe' ? 'Solid View' : 'Wireframe View'}
          </ControlButton>
          <ControlButton onClick={() => setShowAxes(!showAxes)}>
            {showAxes ? 'Hide Axes' : 'Show Axes'}
          </ControlButton>
          <ControlButton onClick={() => handleDownload('msh')}>
            Download MSH
          </ControlButton>
          <ControlButton onClick={() => handleDownload('stl')}>
            Download STL
          </ControlButton>
          <ControlButton onClick={() => handleDownload('geo')}>
            Download Script
          </ControlButton>
        </Controls>
      )}
    </ViewerContainer>
  );
}

export default MeshViewer;
