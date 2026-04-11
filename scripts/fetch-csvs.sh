#!/bin/bash
set -e

# creates temp and target directories
temp_dir=$(mktemp -d)
curr_date=$(date +%Y-%m-%d)
mkdir -p ./data/$curr_date

# downloads and unzips data to temp
echo "unzipping files"
wget -O data.zip "https://raw.githubusercontent.com/joachimvandekerckhove/cogs205b-s26/main/modules/02-version-control/files/data.zip"
unzip -q data.zip -d "$temp_dir"

# filters and moves files with .csv endings
echo "extracting csvs"
for file in "$temp_dir"/*.csv; do
    mv "$file" "./data/$curr_date"
done

# cleans up temp directory and wget file
rm -rf "$temp_dir"
rm data.zip
echo "done"