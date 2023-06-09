import spacy

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk import word_tokenize          
from nltk.stem import WordNetLemmatizer 

class LemmaTokenizer:
     def __init__(self):
         self.wnl = WordNetLemmatizer()
     def __call__(self, doc):
         return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]



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


class models:
    def __init__(self,model_type = 'main_model'):
        self.model_type = model_type

    def vectorize(self):
        if self.model_type == 'main_model':
            return TfidfVectorizer()
        elif self.model_type == 'tfidf_lemma':
            return TfidfVectorizer(tokenizer=LemmaTokenizer())
        elif self.model_type == 'baseline':
            return CountVectorizer()
            
    def process(self,text: str):
        if self.model_type == 'main_model':
            return generate_weighted_string(text)
        else:
            return text
          


def link_abstract_sentences_to_paragraphs(abstract, full_text, model_name = 'main_model',number_of_suggestions = 1):
    paragraphs = full_text.replace('.\n','\b**b').replace('-\n', '').replace('\n', ' ').split('\b**b')
    abstract_sentences = list(nlp(abstract).sents)

    model = models(model_type = model_name)    
    abstract_sentences = [model.process(sentence.text) for sentence in abstract_sentences]
    paragraphs = [model.process(para) for para in paragraphs]
    
 #   abstract_sentences_wo_preprocessing = 
 #   paragraphs_wo_preprocessing = {i: paragraph for i, paragraph in enumerate(full_text.split('\n'))}

    corpus = abstract_sentences + paragraphs

    vectorizer = model.vectorize()
    vectorizer.fit(corpus)

    sentence_paragraph_scores = {}
    for i,sentence in enumerate(abstract_sentences):
        sentence_vector = vectorizer.transform([sentence]).toarray()
        paragraph_scores = {}
        for j,para in enumerate(paragraphs):
            para_vector = vectorizer.transform([para]).toarray()
            similarity = cosine_similarity(sentence_vector, para_vector)
            paragraph_scores[j] = similarity[0][0]  
        
        sorted_paragraph_scores = sorted(paragraph_scores.items(), key=lambda x: x[1], reverse=True)
        sentence_paragraph_scores[i] = sorted_paragraph_scores[number_of_suggestions-1]
    
    return sentence_paragraph_scores



