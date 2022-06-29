# Configuring firefox, without using a Mozilla account

## Configuration
According to `prefs.js`, we can add a `user.js` to the profile directory and that will make sure specific config settings are applied. Currently we have:
- Tracking protection is set to strict
- Always Send Do Not Track
- Default Search is Duckduckgo
- Firefox studies are off by default

## Extensions
For moving around firefox compatiable browser extensions, so far I've found:
- [ansible-firefox-addon](https://github.com/alzadude/ansible-firefox-addon) - hasn't been updated in like 6 years
- [Mozilla: Deploying Firefox with extensions](https://support.mozilla.org/en-US/kb/deploying-firefox-with-extensions) - there's a script to do this here: [grab_all_firefox_extensions.py](./grab_all_firefox_extensions.py), it grabs all the add on ids

### Current Extensions we always want to install

|   add-on name   |   add-on ID   |
| Woordenboek Nederlands | nl-NL@dictionaries.addons.mozilla.org |
| Twitter Visible Alt Text | {38a01252-6a18-4cbf-831c-88ff451b4263} |
| Privacy Badger | jid1-MnnxcxisBPnSXQ@jetpack |
| Startpage — Private Search Engine & New Tab | {0e58f6a7-1788-470a-a74c-36921e55d3e0} |
| 'Improve YouTube!' (Video & YouTube Tools)🎧 | {3c6bf0cc-3ae2-42fb-9993-0d33104fdcaf} |
| A Teal Glow | {d707729d-d337-47ce-9259-e29cec7af885} |
| Simple Translate | simple-translate@sienori |
| AdBlocker Ultimate | adblockultimate@adblockultimate.net |
| Bitwarden - Free Password Manager | {446900e4-71c2-419f-a6a7-df9c091e268b} |
| LastPass: Free Password Manager | support@lastpass.com |
| Vimium | {d7742d87-e61d-4b78-b8a1-b469842139fa} |
| Renewed Tab | {166411f2-402a-4bca-a3da-38b795ec8007} |
| Dark Reader | addon@darkreader.org |
| Nederlands (NL) Language Pack | langpack-nl@firefox.mozilla.org |
