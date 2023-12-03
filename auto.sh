#!/bin/bash

list=(data/*)
file=${list[0]}

if [[ $file == *\.html ]]; then
    echo "=== Current file: $file ==="
    python3 -m src.collect "$file"
    mv "$file" "data/done"

    num=$(($(ls -1 backup | wc -l) + 1))
    cp json.zlib backup/backup_$num.zlib
    echo "=== Created backup_$num.zlib ==="
fi

