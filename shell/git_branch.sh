# Mac系统在终端下查看分支
# vi /etc/profile 
# alias git_branch="bash /Users/liwenhao/Desktop/github/script/git_branch.sh"
# export PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;36m\]\W$(git_branch)\[\033[00m\]\$ '
# . /etc/profile
branch="`git branch 2>/dev/null | grep "^\*" | sed -e "s/^\*\ //"`"
if [ "${branch}" != "" ];then
    if [ "${branch}" = "(no branch)" ];then
        branch="(`git rev-parse --short HEAD`...)"
    fi
    echo " ($branch)"
fi
