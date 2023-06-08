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


    return ' '.join([' '.join(preprocess(text)), weighted_concepts, weighted_entities])


def link_abstract_sentences_to_paragraphs(abstract, full_text):
    paragraphs = full_text.replace('.\n','\b**b').replace('-\n', '').replace('\n', ' ').split('\b**b')
    abstract_sentences = list(nlp(abstract).sents)
    
    abstract_sentences_wo_preprocessing = list(abstract_sentences)
    paragraphs_wo_preprocessing = list(paragraphs)
    
    abstract_sentences = [generate_weighted_string(sentence.text) for sentence in abstract_sentences]
    paragraphs = [generate_weighted_string(para) for para in paragraphs]
    
 #   abstract_sentences_wo_preprocessing = 
 #   paragraphs_wo_preprocessing = {i: paragraph for i, paragraph in enumerate(full_text.split('\n'))}

    corpus = abstract_sentences + paragraphs

    vectorizer = TfidfVectorizer()

    vectorizer.fit(corpus)

    sentence_paragraph_scores = {}
    sentence_paragraph_scores_wo = {}
    for i,sentence in enumerate(abstract_sentences):
        sentence_vector = vectorizer.transform([sentence]).toarray()
        paragraph_scores = {}
        paragraph_scores_wo = {}
        for j,para in enumerate(paragraphs):
            para_vector = vectorizer.transform([para]).toarray()
            similarity = cosine_similarity(sentence_vector, para_vector)
            paragraph_scores[(j,para)] = similarity[0][0]  
            paragraph_scores_wo[(j,paragraphs_wo_preprocessing[j])] = similarity[0][0]

        sorted_paragraph_scores = sorted(paragraph_scores.items(), key=lambda x: x[1], reverse=True)
        sentence_paragraph_scores[(i,sentence)] = sorted_paragraph_scores[:3]
        sorted_paragraph_scores_wo = sorted(paragraph_scores_wo.items(), key=lambda x: x[1], reverse=True)
        sentence_paragraph_scores_wo[0] = sorted_paragraph_scores_wo[:3]
    
    return sentence_paragraph_scores_wo, paragraphs_wo_preprocessing


