---
title: Android 版本适配
tag: Android
categories: 适配
---



## 基本知识

### targetSdkVersion

`targetSdkVersion`： 目标 SDK 版本，也就是我们最高适配的 SDK 版本

不同版本的 SDK ，为我们提供了不同的 API 接口使用，丰富以及方便开发者。

旧的接口行为发生了变化，为了保证 APK 的行为还是和以前兼容，在源码中多了很多类似于 `ctx.getApplicatioinInfo().targetSdkVersion()` 的判断，因此只要 APK 的 `targetSdkVersion` 不变，即使 APK 安装在新的 Android 系统上，其行为也不会发生变化。

<!-- more -->

### compileSdkVersion

`compileSdkVersion` 定义应用程序编译选择哪个 Android SDK 版本，通常设置为最新的 API，它的属性值不影响 Android 系统运行行为，仅仅是 Android 编译项目时其中的一象配置，不会打包到 APK 中，真实目的时为了 **在编译的时候检查代码的错误和警告，提示开发者修改和优化**

### minSdkVersion

`minSdkVersion`: 最小 SDK 版本，也就是我们最低支持的 SDK 版本

* 告诉 Google Play Store 哪些 Android 版本的手机可以安装这个 APK
* 默认情况下，lint 会对代码中的 API 调用做出提示，加入你调用的 API 在 minSdkVersion 之后才提供，它会告诉你虽然编译可以通过，但是运行时会抛出异常。

如果调用的 API 是在 minSdkVersion 之后才提供的，解决方案有两种

* 运行时判断 API Level， 仅在足够高，有此方法的 API Level 系统中调用

  ```java
  if(android.os.Build.VERSION_SDK_INIT >= Build.VERSION_CODES.M) {
      // 处理逻辑
  }
  ```

* 保证功能的完整性，通过低版本的 API 实现功能

## Android 6.0 适配

### 运行时权限请求

从 `Android 6.0(api >= 23)` 开始，用户开始在运行时向其授予权限，而不是在应用安装时授予。系统权限分为两种

* 正常权限。在 `AndroidManifest` 列出了正常权限，系统将自动授予该权限
* 危险权限。在 `AndroidManifest` 中列出了危险权限，用户必须明确批准您的应用使用这些权限。

## Android 7.0 适配

### 应用间共享文件限制

在 `Android 7.0` 系统上， Android 框架强制执行了 `ScrictMode API` 政策，禁止向应用外公开 `file://URI` 如果一项包含文件 `file://URI` 类型的 `Intent` 离开了你的应用，即调用 `Uri.from(file)` 传递文件路径给第三方应用，会出现 `FileUriExposedException` 异常，如调用系统相机拍照、裁切照片、打开 APK 安装界面等。

如果要在 **应用见共享文件** ，可以发送 `content://URI`类型的 Uri， 并授予 Uri 临时访问全新啊，进行此授权的最简单方式是使用 `FileProvider` 类

步骤如下：

* 在 `AndroidManifest.xml` 清单文件中注册 `provider`

  ```xml
  <provider
            android:name="android.support.v4.content.FileProvider"
            android:authorities="com.demo.***.provider"
            android:exported="false"
            android:grantUriPermissions="true">
  	<meta-data
                 android:name="android.support.FILE_PROVIDER_PATHS"
                 android:resource="@xml/file_provider_paths"/>
  </provider>
  ```

  * `export` 为 `false`

  * `grantUriPermissions` 表示授予 `URI` 临时访问权限

* 指定共享目录

  上面的 `android:resource="@xml/file_provider_paths"` 指定了共享的目录，配置如下：

  ```xml
  <path xmlns:android="http://schemas.android.com/apk/res/android">
       <!-- 代表设备的根目录 new File("/") -->
      <root-path 
                 name="root"
                 path="."/>
       <!-- 代表 content.getFilesDir()-->
  	<files-path
                  name="captured_media"
                  path="captrued_media"/>
       <!-- 代表 content.getCacheDir() -->
      <cache-path
                  name="cache"
                  path="appCache"/>
      <!-- 代表 Environment.getExtrnalStorageDirectory() -->
      <external-path
                     name="data"
                     path="Android"/>
      <!-- 代表 content.getExternalFilesDirs()-->
      <external-files-path
                   name="external"
                   path=""/>
  	<!-- 代表 getExternalCacheDirs() -->    
      <external-cache-path
                   name="external"
                   path=""/>
  </path>
  ```
  
    通过 `FileProvider` 打开下载完的 APK 实例
  
	```java
public static Intent getOpenFileIntent(Context context, DownloadResponse downloadReponse) {
      File file = new File(downloadResponse.getParentPath(), downloadResponse.getFileName());
      if(!file.exists()) {
          return null;
      }
      Intent intent = new Intent();
      intent.addFlag(Intent.FLAG_ACTIVITY_NEW_TASK);
      intent.setAction(Intent.ACTION_VIEW);
      if(Build.VERSION.SDK_INI >= Build.VERSION_CODES.N) {
          intent.setFlag(Intern.FLAG_GRANT_READ_URI_PERMISSION);
          Uri contentUri = FileProvider.getUriForFile(context, "com.demo.***.provider"， file);
          intent.setDataAndType(contentUri, downloadResponse.getMimeType());
      } else {
          intent.setDataAndType(Uri.fromFile(file), downloadResponse.getMimeType());
      }
      
      if(!context instanceof Activity) {
          intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
      }
    return intent;
  }
	```

### 系统广播删除

Android N 管理了三项系统广播:*网络状态变更广播*、*拍照广播*  和 *录像广播*

只有通过 **动态注册** 的方式才能收到网络变化的广播， 在 `AndroidManifest.xml` 中静态注册的无法收到

## Android 8.0 适配

### 通知渠道

在 Android 8.0 中所有的通知都需要提供通知渠道，否则所有通知在 8.0 系统上都不能正常显示

```java
DownloadNotifier(Context context) {
    mContext = context;
    mManager = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
    if(Build.VERSION.SDK_INT >= Build.VERSION_CODE.O) {
        @SuppressWarings("all")
        final NotificationChanncl channel = new NotificationChannel(CHANNEL_ID, CHANNEL_NAME, NotifationManager.IMPORTANCE_HIGH);
        mManager.createNotificationChannel(channel)
    }
}
```

### 悬浮窗（工具类 APP 使用）

8.0 新增了一种悬浮窗的窗口类型， `TYPE_APPLICATION_OVERLAY`, 如果应用使用 `SYSTEM_ALERT_WINDOW` 权限并且使用以下窗口类型之一在其他应用和窗口上方显示提醒窗口，都会显示在 `TYPE_APPLICATION_OVERLAY` 窗口类型的下方

* TYPE_PHONE
* TYPE_PRIORITY_PHONE
* TYPE_SYSTEM_ALERT
* TYPE_SYSTEM_OVERLAY
* TYPE_SYSTEM_ERROR
* TYPE_TOAST

如果该应用的 `targetSdkVersion >= 26` ,则应用只能使用 `TYPE_APPLICATION_OVERLAY` 窗口类型来创建悬浮窗。

```java
if (Build.VERSION.SDK_INT >= 26) {//8.0新特性
   mWindowParams.type = WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY;
} else {
   mWindowParams.type = WindowManager.LayoutParams.TYPE_SYSTEM_ALERT;
}
```

### 透明窗口不允许锁定屏幕旋转

之前应用中的策划返回方案需要将窗口设为透明，但是由于没有适配横屏，因此将其屏幕方法锁定为竖屏

```xml
<activity
          android:name=".HomeActivity"
          android:configChanges="orientation|keyboardHidden|screenSize"
          android:screenOrientation="portrait"
          android:theme="@styple/Base.Theme.CirclePage"/>
```

**透明窗口**+**固定屏幕方向** 会抛出异常

```tex
Caused by: java.lang.IllegalStateException: Only fullscreen opaque activities can request orientation
```

解决方案有两种：

* 适配横屏，去掉固定屏幕方向的限制
* 仅在滑动开始的时候设置窗口透明

### Apk 安装需要权限

在安装 APK 是需要申请安装权限 `REQUEST_INSTALL_PACKAGES`

## Android 9.0 适配

### 明文 HTTP 请求限制

9.0 限制了铭文网络请求，非加密的 http 请求会被系统禁止

* 在 `res/xml` 文件夹啊下常见 `network_security_config.xml`

  ```xml
  <?xml version="1.0" encoding="utf-8"?>
  <network-security-config>
  	<base-config cleartextTrafficPermitted="true"/>
  </network-security-config>
  ```

* 在 `AndroidManifest.xml` 的 `<application` 标签下配置

  ```xml
  <application
               android:networkSecurityConfig="@xml/network_security_config">
  </application>
  ```

或者是改用 `HTTPS` 方式请求

## Android 10.0 适配

### 分区存储

如果还没有准备好适配的功能，可以在 `AndroidManifest.xml` 中添加 `requestLegacyExternalStorage` 来暂时处理

```xml
    <application
        android:requestLegacyExternalStorage="true"/>
```

Android Q 在外部存储设备中为每个应用提供另一个“隔离存储沙盒”。任何其他应用都无法直接访问您应用的沙盒文件。由**于文件是私密的 ，因此不再需要任何权限即可再外部存储设备中访问和保存自己的文件。**

**沙盒**就是应用专属文件夹，并且访问这个文件夹不需要权限申请。官方推荐应用再沙盒内存储文件的地址为 

> Context.getExternalFilesDir() 下的文件夹，比如存储一张照片则应该放在 <font color=red>Context.getExternalFilesDir(Environment.DIRECTORY_PICTURES) </font>中

**适配：**

1. 访问自己文件： Q 中用更精细的媒体特定权限替换并取消了 `READ_EXTERNAL_STORAGE` 和 `WRITE_EXTERNAL_STORAGE` 权限，丙炔无需特定权限，就可以访问沙盒中的文件。
2. 访问系统媒体文件： Q 中引入了一个新定义媒体文件的共享集合，如果要访问沙盒外的媒体共享文件，比如：照片、音乐、视频等。需要申请新的媒体权限 `READ_MEDIA_IMAGES,READ_MEDIA_VIDEO,READ_MEIDA_AUDIO`，时期内那个方法同原来的存储权限
3. 访问系统下载文件：对于系统下载文件的访问，暂时没有限制，但是要访问其中其他应用的文件，必须允许用户使用系统的文件选择器应用来选择文件
4. 访问其他应用沙盒文件：如需要访问其他应用再沙盒内创建的文件，

### 设备唯一标识符

访问设备序列号或者 IMEI 的应用，将会被限制，无法获取成功。因此，在 Android Q 上，应用必须具有 `READ_PRIVILEGED_PHONE_STATE` 签名权限才能访问设备的不可重置标识符（包含 IMEI 和序列号），原来的 `READ_PHONE_STATE` 权限已经不能获取 IMEI 和 序列号。如果想在 Q 设备上通过使用下面的代码获取设备的 ID

```java
((TelephonyManager)getActivity().getSystemService(Context.TELEPHONY_SERVICE)).getDeviceId();
```

**但是，**上面的代码会返回空值（targetASdkVersion <= P）或者报错(targetSdkVersion == Q) ，且官网所说的 `READ_PRIVILEGED_PHONE_STATE` 权限只提供给系统 app，<font color=red>**所以这个方法行不通**</font>

Google 官方给与了设备唯一 ID 最佳方案，但是此方案给出的 ID 是可变的，可以按照具体需求具体解决。

```java
public static String getUUID() {
    String serial = null;
    String m_szDevIdShort = "35" + 
        Build.BOARD.length() % 10 + Build.BRAND.length() % 10 + 
        Build.CPU_ABI.length() % 10 + Build.DEVICE.length() % 10 +
        Build.DISPLAY.length() % 10 + Build.HOST.length() % 10 +
        Build.ID.length() % 10 + Build.MANUFACTURER.length() % 10 +
        Build.MODEL.length() % 10 + Build.PRODUCT.length() % 10 +
        Build.TAGS.length() % 10 + Build.TYPE.length() % 10 +
        Build.USER.length() % 10; //13 位
    try {
      if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
        serial = android.os.Build.getSerial();
      } else {
        serial = Build.SERIAL;
      }
      //API>=9 使用serial号
      return new UUID(m_szDevIDShort.hashCode(), serial.hashCode()).toString();
    } catch (Exception exception) {
    //serial需要一个初始化
    serial = "serial"; // 随便一个初始化
  }
    //使用硬件信息拼凑出来的15位号码
    return new UUID(m_szDevIDShort.hashCode(), serial.hashCode()).toString();
}
```

### 非 SDK 接口限制

为确保 稳定性和兼容性， Android 平台开始限制您的应用在 Android 9.0中使用哪些非 SDK 接口。

**非 SDK 接口** 限制就是某些 SDK 中的私有方法，如 private 方法，你通过 Java 反射等方法获取并调用了。那么这些调用将在 `target >= P` 或者 `target >= Q` 的设备上被限制使用。