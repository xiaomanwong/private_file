---
title: WorkManager 源码
tag: Jetpack
category:WorkManager

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
    private void internalInit(@NonNull Context context,
            @NonNull Configuration configuration,
            @NonNull TaskExecutor workTaskExecutor,
            @NonNull WorkDatabase workDatabase,
            @NonNull List<Scheduler> schedulers,
            @NonNull Processor processor) {

        context = context.getApplicationContext();
        mContext = context;
        mConfiguration = configuration;// 配置器
        mWorkTaskExecutor = workTaskExecutor; // 任务线程池
        mWorkDatabase = workDatabase; // Room数据库
        mSchedulers = schedulers; // 任务调度器
        mProcessor = processor; // 进度监听器
        mPreferenceUtils = new PreferenceUtils(workDatabase);
        mForceStopRunnableCompleted = false;

        // Check for direct boot mode
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N && context.isDeviceProtectedStorage()) {
            throw new IllegalStateException("Cannot initialize WorkManager in direct boot mode");
        }

        // Checks for app force stops.
        // 检查应用程序强制停止线程，若有，则安排在合适的工作任务中
        mWorkTaskExecutor.executeOnBackgroundThread(new ForceStopRunnable(context, this));
    }
```

当代理类和默认实现类都为空时，系统为 `sDefaultInstance` 创建了默认对象 `WorkManagerImpl` ，并创建了一个线程池 `WorkManagerTaskExecutor` ,并且其调用了重载构造器，继续创建了一个数据库对象 `WorkDatabase` 和一个 `GreedyScheduler` 调度器 ，一个`SystemJobScheduler` 或 `SystemAlarmScheduler`，以及一个 `Processor` 任务进度监听器。

* 创建一个 `WorkManagerImpl` 的实例： `sDefaultInstance`， 最终返回的是 `mDelegatedInstance` 通过赋值 `sDelegatedInstance = sDefaultInstance;`
* 创建一个新的线程池，并将旧的线程池传递给新的。 `WrokManagerTaskExecutor`
* 创建一个数据库， `WorkDatabase.create()` ，其使用的是 **Room** 数据库。与 Jetpack 内关联
* 创建一组调度器, `GreedyScheduler`, `SystemJobScheduler` 或  `SystemAlarmScheduler`
* 创建一个 `Processor` ，进入进度监听器
* 检查应用程序强制停止的任务，并重新安排合适的时间工作

## enqueue

上面说完了初始化，接下来我们继续说入队列

```java
public Operation enqueue(@NonNull List<? extends WorkRequest> workRequests) 
    return new WorkContinuationImpl(this, workRequests).enqueue();
}
```

