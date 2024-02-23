from ..subproc import subproc
from ..constants import OS


def search_for_package(package: str,
                       package_manager: str|list = None,
                       cfg: dict = {}):
    """
    Search for package using package manager's search function.
    Takes packages config dict and optional package_manager (str or list) to
    search returns output of search command

    If no package_manager is passed in, we search every package_manager with 
    a search command
    returns outputs of search commands as dictionary like {'brew': output}
    """
    # search for a package for a SINGLE package manager
    if isinstance(package_manager, str):
        res = search_pkg_manager(package,
                                 package_manager,
                                 cfg[package_manager]['commands'])

    # search a list of package managers
    elif isinstance(package_manager, list):
        res = {}
        for pkg_mngr in package_manager:
            res[pkg_mngr] = search_pkg_manager(package,
                                               package_manager,
                                               cfg[package_manager]['commands'])

    # search all package managers
    else:
        res = {}
        for pkg_mngr in cfg.keys():
            res[pkg_mngr] = search_pkg_manager(package,
                                               pkg_mngr,
                                               cfg[package_manager]['commands'])
    return res


def search_pkg_manager(package: str, package_manager: str, commands: dict):
    """ 
    searches one package manager for a package
    """
    if package_manager in ['apt', 'flatpak'] and OS[0] == "Darwin":
        return f"{package_manager} is not supported on macOS 😔"

    search_cmd = commands['search']
    if search_cmd:
        info_cmd = commands.get('info', False)
        cmd = " ".join([search_cmd, package])
        res = subproc([cmd]).split('\n')

        # if res is multiple lines, join them with new lines
        if isinstance(res, list):
            res = "\n".join(res)

        if package in res:
            # if there's a pkg info command for this package manager, get info
            if info_cmd:
                full_info_cmd = " ".join([info_cmd, package])
                info_res = subproc([full_info_cmd]).split('\n')

                # highlight the name of the package anywhere we find it
                for idx, item in enumerate(info_res):
                    if "==>" in item or package in item:
                        info_res[idx] = "[green]" + item + "[/green]"
                return "\n".join(info_res)
            else:
                return res.replace(package, f"[green]{package}[/green]")

        # if no package was found
        else:
            return f"{package} was not found in {package_manager}."

    # if there's no search command for this package
    else:
        return f"{package_manager} does not have a search command."
