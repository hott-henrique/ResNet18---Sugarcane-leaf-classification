#!/bin/bash

for d in ".data/Dataset/Diseases" ".data/Dataset/Dried Leaves" ".data/Dataset/Healthy Leaves"; do
    if [ "$d" == ".data/Dataset/Diseases" ]; then
        for sub in "$d"/*/; do
            echo -n "$sub: "
            find "$sub" -maxdepth 1 -type f | wc -l
        done
    else
        echo -n "$d: "
        find "$d" -maxdepth 1 -type f | wc -l
    fi
done
