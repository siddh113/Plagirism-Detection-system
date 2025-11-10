# Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## Step 1: Backend Setup

1. Open a terminal and navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - **Windows**: `venv\Scripts\activate`
   - **Linux/Mac**: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Start the backend server:
```bash
python main.py
```

The backend will be running at `http://localhost:8000`

**Note**: The first time you run the application, Sentence-BERT will download the model (~80MB). This may take a few minutes.

## Step 2: Frontend Setup

1. Open a **new terminal** and navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the frontend development server:
```bash
npm run dev
```

The frontend will be running at `http://localhost:5173`

## Step 3: Use the Application

1. Open your browser and navigate to `http://localhost:5173`
2. Upload a source document (the document to check for plagiarism)
3. Upload one or more corpus documents (documents to compare against)
4. Click "Analyze Documents"
5. View the results:
   - Overall plagiarism percentage
   - Similarity scores for each document
   - Matched segments with highlighted text
   - Detailed analysis by document

## Using the Dataset

The project includes the PAN-PC-11 dataset in the `pan_pc_11_txt/` directory:
- Source documents: `pan_pc_11_txt/source-document/`
- Suspicious documents: `pan_pc_11_txt/suspicious-document/`

You can upload any of these files to test the application.

## Troubleshooting

### Backend Issues

- **Port 8000 already in use**: Change the port in `backend/main.py` (line 105)
- **Model download fails**: Check your internet connection. The model will be downloaded on first run.
- **Import errors**: Make sure you're in the virtual environment and all dependencies are installed.

### Frontend Issues

- **Port 5173 already in use**: Vite will automatically use the next available port
- **CORS errors**: Make sure the backend is running and CORS is properly configured
- **API connection fails**: Verify the backend is running at `http://localhost:8000`

## Windows Users

You can use the provided batch files:
- `start_backend.bat` - Starts the backend server
- `start_frontend.bat` - Starts the frontend server

## Linux/Mac Users

You can use the provided shell scripts:
- `start_backend.sh` - Starts the backend server (make executable: `chmod +x start_backend.sh`)
- `start_frontend.sh` - Starts the frontend server (make executable: `chmod +x start_frontend.sh`)

## Performance Tips

- For large documents, the analysis may take several minutes
- The first analysis will be slower as the model loads
- Consider using smaller chunk sizes for faster processing (adjust in `backend/services/document_processor.py`)
- GPU acceleration is automatically used if available

## Next Steps

- Adjust similarity threshold in `backend/services/similarity_analyzer.py`
- Modify chunk size in `backend/services/document_processor.py`
- Customize the UI in `frontend/src/components/`
- Add support for PDF and DOCX files

