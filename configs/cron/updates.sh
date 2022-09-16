#!/bin/bash -
#===============================================================================
#
#          FILE: updates.sh
#
#         USAGE: ./updates.sh
#
#   DESCRIPTION: Run updates for packages managers and various programs.
#                Currently Supported programs: tldr
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#         NOTES: ---
#        AUTHOR: @jessebot 
#       CREATED: 09/16/2022 12:31:37 PM
#      REVISION: v0.0.1
#===============================================================================

set -o nounset                                  # Treat unset variables as an error

# update my tldr data (cli tool for cheatsheets)
tldr --update
