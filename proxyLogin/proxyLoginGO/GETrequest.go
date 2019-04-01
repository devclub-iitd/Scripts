package main

import (
    "io/ioutil"
    "log"
    "net/http"
    "net/url"
    "crypto/tls"
)

func GET_request(proxyAddrURL *url.URL, url_to_send *url.URL, insecureSkip bool) (data string) {

    //adding the proxy settings to the Transport object

    transport := &http.Transport{
        TLSClientConfig: &tls.Config{InsecureSkipVerify: false},
    }

    if insecureSkip == true {
        if proxyAddrURL == nil {
            transport = &http.Transport{
                TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
            }
        } else {
            transport = &http.Transport{
                TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
                Proxy: http.ProxyURL(proxyAddrURL),
            }
        }
    } else {
        if proxyAddrURL != nil {
            transport = &http.Transport{
                TLSClientConfig: &tls.Config{InsecureSkipVerify: false},
                Proxy: http.ProxyURL(proxyAddrURL),
            }
        }
    }

    //adding the Transport object to the http Client
    client := &http.Client{
        Transport: transport,
    }

    //generating the HTTP GET request
    request, err := http.NewRequest("GET", url_to_send.String(), nil)
    if err != nil {
        log.Println(err)
        return "";
    }

    //calling the URL
    response, err := client.Do(request)
    if err != nil {
        log.Println(err)
        return "";
    }

    defer response.Body.Close()

    //getting the response
    data_raw, err := ioutil.ReadAll(response.Body)
    if err != nil {
        log.Println(err)
        return "";
    }

    return string(data_raw)
}