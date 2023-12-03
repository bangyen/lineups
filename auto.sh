#!/bin/bash

list=(data/*)
file=${list[0]}

if [[ $file == *\.html ]]; then
    echo "=== Current file: $file ==="
    python3 -m src.collect "$file"

    if [ $? -eq 0 ]; then
        num=$(($(ls -1 backup | wc -l) + 1))
        echo "=== Creating backup_$num.zlib ==="

        cp json.zlib backup/backup_$num.zlib
        mv "$file" "data/done"
    fi
else
    echo "=== Invalid file: $file ==="
fi

