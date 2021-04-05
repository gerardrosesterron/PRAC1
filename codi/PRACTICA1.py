#Importem les llibreries necessaries per la realització de la pràctica.
import os
import requests
import json
from json.decoder import JSONDecodeError
from bs4 import BeautifulSoup
import csv
import pandas as pd

#Definim un seguit de funcions que permetran l'obenció del conjunt de dades
#segons unes característiques concretes.  

#Aquesta funció permet escollir l'àrea de Suència desitjada:
def print_areas():
    
    #Definim l'url de la pàgina 
    url = 'https://27crags.com'
    # Mitjançant requests.get descarreguem els continguts HTML de la pàgina. 
    r = requests.get(url)
    #Utilitzem BeautifulSoup per analitzar el document
    soup = BeautifulSoup(r.content, 'html.parser')

    #Utiltizem find_all per trobar les etiquetes
    areas_script = soup.find_all('script')[14].string[:-127] + '}'

    #Definim l'area que ens interessa, en el nostre cas "Sweden"
    areas_data = json.loads(areas_script)
    areas_DF = pd.DataFrame(areas_data['areas'])
    areas_DF.columns = ["Name","Country","Area_Id"]
    areas_sweden_DF = areas_DF[areas_DF['Country']=='Sweden']
    print(areas_sweden_DF)

# Definim una funció semblant a l'anterior que permeti escollir el nivell de dificultat:
def print_grades():
    url = 'https://27crags.com'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    grades_script = soup.find_all('script')[8].string[24:-234]
    
    grades_data = json.loads(grades_script)
    grades_DF = pd.DataFrame.from_dict(grades_data, orient='index')
    grades_DF.columns = ["US","Hueco","Australian","Font","French","UIAA"]
    print(grades_DF[:-1])
    
#Finalment definim una funció que permeti obtenir el conjunt de dades desitjat
def my_routes(area, grade_min, grade_max):
    url = 'https://27crags.com/areas/' + area + '/routelist?grade_min=' + grade_min + '&grade_max=' + grade_max
    r = requests.get(url)
    print(url)

    soup = BeautifulSoup(r.content, 'html.parser')

    routes_script = soup.find("script", {"class": "js-react-on-rails-component", "data-component-name": "RouteList"}).string
    
    routes_data = json.loads(routes_script)
    
    keys = routes_data['routes'][0].keys()
    
    #Volem que les dades es desin en un fitxer csv
    with open('routes.csv','w',encoding="utf-8") as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(routes_data['routes'])
        
    routes_DF = pd.read_csv('routes.csv')
    result_DF = routes_DF.loc[(routes_DF['grade_int'] >= int(grade_min)) & (routes_DF['grade_int'] <= int(grade_max))]
    #Seleccionem els tipus de steepness que ens interessa:
    result_DF = result_DF.loc[(result_DF['overhang'] == 1) | (result_DF['slab'] == 1) | (result_DF['vertical'] == 1)]
    #Ordenem les dades per rating:
    result_DF = result_DF.sort_values(by='rating', ascending=False)
    os.remove('routes.csv')
    
    #Eliminem les variables que no ens interessa tenir en el conjunt de dades
    result_DF.drop(['video_count','discussion_count','crimpers','slopers','jugs','fingery','powerful',
               'dyno','endurance','technical','mental','roof', 'param_id', 'crag_param_id',
                'traverse','sitstart','topslasthold','tradgear_required','dangerous','crack',
               'pockets','tufas'], axis=1, inplace=True)
    
    result_DF.to_csv('result_area_' + area + '_grade_min' + grade_min + '_grade_max' + grade_max + '.csv', index=False)
    
    
   #Executem les funcions:
   #Per obenir el joc de dades que volem l'usuari haurà d'introduir '315' com indentificador de la zona d'Estocolm. 
   #'100' com a nivell minim d'escalada i '1500' com a nivell màxim d'escalada.
print_areas()
location = str(input('Enter area_id: '))


print_grades() 
g_min = str(input('Enter minimum climbing level: '))
g_max = str(input('Enter maximum climbing level: '))

my_routes(location, g_min, g_max)    
