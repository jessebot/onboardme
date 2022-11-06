"""
Using Textualize's rich library to pretty print subprocess outputs,
so during long running commands, the user isn't wondering what's going on,
even if you don't actually output anything from stdout/stderr of the command.
"""
import logging as log
from subprocess import PIPE, Popen

from rich.console import Console


def subproc(commands=[], **kwargs):
    """
    Takes a list of BASH commands to run in a subprocess sequentially.
    Optional keyword arguments:
        error_ok        - catch Exceptions and log them, default: False
        quiet           - don't output from stderr/stdout, Default: False
        spinner         - show an animated progress spinner. can break sudo
                          prompts and should be turned off. Default: True
        cwd             - path to run commands in. Default: pwd of user
        shell           - use shell with subprocess or not. Default: False
        env             - dictionary of env variables for BASH. Default: None
    """

    # get/set defaults and remove the 2 output specific args from the key word
    # args dict so we can use the rest to pass into subproc.Popen later on
    spinner = kwargs.pop('spinner', True)
    quiet = kwargs.pop('quiet', False)

    if spinner:
        # we don't actually need this if we're not doing a progress spinner
        console = Console()

    status_line = "[bold green]♥ Running command[/bold green]"

    for command in commands:
        status = f"{status_line}: {command}"

        if spinner:
            with console.status(status):
                output = run_subprocess(command, **kwargs)
        else:
            if not quiet:
                log.info(status, extra={'markup': True})
            output = run_subprocess(command, **kwargs)

        if output and not quiet:
            log.info(output)

    if output:
        return output


def run_subprocess(command, **kwargs):
    """
    Takes a str commmand to run in BASH in a subprocess.
    Typically run from subproc, which handles output printing.
    error_ok=False, directory="", shell=False
    Optional keyword vars:
        error_ok  - bool, catch errors, defaults to False
        cwd       - str, current working dir which is the dir to run command in
        shell     - bool, run shell or not
        env       - environment variables you'd like to pass in
    """
    # subprocess expects a list if there are spaces in the command
    cmd = command.split()

    error_ok = False
    if 'error_ok' in kwargs:
        error_ok = kwargs.pop('error_ok')

    # this passes in the other optional args such as cwd, shell, and env
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, **kwargs)

    ret_code = p.returncode
    res = p.communicate()
    res_stdout = res[0].decode('UTF-8')
    res_stderr = res[1].decode('UTF-8')

    if not error_ok:
        # check return code, raise error if failure
        if not ret_code:
            if res_stderr:
                log.debug(res_stderr, extra={"markup": True})
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
