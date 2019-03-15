#! /bin/bash
cd /Users/liwenhao/Desktop/github/programming
set -e
print()
{
    echo  "\033[43;37m$1\033[0m"
}
if [ ! -n "$1" ]; then
   message=$(date '+%Y%m%d %H%M%S')
   echo "you don't ipnut git commit message,so the message is $message"
 else
   message="$1"
fi
book sm -i node_modules,_book
gitbook build && git add . && git commit -m "$message" && git push -f origin master && print "gitbook push success-----------" || print "gitbook push fail----------"
