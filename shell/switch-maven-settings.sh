#!/bin/bash

set -e

settings=/Users/liwenhao/.m2/settings.xml
aliyun=/Users/liwenhao/.m2/aliyun.xml
ele=/Users/liwenhao/.m2/ele.xml

if [ -n "$1" ]; then
    if [[ $1 == a* ]]; then
        echo "cp $aliyun $settings"
        cp $aliyun $settings
        elif [[ $1 == e* ]]; then
        echo "cp $ele $settings"
        cp $ele $settings
    else
        echo 'you ipnut wrong vaule'
    fi
else
    echo 'you must ipnut vaule'
fi


