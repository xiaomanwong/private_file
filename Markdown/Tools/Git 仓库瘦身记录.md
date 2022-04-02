# Git 仓库瘦身

## 背景

通常情况下，我们使用 git 仓库用来做文件版本管理，避免不了会有大文件的情况。通常情况下，Git 仓库的大小会随着仓库自身迭代增加，当每次我们修改了文件，在进行 commit 时，都会将这些变化打包成一个 object ，存储在 .git 文件夹下，由此我们可以推断出，当我们多次修改一个大的文件时，就会产生一个量的变化，这也就是我们仓库变大的最主要原因。

根据上面的情况，我们同样还可以推测出另外一种情况，就是当我们 commit 一个大文件之后，但是发现这个文件又没什么用，然而它缺很大，即使我们把文件从这个项目中移除掉，它还是会顽固地永远存在于你的提交历史中。

**那么仓库体积臃肿，会造成什么问题呢？**

* git clone 耗时，因为 .git 文件保存着所有的改变，每一次提交记录中有关大文件的改变都会上传到 git 仓库中
* git pull  耗时，因为 .git 文件保存着所有的改变，每一次提交记录中有关大文件的改变都会上传到 git 仓库中
* git push 耗时，因为 .git 文件保存着所有的改变，每一次提交记录中有关大文件的改变都会上传到 git 仓库中
* 磁盘占用过高（仓库和本地）
* 开发效率

综上，仓库臃肿主要影响的就是我们的**时间成本**，时间成本也间接影响我们的效率和成本。

## 解决方案

在版本管理中，有些大文件频繁更新导致仓库本身变的臃肿问题，我们可以通过其他手段来处理。

**方案一：GLF**

glf 是由 git 推出的大文件管理工具，字面意思可能是（git large file），可参照[官方文档](https://git-lfs.github.com/)来了解和使用。

glf 能帮我们结局的是速度问题，以及大文件管理，大文件并不会和我们的仓库融合在一起，而是在一个单独的服务中，glf 管理后，我们 clone 和 pull push等命令的速度 也会有显著提升。

但同样的，虽然 glf 帮我们管理了大文件，但是同样的会在仓库上存在大的文件系统，虽然不会影响仓库大小，但也会变的越来越臃肿，而且我们无从追踪这些大文件的位置。后续使用过程中也有很多坑要爬。

**方案二： Maven**

这套方案可能不适合所有项目，也不一定适合所有文件，在一些特殊的环境中还是能够起到作用。

方案的核心就是将大文件通过 Maven 的方式依赖进来，再通过 Maven 服务器去管理这些大文件。

>  以上两种方案，针对不同的情况，不同的文件，不同的仓库，都适用；比如：如果一些文件无法通过 Maven 的方式进行依赖，那就需要引入 GLF 功能，当然，两种方案也都可以同时存在。具体情况具体分析。

## 实例

但两种方案都需要先将提交记录中的历史大文件追踪记录删除，这样才能达到瘦身的目的，具体步骤如下：

**查看仓库大小命令**：`git count-objects -vH`

![image-20220402102916645](https://raw.githubusercontent.com/xiaomanwong/static_file/master/images/202204021029304.png)

可看到 `size-pack` 有 56G 

接下来我们通过终端，进入到仓库目录

**开始检查大文件，获取仓库记录中排名前五的大文件名称**

 `git rev-list --objects --all | grep "$(git verify-pack -v .git/objects/pack/*.idx | sort -k 3 -n | tail -5 | awk '{print$1}')"`

![image-20220402142444381](https://raw.githubusercontent.com/xiaomanwong/static_file/master/images/202204021424431.png)

**删除大文件**

`git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch "xxxxxxxxxxxxx"' --prune-empty --tag-name-filter cat -- --all`

输入命令后，会展示一个警告，可以忽略，过一会会出现统计数据，如下

![image-20220402142534976](https://raw.githubusercontent.com/xiaomanwong/static_file/master/images/202204021425002.png)

**删除缓存下来的ref和git操作记录**

`git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin && git reflog expire --expire=now --all`

**垃圾回收**

`git gc --prune=now`

**推送到远端**

这里需要注意，在公司内部有很多都是使用 gitLab，有些公司会对文件上传有大小限制，这就会导致如果我们单次上传的文件整体还是很大，就依然无法上传上去，需要联系相关运维同学修改一下配置。

``` shell 
git push origin --force --all
git push origin --force --tags
```

**避坑指南**

1. 在代码仓库中有一些分支是被保护的，测试后，发现只有 Owner 权限的人可以通过 `--force` 命令将更新提交上去。如果没有，就只能通过新建仓库的方式推送到远程。

2. 即使通过 `--force` 命令将代码强推送到远程，但实际上仓库大小也并没有改变，反倒是增加。所以还是新建一个仓库重新上传。

   ```shell
   git remote set-url origin https://git.github.com/username/new.git
   git push origin --force --all
   git push origin --force --tags
   ```

3. 仓库迁移过程中，我要了仓库的限制

   1. 仓库大小限制：仓库有时会限制单次提交到仓库时单个文件的大小限制，具体的限制每个公司、每个环境都不相同，如果瘦身后，上传到仓库失败时，可与仓库管理员沟通修改限制

   2. commit 信息限制：Git 提交规范是没加公司都会做的事情，会过滤提交者的邮箱，用户名，也会过滤 commit message 是否符合规范，如果仓库中有不规范的提交，可通过仓库配置白名单的方式，先全量提交上去。

      那后续我们还是要规范一下 git 提交规范，这里推荐一个插件和具体的修改方案：

      ```shell 
      # 本地用户信息配置, 配置要符合具体的规范
      # 配置全局
      git config --global user.name="xxxxx"
      git config --global user.email="xxxxx@xxx.com"
      
      # 配置当前工程
      git config --local user.name="xxxxx"
      git config --local user.email="xxxx@xxx.com"
      ```

      用户名和邮箱配置完成后，我们需要配置一下 `commit message` 模版，

      **Android Studio：** Git Commit Template，下载插件

      **SourceTree：** 使用 .gitmessage ,配置命令： `git config --global commit.template ~/.gitmessage`

      ``` tex
      # GIT COMMIT MESSAGE FORMAT
      #
      # <type>(<scope>): <subject>
      # <BLANK LINE>
      # <body>
      # <BLANK LINE>
      # <footer>
      #
      # head
      # - type: feat, fix, docs, style, refactor, perf, test, chore, revert
      # - scope: scope of this change, can be empty
      # - subject: start with verb (such as 'change'), 50-character line
      #
      # body: 72-character wrapped. This should answer:
      # * Why was this change necessary?
      # * How does it address the problem?
      # * Are there any side effects?
      #
      # footer:
      # - Include a link to the bug, if any.
      # - BREAKING CHANGE
      #
      ```

      

      

如果上传过程中遇到 413 问题，修改本地 git 配置如下

`git 配置上传超时和最大上传的网络缓存
git config --global http.lowSpeedLimit 0
git config --global http.lowSpeedTime 999999
git config --global http.postBuffer 52428800000`

**附赠自动化脚本：**

```shell
set -x
echo '准备开始 Checkout 出所有分支代码'
start_time=$(date "+%Y%m%d%H%M%S")$((`date +%N`/1000000))
git fetch --all
all_branchs=`git branch -a`
# for branch in ${all_branchs[@]};
for branch in $all_branchs;
do
    branch_simple_name=`echo $branch | grep '/' | cut -d '/' -f3 -f4`
    # branch_simple_name=$branch

    # master 分支除外
    #&& "master" != "$branch_simple_name" 
    echo $branch_simple_name 
    if [[ "" !=  "$branch_simple_name"
            && "HEAD" != "$branch_simple_name" 
            ]]; then
        echo "branch_simple_name is  $branch_simple_name, $branch --->> " $branch_simple_name;
        git reset --hard
        git checkout $branch_simple_name || exit 1
        git pull --rebase origin $branch_simple_name || exit 1


        # cherry-pick
        # git checkout $branch_simple_name || exit 1
        # git pull --rebase origin $branch_simple_name || exit 1

        # git cherry-pick 5f561c4fd2ec68a1088615d60b222a4704938df7
        # git commit -m "update: cherry-pick from 5f561c4fd2ec68a1088615d60b222a4704938df7"
        # git push origin $branch_simple_name || exit 1

    fi;
done;
echo '开始执行脚本，删除大文件'
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch "xxxxxxxxxxxx"' --prune-empty --tag-name-filter cat -- --all
echo '删除引用'
git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin && git reflog expire --expire=now --all
echo '开始清理'
git gc --prune=now
echo '准备推送到远程'
git remote set-url origin https://git.github.com/username/xxxxxxxxxx.git
git push origin --force --all
git push origin --force --tags
git gc --prune=now
git count-objects -vH
end_time=$(date "+%Y%m%d%H%M%S")$((`date +%N`/1000000))
declare -i interval=$end_time-$start_time
declare -i interval=$interval/10
echo $interval
```
