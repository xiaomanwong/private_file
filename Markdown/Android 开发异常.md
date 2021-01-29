# 异常解决方案



## Only fullscreen opaque activities can request orientation

[StackOverflow 解决方案](https://stackoverflow.com/questions/48072438/java-lang-illegalstateexception-only-fullscreen-opaque-activities-can-request-o)

```tex
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

