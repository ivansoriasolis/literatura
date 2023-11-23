import re
from unidecode import unidecode

def eliminar_punto_coma(cadena):
    resultado = ''
    i = 0
    while i < len(cadena):
        if cadena[i] == '.' or cadena[i] == ';':
            if i > 0 and i < len(cadena) - 1:
                if cadena[i-1].isalpha() or cadena[i+1].isalpha():
                    resultado += cadena[i]
            else:
                resultado += cadena[i]
        else:
            resultado += cadena[i]
        i += 1
    return resultado

def procesa_texto(cadena):
    cadena = re.sub('\d+','',cadena)   #Elimina dígitos
    cadena = re.sub(r"^[^a-zA-Z]+", "", cadena)
    #cadena = re.sub(r"[^a-zA-Z.,;¡!¿?\s\n]", "", cadena) #elimina cualquier caracter no alfabetico del texto
    cadena = re.sub(r'\b(\W)\1+\b', '', cadena) #elimina cualquier simbolo repetido
    cadena = re.sub(r'\t+', ' ', cadena) #elimina cualquier espacio, tabulación o salto de linea repetido
    cadena = re.sub(r'([\s]){2,}', r'\1', cadena)
    return cadena

def procesa_categoria(cadena):
    cadena = cadena.lstrip(' \n|t')
    cadena = re.sub('\(|\)|\n','',cadena)
    cadena = cadena.lower()
    return cadena
    
def procesa_titulo(cadena):
    cadena = re.sub('\n','', cadena)
    cadena = cadena.lstrip(' \n|t')
    return cadena

def procesa_numero(cadena):
    cadena = cadena.lstrip(' \n|t')
    cadena = re.sub('[^0-9]','', cadena)
    return cadena

def procesa_resenia(cadena):
    cadena = re.sub('\n','', cadena)
    cadena = cadena.lstrip(' \n|t')
    #cadena = re.sub(r"[^a-zA-Z.,!? \n]", "", cadena)
    return cadena

def lee_composiciones(archivo):
    composiciones = []
    for t in temas:
        campos = t.split("--")
        try:
            if "\n" in campos[8][1:20]:
                print(campos[0], campos[8][:20])
                input()
            cat = procesa_categoria(campos[6])
            etiqueta = unidecode(cat).replace(" ", "") if cat != "" else "ninguna"
            composicion = {
                'numero': procesa_numero(campos[0]),
                'titulo': procesa_titulo(campos[1]),
                'categoria': cat,
                'texto': procesa_texto(campos[3]),
                'tituloespanol': procesa_titulo(campos[5]),
                'textoespanol': procesa_texto(campos[7]),
                'resenia': procesa_resenia(campos[8]),
                'etiqueta': etiqueta,
                'tema': archivo.split()[1][:-4]
                }
        except:
            for c in campos:
                print(c[:10])
            print("-----")
        else:
            composiciones.append(composicion)
    return composiciones
            
def imprime_composiciones(composiciones):
    for c in composiciones:
        for i in c.values():
            print(i[:20])
    print('------------------------\n')
    
import json

def guardar_json(lista_dicts, archivo_json):
    with open(archivo_json, 'w') as archivo:
        json.dump(lista_dicts, archivo)
        
import csv

def guardar_csv(lista_dicts, archivo_csv):
    claves = lista_dicts[0].keys()
    with open(archivo_csv, 'w', newline='', encoding='utf-8') as archivo:
        escritor_csv = csv.DictWriter(archivo, claves, delimiter=';', quoting=csv.QUOTE_ALL, quotechar='"')
        escritor_csv.writeheader()
        escritor_csv.writerows(lista_dicts)
        
import glob
archivos = glob.glob("OCR\\*.txt")



todas = []
for archivo in archivos:
    fleido = open(archivo, encoding="utf-8")
    texto = fleido.read()
    temas = texto.split("---")    
    print("--------------------", archivo)
    composiciones = lee_composiciones(archivo)
    todas += composiciones

guardar_json(todas, 'textos.json')
guardar_csv(todas, 'textos.csv')

        
    
