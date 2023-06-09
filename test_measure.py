import pandas as pd
import numpy as np
import fetch_api
import measures


df = pd.read_csv('arxiv_papers.csv', delimiter=',', encoding = "utf8")


def get_abstract_main(paper_df_index):
    paper_id = df.iloc[paper_df_index]['url'][df.iloc[paper_df_index]['url'].rindex('/')+1:]
    main_text, abstract = fetch_api.get_clean_text(paper_id)
    return main_text,abstract,paper_id

#a couple of indexes
indicis = range(0,50)
#indicis = [40]
#indicis = [7]

compar = {}
#tfidf_base = {}
preds = {}
for i in indicis:
    try:
        main_text, abstract,paper_id = get_abstract_main(i)
        compar[(i,paper_id)], preds[(i,paper_id)] = measures.models_agreement(abstract, main_text)
    except:
        pass


    #print(measures.test(abstract, main_text))
    print('-------------')
    #print(measures.post_process(abstract, main_text))
    
acc = []
for j, pid in compar.keys():
    acc = acc+list(compar[(j,pid)])

indicis = range(0,1)
#indicis = [40]
#indicis = [7]

compar = {}
#tfidf_base = {}
preds = {}
for i in indicis:
    try:
        main_text, abstract,paper_id = get_abstract_main(i)
        x,y = measures.post_process(abstract, main_text)
        w,z = measures.models_agreement(abstract, main_text)
    except:
        pass