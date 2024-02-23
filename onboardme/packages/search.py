from ..subproc import subproc
from ..constants import OS


def search_for_package(package: str,
                       package_manager: str|list = None,
                       cfg: dict = {}):
    """
    Search for package using package manager's search function.
    Takes packages config dict and optional package_manager (str or list) to
    search returns output of search command

    If no package_manager is passed in, we search every package_manager.commands.search
    returns outputs of search commands as dictionary like {'brew': output}
    """
    if isinstance(package_manager, str):
        if package_manager in ['apt', 'flatpak'] and OS[0] == "Darwin":
            return f"{package_manager} is not supported on macOS 😔"

        search_cmd = cfg[package_manager]['commands']['search']
        info_cmd = cfg[package_manager]['commands'].get('info', False)
        cmd = " ".join([search_cmd, package])
        res = subproc([cmd]).split('\n')

        # if res is multiple lines, join them with new lines
        if isinstance(res, list):
            res = "\n".join(res)

        if package in res:
            if info_cmd:
                full_info_cmd = " ".join([info_cmd, package])
                info_res = subproc([full_info_cmd]).split('\n')
                for idx, item in enumerate(info_res):
                    if "==>" in item:
                        info_res[idx] = "[green]" + item + "[/green]"
                return "\n".join(info_res)
            else:
                return res
    elif isinstance(package_manager, list):
        results = {}
        for pkg_mngr in package_manager:
            if pkg_mngr in ['apt', 'flatpak'] and OS[0] == "Darwin":
               results[pkg_mngr] = f"{pkg_mngr} is not supported on macOS 😔"

            search_cmd = cfg[pkg_mngr]['commands'].get('search', None)
            if search_cmd:
                cmd = " ".join([search_cmd, pkg_mngr])
                results[pkg_mngr] = subproc([cmd])
        return results
    else:
        results = {}
        for package_manager, metadata in cfg.items():
            if package_manager in ['apt', 'flatpak'] and OS[0] == "Darwin":
               results[package_manager] = f"{package_manager} is not supported on macOS 😔"

            search_cmd = metadata['commands'].get('search', None)
            if search_cmd:
                cmd = " ".join([search_cmd, package])
                results[package_manager] = subproc([cmd])
        return results
