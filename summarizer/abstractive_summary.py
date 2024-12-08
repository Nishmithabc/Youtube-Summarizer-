from transformers import PegasusTokenizer, PegasusForConditionalGeneration
from nltk.tokenize import sent_tokenize
import re

def preprocess_text(text):
    if not text:
        return ''
    text=text.lower()
    #remove common filler words
    filler_words=r'\b(um|uh|you know|actually|like|so|basically|seriously|literally)\b'
    text=re.sub(filler_words,'',text)
    #removing extra spaces
    text=re.sub(r'\s+',' ',text).strip()
    text=text.strip().replace("\n"," ")
    return text
def split_large_text_pegasus(text, max_tokens=512, tokenizer=None):
    """Split text into manageable chunks if it exceeds the token limit."""
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""
    current_length = 0

    for sentence in sentences:
        sentence_tokens = tokenizer.tokenize(sentence)
        sentence_length = len(sentence_tokens)
        if current_length + sentence_length <= max_tokens:
            current_chunk += " " + sentence.strip()
            current_length += sentence_length
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence.strip()
            current_length = sentence_length

    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def abstractive_summary_chunks_pegasus(
    text, model, tokenizer, max_length=300, min_length=100, num_beams=7, repetition_penalty=1.1
):
    """Generate abstractive summaries for large texts split into chunks."""
    tokenized_text = tokenizer(text, truncation=False, return_tensors="pt")
    if len(tokenized_text["input_ids"][0]) > 512:
        # Split the text into smaller chunks
        chunks = split_large_text_pegasus(text, max_tokens=512, tokenizer=tokenizer)
        summarized_chunks = []
        for chunk in chunks:
            summarized_chunk = abstractive_summary_single_chunk_pegasus(
                chunk, model, tokenizer, max_length, min_length, num_beams, repetition_penalty
            )
            summarized_chunks.append(summarized_chunk)
        combined_summary = " ".join(summarized_chunks)
        # Summarize the combined summary again
        final_summary = abstractive_summary_single_chunk_pegasus(
            combined_summary, model, tokenizer, max_length, min_length, num_beams, repetition_penalty
        )
        return final_summary
    else:
        return abstractive_summary_single_chunk_pegasus(
            text, model, tokenizer, max_length, min_length, num_beams, repetition_penalty
        )

def abstractive_summary_single_chunk_pegasus(
    text, model, tokenizer, max_length=300, min_length=100, num_beams=7, repetition_penalty=1.1
):
    """Summarize a single chunk of text using Pegasus."""
    preprocessed_text=preprocess_text(text)
    inputs = tokenizer(preprocessed_text, truncation=True, return_tensors="pt", max_length=512)
    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=max_length,
        min_length=min_length,
        num_beams=num_beams,
        repetition_penalty=repetition_penalty,
        no_repeat_ngram_size=4,  # Avoid repetition of 4-grams
        early_stopping=True
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return sentence_case_summary(summary)

def sentence_case_summary(summary):
    """Format the summary to ensure proper capitalization."""
    sentences = sent_tokenize(summary)
    sentences = [s.capitalize() for s in sentences]
    return " ".join(sentences)

def summarize_text(text, model_name='google/pegasus-xsum', max_length=300, min_length=100, num_beams=7):
    """Wrapper function for Pegasus summarization."""
    # Load the tokenizer and model
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)
    # Generate the abstractive summary
    return abstractive_summary_chunks_pegasus(
        text, model, tokenizer, max_length=max_length, min_length=min_length, num_beams=num_beams
    )
