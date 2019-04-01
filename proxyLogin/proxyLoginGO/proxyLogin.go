package main

import (
    "fmt"
    "time"
    "strconv"
    "log"
    "github.com/howeyc/gopass"
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
var response_String = "<title>Google</title>"

func get_proxy_address() (proxy_address string) {
    proxy_address = "http://proxy"+strconv.Itoa(proxy_set[proxy_cat])+".iitd.ernet.in:3128"
    return
}

func get_proxy_url() (proxy_url string) {
    proxy_url = "https://proxy"+strconv.Itoa(proxy_set[proxy_cat])+".iitd.ernet.in/cgi-bin/proxy.cgi"
    return
}


func main() {
    // input arguments


    fmt.Print("Enter username: ")
    fmt.Scanln(&username)
    fmt.Print("Enter password: ")
    maskedPassword, _ := gopass.GetPasswdMasked() // Masked
    password = string(maskedPassword);
    fmt.Print("Enter category: ")
    fmt.Scanln(&proxy_cat)

    _ , ok := proxy_set[proxy_cat]
    if !ok {
        fmt.Println("Invalid category "+proxy_cat+". Category could be one of the following only - ")
        fmt.Println("btech,dual,diit,faculty,integrated,mtech,phd,retfaculty,staff,irdstaff,mba,mdes,msc,msr,pgdip")
        log.Fatal("Exiting..")
    }

    first := false

    // start main loop
    for {
        if have_internet(external_site, response_String, true, get_proxy_address()) == false {
            if config_intranet(get_proxy_url()) == false {
                fmt.Println("Not Connected to intranet")
            } else {
                first = true
            }
        } else {
            fmt.Println("Connected to internet")
            if first {
                fmt.Println("Run the following commands on a linux terminal to set the proxy environment variable: ")
                fmt.Println("(This is optional and is only useful for accessing internet via terminal)")
                fmt.Println("export http_proxy=\"http://proxy"+strconv.Itoa(proxy_set[proxy_cat])+".iitd.ac.in:3128\"")
                fmt.Println("export https_proxy=\"http://proxy"+strconv.Itoa(proxy_set[proxy_cat])+".iitd.ac.in:3128\"")
                fmt.Println("export HTTP_PROXY=\"http://proxy"+strconv.Itoa(proxy_set[proxy_cat])+".iitd.ac.in:3128\"")
                fmt.Println("export HTTPS_PROXY=\"http://proxy"+strconv.Itoa(proxy_set[proxy_cat])+".iitd.ac.in:3128\"")
                first = false
            }
        }

        time.Sleep(5000 * time.Millisecond)
    }
}