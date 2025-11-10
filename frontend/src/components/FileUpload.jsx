import React, { useState, useRef } from 'react'
import './FileUpload.css'

function FileUpload({ onAnalysis, loading, error }) {
  const [sourceFile, setSourceFile] = useState(null)
  const [corpusFiles, setCorpusFiles] = useState([])
  const sourceInputRef = useRef(null)
  const corpusInputRef = useRef(null)

  const handleSourceFileChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      setSourceFile(file)
    }
  }

  const handleCorpusFilesChange = (e) => {
    const files = Array.from(e.target.files)
    setCorpusFiles(files)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (sourceFile && corpusFiles.length > 0) {
      onAnalysis(sourceFile, corpusFiles)
    }
  }

  const handleReset = () => {
    setSourceFile(null)
    setCorpusFiles([])
    if (sourceInputRef.current) sourceInputRef.current.value = ''
    if (corpusInputRef.current) corpusInputRef.current.value = ''
  }

  return (
    <div className="file-upload-container">
      <div className="upload-card">
        <h2>Upload Documents</h2>
        <p className="upload-description">
          Upload a source document and one or more corpus documents to analyze for plagiarism.
        </p>

        <form onSubmit={handleSubmit} className="upload-form">
          <div className="file-input-group">
            <label htmlFor="source-file" className="file-label">
              <div className="file-label-content">
                <span className="file-icon">📄</span>
                <div>
                  <div className="file-label-title">Source Document</div>
                  <div className="file-label-subtitle">
                    {sourceFile ? sourceFile.name : 'Select source document to check'}
                  </div>
                </div>
              </div>
              <input
                ref={sourceInputRef}
                id="source-file"
                type="file"
                accept=".txt,.pdf,.doc,.docx"
                onChange={handleSourceFileChange}
                className="file-input"
                disabled={loading}
              />
            </label>
          </div>

          <div className="file-input-group">
            <label htmlFor="corpus-files" className="file-label">
              <div className="file-label-content">
                <span className="file-icon">📚</span>
                <div>
                  <div className="file-label-title">Corpus Documents</div>
                  <div className="file-label-subtitle">
                    {corpusFiles.length > 0 
                      ? `${corpusFiles.length} file(s) selected`
                      : 'Select one or more documents to compare against'}
                  </div>
                </div>
              </div>
              <input
                ref={corpusInputRef}
                id="corpus-files"
                type="file"
                accept=".txt,.pdf,.doc,.docx"
                multiple
                onChange={handleCorpusFilesChange}
                className="file-input"
                disabled={loading}
              />
            </label>
          </div>

          {error && (
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          )}

          <div className="button-group">
            <button
              type="button"
              onClick={handleReset}
              className="btn btn-secondary"
              disabled={loading}
            >
              Reset
            </button>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={!sourceFile || corpusFiles.length === 0 || loading}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Analyzing...
                </>
              ) : (
                <>
                  <span>🔍</span>
                  Analyze Documents
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default FileUpload

