#!/bin/bash

set -e

history="~/Library/Application\ Support/Google/Chrome/Default/History"
dir=~/Desktop/sync
target=$dir"/History"
if [ -e $target ]; then
    size=`ls -l $target | awk '{print $5}'`
    old_size=`eval ls -l $history | awk '{print $5}'`
    # echo ${{old_size}} -ge ${{size}}
    if [ $old_size -ge $size ]; then
        eval cp $history $dir
    fi
fi


