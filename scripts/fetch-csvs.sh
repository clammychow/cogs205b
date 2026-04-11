#!/bin/bash
set -e

# creates temp and target directories
mkdir -p /tmp/extract
curr_date=$(date +%Y-%m-%d)
mkdir -p ./data/$curr_date

# downloads and unzips data to temp
echo "unzipping files"
wget -O data.zip "https://raw.githubusercontent.com/joachimvandekerckhove/cogs205b-s26/main/modules/02-version-control/files/data.zip"
unzip -q data.zip -d /tmp/extract

# filters and moves files with .csv endings
echo "extracting csvs"
for file in /tmp/extract/*.csv; do
    mv "$file" "./data/$curr_date"
done

# clears temp directory and wget file
rm -r /tmp/extract
rm data.zip
echo "done"