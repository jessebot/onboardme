"""
Using Textualize's rich library to pretty print subprocess outputs,
so during long running commands, the user isn't wondering what's going on,
even if you don't actually output anything from stdout/stderr of the command.
"""
import dbm
import logging
from subprocess import PIPE, Popen

from rich import print
from rich.console import Console
from rich.logging import RichHandler

log_opts = {'format': "%(message)s",
            'datefmt': "[%X]",
            'handlers': [RichHandler(rich_tracebacks=True)]}

# set the logger opts for all files
with dbm.open('log_cache', 'r') as db:
    log_opts['level'] = int(db['level'].decode())
    log_file = db['file'].decode()
    if log_file:
        log_opts['console'] = Console(file=log_file.decode())

logging.basicConfig(**log_opts)
log = logging.getLogger("rich")


def subproc(commands=[], error_ok=False, suppress_output=False, spinner=True,
            directory=""):
    """
    Takes a list of str type commands to run in a subprocess.
    Optional vars:
        error_ok        - bool, catch errors, defaults to False
        suppress_output - bool, don't output anything form stderr, or stdout
        spinner         - bool, show an animated progress spinner
    Takes a str commmand to run in BASH, as well as optionals bools to pass on
    errors in stderr/stdout and suppress_output
    """
    for command in commands:
        status_line = f"[bold green]❤ Running command:[/bold green] {command}"
        if not suppress_output:
            log.info(status_line, extra={'markup': True})

        if not spinner:
            output = run_subprocess(command, error_ok, directory)
        else:
            print("")
            console = Console()
            tasks = [command]

            with console.status(status_line):
                while tasks:
                    output = run_subprocess(command, error_ok, directory)
                    tasks.pop(0)

        if output:
            if not suppress_output:
                log.info(output)

    if output:
        return output


def run_subprocess(command, error_ok=False, directory=""):
    """
    Takes a str commmand to run in BASH in a subprocess.
    Typically run from subproc, which handles output printing

    Optional vars:
        error_ok   - bool, catch errors, defaults to False
        directory  - current working dir, directory to run command in
    """
    # subprocess expects a list
    cmd = command.split()
    if directory:
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, cwd=directory)
    else:
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    ret_code = p.returncode
    res = p.communicate()
    res_stdout = res[0].decode('UTF-8')
    res_stderr = res[1].decode('UTF-8')

    if not error_ok:
        # check return code, raise error if failure
        if not ret_code:
            if res_stderr:
                log.debug(res_stderr)
        else:
            if ret_code != 0:
                # also scan both stdout and stdin for weird errors
                for output in [res_stdout.lower(), res_stderr.lower()]:
                    if 'error' in output:
                        err = "Return code not zero! Return code: " + ret_code
                        raise Exception(f'\033[0;33m {err} \n {output} '
                                        '\033[00m')

    # sometimes stderr is empty, but sometimes stdout is empty
    for output in [res_stdout, res_stderr]:
        if output:
            return output
