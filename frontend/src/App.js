import React, { useState } from 'react';
import styled from 'styled-components';
import MeshGenerator from './components/MeshGenerator';
import MeshViewer from './components/MeshViewer';
import Header from './components/Header';

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
`;

const MainContent = styled.div`
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 80px);
`;

const ContentArea = styled.div`
  display: flex;
  flex: 1;
  gap: 20px;
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;

  @media (max-width: 768px) {
    flex-direction: column;
    padding: 10px;
  }
`;

const LeftPanel = styled.div`
  flex: 1;
  min-width: 300px;
`;

const RightPanel = styled.div`
  flex: 2;
  min-width: 400px;
`;

function App() {
  const [currentMesh, setCurrentMesh] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleMeshGenerated = (meshData) => {
    setCurrentMesh(meshData);
  };

  const handleGenerationStart = () => {
    setIsGenerating(true);
  };

  const handleGenerationEnd = () => {
    setIsGenerating(false);
  };

  return (
    <AppContainer>
      <Header />
      <MainContent>
        <ContentArea>
          <LeftPanel>
            <MeshGenerator 
              onMeshGenerated={handleMeshGenerated}
              onGenerationStart={handleGenerationStart}
              onGenerationEnd={handleGenerationEnd}
            />
          </LeftPanel>
          <RightPanel>
            <MeshViewer 
              mesh={currentMesh}
              isGenerating={isGenerating}
            />
          </RightPanel>
        </ContentArea>
      </MainContent>
    </AppContainer>
  );
}

export default App;
