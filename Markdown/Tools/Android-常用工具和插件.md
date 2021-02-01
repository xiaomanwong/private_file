---
title: Android 常用工具和插件
date: 2020-02-20 17:04:13
tags: Tools
category: 开发工具
---
# Android 开发必备插件和工具

## Android Studio 插件



| 插件名  | 注释 |
| --- | --- |
| Alibaba Java Coding Guidelines | 阿里的代码规范检查插件，用来检查代码中是否符合驼峰命名、if else, switch els default 等语法糖的健壮性；以及单方法行数不超过 80 行，提醒”单一职责原则“等； |
| Android Parcelable code generator | 序列化 Po 类时，可以快速生成序列化代码 |
| CodeGlance | 代码预览图，在编辑窗口右侧有一个当前代码的缩略图，可以当做滚动条使用，可以快速定位代码 |
| DataBase Navigator | 支持 Oracle、MySQL、SQLite、PostgreSQL 以及任何符合 JDBC 的数据库；增强我们对数据库数据的读取，定位问题 |
| FindBugs-IDEA | 可以分析现存代码中容易引起异常的部分，并提供修改建议|
| GsonFormater |将 xml 和 json 转换位 pojo 类，可以快速生成数据源 |
| Markdown |    语言工具，通过语法糖，可以快速生成 HTML 的预览窗，写出 GitHub 风格的技术文档|
| Markdown Navigator | Markdown 预览工具，可以观察实时渲染的 HTML 文档 |
| Android Resource Tools | 1. 可以为 layout.xml 中 带 id 的 View 生成变量及 findViewById 代码</br>2. 使用 Google 对 strings.xml 进行翻译（需要配置镜像）    </br>3. 颜色渲染器支持 RGB 和 ARGB，方便配置透明度|
| Codota | 模版代码查找器，可以输入关键词，搜索出相关的业务代码，比如，搜索 FileOutputSrteam 则会有     以及在编译时，会给予相关的代码块提示 |
| GoodFormatter | 保证大家代码格式化风格一致，避免因不同，导致 git 合并是出现大量修改； |
| ButterknifePlugin |   快速生成 butternkife 的注入代码，前提需要引入 butterknife |
| JsonViewer | 可以替换 postman 的插件，用来调试接口 |
|Git Commit Template|Git 提交记录模版工具|
|Sql Android |数据库查询插件，有了 Jetpack 后，room 数据库被广泛应用，此时这个工具，就显得很方便|
| --- | --- |
<!--more-->


**codata**

``` java    
    public void zipFile(File srcFile, File zipFile) throws IOException {
        try (FileInputStream fis = new FileInputStream(srcFile);
            ZipOutputStream zos = new ZipOutputStream(new FileOutputStream(zipFile))) {
          zos.putNextEntry(new ZipEntry(srcFile.getName()));
          int len;
          byte[] buffer = new byte[1024];
          while ((len = fis.read(buffer)) > 0) {
            zos.write(buffer, 0, len);
          }
          zos.closeEntry();
        }
    }   
```

**AndroidResourceTools**
![](https://github.com/xiaomanwong/static_file/blob/master/images/android_resource_tool_variables.png?raw=true)

![](https://github.com/xiaomanwong/static_file/blob/master/images/android_resource_tools_code.png?raw=true)


 **JsonViewer**

 ![](https://github.com/xiaomanwong/static_file/blob/master/images/WX20200220-145420.png?raw=true)

## 开发工具

除必要 AS 之外，需要以下工具, Mac 用户可以通过 [XClient](https://xclient.info/) 下载破解版软件

| 工具 | 注释 |
| --- | --- |
|Sublime Text 3|文本编辑器，除正常的编辑功能外，丰富的插件库让它比 editplus、plus++等文本编辑更强大；<br>**PrettyJson** 插件可以快速将字符串格式化为 JSON 格式，无需再去在线找 json 格式化；也可以校验 json 的合法性；<br>支持列编辑，快速修改<br> **Markdown** 可以用来写 Markdown 文件，但不支持渲染<br>[Sublime Text 3 下载地址](https://www.sublimetext.com/3)|
|Postman| 接口调试工具，也可以用上面推荐的 **JsonViewer**<br>[Postman 下载地址](https://www.postman.com/)|
|Fiddler、Charles| 抓包调试工具，可抓包，修改参数调试接口，任选<br>[Fiddler 下载地址](https://www.telerik.com/fiddler)<br>[Charles 下载地址](https://www.charlesproxy.com/download/)|
|Markdown|Windows 可使用 Typora, Mac 可以使用 MWeb Pro，生成技术类文档使用，马克飞象双平台都可以（Chrome 插件，需要友好访问）<br>[Typora 下载地址](https://typora.io/)<br>[MWeb Pro 下载地址](https://www.mweb.im/)|
|Vysor|Android 设备同屏工具，可将设备同步到电脑上，方便截图，分享屏幕等，需要友好访问<br>[Vysor 下载地址](https://www.vysor.io/)|
|XMind|脑图工具，用来写结构<br>[XMind 下载地址](https://setapp.com/apps/xmind?campaign=setapp_search_vendor_xmind_abn_brand_en&ci=737183467&adgroupid=41332915427&adpos=1t1&ck=xminds&targetid=kwd-642237838482&match=p&gnetwork=g&creative=204109085004&placement=&placecat=&accname=setapp&gclid=Cj0KCQiA-bjyBRCcARIsAFboWg0rXap6WScthL_2Ft6oHTKmQorcfJduEcko1hDR0byUxsdFGubEsBQaAotvEALw_wcB)|
|Beyond Compare|文件比较器，比较两组文件的差异<br>[BeyondCompare 下载地址](https://www.scootersoftware.com/download.php)|
|Dash| 源码查看器， 也可以使用在线的 [Android 社区](http://androidos.net.cn/sourcecode)|
|PxCook|云协作设计工具，可生成相应的前端代码，自动测量尺寸等，支持 Photoshop、Sketch、Adobe XD。[PxCook 下载地址](https://www.fancynode.com.cn/pxcook)|
|---|---|

