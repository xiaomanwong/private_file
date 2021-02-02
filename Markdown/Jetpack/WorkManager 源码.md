---
title: WorkManager 源码
tag: Jetpack
category: WorkManager

---

WorkManager 的工作主要分为两个部分，

1. 初始化
2. 加入队列

```kotlin 
WorkManager.getInstance(mContext).enqueue(workRequest)
```

<!-- more -->

## getInstance()

![workmananger_getInstance](https://raw.githubusercontent.com/xiaomanwong/static_file/master/images/workmananger_getInstance.jpg)

```java
public static @Nullable WorkManagerImpl getInstance() {
    synchronized (sLock) {
        if (sDelegatedInstance != null) { // 返回用户自定义代理类
            return sDelegatedInstance;
        }
		// 返回系统创建的默认对象，初始为 null
        return sDefaultInstance;
    }
}
```

首先，这里我们分析两个变量 **sDelegatedInstance**  和 **sDefaultInstance**

**sDelegatedInstance**

代理实例，是当前用户需要自定义时，自定义的代理类。用户需要完全自己管理 WorkManager ，并通过 `AndroidManifest.xml` 将系统注册的 默认初始化程序 `WorkManagerInitializer extends ContentProvider`   取消注册，才会生效

```xml
<provider
    android:name="androidx.work.impl.WorkManagerInitializer"
    android:authorities="${applicationId}.workmanager-init"
    tools:node="remove" />
```

**sDefaultInstance**

有了上面的描述，那么这里就是系统默认帮我初始化好的实例对象。

所以说，当我们使用 `WorkManager.getInstance(requireContext())` 时，直接就获取到了对象，并没有执行创建过程。因此说 `WorkManager` 的初始化是由系统完成的。

```java
@RestrictTo(RestrictTo.Scope.LIBRARY_GROUP)
public class WorkManagerInitializer extends ContentProvider {
    @Override
    public boolean onCreate() {
        // Initialize WorkManager with the default configuration.
        WorkManager.initialize(getContext(), new Configuration.Builder().build());
        return true;
    }
}
```

Android 系统通过注册一个 `contentProvider` ，在 app 启动时，创建了 Work Manager。我们可以生成一个 apk 文件，查看其 `AndroidManifest.xml` 就能够看到。

![image-20210202174009370](https://raw.githubusercontent.com/xiaomanwong/static_file/master/images/image-20210202174009370.png)

我们在 `AndroidManifest.xml` 中可以看到很多有关 `androidx.work` 的接收者的注册，这些都是后面我们要讨论的。

```java
 public static void initialize(@NonNull Context context, @NonNull Configuration configuration) {
        synchronized (sLock) {
            if (sDelegatedInstance == null) {
                context = context.getApplicationContext();
                if (sDefaultInstance == null) {
                    sDefaultInstance = new WorkManagerImpl(
                            context,
                            configuration,
                            new WorkManagerTaskExecutor(configuration.getTaskExecutor()));
                }
                sDelegatedInstance = sDefaultInstance;
            }
        }
  }
```

当代理类和默认实现类都为空时，系统为 `sDefaultInstance` 创建了默认对象 `WorkManagerImpl` ，并创建了一个线程池 `WorkManagerTaskExecutor` 



## enqueue

