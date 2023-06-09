""" Here we just need something to compare it against the baselines and stuff... """
# Download this file : https://www.kaggle.com/datasets/johoetter/design-thinking-arxiv


import pandas as pd
import numpy as np
import fetch_api
import models_script


def test(abstract, main_text):
    available_models = ['main_model','tfidf_lemma','baseline']
    rs = pd.DataFrame(columns=available_models)
    for model in available_models:
        strong_links = models_script.link_abstract_sentences_to_paragraphs(abstract,main_text,model)
        rs[model] = strong_links
    return rs


def post_process(abstract, main_text):
    df = test(abstract,main_text)
    para_pred = pd.DataFrame(columns=df.columns)
    score = pd.DataFrame(columns=df.columns)
    for i,col_name in enumerate(df.columns):
        para_pred[col_name] , score[col_name] = zip(*df[col_name])
    return para_pred,score


def models_agreement(abstract,main_text):
    para_pred,x = post_process(abstract,main_text)
    if (para_pred==0).all().all():
        return None
    if len(para_pred.columns == 3):
        # main_base_compar = sum(para_pred.main_model == para_pred.baseline)/len(para_pred) 
        # tfidf_base_compar = sum(para_pred.tfidf_lemma == para_pred.baseline)/len(para_pred)
        compar = (para_pred.main_model == para_pred.baseline) & (para_pred.tfidf_lemma == para_pred.baseline)
    return compar , para_pred 



