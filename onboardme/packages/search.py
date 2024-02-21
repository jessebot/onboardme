from ..subproc import subproc


def search_for_package(package: str,
                       package_manager: str|list = None,
                       cfg: dict = {}):
    """
    Search for package using package manager's search function.
    Takes packages config dict and optional package_manager (str or list) to search
    returns output of search command

    If no package_manager is passed in, we search every package_manager.commands.search
    returns outputs of search commands as dictionary like {'brew': output}
    """

    if package_manager:
        search_cmd = cfg[package_manager]['commands']['search']
        info_cmd = cfg[package_manager]['commands'].get('info', False)
        cmd = " ".join([search_cmd, package])
        res = subproc([cmd]).split('\n')
        if package in res:
            if info_cmd:
                full_info_cmd = " ".join([info_cmd, package])
                return subproc([full_info_cmd])
            else:
                return package
    else:
        results = {}
        for package_manager, metadata in cfg.items():
            search_cmd = cfg[package_manager]['commands'].get('search', None)
            if search_cmd:
                cmd = " ".join([search_cmd, package])
                results[package_manager] = subproc([cmd])
        return results
