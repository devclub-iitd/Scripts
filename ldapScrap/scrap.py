from bs4 import BeautifulSoup
import requests
import json
import argparse
import os,os.path

# Taken from https://stackoverflow.com/a/600612/119527
def mkdir_p(path):
    try:
        os.makedirs(path,exist_ok=True)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(os.path.abspath(path)))
    return open(path, 'w')

def get_prof(url):
    # Parses the ldap page at a given url else throws an Exception
    page = requests.get(url)
    if page.status_code==200:
        parsedPage = BeautifulSoup(page.text,"html.parser")
        profs = parsedPage.find_all("tr")[1:]
        result = {}
        for prof in profs:
            uid,name = [x.text for x in prof.find_all("td")]
            uid = uid.lower()
            result[uid] = name
        return result
    else:
        raise Exception("url: "+url+" returned status code: "+str(page.status_code))

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parse prof detail from ldap in IITD')
    parser.add_argument('urls', metavar='U',
                    help='File containing the ldap urls')
    parser.add_argument('out', metavar='O',
                    help='Path of the output json file')
    args = parser.parse_args()

    IN_FILE = args.urls
    OUTPUT_FILE = args.out
    
    with open(IN_FILE,"r") as fl:
        urls = fl.read().split()

    db = {}
    for url in urls:
        try:
            profs = get_prof(url)
            db.update(profs)
        except Exception as e:
            print(e)
    with safe_open_w(OUTPUT_FILE) as fl:
        fl.write(json.dumps(db,sort_keys=True,indent=4))
