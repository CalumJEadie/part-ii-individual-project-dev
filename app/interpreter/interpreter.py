"""
Intrepreter component.
"""

import logging
import subprocess
import tempfile

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def interpret(code):
    """
    Interprets `code` in the following environment:

    ```
    from api.core import display,ask_yes_no_prompt
    from api import youtube,videoplayer
    ```

    Code is executed in a seperate process to the callee.
    Executes code without modification or validation.
    """

    # setup_code = """from api.core import display,ask_yes_no_prompt
# from api import youtube,videoplayer"""

    # program = setup_code + '\n' + code

    # `exec` approach not working - have problems with package/module imports
    # 
    # New approach:
    # - create temporary file for code
    # - use exec_file to run code from root director
     
    # delete=True: delete when closed
    #program_file = tempfile.NamedTemporaryFile()#delete=True)
    #program_file.write(program)
    #program_file.flush()
    #log.info("Created temporary file: %s" % program_file.name)

    # Wait for command to complete and check return code.
    #args = ["python","exec_file.py",program_file.name]
    #log.info("Calling `%s`" % args)
    #print subprocess.check_output(args,stderr=subprocess.STDOUT)
    #program_file.close()

    # Previous approach didn't work either.
    
    def run(code):
        import random
        import time

        import app.api.core
        import app.api.youtube
        import app.api.videoplayer

        # At module level globals and locals are the same dictionary.
        # Need this behaviour to function defintions to work correctly.
        # Called as `exec(code)` different dictionaries were being used
        # for globals and locals and so inside a function it wasn't possible
        # to access other functions that had been defined in the script.
        # The functions had been defined in the local scope of the module
        # which wasn't accessible in the local scope of the function.
        # See: http://stackoverflow.com/questions/871887/using-exec-with-recursive-functions
        globals_ = {
            "random": random,
            "ask_yes_no": app.api.core.ask_yes_no,
            "display": app.api.core.display,
            "display_loading": app.api.core.display_loading,
            "youtube": app.api.youtube,
            "videoplayer": app.api.videoplayer,
            "Speed": app.api.videoplayer.Speed,
            "sleep": time.sleep
        }

        code = """loading_dialog = display_loading()
%s
loading_dialog.close()""" % code

        exec(code, globals_, globals_)

    run(code)