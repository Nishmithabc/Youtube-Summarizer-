import streamlit as st
import re
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

    # Validate the YouTube URL
    youtube_regex = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/(watch\?v=|embed/|v/|e/|watch\?v%3D|)?([a-zA-Z0-9_-]{11})(.*)?$"
    if video_url:
        if not re.match(youtube_regex, video_url):
            st.error("Please provide a valid URL")
            return  # Exit early to avoid further processing

    transcription = None
    if video_url and not st.session_state.transcript_ready:
        with st.spinner('Processing the video... Please wait.'):
            try:
                # Retrieve transcription from cache
                from transcript.transcript_api import yt_transcript_api
                transcription = yt_transcript_api(video_url)

                if transcription:
                    st.session_state.transcription = transcription  # Save to session state
                    st.session_state.transcript_ready = True
                    st.success("Transcript retrieved successfully using API!")
            except:
                st.info("Attempting to transcribe audio...")
                try:
                    from transcript.transcriber import transcribe_from_youtube
                    transcription = transcribe_from_youtube(video_url)
                    if transcription:
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

                    # Retrieve extractive summary from cache
                    from summarizer.extractive_summary import extractive_summary
                    extractive = extractive_summary(transcription)

                    # Retrieve abstractive summary from cache
                    from summarizer.abstractive_summary import summarize_text
                    abstractive = summarize_text(extractive)

                    # Save summary to session state
                    st.session_state.summary = abstractive
                    st.session_state.summary_generated = True
                    st.success("Summary generated successfully!")
                except Exception as e:
                    st.error(f"Error during summary generation: {e}")

    # Navigate to Summary Page (Single Click)
    if st.session_state.summary_generated:
        if st.button("View Summary"):
            st.session_state.current_page = "summary_page"  # Navigate to summary page

def summary_page():
    st.title("Summary")
    summary = st.session_state.summary
    st.text_area("Generated Summary", value=summary, height=300)
    import pyperclip
    # Button to copy the text to the clipboard
    if st.button("Copy to Clipboard"):
        pyperclip.copy(summary)

    # Go Back to Input Page (Single Click)
    if st.button("Go Back"):
        st.session_state.current_page = "input_page"  # Navigate back to input page

# Routing Logic with Placeholder
placeholder = st.empty()

if st.session_state.current_page == "input_page":
    with placeholder.container():
        input_page()
elif st.session_state.current_page == "summary_page":
    with placeholder.container():
        summary_page()
