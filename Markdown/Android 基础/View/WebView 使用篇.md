---
title: WebView 使用篇
tag: WebView
category: Android
---



## 交互方式

**Android 调用 JS** 

* 通过 `WebView` 的 `loadUrl()`
* 通过 `WebView` 的 `evaluateJavascript()`

**JS 调用 Android**

* 通过 `WebView` 的 `addJavascriptInterface()` 进行对象映射
* 通过 `WebView` 的 `shouldOverrideUrlLoading()` 方法回调拦截 `Url`
* 通过 `WebChromeClient` 的 `onAlert(),onJsConfirm(), onJsPrompt()` 方法回调拦截 JS 对话框 `alert(),confrim(),permpt()`  的消息

## Android 调用 WebView

### 方式一： WebView.loadUrl()

* 点击 Android 按钮，调用 WebView JS 中的 callJs()

```html
<!DOCTYPE html>
<html>
    
    <head>
        <meta chartset="utf-8">
        <title>xxxxx</title>
    </head>
    
    <script>
    	function callJs(){
            alert("Android 调用 JS 的 callJs（）");
        }
    </script>
</html>
```

```java
public class TestActivity extends Activity{
    WebView webView;
    Button button;
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.test_activity);
        webView = (WebView)findViewById(R.id.webview);
        WebSettings setting = webView.getSettings();
        
        // 设置 JS 交互权限
        setting.setJavaScriptEnabled(true);
        // 允许 JS 弹窗
        setting.setJavaScriptCanOpenWindowsAutomatically(true);
        
        // 载入 js 代码
        webView.loadUrl("file://android_asset/javascript.html");
        button = (Button)findViewById(R.id.buttong);
        button.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                webView.post(new Runnable(){
                   // 调用 JS 方法名要对应上
                    webView.loadUrl("javascript::callJs()");
                });
            }
        });
        
        // 由于设置了弹窗检查调用结果，所以需要支持 js 对话框
        // webview 只是载体，内容的渲染需要使用 webviewChromeClient 类去实现
        // 通过设置 WebChromeClient 对象处理 JavaScript 的对话框
        // 设置 JS 的 Alert 函数
        webView.setWebChromeClient(new WebChromeClient(){
            @Override
            public boolean onJsAlert(WebView view, String url, String message, final JsResult result) {
                AlertDialog.Builder dialog = AlertDialog.Builder(TestActivity.this);
                dialog.setTitle("alert");
                dialog.setMessage(message);
                dialog.setPositiveButton(android.R.string.ok, new DialogInterface.OnClickListener(){
                   @Override
                    public void onClick(DialogInterface dialog, int which) {
                        result.confirm();
                    }
                });
                dialog.setCancelable(false);
                dialog.create().show();
                return true;
            }
        });
    }
}
```

### 方式二： WebView.evaluateJavascript()

优点：比第一种效率高，使用更简洁

> 1. 该方法的执行不会使页面刷新， `loadUrl()` 则会执行刷新
> 2. Android 4.4 版本后才可以使用

```java
webView.evluateJavascript("javascript:callJs()", new ValueCallback<String>(){
    @Override
    public void onReceiveValue(String value) {
        // 此处为 JS 返回结果
    }
});
```



### 方法对比

| 调用方法                 | 优点       | 缺点                                  | 使用场景                           |
| ------------------------ | ---------- | ------------------------------------- | ---------------------------------- |
| 使用 loadUrl()           | 方便，简洁 | 效率低<br />获取返回值麻煩            | 不需要获取返回值，对性能要求不高时 |
| 使用 evluateJavascript() | 效率高     | 向下兼容性差，仅 Android 4.4 以上可用 | Android 4.4 以上                   |

### 使用建议

两种混合使用，可保证 Android 4.4 上下都可以使用

```java
// Android 版本变量
final int version = Build.VERSION.SDK_INT;
if(version < 18) {
    webView.loadUrl("javascript:callJs()");
} else {
    webView.evluateJavascript("javascript:callJs()", new ValueCallback<String>(){
        @Override
        public void onReceiveValue(String value) {
            // js 返回结果
        }
    });
}
```

## JS 调用 Android 

1. 通过 `WebView` 的  `addJavascriptInterface()` 进行映射
2. 通过 `WebChromeClient` 的 `shouldOverrideUrlLoading()` 方法拦截 Url
3. 通过 `WebChromeClient` 的 `onJsAlert(), onJsConfirm(), onJsPrompt()` 方法拦截 JS 对话框 `alert(), confirm(), pormpt()` 消息

### 方式一：`addJavascriptInterface()` 进行映射

**定义一个与 JS 对象映射关系的 Android 类**

```java
public class JsCallAndroidInterface {
    // 定义 JS 需要调用的方法
    // 被 JS 调用的方法必须加入 @JavascriptInterface 注解
    // 这部分代码执行在异步线程中
    @JavascriptInterface
    public void hello(String msg) {
        Log.d(TAG, msg);
    }
}
```

**加载 JS 代码**

```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8"/>
        <title>title</title>
        <script>
        	function callAndroid(){
                // 由于对象映射，所以需要调用 test 对象等于调用 Android 映射对象
                test.hello("js 调用 Android 的 hello");
            }
        </script>
    </head>
    
    <body>
        <button type="button" id="button1" "callAndroid()"></button>
    </body>
</html>
```

**在  Android 里通过 WebView 设置 Android 类和 JS 代码的映射**

```java
setting.setJavascriptEnable(true);
// Android to js 类对象映射到 js 对象
webView.addJavascriptIntercept(new JsCallAndroidInterface(), "test");
```

> 使用简单，仅将 Android 对象和 JS 对象映射即可
>
> 存在严重的漏洞问题，容易造成系统信息的泄漏

### 方式二： `shouldOverrideUrlLoading()` 方法拦截 Url

原理：

* Android 通过 WebViewClient 的回调方法 `shouldOverriderUrlLoading()` 拦截 URL
* 解析此 URL 的协议
* 如果检测到了预先约定好的协议，就回调相关方法

> 也就是 JS 调用 Android 的方法

**一：在 JS 中约定所需要的 URL 协议**

```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>title</title>
        
        <script>
        	function callAndroid(){
                document.location = "js://webview?arg1=111%arg2=112";
            }
        </script>
    </head>
    
    <body>
        
        <button type="button" id = "button1" onclick="callAndroid()">
            
        </button>
    </body>
</html>
```

当 JS 通过 Android 的 `webView.loadUrl("file:///android_asset/javascript.html");` 加载后，就会回调 `shouldOverrideUrlLoading()` 

**二：在 Android 通过 WebViewClient 重写 shouldOverrideUrlLoading()**

```java
public class TestActivity extends Activity{
    WebView mWebView;
    
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.test_activity);
        mWebView = findViewById(R.id.webview);
        
        WebSettings settings = mWebView.getSettings();
        // 设置于 JS 交互权限
        settings.setJavascriptEnabled(true);
        // 允许 JS 弹框
        settings.setJavascriptCanOpenWindowsAutomatically(true);
        
        mWebView.loadUrl("file:///android_asset/javascript.html");
        
        
        mWebView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url){
                // 根据协议参数，判断是否由需要的 url
                // 一般根据 scheme（协议格式） 和 authority（协议名）判断
                // 假设传入的时 url ="js://webview?arg1=111&arg2=222"
                
                Uri uri = Uri.parse(url);
                // 如果 url 的协议为事先约定好的 JS 协议， 就解析参数
                if(uri.getScheme().equals("js")) {
                    // 如果 authority 为事先约定好的 webview，表示符合约定协议
                    // 拦截 url ，执行 Android 的放法
                    if( url.getAuthority().equals("webview")) {
                        // 执行 js 需要的调用逻辑
                        Log.d(TAG,"js 调用了 Android 的方法");
                        HashMap<String, String> param = new HashMap();
                        Set<String> collection = uri.getQueryParameterNames();
                    }
                    
                    return true;
                }
                return super.shouldOverrideUrlLoading(view, url);
            }
        });
    }
}
```

> 不存在方式 1 的漏洞
>
> 缺点：JS 获取 Android 方法的返回值复杂
>
> ​		如果 JS 想要 Android 方法的返回值，只能通过 webView.loadUrl() 去执行 js 方法，把返回值传递回去
>
> ```java
> // Android: TestActivity
> mWebView.loadUrl("javascript:returnResult(" + result + ")");
> 
> // js: Javascript.html
> function returnResult(result) {
>     alert(result);
> }
> ```

### 方式三： `onJsAlert(), onJsConfirm(), onJsPrompt()` 方法拦截 JS 对话框 `alert(), confirm(), pormpt()` 消息

JS 中，有三个常用的对话框方法

| 方法      | 作用       | 返回值         | 备注                                                         |
| --------- | ---------- | -------------- | ------------------------------------------------------------ |
| alert()   | 弹出警告框 | 没有           | 在文本中加入 \n 可换行                                       |
| confirm() | 弹出确认框 | 两个返回值     | 1. 返回布尔值<br />2. 通过该值判断点击的是确认还是取消： true 表示确认， false 表示取消 |
| prompt()  | 弹出输入框 | 任意设置返回值 | 1. 点击 “确认”： 返回输入框中的值<br />2. 点击 “取消”： 返回 null |

通过 Android 的 `WebChromeClient` 中 `onJsAlert(), onJsConfirm(), onJsPrompt()` 方法拦截 JS 对话框 `alert(), confirm(), pormpt()` 消息，并解析

如拦截 `prompt()`

> 常用的拦截是： 拦截 JS 的输入框 prompt() 方法
>
> 因为只有 prompt() 方法可以返回任意类型值，操作最全面、方便、灵活。alert() 没有返回值; confirm() 只能返回两种

**加载 js 代码**

```html
<!DOCTYPE html>
<html>
   <head>
      <meta charset="utf-8">
      <title>Carson_Ho</title>
      
     <script>
        
	function clickprompt(){
    // 调用prompt（）
    var result=prompt("js://demo?arg1=111&arg2=222");
    alert("demo " + result);
}

      </script>
</head>

<!-- 点击按钮则调用clickprompt()  -->
   <body>
     <button type="button" id="button1" "clickprompt()">点击调用Android代码</button>
   </body>
</html>
```

当使用 `mWebView.loadUrl("file:///android_asset/javascript.html")` 加载 JS 代码后，就会触发 `onJsPrompt()` 

> 如果拦截警告框 `alert()` ，则触发 `onJsAlert()`
>
> 如果拦截确认框 `confirm()` 则触发 `onJsConfirm()`

**在 Android 中通过 WebChromeClient  重写 onJsPrompt()**

```java
mWebView.setWebChromeClient(new WebChromeClient(){
    
    @Override
    public boolean onJsPrompt(WebView view, String url, String message, String defaultValue, JsPromptResult result) {
        // 根据协议参数，判断是否是需要的 URL
        // 与 方法二相同
        Uri uri = Uri.parse(url);
        if(uri.getScheme().equals("js")){
            if(uri.getAuthority().equalse("webview")) {
		       // 执行 js 需要的逻辑
                Log.d(TAG, message);
                HashMap<String, String> map = new HashMap<String, String>();
                Set<String> collection = uri.getQueryParameterNames();
                
                // 参数 result: 代表消息框的返回值（输入值）
                result.confirm("js 调用了 Android 方法");
            }
            return true;
        }
        return super.onJsPrompt(view, url, message, defaultValue, result);
    }
});
```

### 方法对比

| 调用方式                          | 优点           | 缺点                                                         | 使用场景                                         |
| --------------------------------- | -------------- | ------------------------------------------------------------ | ------------------------------------------------ |
| addJavascriptInterface() 映射关系 | 方便简洁       | Android 4.2 一下存在漏洞                                     | Android 4.2 以上相对简单的互调场景               |
| 重写 shouldOverrideUrlLoading()   | 不存在漏洞问题 | 使用复杂，需要进行协议约束；从 Native 层往 web 层传递数据比较麻煩 | 不需要返回值情况下的互调场景（ios 使用的比较多） |
| 拦截 JS 对话框                    | 不存在漏洞     | 需要近些协议约束                                             | 能满足大多数情况下的互调情况                     |



## 总结

| 类型            | 调用方式                   | 优点           | 缺点                                                         | 使用场景                           | 建议     |
| --------------- | -------------------------- | -------------- | ------------------------------------------------------------ | ---------------------------------- | -------- |
| Android 调用 JS | loadUrl()                  | 简单           | 效率低，获取返回值麻煩                                       | 不需要获取返回值，对性能要求不高   | 混合使用 |
|                 | evaluateJavascript()       | 效率高         | 仅支持 Android 4.4 以上                                      | Android 4.4 以上                   |          |
| JS 调用 Android | addJavascriptInterface()   | 简洁           | Android 4.2 以下存在漏洞                                     | Android 4.2 以上相对简单的调用场景 |          |
|                 | shouldOverrideUrlLoading() | 不存在漏洞问题 | 使用复杂，需要进行协议约束；从 Native 层往 web 层传递数据比较麻煩 | 不需要返回值的情况下               |          |
|                 | 拦截 JS 弹框               | 不存在漏洞问题 | 需要进行协议约束；从 Native 层往 web 层传递数据比较麻煩      | 能满足大多数情况下的调用场景       |          |

