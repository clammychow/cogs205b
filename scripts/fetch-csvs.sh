#!/bin/bash

# creates temporary directory
mkdir -p /tmp/extract

# downloads and unzips data to temp
echo "unzipping files"
wget -0 data.zip https://github.com/joachimvandekerckhove/cogs205b-s26/raw/9dca64e57fd88213f2422c19a8b10953a8fbfdbe/modules/02-version-control/files/data.zip
unzip -q data.zip -d /tmp/extract