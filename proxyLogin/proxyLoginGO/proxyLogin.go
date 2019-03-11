package main

import (
    "time"
    "os"
    "strings"
    "strconv"
    "io/ioutil"
    "log"
    "net/http"
    "net/url"
    "crypto/tls"
    "golang.org/x/net/html"
)

var username, password, proxy_cat string;


var proxy_set = map[string]int{
    "btech":22,
    "dual":62,
    "diit":21,
    "faculty":82,
    "integrated":21,
    "mtech":62,
    "phd":61,
    "retfaculty":82,
    "staff":21,
    "irdstaff":21,
    "mba":21,
    "mdes":21,
    "msc":21,
    "msr":21,
    "pgdip":21}

var external_site = "http://www.google.com"     //customizable

func get_proxy_address() (proxy_address string) {
    proxy_address = "http://proxy"+strconv.Itoa(proxy_set[proxy_cat])+".iitd.ernet.in:3128"
    return
}

func get_proxy_url() (proxy_url string) {
    proxy_url = "https://proxy"+strconv.Itoa(proxy_set[proxy_cat])+".iitd.ernet.in/cgi-bin/proxy.cgi"
    return
}

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

func have_internet() (do_we bool) {
    //creating the proxyURL
    proxyAddr := get_proxy_address()
    proxyAddrURL, err := url.Parse(proxyAddr)
    if err != nil {
        log.Fatal(err)
    }

    //log.Println(proxyAddrURL.String())              //debug

    //creating the URL to be loaded through the proxy
    urlStr := external_site
    url_to_send, err := url.Parse(urlStr)
    if err != nil {
        log.Fatal(err)
    }

    //adding the proxy settings to the Transport object
    transport := &http.Transport{
        TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
        Proxy: http.ProxyURL(proxyAddrURL),
    }

    //adding the Transport object to the http Client
    client := &http.Client{
        Transport: transport,
    }

    //generating the HTTP GET request
    request, err := http.NewRequest("GET", url_to_send.String(), nil)
    if err != nil {
        log.Fatal(err)
    }

    //calling the URL
    response, err := client.Do(request)
    if err != nil {
        log.Fatal(err)
    }

    defer response.Body.Close()

    //getting the response
    data, err := ioutil.ReadAll(response.Body)
    if err != nil {
        log.Println(err)
    }
    
    //printing the response - debug
    //log.Println(string(data))

    return strings.Contains(string(data), "<title>Google</title>") 
}

func config_intranet() (do_we bool){

    //creating the URL to be loaded through the proxy
    urlStr := get_proxy_url()
    url_to_send, err := url.Parse(urlStr)
    if err != nil {
        log.Fatal(err)
    }

    //adding the proxy settings to the Transport object
    transport := &http.Transport{
        TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
    }

    //adding the Transport object to the http Client
    client := &http.Client{
        Transport: transport,
    }

    //generating the HTTP GET request
    request, err := http.NewRequest("GET", url_to_send.String(), nil)
    if err != nil {
        log.Fatal(err)
    }

    //calling the URL
    response, err := client.Do(request)
    if err != nil {
        log.Fatal(err)
    }

    defer response.Body.Close()

    //getting the response
    data, err := ioutil.ReadAll(response.Body)
    if err != nil {
        log.Println(err)
    }
    
    //printing the response - debug
    //log.Println(string(data)) 

    if strings.Contains(string(data), "<title>IIT Delhi Proxy Login</title>") == false {
        return false
    }

    if strings.Contains(string(data), "already logged in") {
        log.Println("Logged in successfully")
        return true
    }

    root, err := html.Parse(strings.NewReader(string(data)))
    if err != nil {
        log.Fatal(err)
    }

    element, ok := getElementByName("sessionid", root)
    if !ok {
        log.Fatal("Wasn't able to parse session ID from proxy login page")
    }

    var sessionid string
    for _, a := range element.Attr {
        if a.Key == "value" {
            sessionid = a.Val
            break
        }
    }

    //log.Println(sessionid)          //debug

    urlData := url.Values{}
    urlData.Set("sessionid", sessionid)
    urlData.Set("userid", username)
    urlData.Set("pass", password)
    urlData.Set("action", "Validate")

    response, err = client.PostForm(urlStr, urlData)

    if err != nil {
        log.Println(err)
    }

    defer response.Body.Close()

    //getting the response
    data, err = ioutil.ReadAll(response.Body)
    if err != nil {
        log.Println(err)
    }
    
    //log.Println(string(data))

    if strings.Contains(string(data), "Either your userid and/or password does'not match.") {
        log.Fatal("Wrong username or password")
    } else if strings.Contains(string(data), "You are logged in successfully as") {
        log.Println("Logged in successfully")
        return true
    }
    
    return false
}


func main() {
    // parse arguments

    username = os.Args[1]
    password = os.Args[2]
    proxy_cat = os.Args[3]

    // start main loop
    for {
        if have_internet() == false {
            if config_intranet() == false {
                log.Println("Not Connected to intranet")
            }
        } else {
            log.Println("Connected to internet")
        }

        time.Sleep(5000 * time.Millisecond)
    }
}