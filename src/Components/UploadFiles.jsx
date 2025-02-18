import { useState, useRef } from 'react';

const FileUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  // Valid file formats
  const validFormats = [
    // Images
    'image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp', 
    'image/webp', 'image/tiff', 'image/svg+xml', 'image/heic', 'image/heif',
    'image/avif', 'image/jxr', 'image/jpe',
    // PDFs
    'application/pdf'
  ];

  const isValidFileType = (file) => {
    return validFormats.includes(file.type) || 
           // Fallback for some browsers that might not correctly identify file types
           (file.name.toLowerCase().endsWith('.pdf') ||
            file.name.toLowerCase().match(/\.(jpe?g|png|gif|bmp|webp|tiff?|svg|heic|heif|avif|jxr)$/));
  };

  const handleFileChange = (e) => {
    if (e.target.files.length > 0) {
      const file = e.target.files[0];
      if (isValidFileType(file)) {
        setSelectedFile(file);
        setError(null);
      } else {
        setError('Please select an image or PDF file');
        setSelectedFile(null);
      }
    }
  };

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    
    if (e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      if (isValidFileType(file)) {
        setSelectedFile(file);
        setError(null);
      } else {
        setError('Please select an image or PDF file');
        setSelectedFile(null);
      }
    }
  };

  const handleUpload = () => {
    if (!selectedFile) {
      setError('Please select a file first!');
      return;
    }
    
    // Here you would handle the actual file upload to your server
    console.log('Uploading file:', selectedFile);
    
    // Mock successful upload
    alert(`File "${selectedFile.name}" uploaded successfully!`);
    setSelectedFile(null);
    setError(null);
  };

  const openFileSelector = () => {
    fileInputRef.current.click();
  };

  // Function to show a readable file format list 
  const getFileFormatText = () => {
    return 'Supports all image formats (JPG, PNG, GIF, BMP, WebP, etc.) and PDF files';
  };

  // Function to check if file is an image
  const isImageFile = (file) => {
    return file.type.startsWith('image/') || 
           file.name.toLowerCase().match(/\.(jpe?g|png|gif|bmp|webp|tiff?|svg|heic|heif|avif|jxr)$/);
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center p-6">
      <div className="card bg-gray-900 shadow-2xl w-full max-w-md border border-gray-700">
        <div className="card-body">
          <h2 className="card-title text-center text-white">Upload Document</h2>
          
          {/* Hidden file input with accepted file types */}
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept="image/*,application/pdf"
            className="hidden"
          />
          
          {/* Drag & drop area with enhanced border */}
          <div
            className={`border-3 border-dashed rounded-lg p-8 text-center cursor-pointer mt-4 transition-all duration-200 ${
              error ? 'border-red-500 bg-red-500/10' :
              isDragging ? 'border-primary bg-primary/10' : 
              'border-blue-500 hover:border-blue-400'
            }`}
            onClick={openFileSelector}
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
            onDragOver={handleDragOver}
            onDrop={handleDrop}
          >
            <div className="flex flex-col items-center justify-center space-y-3">
              {selectedFile && isImageFile(selectedFile) ? (
                <div className="relative w-32 h-32 mb-2 overflow-hidden rounded-lg border border-gray-700">
                  <img 
                    src={URL.createObjectURL(selectedFile)} 
                    alt="Preview" 
                    className="object-cover w-full h-full"
                  />
                </div>
              ) : (
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-12 w-12 text-blue-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                  />
                </svg>
              )}
              <div className="text-lg font-medium text-white">
                {error ? (
                  <span className="text-red-400">{error}</span>
                ) : isDragging ? (
                  'Drop file here'
                ) : selectedFile ? (
                  `Selected: ${selectedFile.name}`
                ) : (
                  'Click to browse or drag and drop'
                )}
              </div>
              <p className="text-xs text-gray-400">
                {getFileFormatText()} (Max 10MB)
              </p>
            </div>
          </div>
          
          {/* Upload button */}
          <div className="card-actions justify-center mt-6">
            <button
              className={`btn btn-primary btn-lg ${!selectedFile ? 'btn-disabled opacity-50' : ''}`}
              onClick={handleUpload}
            >
              {selectedFile ? 'Upload Document' : 'Select a file first'}
            </button>
          </div>
          
          {/* File info display */}
          {selectedFile && (
            <div className="mt-4 bg-gray-800 p-3 rounded-lg border border-gray-700">
              <div className="text-sm text-gray-300">
                <span className="font-semibold text-blue-400">Filename:</span> {selectedFile.name}
              </div>
              <div className="text-sm text-gray-300">
                <span className="font-semibold text-blue-400">Size:</span> {(selectedFile.size / 1024).toFixed(2)} KB
              </div>
              <div className="text-sm text-gray-300">
                <span className="font-semibold text-blue-400">Type:</span> {selectedFile.type || 'Unknown'}
              </div>
              {isImageFile(selectedFile) && (
                <div className="text-sm text-gray-300">
                  <span className="font-semibold text-blue-400">Preview:</span> Available above
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FileUpload;