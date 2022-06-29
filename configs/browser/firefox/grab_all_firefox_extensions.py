#!/usr/bin/env python3
# import and print all the firefox add-on ids from macOS
import json
import shutil

USER_NAME='jhitch'
FIREFOX_PROFILE="n390gdog.default-release"
EXTENSION_FILE_PATH=(f"/Users/{USER_NAME}/Library/Application Support/Firefox/"
                     f"Profiles/{FIREFOX_PROFILE}/extensions.json")

print(f'Processing add-ons from:\n{EXTENSION_FILE_PATH}')

# load the json into a python dict
extensions_json = None
with open(EXTENSION_FILE_PATH) as json_file:
    data = json_file.read()
    extensions_json = json.loads(data)

# print each extension's add-on ID, as well as the human readable name
print("|   add-on name   |   add-on ID   |")
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
        print(f"| {add_on_name} | {add_on_id} |")
        extensions_dir = EXTENSION_FILE_PATH.replace(".json","")
        extensions_xpi_file = f"{add_on_id}.xpi"
        extensions_xpi_file_path = "/".join([extensions_dir,
                                             extensions_xpi_file])

        shutil.copyfile(extensions_xpi_file_path,
                        f"./distribution/extensions/{extensions_xpi_file}")
