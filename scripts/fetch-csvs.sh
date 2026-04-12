#!/bin/bash
set -e

# creates temp and target directories
temp_dir=$(mktemp -d)
trap 'rm -rf "$temp_dir"' EXIT
curr_date=$(date +%Y-%m-%d)
mkdir -p ./data/$curr_date

# downloads and unzips data to temp
echo "Unzipping files"
wget -O data.zip "https://raw.githubusercontent.com/joachimvandekerckhove/cogs205b-s26/main/modules/02-version-control/files/data.zip"
unzip -q data.zip -d "$temp_dir"

# filters and moves files with .csv endings
echo "Extracting CSVs"
for file in "$temp_dir"/*.csv; do
    mv "$file" "./data/$curr_date"
done

# cleans up wget file
rm data.zip

# commits and pushes to github
echo "Pushing to GitHub"
git add data scripts/fetch-csvs.sh
git commit -m "update CSVs and script"
git push

echo "Done"