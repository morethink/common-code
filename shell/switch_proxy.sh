#!/bin/bash

set -e

if [ -n "$1" ]; then
    if [[ $1 == off* ]]; then
        echo dd
        sed -i '' 's?export http_proxy=\"http://127.0.0.1:7877\"?#export http_proxy=\"http://127.0.0.1:7877\"?' ~/.bash_profile
        sed -i '' 's?export https_proxy=\"http://127.0.0.1:7877\"?#export https_proxy=\"http://127.0.0.1:7877\"?' ~/.bash_profile
        elif [[ $1 == on* ]]; then
        sed -i '' 's?#export http_proxy=\"http://127.0.0.1:7877\"?export http_proxy=\"http://127.0.0.1:7877\"?' ~/.bash_profile
        sed -i '' 's?#export https_proxy=\"http://127.0.0.1:7877\"?export https_proxy=\"http://127.0.0.1:7877\"?' ~/.bash_profile
    else
        echo 'you ipnut wrong vaule'
    fi
    echo '$http_proxy='"$http_proxy"
else
    echo 'you must ipnut vaule'
fi


