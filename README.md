# Plagiarism Detection System

An AI-powered web application for detecting rephrased or semantically plagiarized content across multiple documents using Sentence-BERT embeddings and semantic similarity analysis.

## Features

- **Semantic Analysis**: Uses Sentence-BERT (all-MiniLM-L6-v2) for context-aware similarity detection
- **Text Chunking**: Intelligent document chunking with overlap for better context retention
- **Real-time Analysis**: Fast similarity computation with optimized embeddings
- **Visual Results**: Interactive UI showing similarity scores, matched segments, and plagiarism percentage
- **Multiple Document Support**: Compare one source document against multiple corpus documents

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Sentence-BERT**: Semantic text embeddings
- **scikit-learn**: Cosine similarity computation
- **NumPy**: Numerical operations

### Frontend
- **React**: UI library
- **Vite**: Build tool and dev server
- **Axios**: HTTP client

## Project Structure

```
.
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   └── services/
│       ├── document_processor.py    # Text chunking
│       └── similarity_analyzer.py   # Sentence-BERT analysis
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main React component
│   │   ├── components/
│   │   │   ├── FileUpload.jsx  # File upload component
│   │   │   └── ResultsView.jsx # Results visualization
│   │   └── main.jsx            # React entry point
│   ├── package.json            # Node dependencies
│   └── vite.config.js          # Vite configuration
└── README.md                   # This file
```

## Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Usage

1. **Start the backend server** (port 8000)
2. **Start the frontend server** (port 5173)
3. **Open your browser** and navigate to `http://localhost:5173`
4. **Upload documents**:
   - Select a source document to check for plagiarism
   - Select one or more corpus documents to compare against
5. **View results**:
   - See overall plagiarism percentage
   - Review similarity scores for each document
   - Examine matched segments with highlighted text
   - View detailed analysis by document

## API Endpoints

### POST `/api/analyze`
Analyze documents for plagiarism.

**Request:**
- `source_file`: Source document file
- `corpus_files`: Array of corpus document files

**Response:**
```json
{
  "similarity_scores": [0.85, 0.72, ...],
  "matches": [...],
  "plagiarism_percentage": 45.2,
  "detailed_results": [...]
}
```

### POST `/api/analyze-text`
Analyze text directly without file upload.

**Request:**
```json
{
  "source_text": "Source document text...",
  "corpus_texts": ["Corpus text 1...", "Corpus text 2..."]
}
```

## Configuration

### Chunk Size
Adjust chunk size in `backend/services/document_processor.py`:
```python
DocumentProcessor(chunk_size=500, chunk_overlap=50)
```

### Similarity Threshold
Adjust similarity threshold in `backend/services/similarity_analyzer.py`:
```python
SimilarityAnalyzer(similarity_threshold=0.7)
```

### Model Selection
Change the Sentence-BERT model in `backend/services/similarity_analyzer.py`:
```python
SimilarityAnalyzer(model_name="all-MiniLM-L6-v2")
```

## Dataset

The project includes the PAN-PC-11 dataset with:
- 11,093 source documents
- 11,093 suspicious documents

Located in `pan_pc_11_txt/` directory.

## Performance Considerations

- **Document Size**: Large documents are automatically chunked for efficient processing
- **Embedding Caching**: Consider implementing embedding caching for repeated analyses
- **Batch Processing**: For large corpora, consider batch processing embeddings
- **GPU Acceleration**: Sentence-BERT automatically uses GPU if available

## Challenges Addressed

- ✅ **Document Size**: Intelligent chunking handles large documents
- ✅ **Speed vs. Accuracy**: Optimized embeddings balance both
- ✅ **Chunk Optimization**: Configurable chunk size with overlap
- ✅ **Scaling Embeddings**: Efficient batch processing

## Future Enhancements

- [ ] Support for PDF and DOCX file formats
- [ ] Database integration for storing results
- [ ] User authentication and history
- [ ] Batch processing for multiple source documents
- [ ] Export results to PDF/CSV
- [ ] Advanced visualization with charts
- [ ] Citation detection and proper attribution

## License

This project is open source and available for academic and research purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Sentence-BERT by UKP Lab
- PAN-PC dataset for plagiarism detection
- FastAPI and React communities

