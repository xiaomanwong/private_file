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

