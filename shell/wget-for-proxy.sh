#!/bin/bash

set -e
# 通过 wget 代理下载
url=$1
proxy=127.0.0.1:1087


if [[ $url == https* ]];
then
basename $(dirname $url)
wget --no-check-certificate basename $(dirname $url) -e use_proxy=yes -e https_proxy=$proxy $url
else
wget -e use_proxy=yes -e http_proxy=$proxy $url
fi



