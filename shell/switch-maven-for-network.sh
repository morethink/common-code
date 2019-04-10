#!/bin/bash

set -ex

settings=~/.m2/settings.xml
aliyun=~/.m2/aliyun.xml
ele=~/.m2/ele.xml

for element in `ifconfig |grep 'inet '|awk {'print $2'}|grep -v '127.0.0.1'|cut -d: -f2`
do
    if [[ $element == 192* ]]; then
        echo "cp $aliyun $settings"
        cp $aliyun $settings
        elif [[ $element == 30* ]]; then
        echo "cp $ele $settings"
        cp $ele $settings
    fi
done


