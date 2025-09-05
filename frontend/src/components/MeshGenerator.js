import React, { useState } from 'react';
import styled from 'styled-components';
import axios from 'axios';

const GeneratorContainer = styled.div`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const Title = styled.h2`
  color: #333;
  margin-bottom: 20px;
  font-size: 1.5rem;
  font-weight: 600;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const InputGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

const Label = styled.label`
  color: #555;
  font-weight: 500;
  font-size: 0.9rem;
`;

const TextArea = styled.textarea`
  padding: 15px;
  border: 2px solid #e1e5e9;
  border-radius: 10px;
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
  min-height: 120px;
  transition: border-color 0.3s ease;

  &:focus {
    outline: none;
    border-color: #667eea;
  }

  &::placeholder {
    color: #999;
  }
`;

const Select = styled.select`
  padding: 12px;
  border: 2px solid #e1e5e9;
  border-radius: 10px;
  font-size: 1rem;
  background: white;
  transition: border-color 0.3s ease;

  &:focus {
    outline: none;
    border-color: #667eea;
  }
`;

const Input = styled.input`
  padding: 12px;
  border: 2px solid #e1e5e9;
  border-radius: 10px;
  font-size: 1rem;
  transition: border-color 0.3s ease;

  &:focus {
    outline: none;
    border-color: #667eea;
  }
`;

const Button = styled.button`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const LoadingSpinner = styled.div`
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const ErrorMessage = styled.div`
  background: #fee;
  color: #c33;
  padding: 15px;
  border-radius: 10px;
  border: 1px solid #fcc;
  font-size: 0.9rem;
`;

const SuccessMessage = styled.div`
  background: #efe;
  color: #363;
  padding: 15px;
  border-radius: 10px;
  border: 1px solid #cfc;
  font-size: 0.9rem;
`;

const ExamplePrompts = styled.div`
  margin-top: 15px;
`;

const ExampleTitle = styled.h4`
  color: #666;
  margin-bottom: 10px;
  font-size: 0.9rem;
`;

const ExamplePrompt = styled.button`
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  color: #495057;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 0.8rem;
  cursor: pointer;
  margin: 2px;
  transition: background-color 0.2s ease;

  &:hover {
    background: #e9ecef;
  }
`;

function MeshGenerator({ onMeshGenerated, onGenerationStart, onGenerationEnd }) {
  const [prompt, setPrompt] = useState('');
  const [meshType, setMeshType] = useState('2D');
  const [elementSize, setElementSize] = useState(0.1);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const examplePrompts = [
    "Create a 2D rectangular mesh with a circular hole at the center",
    "Generate a triangular mesh for a square domain with fine elements near the center",
    "Create a mesh for a L-shaped domain with adaptive refinement",
    "Generate a mesh for a circular domain with structured elements"
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) {
      setError('Please enter a mesh generation prompt');
      return;
    }

    setIsLoading(true);
    setError('');
    setSuccess('');
    onGenerationStart();

    try {
      const response = await axios.post('/generate-mesh', {
        prompt: prompt.trim(),
        mesh_type: meshType,
        element_size: parseFloat(elementSize)
      });

      if (response.data.status === 'success') {
        setSuccess('Mesh generated successfully!');
        onMeshGenerated(response.data);
      } else {
        setError(response.data.message || 'Failed to generate mesh');
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to connect to the server');
    } finally {
      setIsLoading(false);
      onGenerationEnd();
    }
  };

  const handleExampleClick = (examplePrompt) => {
    setPrompt(examplePrompt);
  };

  return (
    <GeneratorContainer>
      <Title>Generate Mesh</Title>
      <Form onSubmit={handleSubmit}>
        <InputGroup>
          <Label htmlFor="prompt">Mesh Description</Label>
          <TextArea
            id="prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe the mesh you want to generate. Be specific about geometry, element types, and refinement requirements."
            disabled={isLoading}
          />
        </InputGroup>

        <InputGroup>
          <Label htmlFor="meshType">Mesh Type</Label>
          <Select
            id="meshType"
            value={meshType}
            onChange={(e) => setMeshType(e.target.value)}
            disabled={isLoading}
          >
            <option value="2D">2D Mesh</option>
            <option value="3D">3D Mesh</option>
          </Select>
        </InputGroup>

        <InputGroup>
          <Label htmlFor="elementSize">Element Size</Label>
          <Input
            id="elementSize"
            type="number"
            value={elementSize}
            onChange={(e) => setElementSize(e.target.value)}
            min="0.01"
            max="1.0"
            step="0.01"
            disabled={isLoading}
          />
        </InputGroup>

        {error && <ErrorMessage>{error}</ErrorMessage>}
        {success && <SuccessMessage>{success}</SuccessMessage>}

        <Button type="submit" disabled={isLoading}>
          {isLoading ? (
            <>
              <LoadingSpinner />
              Generating...
            </>
          ) : (
            'Generate Mesh'
          )}
        </Button>
      </Form>

      <ExamplePrompts>
        <ExampleTitle>Example Prompts:</ExampleTitle>
        {examplePrompts.map((example, index) => (
          <ExamplePrompt
            key={index}
            type="button"
            onClick={() => handleExampleClick(example)}
            disabled={isLoading}
          >
            {example}
          </ExamplePrompt>
        ))}
      </ExamplePrompts>
    </GeneratorContainer>
  );
}

export default MeshGenerator;
