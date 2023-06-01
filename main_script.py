import spacy

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



nlp = spacy.load('en_core_web_sm')  

def preprocess(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return tokens

def extract_key_concepts(abstract):
    doc = nlp(abstract)
    key_concepts = [chunk.text for chunk in doc.noun_chunks]  
    return key_concepts


def entity_recognition(abstract):
    doc = nlp(abstract)
    entities = [(X.text, X.label_) for X in doc.ents]  
    return entities


def generate_weighted_string(text, repeat=3):
    concepts = extract_key_concepts(text)
    entities = entity_recognition(text)
    entities = [e[0] for e in entities] 
    weighted_concepts = ' '.join(concepts * repeat)
    weighted_entities = ' '.join(entities * repeat)
    return ' '.join([preprocess(text), weighted_concepts, weighted_entities])


def link_abstract_sentences_to_paragraphs(abstract, full_text):
    paragraphs = full_text.split('\n')
    abstract_sentences = list(nlp(abstract).sents)
    
    abstract_sentences = [generate_weighted_string(sentence.text) for sentence in abstract_sentences]
    paragraphs = [generate_weighted_string(para) for para in paragraphs]

    corpus = abstract_sentences + paragraphs

    vectorizer = TfidfVectorizer()

    vectorizer.fit(corpus)

    sentence_paragraph_scores = {}
    for sentence in abstract_sentences:
        sentence_vector = vectorizer.transform([sentence]).toarray()
        paragraph_scores = {}
        for para in paragraphs:
            para_vector = vectorizer.transform([para]).toarray()
            similarity = cosine_similarity(sentence_vector, para_vector)
            paragraph_scores[para] = similarity[0][0]  

        sorted_paragraph_scores = sorted(paragraph_scores.items(), key=lambda x: x[1], reverse=True)
        sentence_paragraph_scores[sentence] = sorted_paragraph_scores

    return sentence_paragraph_scores
