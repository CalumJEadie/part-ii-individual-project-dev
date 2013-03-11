## Part II Individual Project - Development Repository

### Dependancies

PySide - LGPL Python binding for Qt

```sh
port install py-pyside
```

gdata - includes YouTube Python API

```sh
pip install gdata
```

pyomxplayer - Python bindings for OMXPlayer

```sh
pip install pyomxplayer
```

show - Python debugging library

```sh
pip install show
```

### Using

Running the editor

```sh
cd app
# nosetests.sh makes sure MacPorts Python version is used rather than Mac version
# to make sure PySide available
../tools/nosetests.sh test/ui/test_editor.py
```
