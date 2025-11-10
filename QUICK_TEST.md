# Quick Testing Guide

## 🚀 Quick Test Steps

### 1. Open the Application
- Go to: **http://localhost:5173** in your browser

### 2. Test with Dataset Files

#### Test Case 1: High Similarity (Matching Documents)
1. Click **"Select source document"**
2. Navigate to: `pan_pc_11_txt/source-document/`
3. Select: `source-document00001.txt`
4. Click **"Select corpus documents"**
5. Navigate to: `pan_pc_11_txt/suspicious-document/`
6. Select: `suspicious-document00001.txt` (same number = should match)
7. Click **"Analyze Documents"**
8. **Expected**: High plagiarism percentage (70%+)

#### Test Case 2: Low Similarity (Different Documents)
1. Source: `source-document00001.txt`
2. Corpus: `suspicious-document00002.txt` (different number)
3. **Expected**: Low plagiarism percentage (<30%)

#### Test Case 3: Multiple Documents
1. Source: `source-document00001.txt`
2. Corpus: Select multiple files:
   - `suspicious-document00001.txt`
   - `suspicious-document00002.txt`
   - `suspicious-document00003.txt`
3. **Expected**: One high match, others low

## 📊 Understanding Results

### Plagiarism Meter
- **Green (0-20%)**: Original content
- **Yellow (20-50%)**: Moderate similarity
- **Red (50-100%)**: High plagiarism risk

### Tabs to Explore
1. **Overview**: Overall statistics and plagiarism percentage
2. **Matches**: See matched text segments
3. **Detailed Results**: Breakdown by each corpus document

## 💡 Pro Tips

1. **First Run**: The first analysis downloads the model (~80MB) - be patient!
2. **File Selection**: Use Windows File Explorer to navigate to the dataset folder
3. **Multiple Files**: Hold Ctrl while clicking to select multiple corpus files
4. **View Matches**: Click on matched segments to see the actual text

## 🎯 Recommended Test Files

| Test Type | Source File | Corpus File | Expected Result |
|-----------|------------|-------------|-----------------|
| High Match | source-document00001.txt | suspicious-document00001.txt | 70-100% |
| Low Match | source-document00001.txt | suspicious-document00010.txt | <30% |
| Multiple | source-document00001.txt | suspicious-document00001.txt<br>suspicious-document00002.txt | One high, one low |

## ⚠️ Troubleshooting

- **"Failed to fetch"**: Make sure backend is running on port 8000
- **Slow analysis**: Normal for first run (model download) or large files
- **No matches**: Try with matching document numbers (same number = should match)

