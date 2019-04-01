package main

import (
    "strings"
    "log"
    "net/url"
)

func have_internet(urlStr string, response_String string, useProxy bool, proxyAddr string) (do_we bool) {
    
    var proxyAddrURL *url.URL = nil

    if useProxy {
        proxyAddrURL, _ = url.Parse(proxyAddr)
    }

    //creating the URL to be loaded through the proxy
    url_to_send, err := url.Parse(urlStr)
    if err != nil {
        log.Fatal(err)
    }

    data := GET_request(proxyAddrURL, url_to_send, true)

    return strings.Contains(data , response_String) 
}