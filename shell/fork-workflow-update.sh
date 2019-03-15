print()
{
    echo  "\033[1;33m$1   \033[0m"
}
update()
{
    cd $1
    git remote add upstream $2
    print "添加远程分支成功，远程分支列表:"
    git remote -v
    print "fetch 源分支的新版本到本地"
    git fetch upstream
    print "切换到本地master分支"
    git checkout master
    print "合并 origin 和 upstream 两个版本 master 分支的代码"
    git merge upstream/master
    print "切换到本地develop分支"
    git checkout develop
    print "合并 origin 和 upstream 两个版本 develop 分支的代码"
    git merge upstream/develop
    print "删除远程分支"
    git remote remove upstream
}
dir=(
    /Users/liwenhao/Desktop/IDEAProject/cps
    /Users/liwenhao/Desktop/IDEAProject/eship
)
upstream=(
    git@git.elenet.me:testinfra/cps.git
    git@git.elenet.me:testinfra/eship.git
)

for((i=0;i<${#dir[*]};i++));
do
    # 更新代码
    echo "\033[43;37mpull code from ${upstream[$i]}\033[0m"
    update ${dir[$i]} ${upstream[$i]}
done



