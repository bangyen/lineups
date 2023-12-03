#!/bin/bash

list=(data/*)
file=${list[0]}

if [[ $file == *\.html ]]; then
    echo "Current file: $file"
    python3 -m collect "$file"
    mv "$file" "data/done"

    echo "Creating backup_$num.zlib"
    num=$(($(ls -1 backup | wc -l) + 1))
    cp json.zlib backup/backup_$num.zlib
fi

