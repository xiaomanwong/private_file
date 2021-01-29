---
title: Android WebView
tag: Android View
---



## **问题**：

### **为什么** **WebView 的加载速度那么慢?**

1. js 解析效率

   如果 js 文件较多、解析比较复杂，就会导致渲染速度较慢。或者手机硬件性能比较差的花，也会导致渲染速度比较慢

2. 页面资源的下载

   一般加载一个 H5 页面，都会产生比较多的网络请求，如图片、js 文件、css 文件等，需要将这些资源都下载完成之后才能完成渲染，这样也会导致页面渲染速度变慢

<!-- more -->

### **那如何解决呢？**

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
