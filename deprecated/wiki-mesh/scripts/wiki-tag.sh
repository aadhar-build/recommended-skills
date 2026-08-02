#!/bin/bash
# wiki-tag project_name file_path
if [ "$#" -ne 2 ]; then
    echo "Usage: wiki-tag <project_name> <file_path>"
    exit 1
fi

PROJECT=$1
FILE=$2

if [ ! -f "$FILE" ]; then
    echo "Error: File $FILE not found."
    exit 1
fi

echo -e "\n#wiki-target: [[$PROJECT]]" >> "$FILE"
echo "Tagged $FILE for project $PROJECT."
