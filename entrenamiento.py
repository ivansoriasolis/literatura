# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 21:36:42 2023

@author: ivan
"""

import fasttext
import fasttext.util

import pandas as pd
import preprocesador as pre

def result_random(data, col_etiqueta):
    conteo = df[col_etiqueta].value_counts()
    total = sum(conteo)
    probabilidades = [i/total for i in conteo]
    precision = recall = sum(p*p for p in probabilidades)
    f1 = 2 * (precision * recall) / (precision + recall)
    return precision, recall, f1

def stop_words(data_pre, col_texto, top):
    '''

    Determina los stop_words, utilizando el método de palabras más frecuentes
    Parameters
    ----------
    data_pre : dataFrame
        Data frame con la columna de texto ya tokenizada y limpiada.
    col_texto : str
        Clave de la serie del dataFrmae data_pre, que contiene el texto a analizar para obtener las palabras mas frecuentes.
    top : int
        top de palabras más frecuentes
    Returns
    -------
    Lista de cadenas que se corresponden con las palabras mas frecuentes.

    '''
    todas = ' '.join(list(data_pre[col_texto]))
    palabras = todas.split()
    frecuencias = {}
    for palabra in palabras:
        if palabra in frecuencias:
            frecuencias[palabra] += 1
        else:
            frecuencias[palabra] = 1
    valores_mas_altos = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)[:top]
    return [tupla[0] for tupla in valores_mas_altos]

def crea_dataset_fasttext(archivo, data, col_texto, col_etiqueta, tsw = 100):
    '''
    Parameters
    ----------
    archivo : TYPE
        DESCRIPTION.
    data : TYPE
        DESCRIPTION.
    col_texto : TYPE
        DESCRIPTION.
    col_etiqueta : TYPE
        DESCRIPTION.

    Returns
    -------
    None.
    '''
    data[col_texto] = data[col_texto].apply(pre.preprocesar)
    sw = stop_words(data, col_texto, tsw)
    data[col_texto] = data[col_texto].apply(lambda x: pre.eliminar_stop_words(x, sw))
    data[col_texto] = data[col_texto].apply(pre.preprocesar)
    
    with open(archivo, "w", encoding="utf-8") as f:
        for i in range(len(data)):
            etiqueta = data.iloc[i][col_etiqueta]
            texto = data.iloc[i][col_texto]
            f.write("__label__{} {}\n".format(etiqueta , texto)) 
          
def print_results(model, input_path, k=1):
    num_records, precision_at_k, recall_at_k = model.test(input_path, k)
    f1_at_k = 2 * (precision_at_k * recall_at_k) / (precision_at_k + recall_at_k)

    print("records\t{}".format(num_records))
    print("Precision@{}\t{:.3f}".format(k, precision_at_k))
    print("Recall@{}\t{:.3f}".format(k, recall_at_k))
    print("F1@{}\t{:.3f}".format(k, f1_at_k))
    print()


#####  Cargar el dataset
df = pd.read_json("textos.json")

model_id = 'quechua_pre'
language = 'qu'
texto = {'qu': 'texto',
         'es': 'textoespanol'}
input_path_train = 'train_data'
pretrained_path = 'cc.{}.300.vec'.format(language)

crea_dataset_fasttext(
    archivo = input_path_train, 
    data = df, 
    col_texto = texto[language], 
    col_etiqueta = "tema", 
    tsw = 100
    )



#Parámetros de entrenamiento
fasttext_params = {
    'input': input_path_train,
    'lr': 0.1,
    'lrUpdateRate': 100,
    'thread': 8,
    'epoch': 10,
    'wordNgrams': 1,
    'dim': 300,
    'loss': 'softmax',
    'pretrainedVectors': pretrained_path
    }

#Hiperparámetros para hacer validación cruzada
fasttext_hyper_params = {
    'dim': [300],
    'epoch': [10,50,100, 150, 200],
    'wordNgrams': [1, 2, 3, 4, 5],
    'lrUpdateRate': [100, 200],
    'loss': ['softmax', 'hs', 'ns']
}

fasttext_search_parameters =  {
    "n_iter": 100,
    "n_jobs": 2,
    "verbose": 1,
    "scoring": "f1@1",
    "random_state": 1234
}
val_size = 0.2
split_random_state = 2023


from fasttext_module.model import FasttextPipeline

fasttext_pipeline = FasttextPipeline(model_id,
                                     fasttext_params,
                                     fasttext_hyper_params,
                                     fasttext_search_parameters)

# fit the pipeline by giving it the training text file and specify the
# size of the validation split that will be used for hyperparameter tuning
# note that here the file in input_path_train should already be tokenized and
# in the format that fasttext expects
fasttext_pipeline.fit_file(input_path_train, val_size, split_random_state)

# check the hyperparameter tuning result stored in a pandas DataFrame
fasttext_pipeline.df_tune_results_
fasttext_pipeline.df_tune_results_.to_excel('results_{}.xlsx'.format(model_id), index=False)