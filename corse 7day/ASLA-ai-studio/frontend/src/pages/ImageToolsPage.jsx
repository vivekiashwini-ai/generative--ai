import React, { useState } from 'react';
import { Card, Separator, Input, Button, Progress, Alert } from './components';

const ImageToolsPage = () => {
  const [backgroundRemoval, setBackgroundRemoval] = useState({
    originalImage: null,
    processedImage: null,
    isLoading: false,
    showBackgroundReplace: false,
    backgroundColor: '#ffffff',
    backgroundImage: null,
  });

  const [imageResize, setImageResize] = useState({
    originalImage: null,
    resizedImage: null,
    width: '',
    height: '',
    maintainAspectRatio: true,
    isLoading: false,
  });

  const [imageCompress, setImageCompress] = useState({
    originalImage: null,
    compressedImage: null,
    outputFormat: 'png',
    quality: 0.8,
    isLoading: false,
  });

  // Handle file selection for background remover
  const handleBackgroundFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setBackgroundRemoval(prev => ({
        ...prev,
        originalImage: URL.createObjectURL(file),
        processedImage: null,
      }));
    }
  };

  // Handle file selection for resize
  const handleResizeFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setImageResize(prev => ({
        ...prev,
        originalImage: URL.createObjectURL(file),
        resizedImage: null,
      }));
    }
  };

  // Handle file selection for compress
  const handleCompressFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setImageCompress(prev => ({
        ...prev,
        originalImage: URL.createObjectURL(file),
        compressedImage: null,
      }));
    }
  };

  // Background removal handler
  const handleBackgroundRemove = async () => {
    if (!backgroundRemoval.originalImage) return;
    
    setBackgroundRemoval(prev => ({ ...prev, isLoading: true }));
    
    // In a real implementation, this would call the backend API
    // For now, simulate processing
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Create a placeholder processed image
    const canvas = document.createElement('canvas');
    canvas.width = 400;
    canvas.height = 300;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(
      new Image(),
      0, 0, canvas.width, canvas.height
    );
    
    setBackgroundRemoval(prev => ({
      ...prev,
      processedImage: canvas.toDataURL('image/png'),
      isLoading: false,
    }));
  };

  // Image resize handler
  const handleImageResize = async () => {
    if (!imageResize.originalImage) return;
    if (!imageResize.width || !imageResize.height) {
      alert('Please enter both width and height');
      return;
    }
    
    setImageResize(prev => ({ ...prev, isLoading: true }));
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    setImageResize(prev => ({
      ...prev,
      resizedImage: URL.createObjectURL(new Blob([], { type: 'image/png' })),
      isLoading: false,
    }));
  };

  // Image compress handler
  const handleImageCompress = async () => {
    if (!imageCompress.originalImage) return;
    
    setImageCompress(prev => ({ ...prev, isLoading: true }));
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    setImageCompress(prev => ({
      ...prev,
      compressedImage: URL.createObjectURL(new Blob([], { type: 'image/jpeg' })),
      isLoading: false,
    }));
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Image Tools</h1>
      
      {/* Background Remover Section */}
      <Card className="mb-6">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Background Remover</h2>
        <Separator />
        
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
            Upload Image (JPG, PNG, WebP)
          </label>
          <input 
            type="file" 
            accept="image/jpeg,image/png,image/webp"
            onChange={handleBackgroundFileChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:text-white"
          />
        </div>
        
        {backgroundRemoval.originalImage && (
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <h3 className="text-sm font-medium text-gray-600 dark:text-gray-300">Original</h3>
              <img 
                src={backgroundRemoval.originalImage} 
                alt="Original" 
                className="max-w-full rounded-md border p-2"
              />
            </div>
            {backgroundRemoval.processedImage && (
              <div>
                <h3 className="text-sm font-medium text-gray-600 dark:text-gray-300">Processed</h3>
                <img 
                  src={backgroundRemoval.processedImage} 
                  alt="Processed" 
                  className="max-w-full rounded-md border p-2"
                />
                {backgroundRemoval.isLoading && (
                  <Progress className="my-4" />
                )}
              </div>
            )}
          </div>
        )}
        
        <div className="mt-4">
          <Button 
            onClick={handleBackgroundRemove}
            disabled={backgroundRemoval.isLoading || !backgroundRemoval.originalImage}
            className="w-full"
          >
            {backgroundRemoval.isLoading ? 'Processing...' : 'Remove Background'}
          </Button>
        </div>
      </Card>

      {/* Image Resizer Section */}
      <Card className="mb-6">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Image Resizer</h2>
        <Separator />
        
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
              Width
            </label>
            <Input 
              type="number" 
              placeholder="Enter width"
              value={imageResize.width}
              onChange={(e) => setImageResize(prev => ({ ...prev, width: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:text-white"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
              Height
            </label>
            <Input 
              type="number" 
              placeholder="Enter height"
              value={imageResize.height}
              onChange={(e) => setImageResize(prev => ({ ...prev, height: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:text-white"
            />
          </div>
        </div>
        
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
            Maintain Aspect Ratio
            <input 
              type="checkbox" 
              checked={imageResize.maintainAspectRatio}
              onChange={(e) => setImageResize(prev => ({ ...prev, maintainAspectRatio: e.target.checked }))}
              className="rounded border-gray-300 dark:border-gray-600 w-4 h-4"
            />
          </label>
        </div>
        
        {imageResize.originalImage && (
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <h3 className="text-sm font-medium text-gray-600 dark:text-gray-300">Original</h3>
              <img 
                src={imageResize.originalImage} 
                alt="Original" 
                className="max-w-full rounded-md border p-2"
              />
            </div>
            {imageResize.resizedImage && (
              <div>
                <h3 className="text-sm font-medium text-gray-600 dark:text-gray-300">Resized</h3>
                <img 
                  src={imageResize.resizedImage} 
                  alt="Resized" 
                  className="max-w-full rounded-md border p-2"
                />
                {imageResize.isLoading && (
                  <Progress className="my-4" />
                )}
              </div>
            )}
          </div>
        )}
        
        <div className="mt-4">
          <Button 
            onClick={handleImageResize}
            disabled={imageResize.isLoading || !imageResize.originalImage || !imageResize.width || !imageResize.height}
            className="w-full"
          >
            {imageResize.isLoading ? 'Resizing...' : 'Resize Image'}
          </Button>
        </div>
      </Card>

      {/* Image Compressor Section */}
      <Card>
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Image Compressor</h2>
        <Separator />
        
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
              Output Format
            </label>
            <select 
              value={imageCompress.outputFormat}
              onChange={(e) => setImageCompress(prev => ({ ...prev, outputFormat: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-gray-700 dark:text-white"
            >
              <option value="jpeg">JPEG</option>
              <option value="png">PNG</option>
              <option value="webp">WebP</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
              Quality
            </label>
            <input 
              type="range" 
              min="0.1" 
              max="1" 
              step="0.1" 
              value={imageCompress.quality}
              onChange={(e) => setImageCompress(prev => ({ ...prev, quality: parseFloat(e.target.value) }))}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-500">
              <span>Low (0.1)</span>
              <span>High (1.0)</span>
            </div>
          </div>
        </div>
        
        {imageCompress.originalImage && (
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <h3 className="text-sm font-medium text-gray-600 dark:text-gray-300">Original</h3>
              <img 
                src={imageCompress.originalImage} 
                alt="Original" 
                className="max-w-full rounded-md border p-2"
              />
            </div>
            {imageCompress.compressedImage && (
              <div>
                <h3 className="text-sm font-medium text-gray-600 dark:text-gray-300">Compressed</h3>
                <img 
                  src={imageCompress.compressedImage} 
                  alt="Compressed" 
                  className="max-w-full rounded-md border p-2"
                />
                {imageCompress.isLoading && (
                  <Progress className="my-4" />
                )}
              </div>
            )}
          </div>
        )}
        
        <div className="mt-4">
          <Button 
            onClick={handleImageCompress}
            disabled={imageCompress.isLoading || !imageCompress.originalImage}
            className="w-full"
          >
            {imageCompress.isLoading ? 'Compressing...' : 'Compress Image'}
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default ImageToolsPage;