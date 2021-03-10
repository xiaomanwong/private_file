---
title: WebView 性能篇
tag: WebView
category: Android
---

## **问题**：

### **为什么** **WebView 的加载速度那么慢?**

1. js 解析效率

   如果 js 文件较多、解析比较复杂，就会导致渲染速度较慢。或者手机硬件性能比较差的花，也会导致渲染速度比较慢

2. 页面资源的下载

   一般加载一个 H5 页面，都会产生比较多的 **串行** 网络请求，如图片、js 文件、css 文件等，需要将这些资源都下载完成之后才能完成渲染，这样也会导致页面渲染速度变慢
   
3. 耗费流量

   每次 H5 页面加载时，都需要重新加载 Android WebView 的 H5 页面，每加载一个页面，就会产生很多请求，导致同一个页面被加载多次



<!-- more -->

### **那如何解决呢？**

*  前端H5 缓存机制（WebView 自带）
* 资源预加载
* 资源拦截

#### 前端 H5 缓存机制

**定义：** 缓存、离线存储

* 意味着 H5 网页加载后会存储在缓存区域，在无网络情况下也可以访问
* WebView 的本质时在 Android 中嵌入 H5 页面，所以 Android  WebView 自带的缓存机制就是 H5 页面的缓存机制
* Android WebView 除了新的 file_system 缓存机制还不支持，其他的都支持

**作用：**

* 离线浏览：用户可以在没有网络时，访问 H5 页面
* 提高页面加载速度 & 减少流量消耗：直接使用已缓存的资源，不需要重新请求和加载

**应用：**

* 缓存机制：如何将加载过的网页数据保存到本地（保存）
* 缓存模式：加载网页时如何读取之前保存到本地的网页缓存（读取）

##### 缓存机制

Android WebView 自带的缓存机制有 5 种：

1. 浏览器缓存机制
2. Application Cache 缓存机制
3. Dom Storage 缓存机制
4. Web Sql Database 缓存机制
5. Indexed Database 缓存机制
6. File System 缓存机制（H5 页面新加入的缓存机制）

##### 浏览器缓存机制

**原理：**根据 HTTP 协议头里的 `cache-control` 或 `Expires` 和 `Last-Modified` 和 `Etag` 等字段来控制文件缓存的机制

1. `Cache-Control` 用于控制文件在本地缓存有效时长
   如服务器返回 `Cache-Control:max-age=600`，则表示文件在本地应该缓存，且有效时长是  600s。在接下来的 600s 内，如果有请求这个资源，浏览器不会发出 HTTP 请求，而是直接使用本地缓存的文件

2. `Expires`: 与 `Cache-Control` 功能相同，即控制缓存的有效时间

   1. Expires 是 Http 1.0 标准中的字段， Cache-Control 是 Http 1.1 中新增字段
   2. 当这两个同时出现时， Cache-Control 优先级高

3. `Last-Modified` 标识文件在服务器上的最新更新时间
   下次请求时，如果文件缓存过期，浏览器通过 `If-Modified-Since` 字段带上这个时间，发送给服务器，由服务器比较时间戳来判断文件是否有修改。如果没有修改，服务器返回 304 告诉前端继续使用缓存；如果有修改，则返回 200， 同时返回新文件。

4. Etag 功能和 `Last-Modified` 一样，标识文件再服务器上的最新更新时间

   不同的是， Etag 的取值是一个对文件进行标识的特征字串

   再向服务器查询文件是否有更新时，浏览器通过 `If-None-Match`  字段把特征字串发送给服务器，由服务器和文件的最新特征字串进行匹配，来判断文件是否有更新。

   Etag 和 Last-Modified 可根据需求使用一个或两个同时使用。两个同时使用时，只要满足其中要给就可以。

**常用方法：**

* Cache-Control 与 Last-Modified 一起使用
* Expires 和 Etag 一起使用

即 一个控制缓存有效时间，一个用户在缓存失效后，向服务器查询是否有更新

***浏览器缓存机制是浏览器内核的机制，一般都是标准的实现***, 缓存的内容，受存储空间约束，同时也有被清除的风险

##### Application Cache 缓存机制

**原理：**

* 以文件为单位进行缓存，且文件有一定更新机制（类似于浏览器缓存机制）

* AppCache 有啷个关键点 manifest 属性和 manifest 文件

  ```html
  <!DOCTYPE html>
  <html manifest="demo_html.appcache">
  // HTML 在头中通过 manifest 属性引用 manifest 文件
  // manifest 文件：就是上面以 appcache 结尾的文件，是一个普通文件文件，列出了需要缓存的文件
  // 浏览器在首次加载 HTML 文件时，会解析 manifest 属性，并读取 manifest 文件，获取 Section：CACHE MANIFEST 下要缓存的文件列表，再对文件缓存
  <body>
  ...
  </body>
  </html>
  
  // 原理说明如下：
  // AppCache 在首次加载生成后，也有更新机制。被缓存的文件如果要更新，需要更新 manifest 文件
  // 因为浏览器在下次加载时，除了会默认使用缓存外，还会在后台检查 manifest 文件有没有修改（byte by byte)
  发现有修改，就会重新获取 manifest 文件，对 Section：CACHE MANIFEST 下文件列表检查更新
  // manifest 文件与缓存文件的检查更新也遵守浏览器缓存机制
  // 如用户手动清了 AppCache 缓存，下次加载时，浏览器会重新生成缓存，也可算是一种缓存的更新
  // AppCache 的缓存文件，与浏览器的缓存文件分开存储的，因为 AppCache 在本地有 5MB（分 HOST）的空间限制
  ```
  



**特点：**

方便构建 WebApp 的缓存， 准们为 WebApp 离线使用而开发的缓存机制

**应用场景：**

存储静态文件（js， css，字体文件等）

是对浏览器缓存机制的补充，不是替代

**实现方案：**

```java
// 通过设置WebView的settings来实现
WebSettings settings = getSettings();

String cacheDirPath = context.getFilesDir().getAbsolutePath()+"cache/";
settings.setAppCachePath(cacheDirPath);
// 1. 设置缓存路径

settings.setAppCacheMaxSize(20*1024*1024);
// 2. 设置缓存大小

settings.setAppCacheEnabled(true);
// 3. 开启Application Cache存储机制

// 特别注意
// 每个 Application 只调用一次 WebSettings.setAppCachePath() 和
WebSettings.setAppCacheMaxSize()
```



##### Dom Storage 缓存机制

**原理：**

通过存储 key - value 来提供

> Dom Storage 分为 sessiongStorage 和 localStorae, 两者基本相同，区别于作用范围
>
> sessionStorage：具备临时性，即存储与页面相关的数据，在离开页面后无法使用
>
> localStorage：具备持久性，即保存的数据在页面关闭后还可以使用

**特点：**

存储空间大（5mb）存储空间对于不同浏览器不同

存储安全、边界：Dom Storage 存储的数据在本地，不需要经常和服务器交互

**应用场景：**

存储临时，简单的数据，类似于 Android 的 SharedPreference 机制。

```java
getSettings().setDomStorageEnabled(true);
```

##### Web SQL Database 缓存机制

**原理：**

基于 SQL 的数据库存储机制

**特点：**

充分利用数据库的有时，可方便对数据进行 CUDA

**场景**

适合数据库的结构化数据

**实现：**

```java
// 通过设置WebView的settings实现
WebSettings settings = getSettings();

String cacheDirPath = context.getFilesDir().getAbsolutePath()+"cache/";
settings.setDatabasePath(cacheDirPath);
// 设置缓存路径

settings.setDatabaseEnabled(true);
// 开启 数据库存储机制

```



##### IndexDB 缓存机制

属于 NoSQL 数据库，通过存储字符串的 Key - Value 来提供。

**特点**

可存储复杂，数据量大的结构化数据

**实现**

```java
// 通过设置WebView的settings实现
WebSettings settings = getSettings();

settings.setJavaScriptEnabled(true);
// 只需设置支持JS就自动打开IndexedDB存储机制
// Android 在4.4开始加入对 IndexedDB 的支持，只需打开允许 JS 执行的开关就好了。
```



##### File System 

**原理：**

为 H5 页面的数据，提供一个虚拟的文件系统

* 可进行文件的 CUDA，就像 Native App 访问本地文件系统一样
* 虚拟的文件系统运行在沙盒中
* 不同 WebApp 的虚拟文件系统的互相隔离的，虚拟文件系统与本地文件系统也是互相隔离的。

虚拟文件系统提供了两种类型的存储空间：临时和持久

* 临时的存储空间：由浏览器自动分配，但可能被浏览器回收
* 持久性存储空间：需要显示申请；自己管理（浏览器不会回收，也不会清除内容）；内存空间大小通过配额管理，首次申请时会一个初始的配额，配额用完需要再次申请。

**特点：**

* 可存储数据体积较大的二进制数据
* 可预加载资源文件
* 可直接编辑文件

**场景：**

通过文件系统管理数据

**使用**

由于 file system 时 H5 新加入的缓存机制， Android WebView 暂时不支持



##### 使用建议

| 存储静态资源文件（js等）       | 浏览器缓存机制<br />Application Cache 存储机制 |
| ------------------------------ | ---------------------------------------------- |
| 存储，临时、简单的数据         | Dom Stroage 缓存机制                           |
| 存储复杂、数据量大的结构化数据 | indexedDB缓存机制                              |
| 在 Android WebView 中进行设置  |                                                |



##### 缓存模式

**WebView 的 5 种缓存模式**

* LOAD_CACHE_ONLY: 不使用网络，只读取本地缓存数据
* LOAD_DEFAULT: 根据 cache-control 决定是否从网络上取数据
* LOAD_CACHE_NORMAL: API Level 17 中已废弃，从 API Level 11 开始作用同 LOAD_DEFAULT 模式
* LOAD_NO_CACHE： 不使用缓存，只从网络获取
* LOCA_CACHE_ELSE_NETWORK: 只要本地有，无论是否过期，或者 no-cache 都使用缓存的数据。本地没有缓存时才从网络上获取

```java
WebSettings settings = mWebView.getSettings();
settings.setCacheMode(WebSettings.LOAD_DEFAULT);
```



#### 资源预加载

**定义：**

提早加载将需要使用的 H5 页面，即 *提前构建缓存*

使用时直接取过来用，而不是用时才加载

##### 预加载 WebView 对象

* 此处主要分为 2 方面，首次使用 WebView 对象 和 后续使用 WebView 对象

| 类型                  | 原因                                                         | 思路                                                         | 实现                                                        |
| --------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ----------------------------------------------------------- |
| 首次使用 WebView 对象 | 首次初始化 WebView 会比第二次初始化慢很多<br />初始化后，即使 WebView 已释放，但一些多个 WebView 公用的全局服务 / 资源对象仍未释放<br />第二次初始化时则不需要在生成，从而快。 | 1. 用用启动时初始化一个全局的 WebView 对象<br />2. 当用户需要加载 H5 页面时，则直接使用该 WebView 对象加载并显示 | 在 Android  的 BaseApplication 里初始化要给 web View 对象   |
| 后续使用 WebView 对象 | 多次创建 WebView 对象会耗费很多时间和资源                    | 1. 自身构建 WebView 服用池<br />2. 当用户需要使用 WebView 加载 H5 时，直接使用该 WebView 对象池加载和展示 | 采用  2个/多个 webView 重复使用，而不需要每次打开 H5 都新建 |


































对于第一点，其实主要是由前端代码和手机硬件决定，因为我们这里讨论的是对于 app 的性能优化，暂时不考虑；

所以我们可以从第二点做文章，主要思路就是一些资源文件都使用 App 本地资源，而不需要从网络下载，从而提高页面的打开速度

1. 首先将一些资源文件放在本地的 `assets` 目录，然后重写 WebViewClient 的 `shouldInterceptRequest(WebView view, String url)` 和  `shouleInterceptRequest(WebView view, WebResourceRequest request)` 这两个方法，对访问地址进行拦截，当 `url` 地址命中本地配置的 `url` 时，使用本地资源替代，否则就使用网络上的资源。

   ```Java
   mWebView.setWebViewClient(new WebViewClient() {
       // 设置不使用系统浏览器打开，直接显示在当前 WebView
       @Override
       public boolean shouldOverrideUrlLoading(WebView view, String url) {
           view.loadUrl(url);
           return true;
       }
       
       @Override
       public WebResourceResponse shouldIntercepteReqeuest(WebView view, String url) {
           // 如果命中本地资源，使用本地资源替代
           if(mDataHelper.hasLocalResource(url)){
               WebResourceResponse response = mDataHelper.getReplaceWebResourceResponse(getApplicationContext(), url);
               if(response != null) {
                   return response;
               }
           }
           return super.shouldInterceptRequest(view, url);
       }
       
       // 兼容 5.0 以上的设备
       @TargetApi(VERSION_CODE.LOLLIPOP)
       @Override
       public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
           String url = request.getUrl().toString();
           if(mDataHelper.hasLocalResource(url)) {
               WebResourceResponse response = mDataHelper.getReplaceWebResourceResponse(getApplicationContext(), url);
               if(response != null) {
                   return response;
               }
           }
           return super.shouleInterceptRequest(view, request);
       }
   });
   ```

   DataHelper 是一个工具类

   ```java
   public class DataHelper {
       private Map<String, String> mMap;
       public DataHelper(){
           mMap = new HashMap<>();
           initData();
       }
       
       private void initData(){
           String imageDir = "images/";
           String pngSuffix = ".png";
           mMap.put("http://renyugang.io/wp-content/themes/twentyseventeen/style.css?ver=4.9.8", "css/style.css");
           mMap.put("http://renyugang.io/wp-content/uploads/2018/06/cropped-ryg.png",imageDir + "cropped-ryg.png");
           // ...
       }
       
       public boolean hasLocalResource(String url) {
           return mMap.containsKey(url);
       }
       
       public WebResourceResponce getReplacedWebResourceResponse(Context context, String url) {
           String localResourcePath = mMap.get(url);
           if(TextUtils.isEmpty(localResourcePath)) {
               return null;
           }
           InputStream is = null;
           try {
               is = context.getApplicationContext().getAssets().open(localResourcePath);
           } catch (Exception e) {
               e.printStackTrace();
               return null;
           }
           String mimeType;
           if(url.contans("css")) {
               mimeType = "text/css";
           } else if (url.contains(".jpg")) {
               mimeType = "image/jpeg";
           } else {
               mimeType = "image/png";
           }
           
           WebResourceResponse response = new WebResourceResponse(mimeType, "utf-8", is);
           return response;
       }
   }
   ```

****

### **WebView 的缓存**

在不配置本地资源的时候，我们第一次打开页面，产生了 n  多请求。但是当我们退出后再次打开这个页面（没有设置加载本地资源）的时候，居然只发生了一次请求，这现象与加载本地资源十分相似。![image-20201027164335807](https://github.com/xiaomanwong/static_file/blob/master/images/image-20201027164335807.png?raw=true)

我们观察到，这个请求的 response 的 headers 中的参数，`Last-Modified,ETag, Expires, Cache-Control` 

**Cache-Control：** 例如 Cache-Control:max-age=2592000, 表示缓存时长为 2592000 秒，也就是一个月30天的时间，如果30天内需要再次请求这个文件，那么浏览器不会发生出请求，直接使用本地缓存的文件。这是 `Http/1.1`  标准中的字段。

**Expires：** 例如 Expires:Tue, 25 Sep 2018 07L17L34 GMT, 表示这个文件的过期时间是格林尼治时间2018年9月25日7点17分。因为我们是北京时间 2018年8月26日15点请求的，所以可以看出也是差不多一个月的有效期。在这个事件之前浏览器都不会再次发出请求去获取这个文件。Expires 是 `HTTP/1.0` 中的字段，如果客户端和服务器事件不同步会导致话u农村出现问题，因此才有了上面的 Cache-Control 。当他们同时出现时， Cache-Control 的优先级会更高。

**Last-Modified:** 标识文件在服务器上的最新更新时间，下次请求时，如果文件缓存过期，浏览器通过 `If-Modified-Since` 字段带上这个时间，发送给服务器，由服务器比较时间戳来判断文件是否由修改。如果没有修改，服务器范围 304 （未修改）告诉浏览器继续使用缓存；如果有修改，则返回 200， 同时返回最新的文件。

**ETag：** ETag 的取值时一个对文件进行标识的特征字段，在向服务器查询文件是否有更新时，浏览器通过 `If-None-Match` 字段把特征字串发送给服务器，由服务器和文件最新特征字串进行匹配，来判断文件是否有更新：没有返回 304， 有返回 200。 ETag 和 Last-Modified 可根据需求使用一个或两个同时使用。两个同时使用时，只要满足其中一个条件，就可以认为有更新。

> 常见用法是， `Cache-Control` 与 `Last-Modified` 一起使用， `Expires` 和 `ETag` 一起使用。但实际情况可能并不是这样

**设置 WebView 使用这些内容**

想要 WebView 使用上面说到的缓存机制配置（答案是，不配置或手动设置）

```java
WebSettings settings = mWebView.getSettings();
settings.setCacheMode(WebSettings.LOAD_DEFAULT);
```

**WebView 的 5 种缓存模式**

* LOAD_CACHE_ONLY: 不使用网络，只读取本地缓存数据
* LOAD_DEFAULT: 根据 cache-control 决定是否从网络上取数据
* LOAD_CACHE_NORMAL: API Level 17 中已废弃，从 API Level 11 开始作用同 LOAD_DEFAULT 模式
* LOAD_NO_CACHE： 不使用缓存，只从网络获取
* LOCA_CACHE_ELSE_NETWORK: 只要本地有，无论是否过期，或者 no-cache 都使用缓存的数据。本地没有缓存时才从网络上获取

在移动端，我们一般设置为默认的缓存模式就可以了，关于缓存的配置，主要还是靠 web 前端和后台设置。



## WebView 的速度方案

### WebView 的初始化

本地 WebView 初始化都要不少时间，首次初始化 webview 与第二次初始化不同，首次会比第二次慢很多。原因第一次初始化是初始化浏览器的内核引擎，第二次则是可以直接拿来使用，并且一些已经初始化好，还没有被回收和销毁的对象也可以直接复用。

### 预加载数据

就是在客户端初始化 WebView 的同时，直接由 native 开始网络请求数据，当页面初始化完成后，向 native 获取其代理请求的数据，数据请求和 WebView 初始化可以并行进行，缩短总体的页面加载时间。‘

简单来说就是配置一个预加载列表，在 APP 启动或者默写时机提前去请求，这个预加载列表需要包含所有 H5 模块的页面和资源，客户端可以接管所有请求的缓存，不走 webview 默认缓存逻辑，自行实现缓存机制，原理其实就是拦截 WebViewClient 的那两个 `shouleInterceptRequest` 方法。

### 离线包

离线包的意思就是将 H5 的页面和资源进行打包后下发到客户端，并由客户端直接解压到本次存储中。优点是由于其本地化，首屏加载速度快，用户体验更接近原生，可以不依赖网络，离线运行，缺点就是开发流程/更新机制复杂，需要客户端、甚至服务端的共同协作。

**资源：**

* H5： 每个代码包都有一个唯一且递增的版本号
* Native：提供包下载且解压资源文件到对应目录
* 服务端：提供一个接口，可以获取线商最新代码包的版本号和下载地址

**流程：**

* 前端更新代码打包后按版本号上传至指定的服务器上
* 每次打开页面时， H5 请求接口获取线商最新代码包版本号，并与本地包进行版本号比对，当线商版本号大于本地包版本号时，调用原生下载离线包
* 客户端直接去线商地址下载最新的代码包，并解压替换到当前目录文件
