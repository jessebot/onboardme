from ..subproc import subproc
from ..constants import OS


def search_for_package(package: str,
                       package_manager: str|list = None,
                       cfg: dict = {}) -> dict:
    """
    Search for package using package manager's search function.
    Takes packages config dict and optional package_manager (str or list) to
    search returns output of search command

    If no package_manager is passed in, we search every package_manager with 
    a search command
    returns outputs of search commands as dictionary like {'brew': output}
    """
    if not package_manager:
        package_manager = cfg.keys()

    res = {}

    # search for a package for a SINGLE package manager
    if isinstance(package_manager, str):
        res[package_manager] = {}

        res[package_manager]["group"] = check_package_groups(
                cfg[package_manager]["packages"],
                package,
                package_manager 
                )

        res[package_manager]["info"] = search_pkg_manager(
                package,
                package_manager,
                cfg[package_manager]['commands']
                )

        res[package_manager]["installed"] = check_if_package_installed(
                package_manager,
                package,
                res[package_manager]["info"]
                )

    # search a list of package managers
    elif isinstance(package_manager, list):
        for pkg_mngr in package_manager:
            res[pkg_mngr] = {}

            res[pkg_mngr]["group"] = check_package_groups(
                    cfg[pkg_mngr]["packages"],
                    package,
                    pkg_mngr
                    )

            res[pkg_mngr]["info"] = search_pkg_manager(
                    package,
                    pkg_mngr,
                    cfg[pkg_mngr]['commands']
                    )

            res[pkg_mngr]["installed"] = check_if_package_installed(
                    pkg_mngr,
                    package,
                    res[pkg_mngr]["info"]
                    )
    return res


def check_if_package_installed(pkg_mngr: str,
                               package: str,
                               info_str: str = "") -> bool:
    """ 
    checks if package is currently installed via a given package manager
    takes info_str, which is parsed to see if the package is installed
    """
    if pkg_mngr == "brew":
        if "Not installed" not in info_str:
            return True

    elif pkg_mngr == "pipx":
        check_pipx_list = subproc(["pipx list"])
        if isinstance(check_pipx_list, list):
            for line in check_pipx_list:
                if package in line:
                    return True
        elif isinstance(check_pipx_list, str):
            if package in check_pipx_list:
                return True

    elif "pip3" in pkg_mngr:
        if "WARNING: Package(s) not found" not in info_str:
            return True

    return False


def search_pkg_manager(package: str, package_manager: str, commands: dict) -> str:
    """ 
    searches one package manager for a package.
    returns a string with info about the package if found.
    """
    if package_manager in ['apt', 'flatpak'] and OS[0] == "Darwin":
        return f"{package_manager} is not supported on macOS 😔"

    if package_manager == 'cargo' and "--git" in package:
        return "Search for --git packages not supported 😔"

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
                    if "==>" in item:
                        info_res[idx] = "[#A8FD57]" + item.replace(f"{package}: ", "") + "[/]"
                    elif package_manager != "brew" and package in item:
                        info_res[idx] = "[#A8FD57]" + item + "[/]"

                return "\n".join(info_res)
            else:
                return res.replace(package, f"[#A8FD57]{package}[/]")

        # if no package was found
        else:
            return f"{package} was not found in {package_manager}"

    # if there's no search command for this package
    else:
        return f"{package_manager} does not have a search command."


def check_package_groups(package_groups: dict,
                         package: str,
                         package_manager: str) -> str:
    """
    check a package manager's groups for package and if exists, returns name of
    package group, else returns None
    """
    for pkg_group, pkg_group_list in package_groups.items():
        if package in pkg_group_list:
            return pkg_group

    # if no package group was found, we just return default
    return 'default'
