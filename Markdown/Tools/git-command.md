---
title: git command
date: 2019-04-16 17:43:58
tags: Git
category: 开发工具
---

# Git 命令



## Git 文件的三种状态

1. 已提交：表示该文件已经被安全地保存在本地版本库中，执行过git commit。
2. 已修改：表示修改了某个文件，但还没有提交保存
3. 已暂存：表示把已修改的文件房子啊下次提交时要保存的清单中，也就是执行了 git add 命令。

<!--more-->

## 远程仓库与本地代码的配置

我们在 github 上创建一个新的仓库时，github 都会给我们一些基础命令，让我们可以将本地已经有的项目上传到远程空仓库中。

如果您不会使用 git 命令，那么可能会比较惨，有时通过工具将本地非空的目录，和 github 上的仓库建立连接还是很麻烦的，相对命令行是最简单的。我们只需要按照 github 上给我们的命令行提示，一行一行敲就可以。

``` git
cd <project path>
git init
git remote add origin <远程仓库地址>
git add .
git commit -m '提交日志'
git push -u origin master
```

## Git 基本配置

配置个人的用户名称和电子邮件地址，每次提交时，都会引用这两条信息，以用来说明是谁提交的更新。


使用 `--global` 选项，更改的未用户主目录下的配置，如果想在某个特定的项目中使用其他的名称和邮件，只需要去掉 `--global` 选项重新配置，新的配置位于当前项目的 `.git/config` 文件中。

```git
 git config --global user.name ''yourname''
 git config --global user.email  yourname@gmail.com
```

### 常用操作

#### 初始化

`git init` ，通过此命令会在当前目录创建一个`.git`的隐藏目录，这是`git`的第一步。

* **克隆代码**

     ```cmake
    #拉取远程仓库代码,此项目并不一定是你所创建
    #例如： `git clone git@github.com:bboyfeiyu/AndroidEventBus.git`
    #执行完成后，会在本地当前目录创建一个AndroidEventBus的目录来存放仓库代码
    git clone <远程仓库地址>
    ```

* 查看本地代码状态

    ``` cmake
    # 是最为常用的命令之一，用于检查本地项目的状态.仔细阅读红色/绿色部分，
    # 可以获得相关文件的操作信息，根据提示，判断是执行`git commit` 还是执行`git add` 操作。
    git status 
    ```

* 同步远端分支变化

    ```cmake
    # 拉取指定分支的变化
    git fetch origin master
    # 拉取所有分支变化
    git fetch
    # 拉取所有分支的变化，并将远端不存在的分支从本地同步移除
    git fetch -p
    ```

* 同步远端代码变化

  ```cmake
  # 都会先执行 git fetch， 然后执行合并操作
  # 不同的是 git pull  执行的是 git merge, git pull -r  执行的是 git rebase
  git pull origin master
  git pull -r origin master
  ```
  
* 仓库状态 

    ```cmake
    # 查看远程仓库信息
    git remote -v
    
    > origin git@github.com:username/repository.git (fetch)
    > origin git@github.com:username/repository.git (push)
    
    # 将本地已经 init 过的工程链接到远程的空仓库中，以此来完成远程版本库的创建
    # 链接远程版本库
    git remote add origin <远程地址>
    # 切换远程仓库地址：
    git remote set-url <仓库地址>
    ```

    SSH 和 HTTPS 方式切换

    ```cmake
    # ssh to https
    $ git remote set-url origin https://github.com/USERNAME/repository.git
    # https to ssh
    $ git remote set-url origin git@github.com:USERNAME/repository.git
    ```

    SSH 和 HTTPS 的区别：

    使用 SSH 方式需要在本地配置一个密钥，具体可参见[多个 SSH 公钥提交代码到不同平台](https://xiaoman.ren/2019/04/17/%E5%A4%9A%E4%B8%AA-ssh-%E5%85%AC%E9%92%A5%E6%8F%90%E4%BA%A4%E4%BB%A3%E7%A0%81%E5%88%B0%E4%B8%8D%E5%90%8C%E5%B9%B3%E5%8F%B0/)中介绍；
    而使用 HTTPS 的方式操作简单，弊端是需要经常输入密码。

#### Commit 操作

每一次 commit 操作，都是一次完整的代码状态的记录，会生成一个 `commit ID`  作为唯一标识记录。

* 新增 commit 记录

  ```cmake
  # 添加文件到缓冲器，然后提交到本地仓库
  # add file 添加暂存区中的单个文件，多个文件可以后续追加文件名
  # add . 将暂存区的全部文件都添加到缓冲区
  git add file
  git add .
  # commit -m 将已添加到缓冲区的文件，提交到本地仓库
  # commit -a -m 将本地全部文件添加到缓冲区，并提交到本地
  git commit -m "备注信息"
  git commit -a -m "备注信息"
  ```

* 撤销 commit


  ```cmake
  # 会将提交记录回滚，代码不回滚
  git reset b15b3b52
  # 会将提交记录和代码全部回滚
  git reset --hard b1535351
  # 将部分代码文件回滚
  git checkout --files
  ```

* 合并 commit

  合并 commit ，本质上合并两份不同状态下的代码

  ```cmake
  # git 提供了两种合并 commit 的方法
  git merge master
  git rebase master
  ```

  那么 `git rebase` 和  `git merge` 的区别是什么呢？ `merge`  是将两个分支处理冲突后，新增一个 `commit` 追加到 `master` 上。 `rebase` 是将新特性分支上的 `commit` 记录追加到目标分支上，这个时候，他的 commit 其实已经发生了变化。

  ![rebase 和 merge 的区别](https://raw.githubusercontent.com/xiaomanwong/static_file/master/images/v2-d77a94abbae73c7709014167afd4603c_720w.jpg)

  相对来说，merge 处理冲突更直接， rebase 能够保证清晰的 commit 记录。

  合并时，通常会发生冲突，。可以全局搜索特殊字符如 `<<<<<` 找到需要处理的代码位置，然后认真分析应该保留哪一部分代码。

* 移除文件追踪

  ```cmake
  # 将 add 过后的文件从追踪列表中移除，只是逻辑删除（从版本库中移除），并不会将本地文件删除
  git rm --cached  <file>
  ```

#### 分支操作

所谓的分支操作其实就是一个指向 commitID 的指针，可以在 `.git/refs/heads` 中查看

通常情况下，分支要至少能够明确的标记出其功能和作用，便于查找。

分支是用来管理代码版本、类型的有效工具，可根据不同的服务对象、不同的上线版本等等，来做代码分离，版本管理操作

* 查看分支

  ```cmake
  # 列出本地仓库的全部分支信息
  git branch
  # 列出本地和远程的全部分支
  git branch -a
  # 查看带提交信息的分支信息
  git branch -v
  ```

* 创建分支

  ```cmake
  # 新建本地分支
  git branch <分支名称>
  # 切换分支
  git checkout <分支名称>
  # 创建并切换本地分支
  git checkout -b <分支名称>
  # 新增远端分支，前提是创建好本地分支，然后推送到远程, -u 表示本地分支和远端分支关联，不然后续的 push 和 pull 以及 fetch 操作不够灵活
  git push -u origin/feature
  ```

* 删除分支

  ```cmake
  # 删除本地分支,如果本地有未合并的代码，则不能删除
  git branch -d <分支名称>
  # 强制删除
  git branch -D <分支名称>
  # 删除远端分支
  git push origin :<分支名称>
  ```

* 代码推送

  ```cmake
  # 推送本地修改到远端服务器
  git push
  # 推送到指定分支
  git push origin master
  # 有时因两个独立的历史，会导致推送无法达成， 通常在 git pull 时会提示 `fatal: refusing to merge unrelated histories 
  # 绝合并无关历史，时可是使用下面的命令来解决
  # 一般无法达成推送时，git 都会给出相应的解决方案，按照命令行的提示追一执行命令即可
  git pull origin master --allow-unrelated-histories 
  ```

#### 日志信息

提交日志是每当我们创建一个新的 commitID 时要必须填写的内容，清晰的标记着我们这一次提交，都修改了什么内容，方便日后查找和团队的协作。

```cmake
# 查看历史提交记录， 包括**提交人**、**时间**、**信息**、**信息指纹**等.
git log
# 单行展示记录： 
git log --pretty=oneline
#展示全部信息： 
git log --pretty=fuller
```

#### Tag 标签

Tag 在协作开发中起着不可磨灭的作用，使用 tag 来记录某一次的 commitID, 标记某一个里程碑，对代码的版本管理效果非常明显

* 查看 Tag 标签

  ```cmake
  # 查看全部 tag 标签
  git tag
  # 模糊查询 tag 标签,-l 是 like ， * 表示模糊的位置
  git tag -l 'v1.5.*'
  # 查看 tag 标签的备注信息
  git tag -ln
  # 查看标签信息
  git show <tag 名称>
  ```

* 创建 Tag

  ```cmake
  # 创建本地 Tag
  git tag -a <标签名> -m <标签备注信息>
  # 将本地 tag 推送到远程仓库
  git push origin <标签名>
  # 将本地全部 tag 随送到远程服务器
  git push origin -tags
  ```

* 删除Tag

  ```cmake
  # 删除本地 Tag
  git tag -d <标签名>
  # 删除远程 Tag
  git push origin :refs/tags/<标签名>
  ```

### 使用中的一些技巧

* 命名别名

  复杂并超长的命令，可以通过起别名的方式方便在终端中书协

  ```cmake
  git config --global alias.ci commit
  git config --global alias.ck checkout
  git config --global alias.st status
  ```

  然后就可以很愉快的使用git命令了

  ```cmake
  git st
  git ci -m "commit message"
  ```

* fork 项目更新

  ```cmake
  git remote -v
  # fork 主项目地址
  git remote add upstream git@github.com:XXX/XXX.git 
  # 将主项目地址同步到本地
  git fetch upstream
  # 合并并推送
  git merge upstream/master
  git push
  ```

* revert，reset，rebase 的区别

  首先，他们都是操作 commitID 的命令，但作用不一样。 reset 和 rever 对某一次 commitId 操作， rebase 是用来做分支合并(merge)的。

  * git revert: 放弃某次提交

    git revert 之前的提交仍会保留在 git log 中，而此次撤销会作为一次新的提交

  * git reset

    回滚到某次提交 

    * git reset –soft

      此次提交之后的修改会被退回到暂存区

    * git reset –hard

      此次提交之后的修改不做任何保留， git status 干净的工作区

  * git rebase

    当两个分支不在一条线上，需要执行 merge 操作时，使用的命令

    执行命令时，很容易显示 **merge 失败**，使用 `git diff` 查看冲突内容，并手动修改冲突，执行 `git add filename` 以表示解决冲突，再执行 `git rebase --continue` 继续执行 rebase。

  