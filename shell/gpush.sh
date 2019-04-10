#!/bin/bash
set -e
print()
{
    echo  "\033[43;37m$1\033[0m"
}
message=$1
if [ ! -n "$1" ]
then
    read -p "please input git commit message:" message
fi
print "git commit message is $message"

git add .
git commit -m "$message"
git push
print "git push success"
