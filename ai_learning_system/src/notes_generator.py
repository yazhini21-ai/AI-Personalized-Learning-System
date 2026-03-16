from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter

def summarize_notes(notes):
    sentences = sent_tokenize(notes)
    words = word_tokenize(notes.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    
    word_freq = Counter(filtered_words)
    most_common_words = word_freq.most_common(5)
    
    summary_sentences = []
    for sentence in sentences:
        for word, freq in most_common_words:
            if word in sentence.lower():
                summary_sentences.append(sentence)
                break
    
    summary = ' '.join(summary_sentences[:2])  # Taking first 2 sentences for summary
    return summary

def extract_key_points(notes):
    sentences = sent_tokenize(notes)
    key_points = []
    
    for sentence in sentences:
        if len(sentence.split()) > 10:  # Assuming key points are longer sentences
            key_points.append(sentence)
    
    return key_points[:5]  # Return first 5 key points

def process_student_notes(notes):
    summary = summarize_notes(notes)
    key_points = extract_key_points(notes)
    return summary, key_points