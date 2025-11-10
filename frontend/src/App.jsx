import React, { useState } from 'react'
import FileUpload from './components/FileUpload'
import ResultsView from './components/ResultsView'
import './App.css'

function App() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleAnalysis = async (sourceFile, corpusFiles) => {
    setLoading(true)
    setError(null)
    setResults(null)

    try {
      const formData = new FormData()
      formData.append('source_file', sourceFile)
      corpusFiles.forEach(file => {
        formData.append('corpus_files', file)
      })

      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Analysis failed')
      }

      const data = await response.json()
      setResults(data)
    } catch (err) {
      setError(err.message || 'An error occurred during analysis')
      console.error('Analysis error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setResults(null)
    setError(null)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🔍 Plagiarism Detection System</h1>
        <p>AI-Powered Semantic Similarity Analysis</p>
      </header>

      <main className="app-main">
        {!results ? (
          <FileUpload 
            onAnalysis={handleAnalysis} 
            loading={loading}
            error={error}
          />
        ) : (
          <ResultsView 
            results={results} 
            onReset={handleReset}
          />
        )}
      </main>

      <footer className="app-footer">
        <p>Built with FastAPI, React, and Sentence-BERT</p>
      </footer>
    </div>
  )
}

export default App

