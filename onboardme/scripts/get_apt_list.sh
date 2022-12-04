#!/bin/bash

# list apt packages by only their short name
apt list --installed | cut -d '/' -f 1
