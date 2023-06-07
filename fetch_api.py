# write an API to connect to the database, and change the text to be in a usable format 
# [a usable format is the text form for abstract and the rest of the document as a long text separated by \n]
import arxiv
import re

import pandas as pd
import numpy as np

def get_clean_text(paper_id):
    
    # search = arxiv.Search(id_list=["2111.11418v1"])
    search = arxiv.Search(id_list=[paper_id])

    papers = next(search.results())
    print(papers.title)


    if len(papers.title) > 0:
        paper = papers
        pdf_url = paper.pdf_url

        # Extract text from the PDF
        import io
        import requests
        import PyPDF2

        response = requests.get(pdf_url)
        pdf_file = io.BytesIO(response.content)

        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Extract text from each page
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()


        last_index = paper.summary[:50]

        # cleaned_text = text[:text.index('Abstract')] + text[text.index('Introduction'):]
        cleaned_text = text[text.index(last_index)+len(paper.summary)-50:]

        # print(cleaned_text)#print(text)
        
        return cleaned_text, paper.summary

    else:
        print("Paper not found.")
        return '',''
