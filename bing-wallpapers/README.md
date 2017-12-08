# Bing-Wallpaper Update


## What is it all about?
This small python script enables a user to dynamically update the Ubuntu desktop wallpaper. The images are used from [Bing](https://bing.com)

## Getting Started: 
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

The following packages are required on a linux machine to compile and use the software package.

```
python3
pip3
```

### Installing

Using bing-wallpaper is fairly simple. Just issue the following commands on a linux machine

```
cd ~
wget https://github.com/devclub-iitd/Scripts/raw/master/release/bing-wallpapers.zip
unzip bing-wallpapers.zip
cd bing-wallpapers
pip3 install --user requests os mimetypes datetime argparse shutil
```
### Running the Web-App

Edit the path variable in the bing-wallpaper.py script to the path where you want the wallpapers to be stored. In the default case just replace `$USER` with your username.

Now, you can run the code using the command:

```
python3 bing-wallpaper.py --fetch
``` 
This will fetch the wallpapers in a directory with today's date.

To change the wallpaper run 

```
python3 bing-wallpaper.py
```


## Built With

* [Python 3.6](http://www.python.org/) - Python is a programming language that lets you work quickly and integrate systems more effectively.


## Added Use case

* You can also make this script run at startup. See [Here](https://stackoverflow.com/questions/24518522/run-python-script-at-startup-in-ubuntu)
* You can configure various options like next background on right click using nautilus actions. See [Here](https://askubuntu.com/questions/657111/how-to-add-options-to-the-mouse-right-click-menu-in-ubuntu-14-04)
