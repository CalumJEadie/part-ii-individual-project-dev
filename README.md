
# Source Code Package

## Calum J. Eadie
## Video Processing Language for the Raspberry Pi
## Computer Science Tripos, Part II
## Girton College

## Part II Individual Project - Development Repository

### Dependancies

PySide - LGPL Python binding for Qt

```sh
apt-get install python-pyside
port install py-pyside
```

gdata - includes YouTube Python API

```sh
pip install gdata
```

pyomxplayer - Python bindings for OMXPlayer

```sh
git clone https://github.com/CalumJEadie/pyomxplayer
python pyomxplayer/setup.py install
```

show - Python debugging library

```sh
pip install show
```

nose - Python unit testing framework

```sh
pip install nose
```

pexpect - interprocess communication

```sh
pip install pexpect
```

youtube-dl

```sh
apt-get install youtube-dl
# Update to make sure up to date with YouTube API
youtube-dl -U
```


### Running

```sh
cd app
# nosetests.sh makes sure MacPorts Python version is used rather than Mac version
# to make sure PySide available
../tools/nosetests.sh test/ui/test_editor.py
```
