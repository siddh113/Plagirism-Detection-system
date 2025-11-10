import React, { useState } from 'react'
import './ResultsView.css'

function ResultsView({ results, onReset }) {
  const [selectedMatch, setSelectedMatch] = useState(null)
  const [activeTab, setActiveTab] = useState('overview')

  const plagiarismPercentage = results.plagiarism_percentage || 0
  const totalMatches = results.total_matches || 0

  const getPlagiarismColor = (percentage) => {
    if (percentage < 20) return '#4caf50'
    if (percentage < 50) return '#ff9800'
    return '#f44336'
  }

  const getSimilarityColor = (similarity) => {
    if (similarity >= 0.8) return '#f44336'
    if (similarity >= 0.7) return '#ff9800'
    if (similarity >= 0.6) return '#ffc107'
    return '#4caf50'
  }

  return (
    <div className="results-container">
      <div className="results-header">
        <h2>Analysis Results</h2>
        <button onClick={onReset} className="btn-reset">
          ← New Analysis
        </button>
      </div>

      {/* Overview Cards */}
      <div className="overview-cards">
        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <div className="stat-label">Plagiarism Percentage</div>
            <div 
              className="stat-value"
              style={{ color: getPlagiarismColor(plagiarismPercentage) }}
            >
              {plagiarismPercentage.toFixed(2)}%
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🔗</div>
          <div className="stat-content">
            <div className="stat-label">Total Matches</div>
            <div className="stat-value">{totalMatches}</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📄</div>
          <div className="stat-content">
            <div className="stat-label">Source Chunks</div>
            <div className="stat-value">{results.source_chunk_count || 0}</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📚</div>
          <div className="stat-content">
            <div className="stat-label">Corpus Documents</div>
            <div className="stat-value">{results.corpus_document_count || 0}</div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="tabs">
        <button
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={`tab ${activeTab === 'matches' ? 'active' : ''}`}
          onClick={() => setActiveTab('matches')}
        >
          Matches ({results.matches?.length || 0})
        </button>
        <button
          className={`tab ${activeTab === 'detailed' ? 'active' : ''}`}
          onClick={() => setActiveTab('detailed')}
        >
          Detailed Results
        </button>
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {activeTab === 'overview' && (
          <div className="overview-content">
            <div className="plagiarism-meter">
              <h3>Plagiarism Detection Meter</h3>
              <div className="meter-bar">
                <div
                  className="meter-fill"
                  style={{
                    width: `${Math.min(plagiarismPercentage, 100)}%`,
                    backgroundColor: getPlagiarismColor(plagiarismPercentage)
                  }}
                />
              </div>
              <div className="meter-labels">
                <span>Original</span>
                <span>Plagiarized</span>
              </div>
            </div>

            {results.detailed_results && results.detailed_results.length > 0 && (
              <div className="document-scores">
                <h3>Document Similarity Scores</h3>
                <div className="scores-list">
                  {results.detailed_results.map((doc, idx) => (
                    <div key={idx} className="score-item">
                      <div className="score-header">
                        <span className="score-filename">{doc.filename}</span>
                        <span
                          className="score-badge"
                          style={{
                            backgroundColor: getSimilarityColor(doc.avg_similarity)
                          }}
                        >
                          {(doc.avg_similarity * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div className="score-details">
                        <span>Matches: {doc.match_count}</span>
                        <span>Plagiarism: {doc.plagiarism_percentage.toFixed(2)}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'matches' && (
          <div className="matches-content">
            <h3>Matched Segments</h3>
            {results.matches && results.matches.length > 0 ? (
              <div className="matches-list">
                {results.matches.map((match, idx) => (
                  <div
                    key={idx}
                    className={`match-item ${selectedMatch === idx ? 'selected' : ''}`}
                    onClick={() => setSelectedMatch(selectedMatch === idx ? null : idx)}
                  >
                    <div className="match-header">
                      <span className="match-similarity" style={{
                        backgroundColor: getSimilarityColor(match.similarity)
                      }}>
                        {(match.similarity * 100).toFixed(1)}% similar
                      </span>
                      <span className="match-source">
                        {match.corpus_filename || 'Unknown'}
                      </span>
                    </div>
                    <div className="match-chunks">
                      <div className="chunk-box">
                        <div className="chunk-label">Source Chunk</div>
                        <div className="chunk-text">{match.source_chunk}</div>
                      </div>
                      <div className="chunk-box">
                        <div className="chunk-label">Matched Chunk</div>
                        <div className="chunk-text">{match.corpus_chunk}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-matches">
                <p>No matches found above the similarity threshold.</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'detailed' && (
          <div className="detailed-content">
            <h3>Detailed Analysis by Document</h3>
            {results.detailed_results && results.detailed_results.length > 0 ? (
              <div className="detailed-list">
                {results.detailed_results.map((doc, idx) => (
                  <div key={idx} className="detailed-item">
                    <div className="detailed-header">
                      <h4>{doc.filename}</h4>
                      <div className="detailed-stats">
                        <div className="detailed-stat">
                          <span className="stat-name">Avg Similarity:</span>
                          <span
                            className="stat-value"
                            style={{ color: getSimilarityColor(doc.avg_similarity) }}
                          >
                            {(doc.avg_similarity * 100).toFixed(2)}%
                          </span>
                        </div>
                        <div className="detailed-stat">
                          <span className="stat-name">Max Similarity:</span>
                          <span
                            className="stat-value"
                            style={{ color: getSimilarityColor(doc.max_similarity) }}
                          >
                            {(doc.max_similarity * 100).toFixed(2)}%
                          </span>
                        </div>
                        <div className="detailed-stat">
                          <span className="stat-name">Plagiarism:</span>
                          <span
                            className="stat-value"
                            style={{ color: getPlagiarismColor(doc.plagiarism_percentage) }}
                          >
                            {doc.plagiarism_percentage.toFixed(2)}%
                          </span>
                        </div>
                        <div className="detailed-stat">
                          <span className="stat-name">Matches:</span>
                          <span className="stat-value">{doc.match_count}</span>
                        </div>
                      </div>
                    </div>
                    {doc.matches && doc.matches.length > 0 && (
                      <div className="detailed-matches">
                        <h5>Top Matches:</h5>
                        {doc.matches.map((match, matchIdx) => (
                          <div key={matchIdx} className="detailed-match">
                            <span className="match-sim">{(match.similarity * 100).toFixed(1)}%</span>
                            <div className="match-texts">
                              <div className="match-text">
                                <strong>Source:</strong> {match.source_chunk.substring(0, 200)}...
                              </div>
                              <div className="match-text">
                                <strong>Match:</strong> {match.corpus_chunk.substring(0, 200)}...
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-results">
                <p>No detailed results available.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default ResultsView

