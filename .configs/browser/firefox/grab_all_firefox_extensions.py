#!/usr/bin/env python3
# import and print all the macos firefox add-on ids in mardown table
# and then moves all the xpis to a local directory: distributions/extensions
import json
import shutil
from sys import platform

USER_NAME='jhitch'
FIREFOX_PROFILE="n390gdog.default-release"

# different os will have this in different places
if platform == "linux" or platform == "linux2":
    # linux - untested
    PROFILE_PATH=(f"/home/{USER_NAME}/Firefox/Profiles/{FIREFOX_PROFILE}/")
elif platform == "darwin":
    # OS X
    PROFILE_PATH=(f"/Users/{USER_NAME}/Library/Application Support/Firefox/"
                  f"Profiles/{FIREFOX_PROFILE}/")
elif platform == "win32" or platform == "windows":
    # Windows... - untested
    PROFILE_PATH=(f"/Users/{USER_NAME}/Library/Application Support/Firefox/"
                  f"Profiles/{FIREFOX_PROFILE}/")

EXT_JSON_FILE = PROFILE_PATH + "extensions.json" 

print(f'Processing add-ons from:\n{EXT_JSON_FILE}')

# load the extensions.json into a python dict
extensions_json = None
with open(EXT_JSON_FILE) as json_file:
    data = json_file.read()
    extensions_json = json.loads(data)

print("add-on name | add-on ID")
print("---|---")
# iterate through the new json dict and of add-ons and grab the name and id
for add_on_dict in extensions_json["addons"]:
    add_on_id = add_on_dict["id"]
    add_on_name = add_on_dict["defaultLocale"]["name"]

    # don't care for the following extensions, as they're defaults with Firefox
    ignored_add_on_ids = ["amazon@search.mozilla.org",
                          "ebay@search.mozilla.org"
                          "google@search.mozilla.org",
                          "bing@search.mozilla.org",
                          "default-theme@mozilla.org",
                          "firefox-compact-light@mozilla.org",
                          "firefox-compact-dark@mozilla.org",
                          "addons-search-detection@mozilla.com",
                          "pictureinpicture@mozilla.org",
                          "firefox-alpenglow@mozilla.org",
                          "formautofill@mozilla.org",
                          "screenshots@mozilla.org",
                          "wikipedia@search.mozilla.org",
                          "webcompat-reporter@mozilla.org",
                          "ddg@search.mozilla.org",
                          "webcompat@mozilla.org",
                          "doh-rollout@mozilla.org"]

    if not any(add_on_id in s for s in ignored_add_on_ids):
        # print each extension's name and add-on ID
        print(f"| {add_on_name} | {add_on_id} |")

        # also copy extension xpi files locally
        extensions_xpi_file = f"{add_on_id}.xpi"
        extensions_dir = PROFILE_PATH + "extensions/"  + extensions_xpi_file

        shutil.copyfile(extensions_dir,
                        f"./distribution/extensions/{extensions_xpi_file}")
