import sys
from microbuild.microbuild import task, build
import subprocess

@task()
def apidoc():
    """
    Generate API documentation.
    """
    subprocess.call(["epydoc-2.7","--config","setup.cfg"])

@task()
def view_apidoc():
    """
    View API documentation.
    """
    subprocess.call(["open","apidocs/index.html"])

build(sys.modules[__name__], sys.argv[1:])