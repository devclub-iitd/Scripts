#!/bin/python3

from bs4 import BeautifulSoup
import requests
import os
import shutil
import mimetypes
import json
import errno


BSW_URL = "http://bsw.iitd.ac.in/"
DOWNLOAD_BASE = 'database'
def store_link(link_url):
    response = requests.get(BSW_URL + link_url)
    if(response.status_code != 200):
        return
        # print("Error occured, with code ",response.status_code)
    extension = mimetypes.guess_extension(response.headers['Content-Type'])
    splitPath = link_url.split('/')
    destination = DOWNLOAD_BASE + '/' + splitPath[2][0:2] + '/' + splitPath[2] + '/' + 'Question-Papers' + '/' + splitPath[3].capitalize() + '/'
    filename = "[";
    splitFilename = splitPath[-1].split('.')[0].split('_')
    sem = splitFilename[-1].upper()
    if(sem == 'SEM1'):
        filename = filename + "Fall" + splitFilename[-2].split('-')[0][-2:] + "]" + "-" + splitPath[3].capitalize() + extension;
    elif(sem == 'SEM2'):
        filename = filename + "Fall" + splitFilename[-2].split('-')[1][-2:] + "]" + "-" + splitPath[3].capitalize() + extension;
    print(destination+filename)
    if not os.path.exists(os.path.dirname(destination+filename)):
        try:
            os.makedirs(os.path.dirname(destination+filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(destination+filename, "wb") as f:
        f.write(response.content)    

def store_page(page_url):
    response = requests.get(BSW_URL + page_url)
    if(response.status_code != 200):
        print("Error occured, with code ",response.status_code)
        exit(-1);
    soup = BeautifulSoup(response.text,'html.parser')
    links = soup.findAll( "a", { "class": "list-group-item" })
    for link in links:
        store_link(link.get('href'))


def main():
    with open('courses.json') as data_file:    
        courses = json.load(data_file)
    for course in courses:
        print(course)
        store_page('coursepage.php?course='+course)

if __name__ == '__main__':
    main()
