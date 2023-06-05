import pandas as pd
import numpy as np
import api

df = pd.read_csv('arxiv_papers.csv', delimiter=',', encoding = "utf8")

df_1 = df.head()

for row,index in df_1.iterrows():
  paper_id = row['url'][row['url'].rindex('/')+1:]
  main_text, abstract = api.get_clean_text(paper_id)
  print(paper_id)
  

