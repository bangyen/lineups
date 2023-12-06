#!/bin/bash

for file in data/*.html; do
    echo "=== Current file: $file ==="
    python3 -m scripts.main "$file"

    if [ $? -eq 0 ]; then
        num=$(($(ls -1 backup | wc -l) + 1))
        echo "=== Creating backup_$num.zlib ==="

        cp scripts/json.zlib backup/backup_$num.zlib
        mv "$file" "data/done"
        exit 0
    else
        exit 1
    fi
done
