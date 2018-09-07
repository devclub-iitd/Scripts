
## Precompiled binary

Just unzip proxy_release.zip and run the as follows

```
unzip proxy_release.zip
cd proxy_release
./login_terminal <username> <category> --passwd <password>
```




1. Install Nuitka as

```
CODENAME=`lsb_release -c -s`
wget -O - http://nuitka.net/deb/archive.key.gpg | apt-key add -
echo >/etc/apt/sources.list.d/nuitka.list "deb http://nuitka.net/deb/stable/$CODENAME $CODENAME main"
apt-get update
apt-get install nuitka
```

2. Compile as 

```
python3 -m nuitka --standalone login_terminal.py
```

3. Now you can ship the folder login_terminal.dist


