import streamlit as st
from transcriber import transcribe_from_youtube
from extractive_summary import extractive_summary
from abstractive_summary import summarize_text
from transcript_api import yt_transcript_api 

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "input_page"
if "transcript_ready" not in st.session_state:
    st.session_state.transcript_ready = False
if "summary_generated" not in st.session_state:
    st.session_state.summary_generated = False
if "summary" not in st.session_state:
    st.session_state.summary = ""

# Input Page
def input_page():
    st.title("Welcome To SummariFi")
    st.write("Enter the YouTube video link below:")

    video_url = st.text_input("YouTube Video Link", "")
    transcription = None

    if video_url and not st.session_state.transcript_ready:
            with st.spinner('Processing the video... Please wait.'):
                try:
                    
                    # Get transcription using API
                    transcription = yt_transcript_api(video_url)
                    if transcription:
                        st.session_state.transcription = transcription  # Save to session state
                        st.session_state.transcript_ready = True
                        st.success("Transcript retrieved successfully!")
                except Exception as e:
                    st.error(f"API Transcript Error: {e}")
                    st.info("Attempting to transcribe audio...")

                    try:
                        transcription = transcribe_from_youtube(video_url)
                        st.session_state.transcription = transcription  # Save to session state
                        st.session_state.transcript_ready = True
                        st.success("Transcript generated from audio!")
                    except Exception as e:
                        st.error(f"Audio Transcription Error: {e}")
                        return

    # Generate Summary
    if st.session_state.transcript_ready:
        if st.button("Generate Summary"):
            with st.spinner('Generating summary... Please wait.'):
                try:
                    # Access transcription from session state
                    transcription = st.session_state.transcription

                    extractive = extractive_summary(transcription)

                    abstractive = summarize_text(extractive)

                    # Save summary to session state
                    st.session_state.summary = abstractive
                    st.session_state.summary_generated = True
                    st.success("Summary generated successfully!")
                except Exception as e:
                    st.error(f"Error during summary generation: {e}")

    # Navigate to Summary Page
    if st.session_state.summary_generated:
        if st.button("View Summary"):
            st.session_state.current_page = "summary_page"
# Summary Page
def summary_page():
    st.title("Summary")
    st.text_area("Generated Summary", value=st.session_state.summary, height=300)

    if st.button("Go Back"):
        st.session_state.current_page = "input_page"

# Routing
if st.session_state.current_page == "input_page":
    input_page()
elif st.session_state.current_page == "summary_page":
    summary_page()
