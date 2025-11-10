from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import uvicorn
from pydantic import BaseModel
import os

from services.document_processor import DocumentProcessor
from services.similarity_analyzer import SimilarityAnalyzer

app = FastAPI(title="Plagiarism Detection API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services (lazy loading to avoid blocking startup)
document_processor = DocumentProcessor()
similarity_analyzer = None

def get_similarity_analyzer():
    """Lazy initialization of similarity analyzer"""
    global similarity_analyzer
    if similarity_analyzer is None:
        similarity_analyzer = SimilarityAnalyzer()
    return similarity_analyzer

class AnalysisRequest(BaseModel):
    source_text: str
    corpus_texts: List[str]

class AnalysisResponse(BaseModel):
    similarity_scores: List[float]
    matches: List[dict]
    plagiarism_percentage: float
    detailed_results: List[dict]

@app.get("/")
async def root():
    return {"message": "Plagiarism Detection API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/analyze")
async def analyze_documents(
    source_file: UploadFile = File(...),
    corpus_files: List[UploadFile] = File(...)
):
    """
    Analyze a source document against a corpus of documents for plagiarism detection.
    """
    try:
        # Read source document
        source_content = await source_file.read()
        source_text = source_content.decode('utf-8')
        
        # Read corpus documents
        corpus_texts = []
        corpus_filenames = []
        for corpus_file in corpus_files:
            corpus_content = await corpus_file.read()
            corpus_texts.append(corpus_content.decode('utf-8'))
            corpus_filenames.append(corpus_file.filename)
        
        # Process documents
        source_chunks = document_processor.chunk_document(source_text)
        corpus_chunks_list = [document_processor.chunk_document(text) for text in corpus_texts]
        
        # Analyze similarity
        analyzer = get_similarity_analyzer()
        results = analyzer.analyze(
            source_chunks=source_chunks,
            corpus_chunks_list=corpus_chunks_list,
            corpus_filenames=corpus_filenames
        )
        
        return JSONResponse(content=results)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing documents: {str(e)}")

@app.post("/api/analyze-text")
async def analyze_texts(request: AnalysisRequest):
    """
    Analyze text directly without file upload.
    """
    try:
        # Process documents
        source_chunks = document_processor.chunk_document(request.source_text)
        corpus_chunks_list = [document_processor.chunk_document(text) for text in request.corpus_texts]
        
        # Analyze similarity
        analyzer = get_similarity_analyzer()
        results = analyzer.analyze(
            source_chunks=source_chunks,
            corpus_chunks_list=corpus_chunks_list,
            corpus_filenames=[f"corpus_{i}" for i in range(len(request.corpus_texts))]
        )
        
        return JSONResponse(content=results)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing texts: {str(e)}")

if __name__ == "__main__":
    import sys
    print("Starting Plagiarism Detection API Server...")
    print("Server will be available at http://127.0.0.1:8000")
    print("API Documentation: http://127.0.0.1:8000/docs")
    try:
        uvicorn.run(
            app, 
            host="127.0.0.1", 
            port=8000,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

