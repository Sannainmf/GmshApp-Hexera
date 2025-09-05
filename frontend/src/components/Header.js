import React from 'react';
import styled from 'styled-components';

const HeaderContainer = styled.header`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 20px;
  text-align: center;
`;

const Title = styled.h1`
  color: white;
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  
  @media (max-width: 768px) {
    font-size: 2rem;
  }
`;

const Subtitle = styled.p`
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.1rem;
  margin: 10px 0 0 0;
  font-weight: 300;
`;

function Header() {
  return (
    <HeaderContainer>
      <Title>AI Mesh Generator</Title>
      <Subtitle>Generate and visualize 3D meshes using AI-powered GMSH scripting</Subtitle>
    </HeaderContainer>
  );
}

export default Header;
