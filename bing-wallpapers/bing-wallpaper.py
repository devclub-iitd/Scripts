#!/bin/python3

import requests
import json
import os
import mimetypes
import datetime
import argparse
import shutil

PATH='home/$USER/bing-wallpapers'

BING_URL = 'https://bing.com'
BING_API_URL = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=10"

def get_images():
    response = requests.get(BING_API_URL)
    if(response.status_code != 200):
        print("Error occured, with code ",response.status_code)
        exit(-1);
    images = json.loads(response.text)
    now = datetime.datetime.now()
    today = now.strftime('%d-%m-%Y')
    if(os.path.exists(PATH+'/'+today)):
        return -1
    os.makedirs(PATH+'/'+today,exist_ok=True)
    i=0
    for image in images['images']:
        img_response = requests.get('https://bing.com'+image['url'])
        if(img_response.status_code != 200):
            print("Error occured, with code ",img_response.status_code)
            exit(-1);
        if('Content-Type' in img_response.headers):
            extension = mimetypes.guess_extension(img_response.headers['Content-Type'])
        with open(PATH+'/'+today+'/'+str(i)+extension,'wb') as f:
            f.write(img_response.content)    
        i = i+1
    return 0


def set_img(idx):
    now = datetime.datetime.now()
    today = now.strftime('%d-%m-%Y')
    filename = sorted(os.listdir(PATH+'/'+today))[idx]
    os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-uri file://"+PATH+'/'+today+'/'+filename)    


def next_img(def_idx=-2):
    now = datetime.datetime.now()
    today = now.strftime('%d-%m-%Y')
    total_imgs = len(os.listdir(PATH+'/'+today))
    try:
        with open(PATH+'/idx.txt','r') as f:
            idx = f.read(1)
    except IOError:
        idx = -1
    if(def_idx!=-2):
        idx = def_idx
    new_idx = (int(idx)+1)%total_imgs
    with open(PATH+'/idx.txt','w') as f:
        f.write(str(new_idx))
    set_img(new_idx)
    

if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description='Bing Wallpaper auto update')
    parser.add_argument('--fetch', action='store_true',help='Turn on to fetch new images')

    args = parser.parse_args()
    
    if args.fetch:
        ret_code = get_images()
        if(ret_code==0):
            next_img(-1)
    else:
        next_img()
    
