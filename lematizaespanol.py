# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 21:51:44 2023

@author: ivan
"""

import spacy

def lematizar_texto(texto):
    nlp = spacy.load("es_core_news_sm")
    doc = nlp(texto)
    lemas = [token.lemma_ for token in doc]
    lematizado = ' '.join(lemas)
    return lematizado

