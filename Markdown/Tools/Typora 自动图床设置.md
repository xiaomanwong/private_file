---
title: Typora 设置图床
tag: Tools
category: 开发工具

---

自动图床设置，在我们撰写文档时，会自动将图片保存到图库，并转化 URL 展示出来，最终我们在分享 MD 文档时，避免了本地相对目录，无法引用的情况发生。<!-- more -->

```json
{
  "picBed": {
    "uploader": "github",
    "github": {
      "repo": "xxxxxxx/static_file", // 仓库名，格式时 username/reponame
      "token": "xxxxxxxxxxxx", // github token
      "path": "images/", // 自定义存储路径 如： image/
      "branch": "master" // 分支名，默认是 master
    }
  },
  "picgoPlugins": {}
}
```

1. 首先您要有一个 Github 账号

2. 新建一个仓库

   ![image-20210128140803755](https://raw.githubusercontent.com/xiaomanwong/static_file/master/images/image-20210128140803755.png)

3. 生成一个 token 用于 Picgo 操作您的仓库， 

   * 访问 https://github.com/settings/tokens

   * 然后点击 `Generate new token`

     ![image-20210128141003873](https://raw.githubusercontent.com/xiaomanwong/static_file/master/images/image-20210128141003873.png)

   * 勾选 `repo` 并记录 token

4. 配置 Picgo， 如上 JSON

## Typora 设置如下图

![image-20210128141254331](https://raw.githubusercontent.com/xiaomanwong/static_file/master/images/image-20210128141254331.png)

* 下载或更新：大约 18m 的 Picgo 插件，点击安装即可

* 点击打开配置文件，会出现一个 json 数据，按照 github 的配置，将数据对应的填入

* 点击验证图片上传选项，验证 github 是否连通

  ![image-20210128141827255](https://raw.githubusercontent.com/xiaomanwong/static_file/master/images/image-20210128141827255.png)

## 更多配置

我们也可以配置一些插件，如上 Json 中未开发的部分，具体可参考 [Typora 文件配置](https://picgo.github.io/PicGo-Core-Doc/zh/guide/config.html#%E9%BB%98%E8%AE%A4%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6) 和 [图片上传工具配置](https://support.typora.io/Upload-Image/)



![image-20220314100502209](/Users/admin/Downloads/image-20220314100502209.png)
