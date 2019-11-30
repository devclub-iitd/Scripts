from collections import defaultdict
import requests
from config import *


def verify_url(url):
    r = requests.get(url)

    if r.status_code==400:
        return False
    return True

def get_next_link(curr_assignment, email):
    index = ASSIGNMETS.index(curr_assignment)
    if index<len(ASSIGNMETS):
        return LINKS[index+1], 1
    else:
        return None, 0
