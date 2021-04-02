#!/usr/bin/env python3

import os
import requests
import json
from bs4 import BeautifulSoup
import csv
import pandas as pd


def print_areas():
    url = 'https://27crags.com'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    areas_script = soup.find_all('script')[14].string[:-127] + '}'

    areas_data = json.loads(areas_script)
    areas_DF = pd.DataFrame(areas_data['areas'])
    areas_DF.columns = ["Name","Country","Area_Id"]
    areas_sweden_DF = areas_DF[areas_DF['Country']=='Sweden']
    #areas_spain_DF = areas_spain_DF.drop_duplicates()
    print(areas_sweden_DF)

    
def print_grades():
    url = 'https://27crags.com'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    grades_script = soup.find_all('script')[8].string[24:-234]
    
    grades_data = json.loads(grades_script)
    grades_DF = pd.DataFrame.from_dict(grades_data, orient='index')
    grades_DF.columns = ["US","Hueco","Australian","Font","French","UIAA"]
    print(grades_DF[:-1])
    

def my_routes(area, grade_min, grade_max):
    url = 'https://27crags.com/areas/' + area + '/routelist?grade_min=' + grade_min + '&grade_max=' + grade_max + '&Sport=1'
    r = requests.get(url)
    print(url)

    soup = BeautifulSoup(r.content, 'html.parser')

    routes_script = soup.find("script", {"class": "js-react-on-rails-component", "data-component-name": "RouteList"}).string
    
    routes_data = json.loads(routes_script)
    
    keys = routes_data['routes'][0].keys()

    with open('routes.csv','w') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(routes_data['routes'])
        
    routes_DF = pd.read_csv('routes.csv')
    result_DF = routes_DF.loc[(routes_DF['grade_int'] >= int(grade_min)) & (routes_DF['grade_int'] <= int(grade_max))]
    result_DF = result_DF.loc[result_DF['genre'] == 'Sport']
    result_DF = result_DF.sort_values(by='rating', ascending=False)
    os.remove('routes.csv')
    
    result_DF.drop(['video_count','discussion_count','crimpers','slopers','jugs','fingery','powerful',
               'dyno','endurance','technical','mental','roof','overhang','vertical','slab',
                'traverse','sitstart','topslasthold','tradgear_required','dangerous','crack',
               'pockets','tufas'], axis=1, inplace=True)
    
    result_DF.to_csv('result_area_' + area + '_grade_min' + grade_min + '_grade_max' + grade_max + '.csv', index=False)


print_areas()
location = str(input('Enter area_id: '))


print_grades() 
g_min = str(input('Enter minimum climbing level: '))
g_max = str(input('Enter maximum climbing level: '))

my_routes(location, g_min, g_max)

print('Your file has been created and saved correctly.')
