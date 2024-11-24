from transformers import T5Tokenizer,T5ForConditionalGeneration
import nltk
from nltk.tokenize import sent_tokenize
import re
nltk.download('punkt')
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
def sentence_case(text):
    #first letter in upper case and other in lower case
    if not text:
        return ''
    return text[0].upper() + text[1:].lower()
def sentence_case_text(text):
    #tokenizing the text into sentences
    sentences=sent_tokenize(text)
    #correcting the case of each sentence by using sentence_case function
    sentences=[sentence_case(sentence) for sentence in sentences]
    return ' '.join(sentences)
def split_large_text(text,max_tokens=512,tokenizer=None):
    sentences=sent_tokenize(text)
    chunks=[]
    current_chunk=""
    current_length=0
    for sentence in sentences:
        sentence_tokens=tokenizer.tokenize(sentence)
        sentence_length=len(sentence_tokens)
        if current_length+sentence_length<=max_tokens:
            current_chunk+=sentence.strip()
            current_length+=sentence_length
        else:
            chunks.append(current_chunk.strip())
            current_chunk=sentence.strip()
            current_length=sentence_length
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks
def abstractive_summary_chunks(text,model_name='t5-small',max_length=100,min_length=50,length_penalty=2.0,num_beams=3):
    tokenizer=T5Tokenizer.from_pretrained(model_name)
    #check if tokens in the text exceeds the token limit
    tokenized_text=tokenizer.encode(text,return_tensors="pt",max_length=1024,truncation=False)
    if len(tokenized_text[0])>512:
        chunks=split_large_text(text,max_tokens=512,tokenizer=tokenizer)
        summarized_chunks=[]
        for chunk in chunks:
            summarized_chunk=abstractive_summary_single_chunk(chunk,tokenizer,model_name,max_length,min_length,length_penalty,num_beams)
            summarized_chunks.append(summarized_chunk)
        #once chunks are summarized then these are combined
        combined=" ".join(summarized_chunks)
        final_summary=abstractive_summary_single_chunk(combined,tokenizer,model_name,max_length,min_length,length_penalty,num_beams)
        return final_summary
    else:
        return abstractive_summary_single_chunk(text,tokenizer,model_name,max_length,min_length,length_penalty,num_beams)
def abstractive_summary_single_chunk(text,tokenizer,model_name='t5-small',max_length=100,min_length=50,length_penalty=2.0,num_beams=3):
    model=T5ForConditionalGeneration.from_pretrained(model_name)
    processed_text=preprocess_text(text)
    t5_input_text="summarize: "+processed_text
    tokenized_text=tokenizer.encode(t5_input_text,return_tensors="pt",max_length=512,truncation=True)
    summary_ids=model.generate(
        tokenized_text,
        max_length=max_length,
        min_length=min_length,
        length_penalty=length_penalty,
        num_beams=num_beams,
        early_stopping=True)
    summary=tokenizer.decode(summary_ids[0],skip_special_tokens=True)
    final_summary=sentence_case_text(summary)
    return final_summary
input_text = """
Natural Language Processing is a fascinating field of AI. It has applications in chatbots, 
summarization, translation, and more. Recent advances like transformers have changed the game. 
Models like T5 process data efficiently but have limits on token size.
""" * 10  # Simulate a long input by repeating the text

summary = abstractive_summary_chunks(input_text,max_length=150, min_length=100)
print("Abstractive Summary:", summary)



    