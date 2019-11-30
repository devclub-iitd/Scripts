from collections import defaultdict
from urllib import parse
import requests
from config import *

def verify_url(url):
    scheme = parse.splittype(url)[0]
    if scheme is None:
        url = 'https://' + url
    url_deconstruct = parse.urlsplit(url)
    host = url_deconstruct[1]
    if not 'github.com' in host:
        return 1

    r = requests.get(url)

    if r.status_code==404:
        return 2
    return 0

def get_next_link(curr_assignment, email):
    index = ASSIGNMETS.index(curr_assignment)
    if index<len(LINKS)-1:
        return LINKS[index+1], 1
    else:
        return None, 0
