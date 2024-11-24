# Youtube-Video-Summarizer-
### Steps to Set Up the Environment

#### 1. Create a Virtual Environment
Run the following commands to create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv virtual_env

# Activate virtual environment
# On Windows
virtual_env\Scripts\activate

# On macOS/Linux
source virtual_env/bin/activate
```

#### 2. Install Dependencies
Install the required Python libraries:
```bash
pip install spacy scikit-learn
```

Download the **spaCy English model**:
```bash
python -m spacy download en_core_web_sm
```

## File Details

- **`summarizer.py`**: Contains the main code for the extractive summarizer.
- **`README.md`**: Documentation for setup and usage.

# Extractive Summarizer

This repository contains a Python implementation of an extractive text summarizer. The summarizer analyzes text to identify and extract the most relevant sentences, creating a concise summary. The implementation leverages libraries such as **spaCy**, **scikit-learn**, and **heapq**, and uses techniques like TF-IDF and cosine similarity to rank and select sentences for the summary.

## Features
1. **Load and Process Text**  
   - Utilizes the **spaCy** model for tokenization, Part-of-Speech (POS) tagging, and other linguistic processing.  
2. **Word Importance Calculation**  
   - Assigns weights to words based on their POS and normalizes them to identify key terms.  
3. **Sentence Scoring**  
   - Scores sentences by summing the importance of words they contain.  
4. **TF-IDF Analysis**  
   - Uses TF-IDF to evaluate word importance across sentences.  
5. **Cosine Similarity**  
   - Identifies and reduces redundancy by calculating similarities between sentences.  
6. **Summary Ratio**  
   - Allows customization of the summary length by setting a ratio of sentences to include.  
7. **Final Summary**  
   - Outputs a summary by ranking sentences based on their importance.

## Setup Instructions

### Prerequisites
Make sure you have Python 3.7 or higher installed on your system. The following Python libraries are required:
- **spaCy**
- **scikit-learn**
- **heapq**
