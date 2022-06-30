# OnBoardMe to [mac, debian]
 ♪ it only shoots t-shirts ♪

This is a project to store config files, as well as programatically install core packages that I need for development. A lot of this was amassed from many years of quickly looking into a thing™️ , jotting it down, and then just hoping I'd remember why it was there later, so this is now a renewed effort in remembering all the thing™️s.

🚧 Under Construction 🚧

Currently tested on macOS monteray 12.4, but will work on debian soon. Please report 🐛 in the GitHub issues, and I will get them as I have time.

### Under the hood
- Installs `.bashrc`/`.vimrc`/`.zshrc` files, by linking them, not overwriting them
- Installs apt/snap/flatpak packages from `./packages/packages.yml`
- Installs brew files from `./packages/Brewfile_*` depending on OS and if `--work` is passed in
- Installs vim-plug, a vim plugin manager to setup things like nerdtree, indentations lines, and fuzzysearch

I'm using github issues to track future work on this thing.

## Quick Start
Run the setup script to install python dependencies and brew. This will ask for your password, because brew does that. Run the following from your home directory:
```bash
# Download the setup.sh
curl -O https://raw.githubusercontent.com/jessebot/onboardme/main/setup.sh

# give it execute permissions
chmod 0500 ./setup.sh

# run the script, to install dependencies like brew, git, and python
# Also clones the onboardme repo
./setup.sh
```

Now you can run the actual script that does the heavy lifting.
```bash
# if you ran setup.sh, it should have installed this repo into repos/
./repos/onboardme/onboardme.py
```

When it's complete, it'll output a number of other steps to take manually that aren't yet automated.

### Current Ecoscape of Personal Tech

Category | App | Replaces
---|---|---
|Desktop Launcher|Albert?|Alfred|
|Email|Protonmail and Bridge for Linux/MacOS|Gmail|
|Local Backups|Restic to minio|Google Drive, iCloud, S3|
|Photo/file Storage|NextCloud - not tested|Google Photos/Drive|
|News - RSS|Fluent Reader|Facebook/Twitter news company feeds|
|Remote Backups|Restic to b2|Google Drive, iCloud, S3|
|Video Streaming|FreeTube|YouTube|
|Video Streaming|PeerTube - not tested|YouTube|

## Things the scripts don't do
**Every** operating system has that one thing™️ that voids the [Is It Worth the Time](https://xkcd.com/1205/) rule, which leaves us in the weird place, where setting up the thing™️ manually is still faster than trying to keep the automation up to date as every OS changes over time, which is illustrated in the [Automation Chart](https://xkcd.com/1319/). So, I don't know that I'll ever have a perfect solution to map capslock to control in a simple automated manner on every OS, but that's just the systems engineer's mental burden: "I have the ability to do x, but do I really have the time or interest... to do it on windows, mac, linux, and android...?"

*That's where docs come in handy, because you can't even trust that you'll be able to re-web-search anything™️  these days*

You can find the bulk of my notes under the `docs/` directory in this repo, but the goal is to get into some sort of wiki somewhere... soonish. Probably something like a little flask app with some sort of material design and a markdown plugin, because I don't have time for frontend at this stage of my life.

## Important Notes on FOSS and Ethics
Here at this humble OnBoardMe repo, we try really hard to do the right thing. We're doing our best to get off of the giants like Google, Microsoft, Apple, Amazon, Samsung, etc... but we've still got a long way to go! Check back here for alternatives as we go on the journey ourselves! We'll link back to any orgs or projects we learn about, but feel free to open an issue with anything else we should link back to. :)

  Living ethically under late stage capitalism is not easy, but we believe generally that software should be Free and Open Source.

#### What is (FOSS), Free and Open Source Software
We believe in free software, and we do our best to use and support actually free and open source software. If you don't know what we mean, please check out this [GNU article on Free SoftWare](https://www.gnu.org/philosophy/free-sw.en.html).

#### Humane Tech Lists
We've had good luck with [Awesome Humane Tech](https://github.com/humanetech-community/awesome-humane-tech) for guides and checking out alternatives to tech from the Giants you previously used.

### Language
We are currently using the philosophy of:
[Terminology, Power, & Exclusionary Language in Internet-Drafts and RFCs - v09](https://datatracker.ietf.org/doc/html/draft-knodel-terminology-09)

### Tips
Contact your local datacenters and see if they offer an object storage service, because they might, and it could be really cheap. Don't give your money to AWS.
