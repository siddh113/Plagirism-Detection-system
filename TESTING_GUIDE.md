# Testing Guide - Plagiarism Detection System

## Quick Start Testing

### Step 1: Access the Application
1. Open your web browser
2. Navigate to: **http://localhost:5173**
3. You should see the Plagiarism Detection System interface

### Step 2: Prepare Test Files
The dataset is located in:
- **Source documents**: `pan_pc_11_txt/source-document/`
- **Suspicious documents**: `pan_pc_11_txt/suspicious-document/`

### Step 3: Upload Documents

#### Option A: Test with Matching Documents (Should Show High Similarity)
1. **Source Document**: Upload any file from `pan_pc_11_txt/source-document/`
   - Example: `source-document00001.txt`
2. **Corpus Documents**: Upload the corresponding suspicious document
   - Example: `suspicious-document00001.txt` (same number)
   - **Expected Result**: High similarity score (likely 70%+)

#### Option B: Test with Different Documents (Should Show Low Similarity)
1. **Source Document**: Upload `source-document00001.txt`
2. **Corpus Documents**: Upload `suspicious-document00002.txt` (different number)
   - **Expected Result**: Lower similarity score

#### Option C: Test with Multiple Documents
1. **Source Document**: Upload `source-document00001.txt`
2. **Corpus Documents**: Upload multiple files:
   - `suspicious-document00001.txt` (should match)
   - `suspicious-document00002.txt` (should not match)
   - `suspicious-document00003.txt` (should not match)

### Step 4: Analyze
1. Click the **"Analyze Documents"** button
2. Wait for the analysis to complete (may take 30 seconds to 2 minutes depending on document size)
3. The first analysis will take longer as it downloads the Sentence-BERT model (~80MB)

### Step 5: View Results

You'll see:
- **Plagiarism Percentage**: Overall percentage of plagiarized content
- **Similarity Scores**: Score for each corpus document
- **Matched Segments**: Specific text chunks that match
- **Detailed Results**: Breakdown by document

## Testing Scenarios

### Scenario 1: Exact Match Test
**Files**: 
- Source: `source-document00001.txt`
- Corpus: `suspicious-document00001.txt`

**Expected**: 
- High plagiarism percentage (80-100%)
- Many matched segments
- High similarity scores

### Scenario 2: No Match Test
**Files**:
- Source: `source-document00001.txt`
- Corpus: `suspicious-document01000.txt` (very different document)

**Expected**:
- Low plagiarism percentage (<20%)
- Few or no matched segments
- Low similarity scores

### Scenario 3: Partial Match Test
**Files**:
- Source: `source-document00001.txt`
- Corpus: Multiple documents including the matching one

**Expected**:
- One document shows high similarity
- Other documents show low similarity
- Clear distinction in results

## Understanding the Results

### Plagiarism Percentage
- **0-20%**: Original content (Green)
- **20-50%**: Moderate similarity (Yellow/Orange)
- **50-100%**: High plagiarism risk (Red)

### Similarity Scores
- **0.0-0.6**: Low similarity (likely original)
- **0.6-0.7**: Moderate similarity
- **0.7-0.8**: High similarity (possible plagiarism)
- **0.8-1.0**: Very high similarity (likely plagiarism)

### Matched Segments
- Shows exact text chunks that match
- Displays similarity percentage for each match
- Highlights source and matched text side-by-side

## Tips for Testing

1. **Start Small**: Test with smaller documents first (files 00001-00010)
2. **Check Multiple Files**: Test with different document pairs
3. **Compare Results**: Upload the same source with different corpus files
4. **Review Matches**: Click on matched segments to see the actual text
5. **Use Tabs**: Switch between "Overview", "Matches", and "Detailed Results" tabs

## Troubleshooting

### If Analysis Takes Too Long
- First run downloads the model (~80MB) - this is normal
- Large documents take longer to process
- Multiple corpus documents increase processing time

### If No Matches Found
- Check if documents are actually related
- Try with matching document pairs (same number)
- Verify files are not empty

### If Error Occurs
- Check browser console for errors
- Verify backend is running on port 8000
- Check that files are valid text files (.txt)

## Sample Test Files

Here are some good test file pairs to start with:

1. **High Similarity Test**:
   - `source-document00001.txt` + `suspicious-document00001.txt`

2. **Medium Similarity Test**:
   - `source-document00050.txt` + `suspicious-document00050.txt`

3. **Low Similarity Test**:
   - `source-document00001.txt` + `suspicious-document01000.txt`

## Next Steps

After testing:
1. Try uploading your own documents
2. Test with different chunk sizes (modify in `backend/services/document_processor.py`)
3. Adjust similarity threshold (modify in `backend/services/similarity_analyzer.py`)
4. Explore the detailed results for each document

