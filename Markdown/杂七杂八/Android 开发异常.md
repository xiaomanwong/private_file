# 异常解决方案

## 1. Only fullscreen opaque activities can request orientation

[StackOverflow 解决方案](https://stackoverflow.com/questions/48072438/java-lang-illegalstateexception-only-fullscreen-opaque-activities-can-request-o)

```txt
01-08 10:17:57.966 26362 26362 E AndroidRuntime: java.lang.RuntimeException: Unable to start activity ComponentInfo{com.fx/com.hachi.iot.main.HomeActivity}: java.lang.IllegalStateException: Only fullscreen opaque activities can request orientation
01-08 10:17:57.966 26362 26362 E AndroidRuntime:        at android.app.ActivityThread.performLaunchActivity(ActivityThread.java:3303)
01-08 10:17:57.966 26362 26362 E AndroidRuntime:        at android.app.ActivityThread.handleLaunchActivity(ActivityThread.java:3411)
01-08 10:17:57.966 26362 26362 E AndroidRuntime:        at android.app.ActivityThread.-wrap12(Unknown Source:0)
01-08 10:17:57.966 26362 26362 E AndroidRuntime:        at android.app.ActivityThread$H.handleMessage(ActivityThread.java:1994)
01-08 10:17:57.966 26362 26362 E AndroidRuntime:        at android.os.Handler.dispatchMessage(Handler.java:108)
01-08 10:17:57.966 26362 26362 E AndroidRuntime:        at android.os.Looper.loop(Looper.java:166)
01-08 10:17:57.966 26362 26362 E AndroidRuntime:        at android.app.ActivityThread.main(ActivityThread.java:7529)
01-08 10:17:57.966 26362 26362 E AndroidRuntime:        at java.lang.reflect.Method.invoke(Native Method)
01-08 10:17:57.966 26362 26362 E AndroidRuntime:        at com.android.internal.os.Zygote$MethodAndArgsCaller.run(Zygote.java:245)
01-08 10:17:57.966 26362 26362 E AndroidRuntime:        at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:921)
01-08 10:17:57.966 26362 26362 E AndroidRuntime: Caused by: java.lang.IllegalStateException: Only fullscreen opaque activities can request orientation
01-08 10:17:57.966 26362 26362 E AndroidRuntime:        at android.app.Activity.onCreate(Activity.java:1081)
01-08 10:17:57.966 26362 26362 E AndroidRuntime:        at androidx.core.app.ComponentActivity.onCreate(ComponentActivity.java:85)
01-08 10:17:57.966 26362 26362 E AndroidRuntime:        at androidx.activity.ComponentActivity.onCreate(ComponentActivity.java:154)
01-08 10:17:57.966 26362 26362 E AndroidRuntime:        at androidx.fragment.app.FragmentActivity.onCreate(FragmentActivity.java:312)
01-08 10:17:57.966 26362 26362 E AndroidRuntime:        at androidx.appcompat.app.AppCompatActivity.onCreate(AppCompatActivity.java:115)
01-08 10:17:57.966 26362 26362 E AndroidRuntime:        at com.hachi.common.mvp.BaseActivity2.onCreate(BaseActivity2.java:21)
01-08 10:17:57.966 26362 26362 E AndroidRuntime:        at com.hachi.base.MyActivity2.onCreate(MyActivity2.java:54)
01-08 10:17:57.966 26362 26362 E AndroidRuntime:        at android.app.Activity.performCreate(Activity.java:7383)
01-08 10:17:57.966 26362 26362 E AndroidRuntime:        at android.app.Instrumentation.callActivityOnCreate(Instrumentation.java:1218)
01-08 10:17:57.966 26362 26362 E AndroidRuntime:        at android.app.ActivityThread.performLaunchActivity(ActivityThread.java:3256)
01-08 10:17:57.966 26362 26362 E AndroidRuntime:        ... 9 more
```

## 2. Failed to open zip file.Gradle’s dependency cache may be corrupt (this sometimes occurs after a network connection timeout.）

当我们打开一个别人的项目时，经常因为 Android Studio 版本不一致，Gradle 版本不一致等原因，造成项目无法编译通过，具体报错日志如下：

```html
Failed to open zip file.
Gradle's dependency cache may be corrupt (this sometimes occurs after a network connection timeout.)
Re-download dependencies and sync project (requires network)
```

那么，首先我们要清楚知道，`Gradle` 的下载是需要科学上网的，那么我就默认您已经会了。那么接下来我们看一下为什么会出现这个问题。

通过报错信息我们分析，可以看出是应为 Gradle 的依赖下载被中断，也有可能是因为网络请求超时。系统提示我们可以点击 `Re-download dependencies and sync project (requires network)` 重新下载。但有些时候，点击后会立即报错，提示 `Failed to open zip file` ，相同的报错一直出现，不论我们如何操作。

那么这个原因是什么呢？我们先来看一下本地的 `gralde` 配置，打开文件 `gradle/wrapper/gradle-wrapper.properties`

```gradle
#Wed Apr 07 10:14:35 CST 2021
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-6.5-bin.zip
```

我们看到，当前工程配置的是 `gradle-6.5-bin.zip` 的工具，因此当我们打开项目后，工具会开始同步下载对应的工具，就会在 `.gradle/wrapper/dists/` 下创建对应的目录结构。因此当网络发生终端后，编译器会傻傻的认为 `gradle` 已经下载完成，会开始解析已下载好的 `zip` 文件，但因为网络问题，该文件是一个破损文件，无法正常使用；当我们点击 `Re-download dependencies and sync project (requires network)` 时，也会优先检查本地配置好的环境中是否有当前信息。因此我们在重复点击 `Re-download dependencies and sync project (requires network)` 就会立即报错。

### 解决方案：

#### 方案一：

通过科学的方式，从 [Gralde 仓库](https://services.gradle.org/distributions/) 下载你对应的 `gradle` 版本，然后通过离线配置的方式，配置给你的项目，当这个方案在 `Android Studio 4.1.3` 中我已经找不到了，可能在 `Android Studio` 的前几个版本也有可能找不到，具体的可自行查阅，也可使用方案二

#### 方案二：

依据产生问题的错误信息，我们对应的去解决问题，

1. 保证自己可以科学上网
2. 保证自己当前以及开始后的一段时间网络状态良好
3. 手动删除 `.gradle/wrapper/dists/` 下不完整的数据（就是一个文件夹）
4. 点击 `Re-download dependencies and sync project (requires network)` 系统就会自动开始下载

## 3. Binder invocation to an incorrect interface

多数情况是因为通信双方包名不匹配



## 4. No signature of method: build 编译错误的方法

```groovy
* What went wrong:
A problem occurred evaluating project ':yidian'.
> No signature of method: build_3ddmv1fz9hc2e9evvptkrv8y6.android() is applicable for argument types: (build_3ddmv1fz9hc2e9evvptkrv8y6$_run_closure3) values: [build_3ddmv1fz9hc2e9evvptkrv8y6$_run_closure3@3b735dd4]
```

**原因分析**

从错误信息看，其实是说你的 `build.gradle` 脚本内容错误，一般是在各个闭包中，添加了不正确的已知闭包实现。

例如 `android{}` 闭包中增加大小写不正确的配置等。

**解决措施**

检查最近添加的 `build.gradle` 脚本

1. 是否添加的层次结构不正确，例如 ndk 应该在 defaultConfig 闭包中
2. 是否有大小写不正确的、拼写错误的；



## 5. Android Resource link error  

有两种原因：
1. xml 文件内容有错误

   可仔细检查报错位置，查找报错

2. SDK 三方资源文件问题

   1. 引入的 AAR 有第三方依赖

      有第三方依赖的情况下， 通过本地打包 AAR， 提供给宿主使用，第三方资源无法通过本地打包打入 AAR 中，导致宿主无法正常使用

   2. 引入的 AAR 使用的系统版本过高，低版本宿主无法使用高版本 API

      ```groovy
      configurations.all {
              resolutionStrategy {
                  force 'com.google.android.material:material:1.1.0'
                  force 'androidx.constraintlayout:constraintlayout:2.1.2'
              }}
      ```

      可通过配置，强制要求宿主使用对应版本的依赖库



