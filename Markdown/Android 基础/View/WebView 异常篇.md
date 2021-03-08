---
title: WebView 异常篇
tag: WebView
category: Android
---

## WebView 漏洞

### 主要问题

WebView 中，主要有三种漏洞问题

1. 任意代码执行漏洞
2. 密码明文存储漏洞
3. 域控制不严格漏洞

### WebView 任意代码执行漏洞

产生漏洞原因有三

1. WebView 中 `addJavascriptInterface()` 接口
2. WebView 内置导出的 `searchBoxJavaBridge_` 对象
3. WebView 内置导出的 `accessibility` 和 `accessibilityTraversal` Object 对象

####  addJavascriptInterface() 引起远程代码执行漏洞

**产生原因：**

JS 调用 Android 的其中一个方式通过 `addJavascriptInterface` 接口进行映射

```java
webview.addJavascriptInterface(new JsCallAndroidInterface(), "JsCallAndroidInterface");
// 参数一： Android 本地对象
// 参数二： JS 对象
// 通过对象映射将 Android 中的本地对象和 JS  中的对象进行关联，从而实现 JS 调用 Android 对象和方法
```

**当 JS 拿到 Android 对象后，可以调用这对象中所有的方法，包括系统类（java.lang.Runtime), 从而进行任意代码执行**

> 可以执行命令获取本地设备的 SD卡中的文件等信息，造成信息泄漏

结合 Java 反射机制，具体获取系统类的描述

* Android 中的对象有一个公共方法， getClass()

* 该方法可以获取到当前类类型

* 该类有关键方法,Class.forName();

* 使用这个方法可以加载一个类

* 获取到类对象后，可以执行本地命令

  JS 攻击本地核心代码：

  ```javascript
  function execute(cmd) {
  	// 遍历 Window 对象
  	// 目的是为了找到包含 getClass() 的对象
  	// 因为 Android 映射的 JS 对象也在 Window 中，一定会拿到
  	for(var obj in window) {
  		if("getClass" in window[obj]) {
  			// 利用反射调用 forName() 得到 Runtime 类
  			alert(obj);
              return window[obj].getClass().forName("java.lang.Runtime");
  		}
          
          // 之后，可以调用静态方法来执行一些命令，比如访问文件
          getMethod("getRuntime", null).invoke(null, null).exec(cmd);
          // 从执行命令后返回的输入流中得到字符串，有很严重暴露隐私信息的危险
          // 如果执行完访问文件的命令后，就可以得到文件名信息等
  	}
  }
  ```

* 当一些 APP 通过扫描二维码打开一个外部网页时，攻击者就可以执行这段 js 代码进行漏洞攻击

**解决方案：**

1. 在 Android 4.2 版本之后
   Google 在 Android 4.2 版本中规定对被调用的函数以 `@JavascriptInterface ` 进行注解，从而避免漏洞攻击
2. 在 Android 4.2 版本之前
   在 Android 4.2 之前采用拦截 `prompt()` 进行漏洞修复
   1. 继承 WebView ，重写 `addJavascriptInterface()` ，然后内部自己维护一个对象映射关系的 Map，将需要添加的 JS 接口放入 Map 中
   2. 每次当 WebView 加载页面前加载一段本地的 JS 代码
      1. 让 JS 调用 Javascript 方法：通过调用 prompt() 把 js 中的信息（含特定表示、方法名等）传递到 Android 端
      2. 在 Android 的 onJsPrompt() 中，解析参数信息，再通过反射机制调用 Java 对象的方法，来实现 JS 调用 Android 的安全性

#### searchBoxJavaBridge_接口引起的远程代码执行漏洞

**产生原因**

* Android 3.0 以下， Android 系统默认通过 searchBoxJavaBridge_ 的 Js 接口给WebView 添加一个 JS映射对象， searchBoxJavaBridge_
* 该接口可能被利用，实现远程任意代码

**解决方案：**

删除 searchBoxJavaBridge_ 接口

```java
// 通过调用该方法移除
removeJavascriptInterface();
```

#### accessibility 和 accessibilityTraversal 接口引起远程代码执行漏洞

与上述基本相同

### 密码明文存储漏洞

**问题分析：**

WebView 默认开启密码保存功能

```java
mWebView.setSavePassword(true);
```

* 开启后，再用户输入密码时，会弹出提示框，询问用户是否保存密码
* 如果选择"是"，密码会被明文保存到 `/data/data/com.package.name/databases/webview.db` 中，这样就有被盗取密码的危险

**解决方案:**

关闭密码保存提醒

```java
WebSettings.setSavePassword(false);
```

### 域控制不严格漏洞

**问题分析：**

再Android里的 `WebViewActrivity.java`

```java
public class WebViewActivity extends Activity {
    private WebView webView;
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_webview);
        webView = findViewById(R.id.webview);
        Intent intent = new Intent();
        
        // webView.getSettings().setAllowFileAccess(false);
        // webView.getSettings().setAllowFileAccessFromFileURLs(true);
        // webView.getSettings().setAllowUniversalAccessFromFileURLs(true);
        // url = file://data/local/tmp/attack.html
        String url = i.getData().toString();
        webView.loadUrl(url);
    }
}
```

将这个 WebViewActivity 再 Manifest.xml 设置 exported 属性，表示：当前 Activity 是否可以被另外一个 Application  的组件启动

`android:exported="true"`

即 A 应用可以通过 B 应用到处的 Activity 让 B 应用加载一个恶意的 file 协议的 url，从而可以获取 B 应用的内部私有文件，从而带来数据泄漏威胁

> 具体：当其他应用启动此 Activity 时，intent 中的 data  直接被当作 url 来加载（假设传入来的 url 时 file://data/local/tmp/attack.html），其他 App 通过使用显式 ComponentName 或者其他类似方式就可以轻松启动该 web ViewActivity，并加载恶意 url

那么 WebView 中 getSettings（）函数对 WebView 安全性的影响

* setAllowFileAccess()
* setAllowFileAccessFromFileURLs()
* setAllowUniversalAccessFromFileURLs()

1. **setAllowFileAccess()**

   ```java
   // 设置是否允 WebView 使用 file 协议
   webView.getSettings().setAllowFileAccess(true);
   // 默认设置为 true，即允许再 File 域下任意执行 JavaScript 代码
   ```

   使用 File 域加载的 js 代码能够使用进行 *同源策略跨域访问*，从而导致隐私信息泄漏

   > 1. 同源策略跨域访问：对私有目录文件进行访问
   > 2. 针对 IM 类产品，泄漏的是聊天信息、联系人等等
   > 3. 针对浏览器类软件， 泄漏的是 cookie 信息

   如果不允许使用 file 协议，则不会出现上述威胁

   ```java
   webView.getSettings().setAllowFileAccess(false);
   ```

   但同时也限制了 WebView 的功能，使得不能加载本地的 HTML 文件

   

   **解决方案**

   1. 对于不需要使用 file 协议的应用，禁用 file 协议

      **setAllowFileAccess(false);**

   2. 对于需要使用 file 协议的用用，禁止 file 协议加载 JavaScript

      ```java
      setAllowFileAccess(true);
      // 禁用文件协议使用 JavaScript
      setJavaScriptEnabled(!url.startsWith("file://");
      ```

   

 2.  setAllowFileAccessFromFileURLs()

    

   

   

   

   

