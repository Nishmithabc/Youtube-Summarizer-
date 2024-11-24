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

- **`text_summarizer`**: Contains the two different models of summarization.
- extractive_summary.py
- abstractive_summary.py
- **`README.md`**: Documentation for setup and usage.

# Extractive Summarizer

This repository contains a Python implementation of an extractive text summarizer. The summarizer analyzes text to identify and extract the most relevant sentences, creating a concise summary. The implementation leverages libraries such as **spaCy**, **scikit-learn**, and **heapq**, and uses techniques like TF-IDF and cosine similarity to rank and select sentences for the summary.

# Abstractive Summarizer

This repository contains a Python implementation of an **abstractive text summarizer**. Unlike extractive methods, this summarizer generates concise summaries by paraphrasing and rephrasing the original content. The implementation uses **Hugging Face's Transformers library** and leverages the **T5 model** to create meaningful summaries. It includes features like text preprocessing, chunking for long inputs, and customizable summarization parameters.

