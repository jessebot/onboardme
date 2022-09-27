#!/bin/bash -
#===============================================================================
#
#          FILE: updates.sh
#
#         USAGE: ./updates.sh
#
#   DESCRIPTION: Run updates for packages managers and various programs.
#                Currently Supported programs: tldr, brew
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#         NOTES: ---
#        AUTHOR: @jessebot 
#       CREATED: 09/16/2022 12:31:37 PM
# LAST_MODIFIED: 2022-09-27 07:24:04.0 +0000
#===============================================================================

set -o nounset                                  # Treat unset variables as an error

# update my tldr data (cli tool for cheatsheets)
tldr --update

# update brew cache and installer
brew update
# upgrade all brew packages every evening
brew upgrade
