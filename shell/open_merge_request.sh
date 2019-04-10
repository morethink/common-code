#!/usr/bin/env bash
# 打开 merge_requests
# 生成 git repository url
# alias pr=shell/open_merge_request.sh
sentence=$(git remote -v | awk '/fetch/{print $2}' | sed -Ee 's#(git@|git://)#http://#' -e 's@com:@com/@' -e 's%\.git$%%')
# 选择第一个git repository url
for word in $sentence
do
    if [ ! -n "$url" ]
    then
        url=$word
    fi
done
# 打开浏览器merge_requests
open $url/merge_requests/new
