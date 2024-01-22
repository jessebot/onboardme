from ..subproc import subproc


def search_for_package(cfg: dict, package_manager: str|list = None):
    """
    Search for package using package manager's search function.
    Takes packages config dict and optional package_manager (str or list) to search
    If no package_manager is passed in, we search every package_manager.commands.search
    """

    if package_manager:
        search_cmd = cfg[package_manager]['commands']['search']
        return subproc([search_cmd])
    else:
        results = {}
        for package_manager, metadata in cfg.items():
            search_cmd = cfg[package_manager]['commands']['search']
            results[package_manager] = subproc([search_cmd])
