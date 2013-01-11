import sys
from microbuild.microbuild import task, build
import subprocess
import nose

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
    subprocess.call(["open","apidoc/index.html"])

@task()
def test():
    """
    Runs all tests.
    """
    nose.run(["test"])

build(sys.modules[__name__], sys.argv[1:])