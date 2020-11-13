#!/bin/bash
if [ -z "$1" ]; then
    echo "usage: $0 path/to/download/folder";
    exit 0;
fi

if [ -d $(pwd)/"downloads" ]; then
    echo "downloads folder exists, do you want to re-create it?"
    read -p "All its content will be overridden (y/n)" -n 1 -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf downloads
    fi
fi

ln -s "$1" $(pwd)/downloads;