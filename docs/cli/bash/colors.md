---
layout: default
title: Colors in BASH
grand_parent: Command Line Interface
parent: BASH
permalink: /cli/bash/colors
---

# Testing colors with BASH

## `colortest`
The simplest way on Debian based systems is to install colortest:

```bash
sudo apt-get install colortest
```

It provides several commands which you can use, depending on how many colors you want:

```bash
colortest-16   colortest-16b  colortest-256  colortest-8
```

Thanks to this [person on askubuntu.com](https://askubuntu.com/a/396569) for showing me the `colortest-256` command. Really pretty stuff :)

<img src="https://raw.githubusercontent.com/jessebot/onboardme/main/screenshots/terminal_palete.png" width="600">

## Test colors with BASH
If you just want the base terminal colors and all you got is bash, you can try this:
```
bash
echo -e "\033[0mNC (No color)"
echo -e "\033[1;37mWHITE\t\033[0;30mBLACK"
echo -e "\033[0;34mBLUE\t\033[1;34mLIGHT_BLUE"
echo -e "\033[0;32mGREEN\t\033[1;32mLIGHT_GREEN"
echo -e "\033[0;36mCYAN\t\033[1;36mLIGHT_CYAN"
echo -e "\033[0;31mRED\t\033[1;31mLIGHT_RED"
echo -e "\033[0;35mPURPLE\t\033[1;35mLIGHT_PURPLE"
echo -e "\033[0;33mYELLOW\t\033[1;33mLIGHT_YELLOW"
echo -e "\033[1;30mGRAY\t\033[0;37mLIGHT_GRAY"
```
<img src="https://i.stack.imgur.com/i2zcd.png">

# Printing colors with BASH

## `printf` with colors

Here's a quick function I wrote for printf with green colors

```bash
# pretty echo so that I don't have to remember this
function p_echo() {
    # prints with green colors and centered
    green=$(tput setaf 2)
    norm=$(tput sgr0)
    COLUMNS=$(tput cols)
    printf "$green\n%*s\n\n$norm" $(((${#title}+$COLUMNS)/2)) "$1"
}

p_echo "Hi everyone :)"
```

### 'printf` color examples
Thanks to [SiegeX on StackOverflow](https://stackoverflow.com/a/4332530) for all the colors.

```bash
BLACK=$(tput setaf 0)
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
LIME_YELLOW=$(tput setaf 190)
POWDER_BLUE=$(tput setaf 153)
BLUE=$(tput setaf 4)
MAGENTA=$(tput setaf 5)
CYAN=$(tput setaf 6)
WHITE=$(tput setaf 7)
BRIGHT=$(tput bold)
NORMAL=$(tput sgr0)
BLINK=$(tput blink)
REVERSE=$(tput smso)
UNDERLINE=$(tput smul)
```

## `echo -e` with colors

**Example**: Prints love in red:

```bash
RED='\033[0;31m'
NC='\033[0m' # No Color
printf "I ${RED}love${NC} Stack Overflow\n"

# Continued from above example
echo -e "I ${RED}love${NC} Stack Overflow"
```

Learn more about [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code).

- From a stackoverflow [Answer from Tobias](https://stackoverflow.com/a/5947802).

### `echo -e` color examples

```bash
# Reset
Color_Off='\033[0m'       # Text Reset

# Regular Colors
Black='\033[0;30m'        # Black
Red='\033[0;31m'          # Red
Green='\033[0;32m'        # Green
Yellow='\033[0;33m'       # Yellow
Blue='\033[0;34m'         # Blue
Purple='\033[0;35m'       # Purple
Cyan='\033[0;36m'         # Cyan
White='\033[0;37m'        # White

# Bold
BBlack='\033[1;30m'       # Black
BRed='\033[1;31m'         # Red
BGreen='\033[1;32m'       # Green
BYellow='\033[1;33m'      # Yellow
BBlue='\033[1;34m'        # Blue
BPurple='\033[1;35m'      # Purple
BCyan='\033[1;36m'        # Cyan
BWhite='\033[1;37m'       # White

# Underline
UBlack='\033[4;30m'       # Black
URed='\033[4;31m'         # Red
UGreen='\033[4;32m'       # Green
UYellow='\033[4;33m'      # Yellow
UBlue='\033[4;34m'        # Blue
UPurple='\033[4;35m'      # Purple
UCyan='\033[4;36m'        # Cyan
UWhite='\033[4;37m'       # White

# Background
On_Black='\033[40m'       # Black
On_Red='\033[41m'         # Red
On_Green='\033[42m'       # Green
On_Yellow='\033[43m'      # Yellow
On_Blue='\033[44m'        # Blue
On_Purple='\033[45m'      # Purple
On_Cyan='\033[46m'        # Cyan
On_White='\033[47m'       # White

# High Intensity
IBlack='\033[0;90m'       # Black
IRed='\033[0;91m'         # Red
IGreen='\033[0;92m'       # Green
IYellow='\033[0;93m'      # Yellow
IBlue='\033[0;94m'        # Blue
IPurple='\033[0;95m'      # Purple
ICyan='\033[0;96m'        # Cyan
IWhite='\033[0;97m'       # White

# Bold High Intensity
BIBlack='\033[1;90m'      # Black
BIRed='\033[1;91m'        # Red
BIGreen='\033[1;92m'      # Green
BIYellow='\033[1;93m'     # Yellow
BIBlue='\033[1;94m'       # Blue
BIPurple='\033[1;95m'     # Purple
BICyan='\033[1;96m'       # Cyan
BIWhite='\033[1;97m'      # White

# High Intensity backgrounds
On_IBlack='\033[0;100m'   # Black
On_IRed='\033[0;101m'     # Red
On_IGreen='\033[0;102m'   # Green
On_IYellow='\033[0;103m'  # Yellow
On_IBlue='\033[0;104m'    # Blue
On_IPurple='\033[0;105m'  # Purple
On_ICyan='\033[0;106m'    # Cyan
On_IWhite='\033[0;107m'   # White
```
- Also, thanks to this *incredibly long* [stackoverflow answer](https://stackoverflow.com/a/28938235) by Shakiba Moshiri.
