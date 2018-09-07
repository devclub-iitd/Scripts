import ssl

if hasattr(ssl,'_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

import sys
import signal
import time
from getpass import getpass
from datetime import datetime
import urllib.request,sys,threading
import argparse
import os

class Proxy:
    proxy_set={'btech':22,'dual':62,'diit':21,'faculty':82,'integrated':21,'mtech':62,'phd':61,'retfaculty':82,'staff':21,'irdstaff':21,'mba':21,'mdes':21,'msc':21,'msr':21,'pgdip':21}
    google = 'http://www.google.com'
    def __init__(self, username, password, proxy_cat):
        self.username = username
        self.password = password
        self.proxy_cat = proxy_cat
        self.auto_proxy = "http://www.cc.iitd.ernet.in/cgi-bin/proxy."+proxy_cat
        self.urlopener = urllib.request.build_opener(urllib.request.ProxyHandler({'auto_proxy':self.auto_proxy}))
        self.proxy_page_address = 'https://proxy'+str(Proxy.proxy_set[proxy_cat])+'.iitd.ernet.in/cgi-bin/proxy.cgi'
        self.new_session_id()
        self.details()
        
    @staticmethod
    def get_proxy_address(proxy_cat):
        proxy_address = 'http://proxy'+str(Proxy.proxy_set[proxy_cat])+'.iitd.ernet.in:3128'
        print(proxy_address)
        return 1

    def is_connected(self):
        proxies = {'http': 'http://proxy'+str(Proxy.proxy_set[self.proxy_cat])+'.iitd.ernet.in:3128'}
        try:
            response = urllib.request.urlopen(Proxy.google, proxies=proxies).read().decode()
        except Exception as e:
            return "Not Connected"
        if "<title>IIT Delhi Proxy Login</title>" in response:
            return "Login Page"
        elif "<title>Google</title>" in response:
            return "Google"
        else:
            return "Not Connected"

    def get_session_id(self):
        try:
            response = self.open_page(self.proxy_page_address)
        except Exception as e:
            return None
        check_token='sessionid" type="hidden" value="'
        token_index=response.index(check_token) + len(check_token)
        sessionid=""
        for i in range(16):
            sessionid+=response[token_index+i]
        return sessionid

    def new_session_id(self):
        self.sessionid = self.get_session_id()
        self.loginform={'sessionid':self.sessionid, 'action':'Validate', 'userid':self.username, 'pass':self.password}
        self.logout_form={'sessionid':self.sessionid, 'action':'logout', 'logout':'Log out'}
        self.loggedin_form={'sessionid':self.sessionid, 'action':'Refresh'}

    def login(self):
        self.new_session_id()
        response = self.submitform(self.loginform)
        if "Either your userid and/or password does'not match." in response:
            return "Incorrect", response
        elif "You are logged in successfully as "+self.username in response:
            def ref():
                if not self.loggedout:
                    res,full = self.refresh()
                    print("Refresh",datetime.now())
                    if res!='Success':
                        print("Refresh Response: ",res,full)
                        loginTimer = threading.Timer(10.0,self.login)
                        loginTimer.daemon = True
                        loginTimer.start()
                        print("Session Expired Run Script again")
                    else:
                        self.timer = threading.Timer(60.0,ref)
                        self.timer.daemon = True
                        self.timer.start()
            self.timer = threading.Timer(60.0,ref)
            # self.timer = threading.Timer(2.0,ref)
            self.timer.daemon = True
            self.timer.start()
            self.loggedout = False
            return "Success", response
        elif "already logged in" in response:
            return "Already", response
        elif "Session Expired" in response:
            return "Expired", response
        else:
            return "Not Connected", response

    def logout(self):
        self.loggedout = True
        response = self.submitform(self.logout_form)
        if "you have logged out from the IIT Delhi Proxy Service" in response:
            return "Success", response
        elif "Session Expired" in response:
            return "Expired", response
        else:
            return "Failed", response
        
    def refresh(self):
        response = self.submitform(self.loggedin_form)
        if "You are logged in successfully" in response:
            if "You are logged in successfully as "+self.username in response:
                return "Success", response
            else:
                return "Not Logged In"
        elif "Session Expired" in response:
            return "Expired", response
        else:
            return "Not Connected", response

    def details(self):
        dictionary = vars(self)
        for property in vars(self):
            if VERBOSE:
                print(property, ": ", dictionary[property])

    def submitform(self, form):
        return self.urlopener.open(urllib.request.Request(self.proxy_page_address,urllib.parse.urlencode(form).encode("ascii"))).read().decode()

    def open_page(self, address):
        return self.urlopener.open(address).read().decode()

STATUS = 0
RESPONSE = 1
VERBOSE = False

def signal_handler(signal, frame):
        print('\nLogout',user.logout()[STATUS])
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Proxy Login program for IIT Delhi')
    parser.add_argument('user', metavar='U',
                    help='Username for proxy login')
    parser.add_argument('category', metavar='C',
                    help='Proxy Category. E.g. btech, dual, mtech, phd etc.')
    parser.add_argument('--passwd',
                    help='Password for proxy. If not specified then will use environment variable $password')
    args = parser.parse_args()
    uname=args.user
    proxycat=args.category
    passwd = args.passwd or os.environ['password']

    user = Proxy(username=uname, password=passwd, proxy_cat=proxycat)
    login_status = user.login()[STATUS]
    print('\nLogin',login_status)
    if login_status=="Success":
        signal.pause()

