#!/usr/bin/env bash
# enables contribution and non-free apt package manager sources

# append "contrib non-free" to lines that end with "bookworm main"
sed -i 's/bookworm main$/bookworm main contrib non-free/g' /etc/apt/sources.list
