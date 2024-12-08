# SummariFi

## Overview
**SummariFi** is a powerful, user-friendly web application that summarizes YouTube videos. Built using **Streamlit**, it uses advanced transcription and summarization techniques to generate concise, meaningful summaries. Whether you're short on time or want a quick overview of a video, SummariFi has you covered!

---

## Features

- **YouTube Video Transcription**:
  - Retrieves video transcripts using APIs or transcribes audio when a transcript is unavailable.
- **Extractive Summarization**:
  - Highlights the most important sentences from the transcript.
- **Abstractive Summarization**:
  - Rewrites the extractive summary into a coherent, human-like summary.
- **Interactive UI**:
  - Simple and intuitive interface for easy navigation.
- **Real-Time Progress**:
  - Displays progress bars and status updates during transcription and summarization.

---

## How It Works

1. **Input the YouTube Video URL**:
   - Enter the link in the input field, and the app processes the video.
   
2. **Transcription**:
   - Uses APIs or audio transcription to generate the video transcript.

3. **Summary Generation**:
   - Extractive summarization selects key sentences.
   - Abstractive summarization refines the extractive summary into a polished, concise output.

4. **View the Summary**:
   - Navigate to the summary page to view the generated summary.

---


## Usage

1. Launch the application in your browser by running the above command.
2. Paste the YouTube video link in the input field.
3. Wait for the transcript to be retrieved or generated.
4. Click **Generate Summary** to process the transcript.
5. View the generated summary on the **Summary Page**.

---

## File Structure

```plaintext
SummariFi/
│
├── app.py                  # Main application logic
├── transcriber.py          # Handles audio transcription
├── extractive_summary.py   # Extractive summarization logic
├── abstractive_summary.py  # Abstractive summarization logic
├── transcript_api.py       # Retrieves YouTube transcript via API
├── requirements.txt        # Python dependencies
└── README.md               # Documentation
```

---

## Dependencies

The application requires the following key libraries:

- **Streamlit**: For the web interface.
- **ylt-dp**: To fetch video streams.
- **youtube-transcript-api**: To retrieve video transcripts.
- **openai-whisper**: For audio transcription.
- **nltk**: For extractive summarization.
- **transformers**: For abstractive summarization.
- **torch**: To power transformer-based models.

Install all dependencies using:
```bash
pip install -r requirements.txt
```

---

## Error Handling

- **Transcript Retrieval Failure**: The app attempts audio transcription if the API fails.
- **Audio Transcription Failure**: Displays error messages if audio transcription cannot proceed.

---
