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

    setup_code = """from api.core import display,ask_yes_no_prompt
from api import youtube,videoplayer"""

    program = setup_code + '\n' + code

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
        from app.api.core import display,ask_yes_no
        from app.api import youtube,videoplayer
        exec(code)

    run(code)