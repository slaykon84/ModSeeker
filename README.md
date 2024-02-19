# ModSeeker
ModSeeker is a user-friendly GUI program designed for Linux users to manage modules efficiently. 
With ModSeeker, users can easily view module information, insert and uninsert modules, simplifying tasks for both new and experienced Linux users.


## Required Libraries
- tkinter
## Installation of Libraries
### Debian Based

```sh 
$ sudo apt install python3-tk
```
### Arch Linux and Manjaro

```sh
$ sudo pacman -s tk
```
### Fedora and CentOS

```sh
$ sudo dnf install python3-tkinter
```
### OpenSUSE

```sh
$ sudo zypper install python3-tkinter
```
Now you can run program by typing:
```sh
$ cd ModSeeker
$ python3 main.py
```

Or you may prefer installing it to your system:

## Installation of Program to the System

```sh
$ git clone https://github.com/slaykon84/ModSeeker
$ cd ModSeeker
$ ./quicksetup.sh
cd ..
```
Now you can start program by typing:
```sh
$ modseeker
```

## Uninstallation

```sh
$ sudo rm /usr/bin/modseeker
$ rm ~/.modseeker
```