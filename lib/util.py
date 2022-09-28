import subprocess
from rich import print
from rich.console import Console


def subproc(command="", error_ok=False, suppress_output=False, spinner=True):
    """
    Takes a str commmand to run in BASH, as well as optionals bools to pass on
    errors in stderr/stdout and suppress_output
    """
    if not spinner:
        output = actual_subproc(command, error_ok)
    else:
        console = Console()
        tasks = [command]

        status_line = f"[bold green]Running cmd:[/bold green] {command}"
        with console.status(status_line) as status:
            while tasks:
                output = actual_subproc(command, error_ok)

                tasks.pop(0)
                print("\n")

    if output:
        if not suppress_output:
            print(output)
        return output


def actual_subproc(command, error_ok=False):
    cmd = command.split()
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return_code = p.returncode
    res = p.communicate()
    res_stdout = res[0].decode('UTF-8')
    res_stderr = res[1].decode('UTF-8')

    if not error_ok:
        # check return code, raise error if failure
        if not return_code or return_code != 0:
            # also scan both stdout and stdin for weird errors
            for output in [res_stdout.lower(), res_stderr.lower()]:
                if 'error' in output:
                    err = ('Return code not zero! Return code: ' + return_code)
                    raise Exception(f'\033[0;33m {err} \n {output} '
                                    '\033[00m')

    for output in [res_stdout, res_stderr]:
        if output:
            return output
