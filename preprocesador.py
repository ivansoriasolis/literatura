# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 21:05:45 2023

@author: ivan
"""
import re
from unidecode import unidecode

sufijos = ['y', 'yki', 'n', 'nchick', 'yku', 'chik', 'ku', 'pa', 
           'man', 'paq', 'manta', 'pi', 'wan', 'kama', 'rayku',
           'pura', 'yuq', 'sapa', 'cha', 'q', 'sqa',
           'na', 'ni', 'nki', 'nki', 'ku', 'rqa', 'sqa', 'nqa',
           'saq', 'saq', 'ka', 'rqa', 'sun', 'chun', 'pti', 'rku',
           'mu', 'ysi', 'naku', 'pu', 'ri', 'chka', 'paya',
           'rpari', 'punim', 'chu']

def stem_quechua(palabra, sufijos=sufijos, tamax=20, rondas=3):
    '''
    Parameters
    ----------
    word : str
        Palabra en quechua con variaciones linguísticas.
    sufijos : list
        Lista de sufijos a eliminar.
    tamax : int, optional
        Tamano máximo de raiz resultado. The default is 20.
    rondas : int, optional
        Cuantos sufijos 
    Returns
    -------
    string
        Token raiz de la palabra.

    '''
    for n in range(rondas):
        palabra = eliminar_sufijo(palabra, sufijos)
    return palabra[:tamax]

def eliminar_sufijo(palabra, sufijos):
    for sufijo in sufijos:
        if palabra.endswith(sufijo):
            palabra = palabra[:-len(sufijo)]
            break
    return palabra

def limpiar(texto):
    '''
    Quitamos signos de puntuación
    '''
    puntuación = r'[,;.:¡!¿?@#$%&[\](){}«<>~=+\-*/|\\_^`"\']'
    # signos de puntuación
    texto = re.sub(puntuación, ' ', texto) 
    # dígitos [0-9]
    texto = re.sub('\d', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto)
    texto = texto.replace(" \'", "\'")
    return texto.replace("\n", " ")

def normalizar(texto, language = "quechua"):
    if language == "quechua":
        return unidecode(texto).lower()

def recortar(texto, minimo=3, rondas=0):
    palabras = texto.split()
    recortadas = [p for p in palabras if len(p)>= minimo]
    return " ".join(recortadas)

def eliminar_stop_words(texto, stop_words):
    palabras = texto.split()
    relevantes = [p for p in palabras if p not in stop_words]
    #relevantes = [stem_quechua(p,sufijos, rondas=1) for p in relevantes]
    return " ".join(relevantes)

def preprocesar(texto, language = "quechua"):
    texto = limpiar(texto)
    texto = normalizar(texto)
    texto = recortar(texto)
    return(texto)

if __name__ == "__main__":
    # word = "ripuchkaniani"
    # stemmed_word = stem_quechua(word, sufijos)
    # stemmed_word = stem_quechua(stemmed_word, sufijos)
    # print(stemmed_word)
    texto = "Q’uñi a uquchapi papacha tarpusqay wiñashanmanraqchu icha manaraqchu rurushanmanraqchu icha manaraqchu. Papa tarpusqayta tapurikushyani papa tarpusqayta tapupayashyani ruruchan rayku lias raphichanraykullas. Yuyashankiraqchu icha manañachu makiwan, chakiwan tarpuyunqanchista ñuqa niñuchay yuyakushanimá makiwan, chakiwan tarpuyusqanchista. Qusñipata patapiri phuyullas puñushan chayta qhawarispas yawarta waqani chayta yuyarispas yawarta waqani. Hawachan Pitaq chay, maytaq chay q’usñipatamanta waqyamuwan. "
    print(preprocesar(texto))
    