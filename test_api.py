# Download this file : https://www.kaggle.com/datasets/johoetter/design-thinking-arxiv


import pandas as pd
import numpy as np
import fetch_api
import main_script
df = pd.read_csv('arxiv_papers.csv', delimiter=',', encoding = "utf8")

df_1 = df.head()

for index,row in df_1.iterrows():
    paper_id = row['url'][row['url'].rindex('/')+1:]
    main_text, abstract = fetch_api.get_clean_text(paper_id)
    print(paper_id)
    
    print(main_script.link_abstract_sentences_to_paragraphs(abstract,main_text))
    
    
  

