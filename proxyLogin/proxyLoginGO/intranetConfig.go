package main

import (
    "fmt"
    "strings"
    "log"
    "net/url"
    "golang.org/x/net/html"
)

func getElementByName(name string, n *html.Node) (element *html.Node, ok bool) {
    for _, a := range n.Attr {
        if a.Key == "name" && a.Val == name {
            return n, true
        }
    }
    for c := n.FirstChild; c != nil; c = c.NextSibling {
        if element, ok = getElementByName(name, c); ok {
            return
        }
    }
    return
}

func getSessionID(data string) (sessionid string) {

    sessionid = ""
    root, err := html.Parse(strings.NewReader(data))
    if err != nil {
        log.Println(err)
        return
    }

    element, ok := getElementByName("sessionid", root)
    if !ok {
        fmt.Println("Wasn't able to parse session ID from proxy login page")
        return
    }

    for _, a := range element.Attr {
        if a.Key == "value" {
            sessionid = a.Val
            break
        }
    }

    return
}

func config_intranet(urlStr string) (do_we bool){

    //creating the URL to be loaded through the proxy
    url_to_send, err := url.Parse(urlStr)
    if err != nil {
        log.Fatal(err)
    }

    data := GET_request(nil, url_to_send, true)

    if strings.Contains(data, "<title>IIT Delhi Proxy Login</title>") == false {
        return false
    }

    if strings.Contains(data, "already logged in") {
        fmt.Println("Logged in successfully")
        return true
    }

    sessionid := getSessionID(data)

    //log.Println(sessionid)          //debug

    urlData := url.Values{}
    urlData.Set("sessionid", sessionid)
    urlData.Set("userid", username)
    urlData.Set("pass", password)
    urlData.Set("action", "Validate")

    data = POST_request(nil, urlStr, urlData, true)

    if strings.Contains(data, "Either your userid and/or password does'not match.") {
        log.Fatal("Wrong username or password")
    } else if strings.Contains(data, "You are logged in successfully as") {
        fmt.Println("Logged in successfully")
        return true
    }
    
    return false
}